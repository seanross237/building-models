/**
 * Resume scoring from where we left off.
 * Finds pending prompts and scores them, then continues evolution cycles.
 */
import { checkEnv, getDb, closeDb } from './utils.js';
import { scoreSongs } from './score-songs.js';
import { evolvePrompts } from './evolve-prompts.js';

async function main() {
  checkEnv();
  const db = getDb();
  const totalStart = Date.now();

  // Find the dataset
  const { rows: [dataset] } = await db.query(
    'SELECT id FROM scoring_datasets ORDER BY created_at DESC LIMIT 1'
  );
  if (!dataset) { console.error('No dataset found'); process.exit(1); }
  const datasetId = dataset.id;
  console.log(`=== Resuming Scoring Agent (dataset: ${datasetId}) ===`);

  // Score any pending prompts from current generation
  const { rows: pending } = await db.query(`
    SELECT id, generation, variant_number FROM scoring_prompts
    WHERE dataset_id = $1 AND status = 'pending'
    ORDER BY generation, variant_number
  `, [datasetId]);

  console.log(`\nFound ${pending.length} pending prompts to score`);

  for (const p of pending) {
    console.log(`\n  --- Prompt gen ${p.generation}, var ${p.variant_number} ---`);
    await scoreSongs(p.id);
  }

  // Figure out what generation we just finished
  const { rows: [maxGen] } = await db.query(`
    SELECT MAX(generation) as gen FROM scoring_prompts
    WHERE dataset_id = $1 AND status = 'scored'
  `, [datasetId]);
  const currentGen = maxGen?.gen || 0;
  console.log(`\nCurrent max scored generation: ${currentGen}`);

  // Continue evolution cycles up to gen 3
  const targetGen = 3;
  for (let gen = currentGen; gen < targetGen; gen++) {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`  GENERATION ${gen} -> ${gen + 1}`);
    console.log(`${'='.repeat(50)}`);

    const newPromptIds = await evolvePrompts(datasetId, gen);

    for (let i = 0; i < newPromptIds.length; i++) {
      console.log(`\n  --- Prompt ${i + 1}/${newPromptIds.length} (gen ${gen + 1}) ---`);
      await scoreSongs(newPromptIds[i]);
    }

    // Mark best of this generation
    const { rows: [best] } = await db.query(`
      SELECT id, accuracy, f1_score FROM scoring_prompts
      WHERE dataset_id = $1 AND generation = $2 AND status = 'scored'
      ORDER BY accuracy DESC, f1_score DESC
      LIMIT 1
    `, [datasetId, gen + 1]);

    if (best) {
      console.log(`\n  Best gen ${gen + 1}: accuracy=${(best.accuracy * 100).toFixed(1)}% F1=${(best.f1_score * 100).toFixed(1)}%`);
    }
  }

  // Print summary
  const { rows: prompts } = await db.query(`
    SELECT generation, variant_number, accuracy, f1_score, tp, fp, tn, fn, hypothesis
    FROM scoring_prompts
    WHERE dataset_id = $1 AND status = 'scored'
    ORDER BY generation, accuracy DESC
  `, [datasetId]);

  console.log('\n\n=== SCORING SUMMARY ===\n');
  console.log('Gen  Var  Acc%    F1%     TP   FP   TN   FN   Hypothesis');
  console.log('-'.repeat(90));
  for (const p of prompts) {
    console.log(
      String(p.generation).padEnd(5) +
      String(p.variant_number).padEnd(5) +
      (p.accuracy * 100).toFixed(1).padEnd(8) +
      (p.f1_score * 100).toFixed(1).padEnd(8) +
      String(p.tp).padEnd(5) +
      String(p.fp).padEnd(5) +
      String(p.tn).padEnd(5) +
      String(p.fn).padEnd(5) +
      (p.hypothesis || 'seed').slice(0, 40)
    );
  }

  const best = prompts.reduce((a: any, b: any) =>
    (a.accuracy > b.accuracy || (a.accuracy === b.accuracy && a.f1_score > b.f1_score)) ? a : b
  , prompts[0]);
  if (best) {
    console.log(`\nBest overall: gen ${best.generation}, var ${best.variant_number} — Accuracy: ${(best.accuracy * 100).toFixed(1)}%, F1: ${(best.f1_score * 100).toFixed(1)}%`);
  }

  const totalElapsed = ((Date.now() - totalStart) / 1000 / 60).toFixed(1);
  console.log(`\nTotal time: ${totalElapsed} minutes`);
  await closeDb();
}

main().catch((err) => {
  console.error('\nFatal error:', err);
  closeDb().finally(() => process.exit(1));
});
