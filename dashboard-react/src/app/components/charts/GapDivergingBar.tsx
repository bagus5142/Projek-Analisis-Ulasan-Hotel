import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { COLORS } from "../../data/constants";
import type { GapRow } from "../../lib/aggregate";

export function GapDivergingBar({ data }: { data: GapRow[] }) {
  const max = Math.max(8, ...data.map((d) => Math.abs(d.gap))) * 1.15;
  return (
    <div>
      <ResponsiveContainer width="100%" height={Math.max(300, data.length * 30)}>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 24, left: 8, bottom: 4 }}>
          <CartesianGrid horizontal={false} stroke={COLORS.grid} />
          <XAxis
            type="number"
            domain={[-max, max]}
            tickFormatter={(v) => `${v > 0 ? "+" : ""}${v}`}
            tick={{ fontSize: 11, fill: COLORS.muted }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis type="category" dataKey="aspek" width={130} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <Tooltip
            formatter={(v: number) => [`${v > 0 ? "+" : ""}${v} poin`, "Selisih (BUMN − Kompetitor)"]}
            contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }}
          />
          <ReferenceLine x={0} stroke={COLORS.muted} />
          <Bar dataKey="gap" radius={2}>
            {data.map((d) => (
              <Cell key={d.aspek} fill={d.gap >= 0 ? COLORS.bumn : COLORS.komp} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="text-muted-foreground mt-2" style={{ fontSize: 12 }}>
        Biru = BUMN unggul, Amber = Kompetitor unggul (poin % sentimen positif).
      </p>
    </div>
  );
}
