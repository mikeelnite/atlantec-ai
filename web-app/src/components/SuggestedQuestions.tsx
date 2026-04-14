interface Props {
  onSelect: (question: string) => void;
  disabled: boolean;
}

const suggestions = [
  'What Gaeltacht towns are in County Galway?',
  'Where can I volunteer in Irish-speaking communities?',
  'Tell me about heritage sites in Connemara',
  'What are the best pubs near Gaeltacht areas in Donegal?',
  'How do I say common place names in Irish?',
  'Which counties have the largest Gaeltacht regions?',
];

export default function SuggestedQuestions({ onSelect, disabled }: Props) {
  return (
    <div className="px-4 pb-3">
      <p className="text-xs text-stone-400 font-medium uppercase tracking-wider mb-2">
        Suggested questions
      </p>
      <div className="flex flex-wrap gap-2">
        {suggestions.map((q) => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            disabled={disabled}
            className="text-xs px-3 py-1.5 rounded-full border border-emerald-200 text-emerald-700 bg-emerald-50 hover:bg-emerald-100 hover:border-emerald-300 transition-colors disabled:opacity-40 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
