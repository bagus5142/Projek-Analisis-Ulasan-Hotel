import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Analisis Ulasan Hotel", page_icon="🏨", layout="wide")

# ── Minimal professional CSS ─────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    *, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    .block-container { padding: 2rem 2rem 3rem !important; max-width: 1100px; }
    #MainMenu, footer, .stDeployButton { display: none; }
    header[data-testid="stHeader"] { background: #fff !important; box-shadow: 0 1px 0 #eee; }

    [data-testid="stSidebar"] { background: #f9fafb !important; }

    /* Metric cards */
    .m-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
    .m-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px 24px; }
    .m-card .label { font-size: 12px; color: #6b7280; font-weight: 500; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.4px; }
    .m-card .val { font-size: 28px; font-weight: 700; color: #111827; line-height: 1; }
    .m-card .sub { font-size: 12px; color: #9ca3af; margin-top: 6px; }

    /* Section divider */
    .sec { font-size: 15px; font-weight: 600; color: #374151; margin: 32px 0 14px; }

    /* Phrase rows */
    .p-row { display: flex; justify-content: space-between; align-items: center;
             padding: 10px 14px; border-radius: 8px; margin-bottom: 6px; font-size: 13px; }
    .p-neg { background: #fef2f2; color: #991b1b; }
    .p-pos { background: #f0fdf4; color: #166534; }
    .p-score { font-size: 11px; color: #9ca3af; }

    /* VS */
    .vs-box { display: flex; align-items: center; justify-content: center; height: 100%;
              font-size: 20px; font-weight: 700; color: #d1d5db; }
</style>
""", unsafe_allow_html=True)

# ── Chart defaults ───────────────────────────────────────────
COLORS = {'pos': '#22c55e', 'neg': '#ef4444', 'blue': '#3b82f6', 'amber': '#f59e0b', 'purple': '#8b5cf6'}
LAYOUT = dict(paper_bgcolor='#fff', plot_bgcolor='#fff',
              font=dict(family='Inter', color='#374151', size=12),
              margin=dict(l=0, r=0, t=30, b=0),
              legend=dict(bgcolor='rgba(0,0,0,0)'))

def clean(fig, h=360):
    fig.update_layout(**LAYOUT, height=h)
    fig.update_xaxes(gridcolor='#f3f4f6', linecolor='#e5e7eb', zeroline=False, tickfont=dict(size=11))
    fig.update_yaxes(gridcolor='#f3f4f6', linecolor='#e5e7eb', zeroline=False, tickfont=dict(size=11))
    return fig

# ── Data ─────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv('data/AI_Structured_Final.csv', sep=';')
    df['Review Time'] = pd.to_datetime(df['Review Time'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Bintang'] = df['Bintang'].astype(str).str.extract(r'(\d)').astype(float)
    df['Bulan'] = df['Review Time'].dt.to_period('M').astype(str)
    kw = pd.DataFrame()
    try: kw = pd.read_csv('data/AI_Structured_Keywords.csv')
    except: pass
    return df, kw

df_all, df_kw = load()

# ── Sidebar — clean filter panel ─────────────────────────────
with st.sidebar:
    st.markdown("#### Filter Data")

    kategori = st.radio("Kategori", ["Semua", "BUMN", "KOMPETITOR"], horizontal=True)

    hotel_pool = df_all.copy()
    if kategori != "Semua":
        hotel_pool = hotel_pool[hotel_pool['Kategori'].str.upper() == kategori]
    hotel_names = sorted(hotel_pool['Nama Hotel'].dropna().unique())

    hotel = st.selectbox("Hotel", ["Semua Hotel"] + hotel_names,
                         help="Pilih satu hotel untuk melihat detail spesifik")

    bulan_list = sorted(df_all['Bulan'].dropna().unique())
    rentang = st.select_slider("Periode", options=bulan_list,
                               value=(bulan_list[0], bulan_list[-1]))

    st.markdown("---")
    st.caption(f"{len(df_all):,} ulasan · {df_all['Nama Hotel'].nunique()} hotel")

# ── Apply filters ────────────────────────────────────────────
df = df_all.copy()
df = df[(df['Bulan'] >= rentang[0]) & (df['Bulan'] <= rentang[1])]
if kategori != "Semua":
    df = df[df['Kategori'].str.upper() == kategori]
if hotel != "Semua Hotel":
    df = df[df['Nama Hotel'] == hotel]

# ── Page header ──────────────────────────────────────────────
judul = hotel if hotel != "Semua Hotel" else (kategori if kategori != "Semua" else "Semua Hotel")
st.markdown(f"### {judul}")
st.caption(f"{len(df):,} ulasan · Periode {rentang[0]} s/d {rentang[1]}")

# ── Tabs ─────────────────────────────────────────────────────
t_overview, t_compare, t_rank, t_trend = st.tabs(["Ringkasan", "Perbandingan", "Peringkat", "Tren"])

# ═════════════════════════════════════════════════════════════
# TAB 1 — RINGKASAN
# ═════════════════════════════════════════════════════════════
with t_overview:
    if df.empty:
        st.info("Tidak ada data untuk filter ini.")
        st.stop()

    pos = (df['AI_Sentiment'] == 'Positive').sum()
    neg = (df['AI_Sentiment'] == 'Negative').sum()
    neu = (df['AI_Sentiment'] == 'Neutral').sum()
    vld = pos + neg
    pp = pos / vld * 100 if vld else 0
    np_ = neg / vld * 100 if vld else 0
    ar = df['Rating'].mean()

    st.markdown(f"""
    <div class="m-grid">
      <div class="m-card"><div class="label">Total Ulasan</div><div class="val">{len(df):,}</div>
        <div class="sub">{pos:,} positif · {neg:,} negatif · {neu:,} netral</div></div>
      <div class="m-card"><div class="label">Sentimen Positif</div>
        <div class="val" style="color:{COLORS['pos']}">{pp:.1f}%</div>
        <div class="sub">{pos:,} dari {vld:,} ulasan</div></div>
      <div class="m-card"><div class="label">Sentimen Negatif</div>
        <div class="val" style="color:{COLORS['neg']}">{np_:.1f}%</div>
        <div class="sub">{neg:,} dari {vld:,} ulasan</div></div>
      <div class="m-card"><div class="label">Rating Rata-rata</div>
        <div class="val">{ar:.1f} <span style="font-size:14px;color:#9ca3af">/ 5</span></div>
        <div class="sub">dari Google Maps</div></div>
    </div>""", unsafe_allow_html=True)

    # ── Aspek analysis ──
    da = df[df['AI_Sentiment'].isin(['Positive', 'Negative'])]
    if da.empty:
        st.info("Data sentimen tidak cukup.")
    else:
        g = da.groupby(['AI_Primary_Theme', 'AI_Sentiment']).size().unstack(fill_value=0)
        for c in ['Positive', 'Negative']:
            if c not in g: g[c] = 0
        g['Total'] = g['Positive'] + g['Negative']
        g['pct_pos'] = g['Positive'] / g['Total'] * 100
        g['pct_neg'] = g['Negative'] / g['Total'] * 100
        g = g.sort_values('pct_pos')

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="sec">Sentimen per Aspek</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(y=g.index, x=-g['pct_neg'], name='Negatif', orientation='h',
                                 marker_color=COLORS['neg'], hovertemplate='%{y}: %{customdata:.1f}% negatif',
                                 customdata=g['pct_neg']))
            fig.add_trace(go.Bar(y=g.index, x=g['pct_pos'], name='Positif', orientation='h',
                                 marker_color=COLORS['pos'], hovertemplate='%{y}: %{x:.1f}% positif'))
            fig.update_layout(barmode='overlay',
                xaxis=dict(tickvals=[-100,-50,0,50,100], ticktext=['100%','50%','0','50%','100%']))
            fig.update_xaxes(zeroline=True, zerolinecolor='#e5e7eb')
            clean(fig, 380)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="sec">Distribusi Topik</div>', unsafe_allow_html=True)
            tc = df['AI_Primary_Theme'].value_counts().reset_index()
            tc.columns = ['Aspek', 'Jumlah']
            fig2 = px.pie(tc, names='Aspek', values='Jumlah', hole=0.55,
                          color_discrete_sequence=['#3b82f6','#22c55e','#f59e0b','#ef4444',
                                                   '#8b5cf6','#06b6d4','#ec4899','#f97316',
                                                   '#14b8a6','#6366f1','#84cc16','#e11d48'])
            fig2.update_traces(textposition='outside', textinfo='percent+label', textfont_size=10,
                               marker=dict(line=dict(color='#fff', width=2)))
            fig2.update_layout(showlegend=False)
            clean(fig2, 380)
            st.plotly_chart(fig2, use_container_width=True)

        # ── Detail per hotel: radar + phrases ──
        if hotel != "Semua Hotel":
            c_r, c_p = st.columns([1, 1])
            with c_r:
                st.markdown('<div class="sec">Profil Aspek</div>', unsafe_allow_html=True)
                scores = g['pct_pos']
                fr = go.Figure()
                fr.add_trace(go.Scatterpolar(r=scores.tolist(), theta=scores.index.tolist(),
                    fill='toself', name=hotel,
                    line=dict(color=COLORS['blue'], width=2), fillcolor='rgba(59,130,246,0.08)'))
                if kategori != "Semua":
                    dk = df_all[(df_all['Kategori'].str.upper() == kategori) &
                                df_all['AI_Sentiment'].isin(['Positive','Negative'])]
                    gk = dk.groupby(['AI_Primary_Theme','AI_Sentiment']).size().unstack(fill_value=0)
                    for c in ['Positive','Negative']:
                        if c not in gk: gk[c] = 0
                    gk['s'] = gk['Positive'] / (gk['Positive']+gk['Negative']) * 100
                    avgs = [gk['s'].get(a,0) for a in scores.index]
                    fr.add_trace(go.Scatterpolar(r=avgs, theta=scores.index.tolist(),
                        fill='toself', name=f'Avg {kategori}',
                        line=dict(color=COLORS['amber'], width=1.5, dash='dot'),
                        fillcolor='rgba(245,158,11,0.04)'))
                fr.update_layout(polar=dict(
                    radialaxis=dict(visible=True, range=[0,100], gridcolor='#f3f4f6', tickfont=dict(size=9)),
                    angularaxis=dict(gridcolor='#f3f4f6')))
                clean(fr, 340)
                st.plotly_chart(fr, use_container_width=True)

            with c_p:
                st.markdown('<div class="sec">Frasa Kunci</div>', unsafe_allow_html=True)
                if not df_kw.empty:
                    hk = df_kw[df_kw['Nama_Hotel'] == hotel]
                    if not hk.empty:
                        st.markdown("**Kelemahan**")
                        for _, r in hk.head(5).iterrows():
                            st.markdown(f'<div class="p-row p-neg"><span>{str(r["Top_Negatif_Phrase"]).title()}</span>'
                                        f'<span class="p-score">{r["Bobot_Neg"]:.2f}</span></div>', unsafe_allow_html=True)
                        st.markdown("**Kekuatan**")
                        for _, r in hk.head(5).iterrows():
                            st.markdown(f'<div class="p-row p-pos"><span>{str(r["Top_Positif_Phrase"]).title()}</span>'
                                        f'<span class="p-score">+{r["Bobot_Pos"]:.2f}</span></div>', unsafe_allow_html=True)
                    else:
                        st.caption("Frasa belum tersedia untuk hotel ini.")

# ═════════════════════════════════════════════════════════════
# TAB 2 — PERBANDINGAN
# ═════════════════════════════════════════════════════════════
with t_compare:
    st.markdown('<div class="sec">BUMN vs Kompetitor — Sentimen per Aspek</div>', unsafe_allow_html=True)

    db = df_all[df_all['AI_Sentiment'].isin(['Positive','Negative'])].copy()
    db = db[(db['Bulan'] >= rentang[0]) & (db['Bulan'] <= rentang[1])]

    if db.empty:
        st.info("Data tidak tersedia.")
    else:
        ag = db.groupby(['Kategori','AI_Primary_Theme','AI_Sentiment']).size().unstack(fill_value=0).reset_index()
        for c in ['Positive','Negative']:
            if c not in ag.columns: ag[c] = 0
        ag['pct'] = ag['Positive'] / (ag['Positive']+ag['Negative']) * 100
        fc = px.bar(ag, x='AI_Primary_Theme', y='pct', color='Kategori', barmode='group',
                    color_discrete_map={'BUMN': COLORS['blue'], 'KOMPETITOR': COLORS['amber']},
                    labels={'pct':'% Positif', 'AI_Primary_Theme':'Aspek'})
        fc.update_traces(marker_line_width=0)
        clean(fc, 400)
        fc.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fc, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="sec">Adu Hotel Spesifik</div>', unsafe_allow_html=True)

    bumn_names = sorted(df_all[df_all['Kategori'].str.upper()=='BUMN']['Nama Hotel'].dropna().unique())
    komp_names = sorted(df_all[df_all['Kategori'].str.upper()=='KOMPETITOR']['Nama Hotel'].dropna().unique())

    cb, cm, ck = st.columns([5, 1, 5])
    with cb: pick_b = st.selectbox("Hotel BUMN", bumn_names, key='vs_b')
    with cm: st.markdown('<div class="vs-box">vs</div>', unsafe_allow_html=True)
    with ck: pick_k = st.selectbox("Hotel Kompetitor", komp_names, key='vs_k')

    def hscore(name):
        d = df_all[(df_all['Nama Hotel']==name) & df_all['AI_Sentiment'].isin(['Positive','Negative'])]
        if d.empty: return None
        gx = d.groupby(['AI_Primary_Theme','AI_Sentiment']).size().unstack(fill_value=0)
        for c in ['Positive','Negative']:
            if c not in gx: gx[c] = 0
        gx['s'] = gx['Positive'] / (gx['Positive']+gx['Negative']) * 100
        return gx['s']

    sb, sk = hscore(pick_b), hscore(pick_k)
    cr, cf = st.columns(2)
    with cr:
        if sb is not None and sk is not None:
            asp = sorted(set(sb.index)|set(sk.index))
            fv = go.Figure()
            fv.add_trace(go.Scatterpolar(r=[sb.get(a,0) for a in asp], theta=asp,
                fill='toself', name=pick_b, line=dict(color=COLORS['blue'], width=2),
                fillcolor='rgba(59,130,246,0.08)'))
            fv.add_trace(go.Scatterpolar(r=[sk.get(a,0) for a in asp], theta=asp,
                fill='toself', name=pick_k, line=dict(color=COLORS['amber'], width=2),
                fillcolor='rgba(245,158,11,0.08)'))
            fv.update_layout(polar=dict(
                radialaxis=dict(visible=True, range=[0,100], gridcolor='#f3f4f6'),
                angularaxis=dict(gridcolor='#f3f4f6')))
            clean(fv, 380)
            st.plotly_chart(fv, use_container_width=True)
        else:
            st.info("Data tidak cukup.")

    with cf:
        if not df_kw.empty:
            st.markdown(f"**Kelemahan — {pick_b}**")
            kb = df_kw[df_kw['Nama_Hotel']==pick_b]
            for _, r in kb.head(4).iterrows():
                st.markdown(f'<div class="p-row p-neg"><span>{str(r["Top_Negatif_Phrase"]).title()}</span>'
                            f'<span class="p-score">{r["Bobot_Neg"]:.2f}</span></div>', unsafe_allow_html=True)
            if kb.empty: st.caption("— tidak tersedia —")
            st.markdown("")
            st.markdown(f"**Kelemahan — {pick_k}**")
            kk = df_kw[df_kw['Nama_Hotel']==pick_k]
            for _, r in kk.head(4).iterrows():
                st.markdown(f'<div class="p-row p-neg"><span>{str(r["Top_Negatif_Phrase"]).title()}</span>'
                            f'<span class="p-score">{r["Bobot_Neg"]:.2f}</span></div>', unsafe_allow_html=True)
            if kk.empty: st.caption("— tidak tersedia —")

# ═════════════════════════════════════════════════════════════
# TAB 3 — PERINGKAT
# ═════════════════════════════════════════════════════════════
with t_rank:
    st.markdown('<div class="sec">Peringkat Hotel</div>', unsafe_allow_html=True)
    rk_filter = st.radio("Tampilkan:", ["Semua","BUMN","KOMPETITOR"], horizontal=True, key='rk')
    dr = df_all.copy()
    if rk_filter != "Semua":
        dr = dr[dr['Kategori'].str.upper() == rk_filter]

    rows = []
    for h in dr['Nama Hotel'].dropna().unique():
        dh = dr[dr['Nama Hotel']==h]
        p = (dh['AI_Sentiment']=='Positive').sum()
        n = (dh['AI_Sentiment']=='Negative').sum()
        v = p+n
        pp = p/v*100 if v else 0
        ar = dh['Rating'].mean()
        wk = dh[dh['AI_Sentiment']=='Negative']['AI_Primary_Theme'].mode()
        w = wk.iloc[0] if not wk.empty else '-'
        rows.append({'Hotel':h, 'Kategori':dh['Kategori'].iloc[0], 'Ulasan':len(dh),
                     '% Positif':round(pp,1), '% Negatif':round(100-pp,1) if v else 0,
                     'Rating':round(ar,1), 'Aspek Terlemah':w})

    dfr = pd.DataFrame(rows).sort_values('% Positif', ascending=False).reset_index(drop=True)
    dfr.index += 1
    dfr.index.name = 'Rank'

    def hl(v):
        if isinstance(v, float):
            if v >= 80: return 'background-color: #dcfce7'
            if v >= 60: return 'background-color: #fef9c3'
            return 'background-color: #fee2e2'
        return ''

    st.dataframe(dfr.style.applymap(hl, subset=['% Positif']).format(
        {'% Positif':'{:.1f}%', '% Negatif':'{:.1f}%', 'Rating':'{:.1f}'}),
        use_container_width=True, height=450)

    st.markdown("---")
    st.markdown('<div class="sec">Peta Posisi</div>', unsafe_allow_html=True)
    st.caption("Kuadran kanan atas = hotel terbaik")
    fs = px.scatter(dfr, x='% Positif', y='Rating', color='Kategori', hover_name='Hotel',
                    size='Ulasan', size_max=30,
                    color_discrete_map={'BUMN':COLORS['blue'],'KOMPETITOR':COLORS['amber']})
    fs.add_vline(x=dfr['% Positif'].mean(), line_dash='dot', line_color='#e5e7eb')
    fs.add_hline(y=dfr['Rating'].mean(), line_dash='dot', line_color='#e5e7eb')
    clean(fs, 420)
    fs.update_layout(xaxis_title='Sentimen Positif (%)', yaxis_title='Rating')
    st.plotly_chart(fs, use_container_width=True)

# ═════════════════════════════════════════════════════════════
# TAB 4 — TREN
# ═════════════════════════════════════════════════════════════
with t_trend:
    st.markdown('<div class="sec">Tren Sentimen</div>', unsafe_allow_html=True)
    dt = df_all.copy()
    if kategori != "Semua": dt = dt[dt['Kategori'].str.upper() == kategori]
    if hotel != "Semua Hotel": dt = dt[dt['Nama Hotel'] == hotel]

    tp = dt[dt['AI_Sentiment']=='Positive'].groupby('Bulan').size()
    tn = dt[dt['AI_Sentiment']=='Negative'].groupby('Bulan').size()
    ta = dt.groupby('Bulan').size()
    tr = pd.DataFrame({'pos':tp,'neg':tn,'tot':ta}).fillna(0)
    tr['pct'] = tr['pos'] / (tr['pos']+tr['neg']) * 100
    tr = tr.reset_index().sort_values('Bulan')

    if tr.empty:
        st.info("Data tidak cukup.")
    else:
        ft = go.Figure()
        ft.add_trace(go.Scatter(x=tr['Bulan'], y=tr['pct'], mode='lines+markers',
            name='% Positif', line=dict(color=COLORS['pos'], width=2.5),
            marker=dict(size=5), fill='tozeroy', fillcolor='rgba(34,197,94,0.05)'))
        avg = tr['pct'].mean()
        ft.add_hline(y=avg, line_dash='dot', line_color='#d1d5db',
                     annotation_text=f"Rata-rata {avg:.1f}%", annotation_font_color='#9ca3af')
        clean(ft, 340)
        ft.update_layout(yaxis=dict(range=[0,100], title='% Positif'), xaxis_title='')
        st.plotly_chart(ft, use_container_width=True)

        st.markdown('<div class="sec">Volume Ulasan</div>', unsafe_allow_html=True)
        fv = go.Figure()
        fv.add_trace(go.Bar(x=tr['Bulan'], y=tr['pos'], name='Positif', marker_color=COLORS['pos']))
        fv.add_trace(go.Bar(x=tr['Bulan'], y=tr['neg'], name='Negatif', marker_color=COLORS['neg']))
        clean(fv, 280)
        fv.update_layout(barmode='stack', yaxis_title='Jumlah', xaxis_title='')
        st.plotly_chart(fv, use_container_width=True)
