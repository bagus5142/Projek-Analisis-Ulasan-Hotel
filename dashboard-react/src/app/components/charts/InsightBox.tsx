import { Lightbulb } from "lucide-react";

export function InsightBox({ text }: { text: string }) {
  if (!text) return null;
  return (
    <div className="mt-4 p-4 rounded-xl bg-gradient-to-br from-indigo-50/50 to-purple-50/50 border border-indigo-100/50 flex items-start gap-3 shadow-sm">
      <div className="bg-white p-1.5 rounded-full shadow-sm border border-indigo-50 shrink-0 mt-0.5">
        <Lightbulb className="w-4 h-4 text-indigo-500" />
      </div>
      <div>
        <h4 className="text-xs font-bold text-indigo-900/80 uppercase tracking-wider mb-1">Executive Insight</h4>
        <p className="text-sm text-slate-700 leading-relaxed font-medium">
          {text}
        </p>
      </div>
    </div>
  );
}
