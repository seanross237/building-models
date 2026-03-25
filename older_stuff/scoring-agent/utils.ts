import pg from 'pg';

const { Pool } = pg;

let pool: pg.Pool | null = null;

export function getDb(): pg.Pool {
  if (!pool) {
    pool = new Pool({ connectionString: process.env.POOLER_URL });
  }
  return pool;
}

export function checkEnv(): void {
  const missing: string[] = [];
  if (!process.env.POOLER_URL) missing.push('POOLER_URL');
  if (!process.env.VITE_SUPABASE_URL) missing.push('VITE_SUPABASE_URL');
  if (!process.env.VITE_SUPABASE_PUBLISHABLE_KEY) missing.push('VITE_SUPABASE_PUBLISHABLE_KEY');
  if (missing.length > 0) {
    console.error(`Missing required env vars: ${missing.join(', ')}`);
    console.error('Run: source .env && npx tsx atlas-supporting-model-experiments/02-23-scoring-agent/run-scoring.ts');
    process.exit(1);
  }
}

/**
 * Call OpenRouter via the scoring-agent-llm edge function.
 * Keeps OPENROUTER_API_KEY server-side in Supabase secrets.
 */
export async function callOpenRouter(
  model: string,
  systemPrompt: string,
  userPrompt: string,
  options?: { temperature?: number }
): Promise<any> {
  const supabaseUrl = process.env.VITE_SUPABASE_URL;
  const anonKey = process.env.VITE_SUPABASE_PUBLISHABLE_KEY;

  const response = await fetch(`${supabaseUrl}/functions/v1/scoring-agent-llm`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${anonKey}`,
      'Content-Type': 'application/json',
      'apikey': anonKey!,
    },
    body: JSON.stringify({
      model,
      system_prompt: systemPrompt,
      user_prompt: userPrompt,
      temperature: options?.temperature ?? 0.1,
      admin_password: 'ggbb',
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Edge function error (${response.status}): ${text}`);
  }

  const data = await response.json();
  if (!data.content) {
    throw new Error('No content in edge function response');
  }
  // Strip markdown code fences if present (LLMs sometimes add them despite json_object mode)
  let content = data.content.trim();
  if (content.startsWith('```')) {
    content = content.replace(/^```(?:json)?\s*\n?/, '').replace(/\n?```\s*$/, '');
  }
  return JSON.parse(content);
}

export interface Metrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  tp: number;
  fp: number;
  tn: number;
  fn: number;
}

export function computeMetrics(predictions: { predicted: boolean; actual: boolean }[]): Metrics {
  let tp = 0, fp = 0, tn = 0, fn = 0;

  for (const p of predictions) {
    if (p.predicted && p.actual) tp++;
    else if (p.predicted && !p.actual) fp++;
    else if (!p.predicted && !p.actual) tn++;
    else fn++;
  }

  const total = tp + fp + tn + fn;
  const accuracy = total > 0 ? (tp + tn) / total : 0;
  const precision = (tp + fp) > 0 ? tp / (tp + fp) : 0;
  const recall = (tp + fn) > 0 ? tp / (tp + fn) : 0;
  const f1 = (precision + recall) > 0 ? 2 * (precision * recall) / (precision + recall) : 0;

  return { accuracy, precision, recall, f1, tp, fp, tn, fn };
}

export async function closeDb(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
  }
}
