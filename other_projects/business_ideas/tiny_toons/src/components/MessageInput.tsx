interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  maxLength?: number;
  disabled?: boolean;
}

export function MessageInput({ value, onChange, maxLength = 500, disabled }: MessageInputProps) {
  return (
    <div className="mx-5 mb-4">
      <div className="text-xs font-bold uppercase tracking-wider text-purple-500 mb-2 ml-1">
        Your Message
      </div>
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-4 shadow-sm border-2 border-purple-100">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value.slice(0, maxLength))}
          disabled={disabled}
          placeholder={"What do you want to say?\n\ne.g. Happy birthday Mom! You're the best and I love you so much."}
          className="w-full min-h-[100px] bg-transparent text-gray-700 placeholder-purple-300 text-base leading-relaxed resize-none outline-none font-medium"
        />
        <div className="text-right text-xs text-purple-300 mt-1">
          {value.length} / {maxLength}
        </div>
      </div>
    </div>
  );
}
