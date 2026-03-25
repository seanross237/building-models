import { getDb } from './utils.js';

export async function extractDataset(
  name?: string,
  sampleSize: number = 200,
  filters?: { style?: string; relationship?: string }
): Promise<string> {
  const db = getDb();
  const datasetName = name || `dataset_${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`;
  const style = filters?.style || 'Country';
  const relationship = filters?.relationship || 'partner';

  console.log(`\nExtracting dataset "${datasetName}" (${sampleSize} per class, ${style} + ${relationship})...`);

  // Get completed songs with context, filtered by style and relationship
  const { rows: allSongs } = await db.query(`
    SELECT
      s.id as song_id,
      s.song_order_id,
      s.song_title,
      s.recipient_name,
      s.lyrics_snapshot,
      s.occasion,
      s.relationship,
      s.styles,
      s.singer,
      s.is_custom_song,
      so.custom_description,
      f.feel,
      f.form_answers,
      s.unlocked as actually_unlocked,
      p.amount_cents as payment_amount_cents
    FROM songs s
    JOIN song_orders so ON s.song_order_id = so.id
    LEFT JOIN lyrics l ON so.lyrics_id = l.id
    LEFT JOIN forms f ON l.form_id = f.id
    LEFT JOIN payments p ON s.unlocked_by_payment_id = p.id
    WHERE so.generation_completed_at IS NOT NULL
      AND s.lyrics_snapshot IS NOT NULL
      AND s.lyrics_snapshot != ''
      AND $1 = ANY(s.styles)
      AND s.relationship = $2
  `, [style, relationship]);

  console.log(`  Total songs with lyrics: ${allSongs.length}`);

  // Split into unlocked and not-unlocked
  const unlocked = allSongs.filter(s => s.actually_unlocked === true);
  const notUnlocked = allSongs.filter(s => !s.actually_unlocked);

  console.log(`  Unlocked: ${unlocked.length}, Not unlocked: ${notUnlocked.length}`);

  // Randomly sample N from each
  const sampledUnlocked = shuffle(unlocked).slice(0, sampleSize);
  const sampledNotUnlocked = shuffle(notUnlocked).slice(0, sampleSize);
  const sampled = [...sampledUnlocked, ...sampledNotUnlocked];

  const actualUnlockedCount = sampledUnlocked.length;
  const actualNotUnlockedCount = sampledNotUnlocked.length;
  const totalSampled = sampled.length;
  const baselineRate = totalSampled > 0 ? actualUnlockedCount / totalSampled : 0;

  console.log(`  Sampled: ${actualUnlockedCount} unlocked + ${actualNotUnlockedCount} not unlocked = ${totalSampled}`);
  console.log(`  Baseline unlock rate: ${(baselineRate * 100).toFixed(1)}%`);

  // Insert dataset record
  const { rows: [dataset] } = await db.query(`
    INSERT INTO scoring_datasets (name, total_count, unlocked_count, not_unlocked_count, baseline_unlock_rate)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id
  `, [datasetName, totalSampled, actualUnlockedCount, actualNotUnlockedCount, baselineRate]);

  const datasetId = dataset.id;

  // Insert all songs
  for (const song of sampled) {
    await db.query(`
      INSERT INTO scoring_dataset_songs (
        dataset_id, song_id, song_order_id, song_title, recipient_name,
        lyrics_snapshot, occasion, relationship, styles, singer,
        is_custom_song, custom_description, feel, form_answers,
        actually_unlocked, payment_amount_cents
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
    `, [
      datasetId, song.song_id, song.song_order_id, song.song_title, song.recipient_name,
      song.lyrics_snapshot, song.occasion, song.relationship,
      song.styles, song.singer,
      song.is_custom_song, song.custom_description, song.feel,
      song.form_answers ? JSON.stringify(song.form_answers) : null,
      song.actually_unlocked, song.payment_amount_cents
    ]);
  }

  console.log(`  Dataset saved: id=${datasetId}`);
  return datasetId;
}

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
