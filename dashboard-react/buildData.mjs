import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';

const REVIEWS_FILE = path.resolve('../data/AI_Structured_Final.csv');
const PHRASES_FILE = path.resolve('../data/AI_Structured_Keywords.csv');
const OUT_FILE = path.resolve('./src/app/data/hotels.json');
const CONSTANTS_FILE = path.resolve('./src/app/data/constants.ts');
const REVIEWS_LITE_FILE = path.resolve('./public/reviews_lite.json');

const ASPECTS = [
  "Kebersihan", "Kualitas Kamar", "Fasilitas Hotel", "Makanan & Minuman",
  "Pelayanan Staf", "Kecepatan Layanan", "Proses Check-in/out", "Lokasi",
  "Harga", "Keamanan", "Penanganan Keluhan", "Fasilitas Khusus",
];

function get(row, keys) {
  for (const k of Object.keys(row)) {
    const norm = k.trim().toLowerCase().replace(/\s+/g, "");
    for (const want of keys) {
      if (norm === want.toLowerCase().replace(/\s+/g, "")) return (row[k] ?? "").trim();
    }
  }
  return "";
}

function normStar(s) {
  const d = s.replace(/\D/g, "");
  if (d === "5") return "bintang5";
  if (d === "3") return "bintang3";
  return "bintang4";
}

function normKategori(s) {
  return s.trim().toUpperCase().startsWith("BUMN") ? "BUMN" : "KOMPETITOR";
}

function normSentiment(s) {
  const v = s.trim().toLowerCase();
  if (v.startsWith("pos")) return "pos";
  if (v.startsWith("neg")) return "neg";
  return "neu";
}

function emptyAspek() {
  const a = {};
  for (const x of ASPECTS) a[x] = { pos: 0, neg: 0, total: 0 };
  return a;
}

function matchAspect(theme) {
  const t = theme.trim().toLowerCase();
  if (!t) return null;
  for (const a of ASPECTS) if (a.toLowerCase() === t) return a;
  for (const a of ASPECTS) if (t.includes(a.toLowerCase()) || a.toLowerCase().includes(t)) return a;
  return null;
}

const indoMonths = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"];
function formatMonth(yyyyMm) {
  const [y, m] = yyyyMm.split('-');
  return `${indoMonths[parseInt(m, 10) - 1]} ${y}`;
}

async function run() {
  console.log("Reading CSVs...");

  // Parse phrases
  const phraseMap = new Map();
  if (fs.existsSync(PHRASES_FILE)) {
    const pcsv = fs.readFileSync(PHRASES_FILE, 'utf-8');
    Papa.parse(pcsv, {
      header: true,
      skipEmptyLines: true,
      complete: (res) => {
        for (const row of res.data) {
          const nama = get(row, ["Nama_Hotel", "Nama Hotel", "NamaHotel"]);
          if (!nama) continue;
          if (!phraseMap.has(nama)) phraseMap.set(nama, { pos: [], neg: [] });
          const entry = phraseMap.get(nama);
          const pp = get(row, ["Top_Positif_Phrase", "TopPositifPhrase"]);
          const np = get(row, ["Top_Negatif_Phrase", "TopNegatifPhrase"]);
          const bp = parseFloat(get(row, ["Bobot_Pos", "BobotPos"]));
          const bn = parseFloat(get(row, ["Bobot_Neg", "BobotNeg"]));
          if (pp) entry.pos.push({ phrase: pp, bobot: isNaN(bp) ? 0 : bp });
          if (np) entry.neg.push({ phrase: np, bobot: isNaN(bn) ? 0 : bn });
        }
        for (const e of phraseMap.values()) {
          e.pos.sort((a, b) => Math.abs(b.bobot) - Math.abs(a.bobot));
          e.neg.sort((a, b) => Math.abs(b.bobot) - Math.abs(a.bobot));
          e.pos = e.pos.slice(0, 5);
          e.neg = e.neg.slice(0, 5);
        }
      }
    });
  }

  // Parse reviews
  const accs = new Map();
  const rcsv = fs.readFileSync(REVIEWS_FILE, 'utf-8');
  
  // First pass: gather all unique YYYY-MM
  const monthSet = new Set();
  Papa.parse(rcsv, {
    header: true,
    skipEmptyLines: true,
    delimiter: ';',
    step: (res) => {
      const rt = get(res.data, ["Review Time", "ReviewTime", "review_time", "date"]);
      if (rt && rt.length >= 7) {
        monthSet.add(rt.substring(0, 7));
      }
    }
  });
  
  const uniqueMonths = Array.from(monthSet).sort();
  const sortedMonths = [];
  if (uniqueMonths.length > 0) {
    let [currYear, currMonth] = uniqueMonths[0].split('-').map(Number);
    const [endYear, endMonth] = uniqueMonths[uniqueMonths.length - 1].split('-').map(Number);
    
    while (currYear < endYear || (currYear === endYear && currMonth <= endMonth)) {
      const ym = `${currYear}-${String(currMonth).padStart(2, '0')}`;
      sortedMonths.push(ym);
      currMonth++;
      if (currMonth > 12) {
        currMonth = 1;
        currYear++;
      }
    }
  }
  const MONTHS = sortedMonths.map(formatMonth);
  console.log(`Found ${uniqueMonths.length} unique months, expanded to ${MONTHS.length} months from ${sortedMonths[0]} to ${sortedMonths[sortedMonths.length-1]}`);

  // Update constants.ts with dynamic MONTHS
  let constContent = fs.readFileSync(CONSTANTS_FILE, 'utf-8');
  constContent = constContent.replace(
    /export const MONTHS = \[\s*[\s\S]*?\s*\] as const;/,
    `export const MONTHS = ${JSON.stringify(MONTHS, null, 2)} as const;`
  );
  fs.writeFileSync(CONSTANTS_FILE, constContent);
  console.log("Updated constants.ts");

  // Second pass: aggregate data
  const rawReviews = [];
  Papa.parse(rcsv, {
    header: true,
    skipEmptyLines: true,
    delimiter: ';',
    step: (res) => {
      const row = res.data;
      const nama = get(row, ["Nama Hotel", "NamaHotel", "Nama_Hotel", "hotel"]);
      if (!nama) return;
      
      let acc = accs.get(nama);
      if (!acc) {
        acc = {
          nama,
          kategori: normKategori(get(row, ["Kategori", "kategori"])),
          bintang: normStar(get(row, ["Bintang", "bintang"])),
          total: 0, pos: 0, neg: 0, neu: 0,
          ratingSum: 0, ratingDist: [0, 0, 0, 0, 0],
          aspek: emptyAspek(), monthly: {}, daily: {},
        };
        accs.set(nama, acc);
      }
      acc.total++;
      const sent = normSentiment(get(row, ["AI_Sentiment", "AISentiment", "sentiment"]));
      acc[sent]++;

      const rating = parseInt(get(row, ["Rating", "rating"]), 10);
      if (rating >= 1 && rating <= 5) {
        acc.ratingSum += rating;
        acc.ratingDist[rating - 1]++;
      }

      const primary = matchAspect(get(row, ["AI_Primary_Theme", "AIPrimaryTheme", "theme"]));
      if (primary) {
        acc.aspek[primary].total++;
        if (sent === "pos") acc.aspek[primary].pos++;
        else if (sent === "neg") acc.aspek[primary].neg++;
      }

      const rt = get(row, ["Review Time", "ReviewTime", "review_time", "date"]);
      if (rt && rt.length >= 7) {
        const yyyymm = rt.substring(0, 7);
        const mi = sortedMonths.indexOf(yyyymm);
        if (mi >= 0) {
          const m = acc.monthly[mi] ?? { pos: 0, neg: 0, neu: 0 };
          m[sent]++;
          acc.monthly[mi] = m;
        }
        
        // Daily
        if (rt.length >= 10) {
          const yyyymmdd = rt.substring(0, 10);
          const d = acc.daily[yyyymmdd] ?? { pos: 0, neg: 0, neu: 0 };
          d[sent]++;
          acc.daily[yyyymmdd] = d;
        }
      }
      
      if (rawReviews.length < 10000) {
        rawReviews.push({
          "Review Time": rt,
          Rating: get(row, ["Rating", "rating"]),
          "Review Text": get(row, ["Review Text", "review_text", "text"]),
          "Nama Hotel": nama,
          Kategori: acc.kategori,
          Bintang: acc.bintang,
          AI_Sentiment: get(row, ["AI_Sentiment", "AISentiment", "sentiment"]),
          AI_Primary_Theme: primary ?? "",
        });
      }
    },
    complete: () => {
      const hotels = [];
      let i = 0;
      for (const acc of accs.values()) {
        const total = acc.total || 1;
        const trenBulanan = MONTHS.map((bulan, idx) => {
          const m = acc.monthly[idx] ?? { pos: 0, neg: 0, neu: 0 };
          return {
            bulan,
            pctPos: +((m.pos / (m.pos + m.neg || 1)) * 100).toFixed(1),
            volPos: m.pos,
            volNeg: m.neg,
            volNeu: m.neu,
          };
        });
        const trenHarian = Object.keys(acc.daily).sort().map(tanggal => {
          const d = acc.daily[tanggal];
          return {
            tanggal,
            pctPos: +((d.pos / (d.pos + d.neg || 1)) * 100).toFixed(1),
            volPos: d.pos,
            volNeg: d.neg,
            volNeu: d.neu,
          };
        });
        const ph = phraseMap.get(acc.nama);
        hotels.push({
          id: `u${i++}`,
          nama: acc.nama,
          kategori: acc.kategori,
          bintang: acc.bintang,
          totalUlasan: acc.total,
          rating: +(acc.ratingSum / total).toFixed(2),
          pctPos: +((acc.pos / total) * 100).toFixed(1),
          pctNeg: +((acc.neg / total) * 100).toFixed(1),
          pctNeu: +((acc.neu / total) * 100).toFixed(1),
          ratingDist: acc.ratingDist,
          aspek: acc.aspek,
          frasaPos: ph?.pos ?? [],
          frasaNeg: ph?.neg ?? [],
          trenBulanan,
          trenHarian,
        });
      }
      fs.writeFileSync(OUT_FILE, JSON.stringify(hotels, null, 2));
      console.log(`Generated ${OUT_FILE} with ${hotels.length} hotels.`);
      fs.writeFileSync(REVIEWS_LITE_FILE, JSON.stringify(rawReviews, null, 2));
      console.log(`Generated ${REVIEWS_LITE_FILE} with ${rawReviews.length} raw reviews.`);
    }
  });
}

run();
