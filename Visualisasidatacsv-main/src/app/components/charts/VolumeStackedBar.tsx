import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { COLORS, fmt } from "../../data/constants";
import type { TrendPoint } from "../../lib/aggregate";
import { Legend } from "./Legend";

export function VolumeStackedBar({ data }: { data: TrendPoint[] }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
          <CartesianGrid stroke={COLORS.grid} vertical={false} />
          <XAxis dataKey="bulan" tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <YAxis tickFormatter={(v) => fmt(v)} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} width={48} />
          <Tooltip formatter={(v: number, n) => [fmt(v), n === "volNeg" ? "Negatif" : "Positif"]} contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} />
          <Bar dataKey="volPos" stackId="v" fill={COLORS.pos} radius={[0, 0, 0, 0]} />
          <Bar dataKey="volNeg" stackId="v" fill={COLORS.neg} radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-3">
        <Legend items={[{ label: "Positif", color: COLORS.pos }, { label: "Negatif", color: COLORS.neg }]} />
      </div>
    </div>
  );
}
