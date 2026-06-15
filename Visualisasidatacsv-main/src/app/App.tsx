import { useState } from "react";
import { Database, Upload } from "lucide-react";
import { DataProvider, useData } from "./context/DataContext";
import { FilterProvider } from "./context/FilterContext";
import { FilterSidebar } from "./components/FilterSidebar";
import { TabBar, type PageKey } from "./components/TabBar";
import { UploadDialog } from "./components/UploadDialog";
import { OverviewPage } from "./components/pages/OverviewPage";
import { ComparisonPage } from "./components/pages/ComparisonPage";
import { PerBintangPage } from "./components/pages/PerBintangPage";
import { RankingPage } from "./components/pages/RankingPage";
import { HotelDetailPage } from "./components/pages/HotelDetailPage";
import { TrendsPage } from "./components/pages/TrendsPage";
import { Button } from "./components/ui/button";
import { Badge } from "./components/ui/badge";

function PageContent({ page }: { page: PageKey }) {
  switch (page) {
    case "ringkasan":
      return <OverviewPage />;
    case "perbandingan":
      return <ComparisonPage />;
    case "bintang":
      return <PerBintangPage />;
    case "peringkat":
      return <RankingPage />;
    case "detail":
      return <HotelDetailPage />;
    case "tren":
      return <TrendsPage />;
  }
}

function Shell() {
  const { source } = useData();
  const [page, setPage] = useState<PageKey>("ringkasan");
  const [uploadOpen, setUploadOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-card sticky top-0 z-30 border-b">
        <div className="mx-auto flex max-w-[1280px] items-center justify-between gap-4 px-5 py-3">
          <div className="flex items-center gap-2.5">
            <div className="bg-primary flex size-8 items-center justify-center rounded-md">
              <Database className="size-4 text-primary-foreground" />
            </div>
            <div>
              <h1 style={{ fontSize: 16, fontWeight: 700, lineHeight: 1.2 }}>Analisis Ulasan Hotel</h1>
              <p className="text-muted-foreground" style={{ fontSize: 12 }}>BUMN vs Kompetitor · Sentimen & Aspek Pelayanan</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Badge variant={source === "uploaded" ? "default" : "secondary"}>
              {source === "uploaded" ? "Data diunggah" : "Data demo"}
            </Badge>
            <Button variant="outline" onClick={() => setUploadOpen(true)} className="gap-1.5">
              <Upload className="size-4" /> Muat Data CSV
            </Button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex max-w-[1280px] flex-col gap-6 px-5 py-6 lg:flex-row">
        <FilterSidebar />
        <main className="min-w-0 flex-1">
          <div className="mb-6">
            <TabBar active={page} onChange={setPage} />
          </div>
          <PageContent page={page} />
        </main>
      </div>

      <UploadDialog open={uploadOpen} onOpenChange={setUploadOpen} />
    </div>
  );
}

export default function App() {
  return (
    <DataProvider>
      <FilterProvider>
        <Shell />
      </FilterProvider>
    </DataProvider>
  );
}
