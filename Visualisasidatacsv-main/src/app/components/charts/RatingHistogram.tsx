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
import { Legend } from "./Legend";

interface Row {
  rating: string;
  BUMN: number;
  KOMPETITOR: number;
  total: number;
}

export function RatingHistogram({ data, split = true }: { data: Row[]; split?: boolean }) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 4 }} barGap={4}>
          <CartesianGrid stroke={COLORS.grid} vertical={false} />
          <XAxis dataKey="rating" tick={{ fontSize: 12, fill: COLORS.muted }} axisLine={false} tickLine={false} />
          <YAxis tickFormatter={(v) => fmt(v)} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} width={48} />
          <Tooltip formatter={(v: number, n) => [fmt(v), n === "KOMPETITOR" ? "Kompetitor" : n === "BUMN" ? "BUMN" : "Total"]} contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} />
          {split ? (
            <>
              <Bar dataKey="BUMN" fill={COLORS.bumn} radius={[3, 3, 0, 0]} />
              <Bar dataKey="KOMPETITOR" fill={COLORS.komp} radius={[3, 3, 0, 0]} />
            </>
          ) : (
            <Bar dataKey="total" fill={COLORS.bumn} radius={[3, 3, 0, 0]} />
          )}
        </BarChart>
      </ResponsiveContainer>
      {split && (
        <div className="mt-3">
          <Legend items={[{ label: "BUMN", color: COLORS.bumn }, { label: "Kompetitor", color: COLORS.komp }]} />
        </div>
      )}
    </div>
  );
}
