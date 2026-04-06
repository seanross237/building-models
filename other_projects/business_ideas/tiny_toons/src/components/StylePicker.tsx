import { useState } from "react";

const PRESET_STYLES = ["Pop", "R&B", "Country", "Jazz", "Hip Hop", "Rock"];

interface StylePickerProps {
  value: string;
  onChange: (style: string) => void;
  disabled?: boolean;
}

export function StylePicker({ value, onChange, disabled }: StylePickerProps) {
  const [showCustom, setShowCustom] = useState(false);
  const isPreset = PRESET_STYLES.includes(value);

  return (
    <div className="mx-5 mb-5">
      <div className="text-xs font-bold uppercase tracking-wider text-purple-500 mb-2 ml-1">
        Choose a Style
      </div>
      <div className="flex flex-wrap gap-2">
        {PRESET_STYLES.map((style) => (
          <button
            key={style}
            disabled={disabled}
            onClick={() => {
              setShowCustom(false);
              onChange(style);
            }}
            className={`px-4 py-2.5 rounded-full text-sm font-semibold transition-all ${
              value === style
                ? "bg-gradient-to-r from-purple-500 to-pink-400 text-white shadow-md shadow-purple-300/40 scale-105"
                : "bg-white/80 text-purple-400 border-2 border-purple-100 hover:border-purple-200"
            }`}
          >
            {style}
          </button>
        ))}
        <button
          disabled={disabled}
          onClick={() => {
            setShowCustom(true);
            if (isPreset) onChange("");
          }}
          className={`px-4 py-2.5 rounded-full text-sm font-semibold transition-all ${
            showCustom
              ? "bg-gradient-to-r from-purple-500 to-pink-400 text-white shadow-md shadow-purple-300/40 scale-105"
              : "bg-white/80 text-purple-300 border-2 border-dashed border-purple-200 hover:border-purple-300"
          }`}
        >
          Custom...
        </button>
      </div>
      {showCustom && (
        <input
          type="text"
          value={isPreset ? "" : value}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          placeholder="e.g. Bossa nova, Lo-fi chill, K-pop..."
          className="mt-3 w-full px-4 py-3 rounded-xl bg-white/80 border-2 border-purple-100 text-gray-700 placeholder-purple-300 text-sm font-medium outline-none focus:border-purple-300 transition-colors"
          autoFocus
        />
      )}
    </div>
  );
}
