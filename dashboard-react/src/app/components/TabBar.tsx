export const PAGES = [
  { key: "ringkasan", label: "Ringkasan" },
  { key: "perbandingan", label: "Perbandingan" },
  { key: "bintang", label: "Per Bintang" },
  { key: "peringkat", label: "Peringkat" },
  { key: "detail", label: "Detail Hotel" },
  { key: "tren", label: "Tren" },
] as const;

export type PageKey = (typeof PAGES)[number]["key"];

export function TabBar({ active, onChange }: { active: PageKey; onChange: (k: PageKey) => void }) {
  return (
    <div className="border-b">
      <div className="flex gap-1 overflow-x-auto">
        {PAGES.map((p) => {
          const isActive = p.key === active;
          return (
            <button
              key={p.key}
              onClick={() => onChange(p.key)}
              className={`relative whitespace-nowrap px-3 py-2.5 transition-colors ${
                isActive ? "text-foreground" : "text-muted-foreground hover:text-foreground"
              }`}
              style={{ fontSize: 14, fontWeight: isActive ? 600 : 500 }}
            >
              {p.label}
              {isActive && <span className="bg-primary absolute inset-x-2 -bottom-px h-0.5 rounded-full" />}
            </button>
          );
        })}
      </div>
    </div>
  );
}
