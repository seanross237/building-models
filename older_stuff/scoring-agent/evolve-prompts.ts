import { getDb, callOpenRouter } from './utils.js';

const META_MODEL = 'anthropic/claude-opus-4-6';

export async function evolvePrompts(
  datasetId: string,
  generation: number
): Promise<string[]> {
  const db = getDb();

  console.log(`\nEvolving prompts for generation ${generation + 1}...`);

  // Find best prompt from current generation
  const { rows: [bestPrompt] } = await db.query(`
    SELECT * FROM scoring_prompts
    WHERE dataset_id = $1 AND generation = $2 AND status = 'scored'
    ORDER BY accuracy DESC, f1_score DESC
    LIMIT 1
  `, [datasetId, generation]);

  if (!bestPrompt) {
    throw new Error(`No scored prompts found for generation ${generation}`);
  }

  console.log(`  Best gen ${generation} prompt: id=${bestPrompt.id} (accuracy=${(bestPrompt.accuracy * 100).toFixed(1)}%, F1=${(bestPrompt.f1_score * 100).toFixed(1)}%)`);

  // Load FP and FN examples
  const { rows: fpExamples } = await db.query(`
    SELECT sp.*, sds.*
    FROM scoring_predictions sp
    JOIN scoring_dataset_songs sds ON sp.dataset_song_id = sds.id
    WHERE sp.prompt_id = $1 AND sp.prediction_type = 'FP'
    ORDER BY RANDOM()
    LIMIT 5
  `, [bestPrompt.id]);

  const { rows: fnExamples } = await db.query(`
    SELECT sp.*, sds.*
    FROM scoring_predictions sp
    JOIN scoring_dataset_songs sds ON sp.dataset_song_id = sds.id
    WHERE sp.prompt_id = $1 AND sp.prediction_type = 'FN'
    ORDER BY RANDOM()
    LIMIT 5
  `, [bestPrompt.id]);

  console.log(`  FP examples: ${fpExamples.length}, FN examples: ${fnExamples.length}`);

  // Build meta-prompt
  const metaSystemPrompt = `You are an expert prompt engineer optimizing a classification prompt. Your task is to generate 10 improved variations of a prompt that predicts whether a personalized song will be purchased (unlocked) by its creator.

You must respond with a JSON object containing a "prompts" array of exactly 5 objects, each with "prompt_text" (string) and "hypothesis" (string) fields.

Generate a SPECTRUM of variations:
- 1 MINOR TWEAK: Small adjustment to wording, emphasis, or scoring criteria order
- 2 MODERATE CHANGES: Restructure evaluation criteria, add/remove factors, change weighting
- 1 MAJOR REWRITE: Completely different approach to the classification task
- 1 WILD CARD: Unconventional approach that might reveal unexpected patterns

Consider:
- Are metadata signals (occasion, relationship) more predictive than lyrics quality?
- Do certain occasions (wedding, birthday) have much higher unlock rates?
- Is custom_song a strong signal?
- Does name integration quality matter more than overall lyric quality?
- Are there length patterns (too short = low effort, too long = unfocused)?
- Would a scoring rubric with explicit point values outperform a holistic judgment?`;

  const metaUserPrompt = buildMetaUserPrompt(bestPrompt, fpExamples, fnExamples);

  const startTime = Date.now();
  const result = await callOpenRouter(META_MODEL, metaSystemPrompt, metaUserPrompt, { temperature: 0.7 });
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

  const newPrompts = result.prompts;
  if (!Array.isArray(newPrompts) || newPrompts.length === 0) {
    throw new Error('Meta-agent did not return valid prompts array');
  }

  console.log(`  Meta-agent generated ${newPrompts.length} prompts in ${elapsed}s`);

  // Insert new prompts
  const newPromptIds: string[] = [];
  for (let i = 0; i < newPrompts.length; i++) {
    const p = newPrompts[i];
    const { rows: [inserted] } = await db.query(`
      INSERT INTO scoring_prompts (
        dataset_id, prompt_text, generation, variant_number,
        parent_prompt_id, hypothesis, status
      ) VALUES ($1, $2, $3, $4, $5, $6, 'pending')
      RETURNING id
    `, [
      datasetId, p.prompt_text, generation + 1, i,
      bestPrompt.id, p.hypothesis
    ]);
    newPromptIds.push(inserted.id);
  }

  // Log evolution
  await db.query(`
    INSERT INTO scoring_evolutions (
      dataset_id, from_generation, to_generation,
      parent_prompt_id, parent_accuracy, parent_f1,
      prompts_generated, fp_examples_shown, fn_examples_shown,
      meta_prompt_used
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
  `, [
    datasetId, generation, generation + 1,
    bestPrompt.id, bestPrompt.accuracy, bestPrompt.f1_score,
    newPrompts.length, fpExamples.length, fnExamples.length,
    metaSystemPrompt
  ]);

  console.log(`  Inserted ${newPromptIds.length} new prompts for generation ${generation + 1}`);
  return newPromptIds;
}

function buildMetaUserPrompt(bestPrompt: any, fpExamples: any[], fnExamples: any[]): string {
  const parts: string[] = [];

  parts.push('=== CURRENT BEST PROMPT ===');
  parts.push(bestPrompt.prompt_text);
  parts.push('');
  parts.push('=== CURRENT METRICS ===');
  parts.push(`Accuracy: ${(bestPrompt.accuracy * 100).toFixed(1)}%`);
  parts.push(`Precision: ${(bestPrompt.precision_score * 100).toFixed(1)}%`);
  parts.push(`Recall: ${(bestPrompt.recall * 100).toFixed(1)}%`);
  parts.push(`F1: ${(bestPrompt.f1_score * 100).toFixed(1)}%`);
  parts.push(`TP: ${bestPrompt.tp} | FP: ${bestPrompt.fp} | TN: ${bestPrompt.tn} | FN: ${bestPrompt.fn}`);

  if (fpExamples.length > 0) {
    parts.push('');
    parts.push('=== FALSE POSITIVES (predicted unlock but did NOT unlock) ===');
    parts.push('These songs seemed good but were NOT purchased. What made the model over-confident?');
    for (const ex of fpExamples) {
      parts.push('');
      parts.push(`--- FP Example ---`);
      parts.push(`Title: ${ex.song_title}`);
      parts.push(`Recipient: ${ex.recipient_name}`);
      parts.push(`Occasion: ${ex.occasion || 'none'}`);
      parts.push(`Relationship: ${ex.relationship || 'none'}`);
      parts.push(`Custom: ${ex.is_custom_song ? 'Yes' : 'No'}`);
      parts.push(`Singer: ${ex.singer || 'default'}`);
      parts.push(`Model reasoning: ${ex.reasoning}`);
      parts.push(`Lyrics preview: ${(ex.lyrics_snapshot || '').slice(0, 300)}...`);
    }
  }

  if (fnExamples.length > 0) {
    parts.push('');
    parts.push('=== FALSE NEGATIVES (predicted NO unlock but DID unlock) ===');
    parts.push('These songs were purchased despite seeming unlikely. What signals did the model miss?');
    for (const ex of fnExamples) {
      parts.push('');
      parts.push(`--- FN Example ---`);
      parts.push(`Title: ${ex.song_title}`);
      parts.push(`Recipient: ${ex.recipient_name}`);
      parts.push(`Occasion: ${ex.occasion || 'none'}`);
      parts.push(`Relationship: ${ex.relationship || 'none'}`);
      parts.push(`Custom: ${ex.is_custom_song ? 'Yes' : 'No'}`);
      parts.push(`Singer: ${ex.singer || 'default'}`);
      parts.push(`Payment: $${((ex.payment_amount_cents || 0) / 100).toFixed(2)}`);
      parts.push(`Model reasoning: ${ex.reasoning}`);
      parts.push(`Lyrics preview: ${(ex.lyrics_snapshot || '').slice(0, 300)}...`);
    }
  }

  return parts.join('\n');
}
