import type { ReactNode } from "react";
import { Card } from "../ui/card";

interface Props {
  title: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function ChartCard({ title, description, action, children, className }: Props) {
  return (
    <Card className={`gap-0 p-5 ${className ?? ""}`}>
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h3 style={{ fontSize: 15, fontWeight: 600, lineHeight: 1.3 }}>{title}</h3>
          {description && (
            <p className="text-muted-foreground mt-0.5" style={{ fontSize: 12 }}>
              {description}
            </p>
          )}
        </div>
        {action}
      </div>
      {children}
    </Card>
  );
}
