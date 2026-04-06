// Floating decorative music notes scattered around the background
const notes = [
  { char: "♪", top: "3%", left: "8%", size: "text-2xl", color: "text-pink-300/50", rotate: "-12deg" },
  { char: "♫", top: "6%", right: "12%", size: "text-xl", color: "text-purple-300/40", rotate: "15deg" },
  { char: "♪", top: "15%", left: "4%", size: "text-lg", color: "text-purple-200/50", rotate: "25deg" },
  { char: "♫", top: "22%", right: "6%", size: "text-2xl", color: "text-pink-200/40", rotate: "-20deg" },
  { char: "♪", top: "40%", left: "2%", size: "text-xl", color: "text-purple-300/30", rotate: "10deg" },
  { char: "♫", top: "55%", right: "4%", size: "text-lg", color: "text-pink-300/40", rotate: "-15deg" },
  { char: "♪", top: "70%", left: "6%", size: "text-2xl", color: "text-purple-200/50", rotate: "20deg" },
  { char: "♫", top: "82%", right: "10%", size: "text-xl", color: "text-pink-200/30", rotate: "-8deg" },
  { char: "♪", top: "90%", left: "15%", size: "text-lg", color: "text-purple-300/40", rotate: "30deg" },
];

export function MusicNotes() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
      {notes.map((note, i) => (
        <span
          key={i}
          className={`absolute ${note.size} ${note.color} select-none`}
          style={{
            top: note.top,
            left: note.left,
            right: note.right,
            transform: `rotate(${note.rotate})`,
          }}
        >
          {note.char}
        </span>
      ))}
    </div>
  );
}
