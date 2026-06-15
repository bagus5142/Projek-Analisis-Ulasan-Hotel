import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { ASPECTS, COLORS } from "../../data/constants";
import { Legend } from "./Legend";

export interface RadarSeries {
  name: string;
  color: string;
  scores: Record<string, number>;
}

export function AspectRadar({ series }: { series: RadarSeries[] }) {
  const data = ASPECTS.map((a) => {
    const row: Record<string, string | number> = { aspek: a };
    series.forEach((s) => (row[s.name] = s.scores[a] ?? 0));
    return row;
  });
  return (
    <div>
      <ResponsiveContainer width="100%" height={360}>
        <RadarChart data={data} outerRadius="72%">
          <PolarGrid stroke={COLORS.grid} />
          <PolarAngleAxis dataKey="aspek" tick={{ fontSize: 10, fill: COLORS.muted }} />
          <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 9, fill: COLORS.muted }} angle={90} />
          {series.map((s) => (
            <Radar key={s.name} name={s.name} dataKey={s.name} stroke={s.color} fill={s.color} fillOpacity={0.18} strokeWidth={2} />
          ))}
          <Tooltip
            formatter={(v: number, n) => [`${v}%`, n as string]}
            contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }}
          />
        </RadarChart>
      </ResponsiveContainer>
      <div className="mt-2 flex justify-center">
        <Legend items={series.map((s) => ({ label: s.name, color: s.color }))} />
      </div>
    </div>
  );
}
