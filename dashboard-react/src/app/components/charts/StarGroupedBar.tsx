import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { COLORS, STAR_LABEL, type Star } from "../../data/constants";
import { Legend } from "./Legend";

export function StarGroupedBar({
  data,
}: {
  data: { bintang: Star; BUMN: number; KOMPETITOR: number }[];
}) {
  const rows = data.map((d) => ({ ...d, label: STAR_LABEL[d.bintang] }));
  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={rows} margin={{ top: 8, right: 16, left: 0, bottom: 4 }} barGap={6}>
          <CartesianGrid stroke={COLORS.grid} vertical={false} />
          <XAxis dataKey="label" tick={{ fontSize: 12, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <YAxis domain={[0, 100]} tickFormatter={(v) => `${v}%`} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <Tooltip formatter={(v: number, n) => [`${v}%`, n === "KOMPETITOR" ? "Kompetitor" : "BUMN"]} contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} />
          <Bar dataKey="BUMN" fill={COLORS.bumn} radius={[3, 3, 0, 0]} />
          <Bar dataKey="KOMPETITOR" fill={COLORS.komp} radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-3">
        <Legend items={[{ label: "BUMN", color: COLORS.bumn }, { label: "Kompetitor", color: COLORS.komp }]} />
      </div>
    </div>
  );
}
