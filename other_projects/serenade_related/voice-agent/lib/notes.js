const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

function headers() {
  return {
    apikey: SUPABASE_KEY,
    Authorization: `Bearer ${SUPABASE_KEY}`,
    "Content-Type": "application/json",
  };
}

async function addNote(whatSeanSaid, { seanLearnings = false, suggestedFile = null, suggestedSection = null } = {}) {
  const row = { what_sean_said: whatSeanSaid };
  if (seanLearnings) row.sean_learnings = true;
  if (suggestedFile) row.suggested_file = suggestedFile;
  if (suggestedSection) row.suggested_section = suggestedSection;

  const res = await fetch(`${SUPABASE_URL}/rest/v1/voice_agent_notes`, {
    method: "POST",
    headers: { ...headers(), Prefer: "return=representation" },
    body: JSON.stringify(row),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to add note: ${res.status} ${err}`);
  }

  const [created] = await res.json();
  return created;
}

async function listNotes({ handled } = {}) {
  const params = new URLSearchParams({ order: "created_at.desc" });
  if (handled !== undefined) params.append("handled", `eq.${handled}`);

  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/voice_agent_notes?${params}`,
    { headers: headers() }
  );

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to list notes: ${res.status} ${err}`);
  }

  return res.json();
}

async function handleNote(id) {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/voice_agent_notes?id=eq.${id}`,
    {
      method: "PATCH",
      headers: { ...headers(), Prefer: "return=representation" },
      body: JSON.stringify({ handled: true }),
    }
  );

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to handle note: ${res.status} ${err}`);
  }

  return res.json();
}

module.exports = { addNote, listNotes, handleNote };
