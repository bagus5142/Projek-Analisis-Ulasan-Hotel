import { useMemo } from "react";
import { MONTHS, STARS, STAR_LABEL, fmt } from "../data/constants";
import { useData } from "../context/DataContext";
import { useFilter } from "../context/FilterContext";
import { metrics, scopeHotels } from "../lib/aggregate";
import { ToggleGroup, ToggleGroupItem } from "./ui/toggle-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Slider } from "./ui/slider";
import { Separator } from "./ui/separator";

function FieldLabel({ children }: { children: string }) {
  return (
    <div className="text-muted-foreground mb-2 uppercase" style={{ fontSize: 11, letterSpacing: "0.05em", fontWeight: 600 }}>
      {children}
    </div>
  );
}

export function FilterSidebar() {
  const { hotels } = useData();
  const { filter, setKategori, setBintang, setHotelId, setPeriode } = useFilter();

  const scoped = useMemo(() => scopeHotels(hotels, filter), [hotels, filter]);
  const m = useMemo(() => metrics(scoped, filter), [scoped, filter]);
  const hotelOptions = useMemo(
    () => [...scoped].sort((a, b) => a.nama.localeCompare(b.nama)),
    [scoped],
  );

  return (
    <aside className="bg-sidebar flex w-full flex-col gap-5 rounded-xl border p-5 lg:w-72 lg:shrink-0">
      <div>
        <h2 style={{ fontSize: 15, fontWeight: 600 }}>Filter Data</h2>
        <p className="text-muted-foreground mt-0.5" style={{ fontSize: 12 }}>
          {fmt(m.totalUlasan)} ulasan terpilih
        </p>
      </div>
      <Separator />

      <div>
        <FieldLabel>Kategori</FieldLabel>
        <ToggleGroup
          type="single"
          value={filter.kategori}
          onValueChange={(v) => v && setKategori(v as typeof filter.kategori)}
          variant="outline"
          className="w-full"
        >
          <ToggleGroupItem value="SEMUA" style={{ fontSize: 12 }}>Semua</ToggleGroupItem>
          <ToggleGroupItem value="BUMN" style={{ fontSize: 12 }}>BUMN</ToggleGroupItem>
          <ToggleGroupItem value="KOMPETITOR" style={{ fontSize: 12 }}>Kompetitor</ToggleGroupItem>
        </ToggleGroup>
      </div>

      <div>
        <FieldLabel>Bintang</FieldLabel>
        <ToggleGroup
          type="single"
          value={filter.bintang}
          onValueChange={(v) => v && setBintang(v as typeof filter.bintang)}
          variant="outline"
          className="w-full"
        >
          <ToggleGroupItem value="SEMUA" style={{ fontSize: 12 }}>Semua</ToggleGroupItem>
          {STARS.map((s) => (
            <ToggleGroupItem key={s} value={s} style={{ fontSize: 12 }}>
              {s.replace("bintang", "")}★
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
      </div>

      <div>
        <FieldLabel>Hotel</FieldLabel>
        <Select
          value={filter.hotelId ?? "ALL"}
          onValueChange={(v) => setHotelId(v === "ALL" ? null : v)}
        >
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Semua Hotel" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">Semua Hotel</SelectItem>
            {hotelOptions.map((h) => (
              <SelectItem key={h.id} value={h.id}>
                {h.nama}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {filter.hotelId && (
          <p className="text-muted-foreground mt-1.5" style={{ fontSize: 11 }}>
            Profil & frasa kunci akan muncul di halaman Ringkasan.
          </p>
        )}
      </div>

      <div>
        <FieldLabel>Periode</FieldLabel>
        <Slider
          min={0}
          max={MONTHS.length - 1}
          step={1}
          value={filter.periode}
          onValueChange={(v) => setPeriode([v[0], v[1]] as [number, number])}
          className="mt-2"
        />
        <div className="text-muted-foreground mt-2 flex justify-between" style={{ fontSize: 11 }}>
          <span>{MONTHS[filter.periode[0]]}</span>
          <span>{MONTHS[filter.periode[1]]}</span>
        </div>
      </div>
    </aside>
  );
}
