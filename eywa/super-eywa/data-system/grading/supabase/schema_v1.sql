create table if not exists public.benchmark_questions (
  question_id text primary key,
  title text not null,
  family text not null,
  question_file text not null,
  has_question boolean not null default false,
  has_task boolean not null default false,
  has_correct_answer boolean not null default false,
  grading_text text not null default '',
  intended_grading_mode text not null default 'unknown',
  currently_auto_graded boolean not null default false,
  source_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.graded_runs (
  run_id text primary key,
  question_id text not null references public.benchmark_questions(question_id) on delete cascade,
  label text not null,
  runtime_provider text not null,
  model text not null,
  grader_provider text,
  grader_model text,
  grading_method text,
  task_correct boolean,
  task_score double precision,
  submission_compliance text,
  recovery_used boolean,
  submission_source text,
  recovery_notes text,
  grading_trace_path text,
  reviewer_provider text,
  reviewer_model text,
  validation_status text,
  grading_status text,
  correct boolean,
  score double precision,
  node_count integer,
  total_tokens bigint,
  total_wall_time_ms bigint,
  total_cost_usd double precision,
  task_text text,
  root_result_excerpt text,
  final_result_excerpt text,
  final_result_node_id text,
  final_result_path text,
  submission_artifact_refs jsonb not null default '[]'::jsonb,
  coding_execution jsonb not null default '{}'::jsonb,
  run_dir text,
  grading_record_path text,
  review_record_path text,
  tutor_record_path text,
  run_level_variable_overrides jsonb not null default '{}'::jsonb,
  root_variables jsonb not null default '{}'::jsonb,
  root_orchestration jsonb not null default '{}'::jsonb,
  grading jsonb not null default '{}'::jsonb,
  review jsonb not null default '{}'::jsonb,
  tutor jsonb not null default '{}'::jsonb,
  mx1_loop_id text,
  mx1_family text,
  mx1_iteration_index integer,
  mx1_iteration_kind text,
  mx1_prompt_text text,
  mx1_prompt_file text,
  mx1_child_prompt_family text,
  mx1_child_prompt_text text,
  mx1_tutor_record_path text,
  mx1_loop_manifest_path text,
  mx1_is_best boolean,
  mx1_best_iteration_index integer,
  mx1_best_run_id text,
  mx1_best_score double precision,
  mx1_best_prompt_text text,
  mx1 jsonb not null default '{}'::jsonb,
  source_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.graded_runs add column if not exists total_tokens bigint;
alter table public.graded_runs add column if not exists total_wall_time_ms bigint;
alter table public.graded_runs add column if not exists total_cost_usd double precision;
alter table public.graded_runs add column if not exists grader_provider text;
alter table public.graded_runs add column if not exists grader_model text;
alter table public.graded_runs add column if not exists grading_method text;
alter table public.graded_runs add column if not exists task_correct boolean;
alter table public.graded_runs add column if not exists task_score double precision;
alter table public.graded_runs add column if not exists submission_compliance text;
alter table public.graded_runs add column if not exists recovery_used boolean;
alter table public.graded_runs add column if not exists submission_source text;
alter table public.graded_runs add column if not exists recovery_notes text;
alter table public.graded_runs add column if not exists grading_trace_path text;
alter table public.graded_runs add column if not exists tutor_record_path text;
alter table public.graded_runs add column if not exists final_result_excerpt text;
alter table public.graded_runs add column if not exists final_result_node_id text;
alter table public.graded_runs add column if not exists final_result_path text;
alter table public.graded_runs add column if not exists submission_artifact_refs jsonb not null default '[]'::jsonb;
alter table public.graded_runs add column if not exists coding_execution jsonb not null default '{}'::jsonb;
alter table public.graded_runs add column if not exists tutor jsonb not null default '{}'::jsonb;
alter table public.graded_runs add column if not exists mx1_loop_id text;
alter table public.graded_runs add column if not exists mx1_family text;
alter table public.graded_runs add column if not exists mx1_iteration_index integer;
alter table public.graded_runs add column if not exists mx1_iteration_kind text;
alter table public.graded_runs add column if not exists mx1_prompt_text text;
alter table public.graded_runs add column if not exists mx1_prompt_file text;
alter table public.graded_runs add column if not exists mx1_child_prompt_family text;
alter table public.graded_runs add column if not exists mx1_child_prompt_text text;
alter table public.graded_runs add column if not exists mx1_tutor_record_path text;
alter table public.graded_runs add column if not exists mx1_loop_manifest_path text;
alter table public.graded_runs add column if not exists mx1_is_best boolean;
alter table public.graded_runs add column if not exists mx1_best_iteration_index integer;
alter table public.graded_runs add column if not exists mx1_best_run_id text;
alter table public.graded_runs add column if not exists mx1_best_score double precision;
alter table public.graded_runs add column if not exists mx1_best_prompt_text text;
alter table public.graded_runs add column if not exists mx1 jsonb not null default '{}'::jsonb;

create index if not exists graded_runs_question_id_idx on public.graded_runs(question_id);
create index if not exists graded_runs_label_idx on public.graded_runs(label);

create table if not exists public.experiment_runs (
  experiment_run_id text primary key,
  benchmark_id text not null,
  runtime_provider text not null,
  model text not null,
  reviewer_provider text,
  reviewer_model text,
  execute_prompt_file text,
  transmute_prompt_file text,
  summary_path text,
  benchmark jsonb not null default '{}'::jsonb,
  variants jsonb not null default '{}'::jsonb,
  aggregate jsonb not null default '{}'::jsonb,
  source_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists experiment_runs_benchmark_id_idx on public.experiment_runs(benchmark_id);

create table if not exists public.experiment_run_cases (
  experiment_run_id text not null references public.experiment_runs(experiment_run_id) on delete cascade,
  question_id text not null references public.benchmark_questions(question_id) on delete cascade,
  variant_id text not null,
  variant_title text,
  question_file text,
  domain text,
  why_included text,
  run_id text references public.graded_runs(run_id) on delete set null,
  score double precision,
  correct boolean,
  grading_status text,
  review_assessment text,
  row_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (experiment_run_id, question_id, variant_id)
);

create index if not exists experiment_run_cases_run_id_idx on public.experiment_run_cases(run_id);

notify pgrst, 'reload schema';
