import { checkEnv, getDb, closeDb } from './utils.js';
import { extractDataset } from './extract-dataset.js';
import { scoreSongs } from './score-songs.js';
import { evolvePrompts } from './evolve-prompts.js';

const SEED_PROMPT = `You are evaluating whether a personalized song will be purchased (unlocked) by its creator.

Analyze the following song and its context. Consider:
1. PERSONALIZATION DEPTH: How specific is the song to this person? Does it mention real details, inside jokes, or specific memories?
2. EMOTIONAL RESONANCE: Does the song capture genuine emotion? Would it make the recipient feel deeply seen?
3. OCCASION FIT: Is this for a meaningful occasion (birthday, wedding, anniversary) vs casual/impulse?
4. NAME INTEGRATION: Is the recipient's name woven naturally into the lyrics?
5. LYRICAL QUALITY: Are the lyrics well-crafted, or generic/awkward?
6. SPECIFICITY vs GENERIC: Does the song feel like it was written FOR this person, or could it be for anyone?
7. COMPLETENESS: Does the song feel finished and polished?

Songs that are highly personalized, emotionally resonant, and for meaningful occasions are more likely to be purchased.

Respond with JSON:
{ "will_unlock": true/false, "confidence": "low" | "medium" | "high", "reasoning": "brief explanation" }`;

// --- CLI argument parsing ---

function parseArgs() {
  const args = process.argv.slice(2);
  const flags = {
    extract: false,
    seed: false,
    generations: 3,
    datasetId: '',
    sampleSize: 200,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--extract':
        flags.extract = true;
        break;
      case '--seed':
        flags.seed = true;
        break;
      case '--generations':
        flags.generations = parseInt(args[++i], 10);
        break;
      case '--dataset-id':
        flags.datasetId = args[++i];
        break;
      case '--sample-size':
        flags.sampleSize = parseInt(args[++i], 10);
        break;
      default:
        console.error(`Unknown flag: ${args[i]}`);
        process.exit(1);
    }
  }

  return flags;
}

// --- Main ---

async function main() {
  checkEnv();

  const flags = parseArgs();
  const db = getDb();
  const totalStart = Date.now();

  console.log('=== Serenade Scoring Agent ===');
  console.log(`  Extract: ${flags.extract} | Seed: ${flags.seed} | Generations: ${flags.generations}`);

  let datasetId = flags.datasetId;

  // Step 1: Extract dataset
  if (flags.extract) {
    datasetId = await extractDataset(undefined, flags.sampleSize);
  } else if (!datasetId) {
    // Use latest dataset
    const { rows } = await db.query(
      'SELECT id FROM scoring_datasets ORDER BY created_at DESC LIMIT 1'
    );
    if (rows.length === 0) {
      console.error('No datasets found. Run with --extract first.');
      process.exit(1);
    }
    datasetId = rows[0].id;
    console.log(`\nUsing latest dataset: ${datasetId}`);
  }

  // Step 2: Seed prompt
  if (flags.seed) {
    console.log('\nCreating seed prompt (generation 0)...');
    const { rows: [seedPrompt] } = await db.query(`
      INSERT INTO scoring_prompts (
        dataset_id, prompt_text, generation, variant_number, status
      ) VALUES ($1, $2, 0, 0, 'pending')
      RETURNING id
    `, [datasetId, SEED_PROMPT]);

    console.log(`  Seed prompt id: ${seedPrompt.id}`);
    await scoreSongs(seedPrompt.id);
  }

  // Step 3: Evolution cycles
  for (let gen = 0; gen < flags.generations; gen++) {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`  GENERATION ${gen} -> ${gen + 1}`);
    console.log(`${'='.repeat(50)}`);

    // Evolve: create new prompts from best of current generation
    const newPromptIds = await evolvePrompts(datasetId, gen);

    // Score each new prompt
    for (let i = 0; i < newPromptIds.length; i++) {
      console.log(`\n  --- Prompt ${i + 1}/${newPromptIds.length} (gen ${gen + 1}) ---`);
      await scoreSongs(newPromptIds[i]);
    }

    // Find and mark best of this new generation
    const { rows: [best] } = await db.query(`
      SELECT id, accuracy, f1_score FROM scoring_prompts
      WHERE dataset_id = $1 AND generation = $2 AND status = 'scored'
      ORDER BY accuracy DESC, f1_score DESC
      LIMIT 1
    `, [datasetId, gen + 1]);

    if (best) {
      console.log(`\n  Best gen ${gen + 1}: id=${best.id} accuracy=${(best.accuracy * 100).toFixed(1)}% F1=${(best.f1_score * 100).toFixed(1)}%`);
    }
  }

  // Summary
  await printSummary(datasetId);

  const totalElapsed = ((Date.now() - totalStart) / 1000 / 60).toFixed(1);
  console.log(`\nTotal time: ${totalElapsed} minutes`);

  await closeDb();
}

async function printSummary(datasetId: string) {
  const db = getDb();

  console.log('\n\n=== SCORING SUMMARY ===\n');

  const { rows: prompts } = await db.query(`
    SELECT id, generation, variant_number, accuracy, precision_score, recall, f1_score,
           tp, fp, tn, fn,
           hypothesis
    FROM scoring_prompts
    WHERE dataset_id = $1 AND status = 'scored'
    ORDER BY generation, accuracy DESC
  `, [datasetId]);

  // Header
  console.log(
    'Gen'.padEnd(5) +
    'Var'.padEnd(5) +
    'Acc%'.padEnd(8) +
    'Prec%'.padEnd(8) +
    'Rec%'.padEnd(8) +
    'F1%'.padEnd(8) +
    'TP'.padEnd(6) +
    'FP'.padEnd(6) +
    'TN'.padEnd(6) +
    'FN'.padEnd(6) +
    'Hypothesis'
  );
  console.log('-'.repeat(100));

  for (const p of prompts) {
    console.log(
      String(p.generation).padEnd(5) +
      String(p.variant_number).padEnd(5) +
      (p.accuracy * 100).toFixed(1).padEnd(8) +
      (p.precision_score * 100).toFixed(1).padEnd(8) +
      (p.recall * 100).toFixed(1).padEnd(8) +
      (p.f1_score * 100).toFixed(1).padEnd(8) +
      String(p.tp).padEnd(6) +
      String(p.fp).padEnd(6) +
      String(p.tn).padEnd(6) +
      String(p.fn).padEnd(6) +
      (p.hypothesis || 'seed').slice(0, 40)
    );
  }

  // Overall best
  const best = prompts.reduce((a, b) => (a.accuracy > b.accuracy || (a.accuracy === b.accuracy && a.f1_score > b.f1_score)) ? a : b, prompts[0]);
  if (best) {
    console.log(`\nBest overall: gen ${best.generation}, var ${best.variant_number} — Accuracy: ${(best.accuracy * 100).toFixed(1)}%, F1: ${(best.f1_score * 100).toFixed(1)}%`);
  }
}

main().catch((err) => {
  console.error('\nFatal error:', err);
  closeDb().finally(() => process.exit(1));
});
