import { COLORS } from "../../data/constants";
import type { Phrase } from "../../data/types";

interface Props {
  title?: string;
  frasaPos: Phrase[];
  frasaNeg: Phrase[];
}

function Column({ phrases, kind }: { phrases: Phrase[]; kind: "pos" | "neg" }) {
  const isPos = kind === "pos";
  return (
    <div className="flex-1">
      <div
        className="mb-2 uppercase"
        style={{ fontSize: 11, letterSpacing: "0.04em", fontWeight: 600, color: isPos ? COLORS.pos : COLORS.neg }}
      >
        {isPos ? "Top 5 Kelebihan" : "Top 5 Kekurangan"}
      </div>
      <div className="flex flex-col gap-1.5">
        {phrases.length === 0 && <span className="text-muted-foreground" style={{ fontSize: 12 }}>—</span>}
        {phrases.map((p) => (
          <div
            key={p.phrase}
            className="flex items-center justify-between rounded-md px-2.5 py-1.5"
            style={{ background: isPos ? COLORS.posSoft : COLORS.negSoft, fontSize: 13 }}
          >
            <span className="truncate">{p.phrase}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function KeyPhrases({ frasaPos, frasaNeg }: Props) {
  return (
    <div className="flex gap-4">
      <Column phrases={frasaNeg} kind="neg" />
      <Column phrases={frasaPos} kind="pos" />
    </div>
  );
}
