import type { ReactNode } from "react";
import { Card } from "../ui/card";

interface Props {
  label: string;
  value: ReactNode;
  hint?: ReactNode;
  accent?: string;
  icon?: ReactNode;
}

export function MetricCard({ label, value, hint, accent, icon }: Props) {
  return (
    <Card className="gap-0 p-5">
      <div className="flex items-start justify-between">
        <span
          className="text-muted-foreground uppercase"
          style={{ fontSize: 11, letterSpacing: "0.05em", fontWeight: 600 }}
        >
          {label}
        </span>
        {icon && <span style={{ color: accent }}>{icon}</span>}
      </div>
      <div className="mt-2" style={{ fontSize: 30, fontWeight: 700, lineHeight: 1.1, color: accent }}>
        {value}
      </div>
      {hint && <div className="text-muted-foreground mt-1" style={{ fontSize: 12 }}>{hint}</div>}
    </Card>
  );
}
