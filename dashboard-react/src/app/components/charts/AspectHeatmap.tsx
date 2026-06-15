import { ASPECTS, type Aspect } from "../../data/constants";

interface Props {
  columns: { key: string; label: string }[];
  // scores[colKey][aspek] = 0..100
  scores: Record<string, Record<Aspect, number>>;
}

function cellColor(v: number): string {
  // merah (rendah) → kuning → hijau (tinggi)
  const t = Math.max(0, Math.min(100, v)) / 100;
  const hue = t * 120; // 0 = merah, 120 = hijau
  return `hsl(${hue}, 70%, ${88 - t * 28}%)`;
}

export function AspectHeatmap({ columns, scores }: Props) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-separate" style={{ borderSpacing: 3 }}>
        <thead>
          <tr>
            <th className="text-left text-muted-foreground" style={{ fontSize: 11, fontWeight: 600, padding: "4px 8px" }}></th>
            {columns.map((c) => (
              <th key={c.key} className="text-muted-foreground text-center" style={{ fontSize: 11, fontWeight: 600, padding: "4px 8px" }}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {ASPECTS.map((a) => (
            <tr key={a}>
              <td className="whitespace-nowrap pr-2" style={{ fontSize: 12 }}>{a}</td>
              {columns.map((c) => {
                const v = scores[c.key]?.[a] ?? 0;
                return (
                  <td key={c.key} className="text-center" style={{ background: cellColor(v), borderRadius: 6, padding: "8px 10px", fontSize: 12, fontWeight: 600, color: "#1f2937", minWidth: 64 }}>
                    {v}%
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
