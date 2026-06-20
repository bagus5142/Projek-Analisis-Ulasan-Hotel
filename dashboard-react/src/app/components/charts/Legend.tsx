interface Item {
  label: string;
  color: string;
  dashed?: boolean;
}

export function Legend({ items }: { items: Item[] }) {
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
      {items.map((it) => (
        <span key={it.label} className="flex items-center gap-1.5 text-muted-foreground" style={{ fontSize: 12 }}>
          {it.dashed ? (
            <span className="inline-block w-3 h-0.5" style={{ borderTop: `2px dashed ${it.color}` }} />
          ) : (
            <span className="inline-block size-2.5 rounded-sm" style={{ background: it.color }} />
          )}
          {it.label}
        </span>
      ))}
    </div>
  );
}
