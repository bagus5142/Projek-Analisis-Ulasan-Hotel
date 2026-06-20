import { useState, useEffect, useMemo } from "react";
import { ChartCard } from "../charts/ChartCard";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { useFilter } from "../../context/FilterContext";
import { ChevronLeft, ChevronRight, Search, FileText } from "lucide-react";

interface ReviewRow {
  "Review Time": string;
  Rating: string;
  "Review Text": string;
  "Nama Hotel": string;
  Kategori: string;
  Bintang: string;
  AI_Sentiment: string;
  AI_Primary_Theme: string;
}

const ROWS_PER_PAGE = 50;

export function RawDataPage() {
  const { filter } = useFilter();
  const [data, setData] = useState<ReviewRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    // Load JSON on mount
    setLoading(true);
    fetch("/reviews_lite.json")
      .then(res => res.json())
      .then(data => {
        setData(data as ReviewRow[]);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading JSON:", err);
        setLoading(false);
      });
  }, []);

  // Filter the data based on global context (kategori) and local search
  const filteredData = useMemo(() => {
    return data.filter((row) => {
      // Global Kategori Filter
      if (filter.kategori !== "SEMUA") {
        if (row.Kategori !== filter.kategori) return false;
      }
      
      // Local Search Query (Hotel Name or Review Text)
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const hotelMatch = row["Nama Hotel"]?.toLowerCase().includes(query);
        const textMatch = row["Review Text"]?.toLowerCase().includes(query);
        if (!hotelMatch && !textMatch) return false;
      }
      
      return true;
    });
  }, [data, filter.kategori, searchQuery]);

  const totalPages = Math.ceil(filteredData.length / ROWS_PER_PAGE) || 1;
  const startIndex = (page - 1) * ROWS_PER_PAGE;
  const currentRows = filteredData.slice(startIndex, startIndex + ROWS_PER_PAGE);

  // Reset page when filter changes
  useEffect(() => {
    setPage(1);
  }, [filter.kategori, searchQuery]);

  const getSentimentColor = (sentiment: string) => {
    const s = sentiment?.toLowerCase();
    if (s?.includes("pos")) return "bg-emerald-500/10 text-emerald-500 border-emerald-500/20";
    if (s?.includes("neg")) return "bg-rose-500/10 text-rose-500 border-rose-500/20";
    return "bg-amber-500/10 text-amber-500 border-amber-500/20";
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in duration-500">
      <ChartCard 
        title="Database Ulasan Mentah" 
        description="Tinjau secara langsung setiap baris ulasan dari dataset CSV asli."
      >
        {/* Toolbar */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
          <div className="relative w-full sm:w-96">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-muted-foreground" />
            </div>
            <input
              type="text"
              placeholder="Cari nama hotel atau isi ulasan..."
              className="w-full pl-10 pr-4 py-2 bg-background border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <div className="text-sm text-muted-foreground flex items-center gap-2">
            <FileText className="h-4 w-4" />
            Total: <span className="font-semibold text-foreground">{filteredData.length.toLocaleString("id-ID")}</span> baris
          </div>
        </div>

        {/* Table */}
        <div className="rounded-md border border-border overflow-hidden bg-card">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-muted/50 text-muted-foreground text-xs uppercase">
                <tr>
                  <th className="px-4 py-3 font-semibold whitespace-nowrap">TANGGAL</th>
                  <th className="px-4 py-3 font-semibold whitespace-nowrap">HOTEL</th>
                  <th className="px-4 py-3 font-semibold">ULASAN</th>
                  <th className="px-4 py-3 font-semibold whitespace-nowrap">RATING</th>
                  <th className="px-4 py-3 font-semibold whitespace-nowrap text-center">SENTIMEN</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-20 text-center text-muted-foreground">
                      <div className="flex flex-col items-center justify-center gap-2">
                        <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
                        <span>Memuat data ulasan...</span>
                      </div>
                    </td>
                  </tr>
                ) : currentRows.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-20 text-center text-muted-foreground">
                      Tidak ada ulasan yang cocok dengan pencarian Anda.
                    </td>
                  </tr>
                ) : (
                  currentRows.map((row, idx) => (
                    <tr key={idx} className="hover:bg-muted/50 transition-colors">
                      <td className="px-4 py-3 whitespace-nowrap text-muted-foreground">{row["Review Time"]}</td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="font-medium text-foreground">{row["Nama Hotel"]}</div>
                        <div className="text-[10px] text-muted-foreground uppercase mt-0.5">{row.Kategori}</div>
                      </td>
                      <td className="px-4 py-3">
                        <p className="line-clamp-3 text-muted-foreground leading-relaxed" title={row["Review Text"]}>
                          {row["Review Text"] || "-"}
                        </p>
                        {row.AI_Primary_Theme && (
                          <div className="mt-1.5 text-[10px] uppercase font-semibold tracking-wider text-primary/70">
                            {row.AI_Primary_Theme}
                          </div>
                        )}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-center">
                        <div className="flex items-center gap-1 font-medium text-amber-500">
                          {row.Rating} <span className="text-lg leading-none">★</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-center">
                        <Badge variant="outline" className={getSentimentColor(row.AI_Sentiment)}>
                          {row.AI_Sentiment}
                        </Badge>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pagination */}
        {!loading && filteredData.length > 0 && (
          <div className="flex items-center justify-between mt-6">
            <div className="text-sm text-muted-foreground">
              Menampilkan <span className="font-medium text-foreground">{startIndex + 1}</span> - <span className="font-medium text-foreground">{Math.min(startIndex + ROWS_PER_PAGE, filteredData.length)}</span> dari <span className="font-medium text-foreground">{filteredData.length.toLocaleString("id-ID")}</span>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                <ChevronLeft className="h-4 w-4 mr-1" /> Prev
              </Button>
              <div className="flex items-center px-2 text-sm font-medium">
                {page} / {totalPages}
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                Next <ChevronRight className="h-4 w-4 ml-1" />
              </Button>
            </div>
          </div>
        )}
      </ChartCard>
    </div>
  );
}
