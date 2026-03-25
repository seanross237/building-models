import { getDb, callOpenRouter, computeMetrics } from './utils.js';

const SCORING_MODEL = 'anthropic/claude-4.5-haiku-20251001';
const BATCH_SIZE = 5;

export async function scoreSongs(promptId: string): Promise<void> {
  const db = getDb();

  // Load prompt
  const { rows: [prompt] } = await db.query(
    'SELECT * FROM scoring_prompts WHERE id = $1', [promptId]
  );
  if (!prompt) throw new Error(`Prompt ${promptId} not found`);

  // Load dataset songs
  const { rows: songs } = await db.query(
    'SELECT * FROM scoring_dataset_songs WHERE dataset_id = $1',
    [prompt.dataset_id]
  );

  console.log(`\n  Scoring prompt ${promptId} (gen ${prompt.generation}, var ${prompt.variant_number}) against ${songs.length} songs...`);

  // Update status to scoring
  await db.query(
    'UPDATE scoring_prompts SET status = $1 WHERE id = $2',
    ['scoring', promptId]
  );

  const predictions: { predicted: boolean; actual: boolean }[] = [];
  let errors = 0;
  const startTime = Date.now();

  // Process in batches
  for (let i = 0; i < songs.length; i += BATCH_SIZE) {
    const batch = songs.slice(i, i + BATCH_SIZE);
    await Promise.all(batch.map(async (song) => {
      try {
        const result = await scoreSingleSong(song, prompt);
        predictions.push(result);
      } catch (err: any) {
        errors++;
        console.error(`\n    Error scoring song ${song.song_id}: ${err.message}`);
      }
    }));
    process.stdout.write(`\r  Scored ${Math.min(i + BATCH_SIZE, songs.length)}/${songs.length}`);
  }

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n  Done in ${elapsed}s (${errors} errors)`);

  // Compute and save metrics
  const metrics = computeMetrics(predictions);
  await db.query(`
    UPDATE scoring_prompts
    SET status = 'scored',
        accuracy = $1, precision_score = $2, recall = $3, f1_score = $4,
        tp = $5, fp = $6, tn = $7, fn = $8,
        scored_at = NOW()
    WHERE id = $9
  `, [
    metrics.accuracy, metrics.precision, metrics.recall, metrics.f1,
    metrics.tp, metrics.fp, metrics.tn, metrics.fn,
    promptId
  ]);

  console.log(`  Accuracy: ${(metrics.accuracy * 100).toFixed(1)}% | Precision: ${(metrics.precision * 100).toFixed(1)}% | Recall: ${(metrics.recall * 100).toFixed(1)}% | F1: ${(metrics.f1 * 100).toFixed(1)}%`);
  console.log(`  TP: ${metrics.tp} | FP: ${metrics.fp} | TN: ${metrics.tn} | FN: ${metrics.fn}`);
}

async function scoreSingleSong(
  song: any,
  prompt: any
): Promise<{ predicted: boolean; actual: boolean }> {
  const db = getDb();

  const userPrompt = formatSongContext(song);
  const result = await callOpenRouter(SCORING_MODEL, prompt.prompt_text, userPrompt);

  const willUnlock = Boolean(result.will_unlock);
  const actual = Boolean(song.actually_unlocked);
  const confidence = result.confidence || 'medium';
  const reasoning = result.reasoning || '';

  let predictionType: string;
  if (willUnlock && actual) predictionType = 'TP';
  else if (willUnlock && !actual) predictionType = 'FP';
  else if (!willUnlock && !actual) predictionType = 'TN';
  else predictionType = 'FN';

  const isCorrect = willUnlock === actual;

  await db.query(`
    INSERT INTO scoring_predictions (
      prompt_id, dataset_song_id, predicted_unlock, actually_unlocked,
      confidence, reasoning, is_correct, prediction_type
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
  `, [
    prompt.id, song.id, willUnlock, actual,
    confidence, reasoning, isCorrect, predictionType
  ]);

  return { predicted: willUnlock, actual };
}

function formatSongContext(song: any): string {
  const parts: string[] = [];

  parts.push(`SONG TITLE: ${song.song_title || 'Untitled'}`);
  parts.push(`RECIPIENT: ${song.recipient_name || 'Unknown'}`);
  if (song.occasion) parts.push(`OCCASION: ${song.occasion}`);
  if (song.relationship) parts.push(`RELATIONSHIP: ${song.relationship}`);
  if (song.styles) {
    const styles = typeof song.styles === 'string' ? song.styles : JSON.stringify(song.styles);
    parts.push(`STYLES: ${styles}`);
  }
  if (song.feel) parts.push(`FEEL/MOOD: ${song.feel}`);
  if (song.singer) parts.push(`SINGER: ${song.singer}`);
  parts.push(`CUSTOM SONG: ${song.is_custom_song ? 'Yes' : 'No'}`);
  if (song.custom_description) parts.push(`CUSTOM DESCRIPTION: ${song.custom_description}`);

  parts.push('');
  parts.push('LYRICS:');
  parts.push(song.lyrics_snapshot);

  return parts.join('\n');
}
