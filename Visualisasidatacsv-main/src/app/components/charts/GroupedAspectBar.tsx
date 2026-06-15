import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { COLORS, type Aspect } from "../../data/constants";
import { Legend } from "./Legend";

export function GroupedAspectBar({
  data,
}: {
  data: { aspek: Aspect; BUMN: number; KOMPETITOR: number }[];
}) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={Math.max(320, data.length * 34)}>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 16, left: 8, bottom: 4 }} barGap={2}>
          <CartesianGrid horizontal={false} stroke={COLORS.grid} />
          <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <YAxis type="category" dataKey="aspek" width={130} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <Tooltip formatter={(v: number, n) => [`${v}%`, n === "KOMPETITOR" ? "Kompetitor" : "BUMN"]} contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} />
          <Bar dataKey="BUMN" fill={COLORS.bumn} radius={[0, 3, 3, 0]} />
          <Bar dataKey="KOMPETITOR" fill={COLORS.komp} radius={[0, 3, 3, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-3">
        <Legend items={[{ label: "BUMN", color: COLORS.bumn }, { label: "Kompetitor", color: COLORS.komp }]} />
      </div>
    </div>
  );
}
