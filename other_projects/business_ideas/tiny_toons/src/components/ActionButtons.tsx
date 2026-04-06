interface ActionButtonsProps {
  onRegenerate: () => void;
  onShare: () => void;
  disabled?: boolean;
}

export function ActionButtons({ onRegenerate, onShare, disabled }: ActionButtonsProps) {
  return (
    <div className="flex gap-3 mx-5 mb-8">
      <button
        onClick={onRegenerate}
        disabled={disabled}
        className="flex-1 py-3.5 rounded-2xl font-bold text-purple-500 bg-purple-50 border-2 border-purple-100 hover:bg-purple-100 disabled:opacity-50 transition-colors"
      >
        Regenerate
      </button>
      <button
        onClick={onShare}
        disabled={disabled}
        className="flex-1 py-3.5 rounded-2xl font-bold text-white bg-gradient-to-r from-emerald-400 to-green-400 shadow-md shadow-green-300/30 hover:shadow-lg disabled:opacity-50 transition-all"
      >
        Send It!
      </button>
    </div>
  );
}
