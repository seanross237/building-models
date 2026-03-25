/**
 * Score songs on quality dimensions and compare unlocked vs not-unlocked.
 * Instead of predicting unlock, we score each song on 6 properties (1-10)
 * and see if there's a meaningful difference between groups.
 */
import { checkEnv, getDb, callOpenRouter, closeDb } from './utils.js';

const DIMENSIONS = [
  'personalization',   // How specific to the recipient (names, details, inside jokes)
  'emotional_depth',   // Genuine emotion vs generic sentiment
  'lyrical_craft',     // Wordplay, imagery, rhythm, rhyme quality
  'occasion_fit',      // How well it matches the stated occasion
  'specificity',       // Concrete details vs vague platitudes
  'singability',       // Natural flow, phrasing that works as a song
];

const SYSTEM_PROMPT = `You are an expert song critic evaluating personalized songs.
Score each song on these 6 dimensions from 1-10:

1. **Personalization** (1-10): How specific is this to the recipient? Does it use their name naturally, reference specific details about them or the relationship? 1 = completely generic, 10 = deeply personal.

2. **Emotional Depth** (1-10): Does this evoke genuine emotion or feel hollow? Does it go beyond surface-level sentiment? 1 = empty platitudes, 10 = genuinely moving.

3. **Lyrical Craft** (1-10): Quality of wordplay, imagery, metaphors, rhyme scheme, and poetic devices. 1 = clumsy/awkward, 10 = masterful songwriting.

4. **Occasion Fit** (1-10): How well does the song match the stated occasion? Does it capture the spirit of the event? 1 = completely off, 10 = perfect match.

5. **Specificity** (1-10): Are there concrete details, stories, or references, or is it all vague generalities? 1 = could be about anyone, 10 = unmistakably about this person.

6. **Singability** (1-10): Does the phrasing flow naturally as a song? Are syllable counts consistent? Would this feel right sung aloud? 1 = reads like prose, 10 = naturally musical.

Respond with ONLY a JSON object, no other text:
{
  "personalization": <number>,
  "emotional_depth": <number>,
  "lyrical_craft": <number>,
  "occasion_fit": <number>,
  "specificity": <number>,
  "singability": <number>,
  "brief_note": "<1 sentence overall impression>"
}`;

function formatSongForScoring(song: any): string {
  const parts = [
    `Title: ${song.song_title}`,
    `Recipient: ${song.recipient_name}`,
    `Occasion: ${song.occasion}`,
    `Relationship: ${song.relationship}`,
    `Style: ${Array.isArray(song.styles) ? song.styles.join(', ') : song.styles}`,
    song.singer ? `Singer: ${song.singer}` : null,
    song.feel ? `Feel: ${song.feel}` : null,
    song.custom_description ? `Custom Description: ${song.custom_description}` : null,
    `\nLyrics:\n${song.lyrics_snapshot}`,
  ];
  return parts.filter(Boolean).join('\n');
}

async function scoreSong(song: any): Promise<any | null> {
  const userPrompt = formatSongForScoring(song);
  try {
    const result = await callOpenRouter(
      'anthropic/claude-4.5-haiku-20251001',
      SYSTEM_PROMPT,
      userPrompt,
      { temperature: 0.1 }
    );
    return result;
  } catch (err: any) {
    console.error(`  Error scoring song ${song.song_id}: ${err.message}`);
    return null;
  }
}

async function main() {
  checkEnv();
  const db = getDb();
  const start = Date.now();

  // Get the dataset
  const { rows: [dataset] } = await db.query(
    'SELECT id FROM scoring_datasets ORDER BY created_at DESC LIMIT 1'
  );
  if (!dataset) { console.error('No dataset found'); process.exit(1); }

  // Get all songs
  const { rows: songs } = await db.query(`
    SELECT song_id, song_title, recipient_name, lyrics_snapshot,
           occasion, relationship, styles, singer, feel,
           custom_description, actually_unlocked
    FROM scoring_dataset_songs
    WHERE dataset_id = $1
    ORDER BY song_id
  `, [dataset.id]);

  console.log(`\n=== Quality Scoring: ${songs.length} songs ===\n`);

  const results: { song_id: string; unlocked: boolean; scores: Record<string, number>; avg: number; note: string }[] = [];
  const BATCH_SIZE = 5;

  for (let i = 0; i < songs.length; i += BATCH_SIZE) {
    const batch = songs.slice(i, i + BATCH_SIZE);
    const batchResults = await Promise.all(batch.map(s => scoreSong(s)));

    for (let j = 0; j < batch.length; j++) {
      const song = batch[j];
      const scored = batchResults[j];
      if (!scored) continue;

      const dimScores: Record<string, number> = {};
      for (const dim of DIMENSIONS) {
        dimScores[dim] = Number(scored[dim]) || 0;
      }
      const avg = DIMENSIONS.reduce((sum, d) => sum + dimScores[d], 0) / DIMENSIONS.length;

      results.push({
        song_id: song.song_id,
        unlocked: song.actually_unlocked,
        scores: dimScores,
        avg,
        note: scored.brief_note || '',
      });
    }

    const done = Math.min(i + BATCH_SIZE, songs.length);
    process.stdout.write(`\r  Scored ${done}/${songs.length}`);
  }

  console.log('\n');

  // Split by unlocked status
  const unlocked = results.filter(r => r.unlocked);
  const notUnlocked = results.filter(r => !r.unlocked);

  // Compute averages per dimension
  console.log('=== RESULTS ===\n');
  console.log('Dimension'.padEnd(20) + 'Unlocked'.padStart(10) + 'Not Unlocked'.padStart(14) + 'Delta'.padStart(8));
  console.log('-'.repeat(52));

  for (const dim of DIMENSIONS) {
    const avgUnlocked = unlocked.reduce((s, r) => s + r.scores[dim], 0) / unlocked.length;
    const avgNot = notUnlocked.reduce((s, r) => s + r.scores[dim], 0) / notUnlocked.length;
    const delta = avgUnlocked - avgNot;
    console.log(
      dim.padEnd(20) +
      avgUnlocked.toFixed(2).padStart(10) +
      avgNot.toFixed(2).padStart(14) +
      (delta >= 0 ? '+' : '') + delta.toFixed(2).padStart(7)
    );
  }

  const avgOverallUnlocked = unlocked.reduce((s, r) => s + r.avg, 0) / unlocked.length;
  const avgOverallNot = notUnlocked.reduce((s, r) => s + r.avg, 0) / notUnlocked.length;
  const overallDelta = avgOverallUnlocked - avgOverallNot;

  console.log('-'.repeat(52));
  console.log(
    'OVERALL AVG'.padEnd(20) +
    avgOverallUnlocked.toFixed(2).padStart(10) +
    avgOverallNot.toFixed(2).padStart(14) +
    (overallDelta >= 0 ? '+' : '') + overallDelta.toFixed(2).padStart(7)
  );

  // Distribution: how many songs fall into each score bucket
  console.log('\n\n=== SCORE DISTRIBUTION ===\n');
  console.log('Score Range'.padEnd(14) + 'Unlocked'.padStart(10) + 'Not Unlocked'.padStart(14) + 'Unlock Rate'.padStart(13));
  console.log('-'.repeat(51));

  const buckets = [
    [1, 3, '1.0 - 3.0'],
    [3, 4, '3.0 - 4.0'],
    [4, 5, '4.0 - 5.0'],
    [5, 6, '5.0 - 6.0'],
    [6, 7, '6.0 - 7.0'],
    [7, 8, '7.0 - 8.0'],
    [8, 10.1, '8.0 - 10.0'],
  ] as const;

  for (const [lo, hi, label] of buckets) {
    const uCount = unlocked.filter(r => r.avg >= lo && r.avg < hi).length;
    const nCount = notUnlocked.filter(r => r.avg >= lo && r.avg < hi).length;
    const total = uCount + nCount;
    const rate = total > 0 ? (uCount / total * 100).toFixed(1) + '%' : 'n/a';
    console.log(
      label.padEnd(14) +
      String(uCount).padStart(10) +
      String(nCount).padStart(14) +
      rate.padStart(13)
    );
  }

  const elapsed = ((Date.now() - start) / 1000 / 60).toFixed(1);
  console.log(`\nScored ${results.length}/${songs.length} songs in ${elapsed} minutes`);
  console.log(`Estimated cost: ~$${(results.length * 0.0002).toFixed(2)}`);

  await closeDb();
}

main().catch((err) => {
  console.error('\nFatal error:', err);
  closeDb().finally(() => process.exit(1));
});
