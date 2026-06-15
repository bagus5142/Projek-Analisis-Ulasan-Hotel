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
import type { AspectRow } from "../../lib/aggregate";
import { Legend } from "./Legend";

const axisStyle = { fontSize: 11, fill: COLORS.muted };

export function DivergingAspectBar({ data }: { data: AspectRow[] }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={Math.max(280, data.length * 30)}>
        <BarChart
          data={data}
          layout="vertical"
          stackOffset="sign"
          margin={{ top: 4, right: 16, left: 8, bottom: 4 }}
          barCategoryGap={6}
        >
          <CartesianGrid horizontal={false} stroke={COLORS.grid} />
          <XAxis
            type="number"
            domain={[-60, 100]}
            tickFormatter={(v) => `${Math.abs(v)}%`}
            tick={axisStyle}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="aspek"
            width={130}
            tick={axisStyle}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            formatter={(v: number, name) => [`${Math.abs(v)}%`, name === "neg" ? "Negatif" : "Positif"]}
            contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }}
          />
          <ReferenceLine x={0} stroke={COLORS.muted} />
          <Bar dataKey="neg" stackId="s" radius={[3, 0, 0, 3]}>
            {data.map((d) => (
              <Cell key={d.aspek} fill={COLORS.neg} />
            ))}
          </Bar>
          <Bar dataKey="pos" stackId="s" radius={[0, 3, 3, 0]}>
            {data.map((d) => (
              <Cell key={d.aspek} fill={COLORS.pos} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-3">
        <Legend items={[{ label: "Positif", color: COLORS.pos }, { label: "Negatif", color: COLORS.neg }]} />
      </div>
    </div>
  );
}
