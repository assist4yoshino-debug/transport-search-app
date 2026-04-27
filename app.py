import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="ASSIST ROUTE FINDER",
    page_icon="🚛",
    layout="centered",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).parent
CARRIERS_CSV = APP_DIR / "carriers.csv"
MARKETS_CSV = APP_DIR / "markets.csv"

# ===================== DESIGN =====================
st.markdown("""
<style>
:root {
  --bg: #070b12;
  --card: #0f1724;
  --card2: #121d2d;
  --line: rgba(125, 211, 248, .22);
  --blue: #38bdf8;
  --blue2: #60a5fa;
  --text: #e5eef8;
  --muted: #94a3b8;
  --gold: #fbbf24;
}
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at top left, #16324f 0, #070b12 34%, #05070c 100%) !important;
  color: var(--text);
}
.block-container {
  padding-top: 1rem;
  padding-bottom: 2rem;
  max-width: 780px;
}
[data-testid="stHeader"] {background: transparent;}
h1 {
  font-size: 1.35rem !important;
  letter-spacing: .02em;
}
h2, h3 {font-size: 1.05rem !important;}
p, label, span, div {font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Noto Sans JP", sans-serif;}
div[data-testid="stTabs"] button {
  color: #cbd5e1;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: white;
  border-bottom-color: var(--blue);
}
div[data-baseweb="select"] > div,
input {
  background: rgba(255,255,255,.96) !important;
  border-radius: 12px !important;
}
.route-hero {
  border: 1px solid var(--line);
  background: linear-gradient(135deg, rgba(15,23,36,.96), rgba(18,29,45,.92));
  border-radius: 22px;
  padding: 18px;
  margin-bottom: 14px;
  box-shadow: 0 12px 40px rgba(0,0,0,.35);
}
.route-title {
  font-size: .78rem;
  color: var(--blue);
  letter-spacing: .22em;
  font-weight: 800;
}
.route-main {
  font-size: 1.28rem;
  font-weight: 900;
  color: white;
  margin-top: 4px;
}
.route-sub {
  font-size: .82rem;
  color: var(--muted);
  margin-top: 5px;
}
.card {
  background: linear-gradient(135deg, rgba(15,23,36,.98), rgba(17,24,39,.94));
  border: 1px solid rgba(148,163,184,.18);
  border-radius: 18px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,.22);
}
.company {
  font-size: 1.03rem;
  font-weight: 900;
  color: white;
  margin-bottom: 4px;
}
.small {font-size: .82rem; color: var(--muted);}
.badge {
  display: inline-block;
  padding: 3px 9px;
  margin: 3px 4px 3px 0;
  border-radius: 999px;
  background: rgba(56,189,248,.13);
  border: 1px solid rgba(56,189,248,.25);
  color: #dff6ff;
  font-size: .76rem;
}
.badge-red {
  background: rgba(248,113,113,.12);
  border-color: rgba(248,113,113,.26);
}
.note {
  background: rgba(251,191,36,.10);
  border-left: 4px solid var(--gold);
  color: #fff7d6;
  padding: 9px 11px;
  border-radius: 10px;
  font-size: .86rem;
}
.match {
  color: var(--blue);
  font-weight: 900;
}
div[data-testid="stMetric"] {
  background: rgba(15,23,36,.75);
  border: 1px solid rgba(56,189,248,.20);
  border-radius: 16px;
  padding: 10px 12px;
}
div[data-testid="stMetricValue"] {
  color: white;
  font-size: 1.35rem;
}
</style>
""", unsafe_allow_html=True)


# ===================== DATA =====================
def split_values(value):
    if pd.isna(value) or str(value).strip() == "":
        return []
    text = str(value).replace(",", "、")
    return [x.strip() for x in text.split("、") if x.strip()]


@st.cache_data
def load_data():
    if not CARRIERS_CSV.exists():
        return pd.DataFrame(), pd.DataFrame()

    carriers = pd.read_csv(CARRIERS_CSV).fillna("")
    markets = pd.read_csv(MARKETS_CSV).fillna("") if MARKETS_CSV.exists() else pd.DataFrame(columns=["pref", "market"])

    required = [
        "origin_areas", "dest_areas", "origin_markets", "dest_markets",
        "items", "shapes", "routes", "memo", "fare_note"
    ]
    for col in required:
        if col not in carriers.columns:
            carriers[col] = ""

    return carriers, markets


carriers, markets = load_data()

if carriers.empty:
    st.error("carriers.csv が見つかりません。")
    st.stop()


# ===================== HELPERS =====================
def market_to_pref_map():
    if markets.empty:
        return {}
    return dict(zip(markets["market"].astype(str), markets["pref"].astype(str)))


def pref_options():
    prefs = set()
    if not markets.empty:
        prefs.update(markets["pref"].dropna().astype(str).tolist())
    for _, row in carriers.iterrows():
        prefs.update(split_values(row.get("origin_areas", "")))
        prefs.update(split_values(row.get("dest_areas", "")))
    return [""] + sorted([p for p in prefs if p])


def market_options(pref=""):
    if markets.empty:
        return [""]
    df = markets
    if pref:
        df = df[df["pref"] == pref]
    return [""] + df["market"].dropna().astype(str).sort_values().tolist()


def get_unique_list(col):
    values = set()
    for v in carriers[col].tolist():
        values.update(split_values(v))
    return [""] + sorted(values)


def has_market_data(row):
    return bool(split_values(row.get("origin_markets", "")) or split_values(row.get("dest_markets", "")))


def match_market_to_market(row, origin_market, dest_market, item, shape):
    # 市場列が空の会社は、市場→市場検索では判定対象外
    if not has_market_data(row):
        return False

    if origin_market:
        origin_markets = split_values(row.get("origin_markets", ""))
        if origin_market not in origin_markets:
            return False

    if dest_market:
        dest_markets = split_values(row.get("dest_markets", ""))
        if dest_market not in dest_markets:
            return False

    if item and item not in split_values(row.get("items", "")):
        return False

    if shape and shape not in split_values(row.get("shapes", "")):
        return False

    return True


def match_pref_to_pref(row, origin_pref, dest_pref, item, shape):
    if origin_pref and origin_pref not in split_values(row.get("origin_areas", "")):
        return False

    if dest_pref and dest_pref not in split_values(row.get("dest_areas", "")):
        return False

    if item and item not in split_values(row.get("items", "")):
        return False

    if shape and shape not in split_values(row.get("shapes", "")):
        return False

    return True


def search_carriers(origin_pref, origin_market, dest_pref, dest_market, item, shape):
    # 1. 市場→市場で検索
    market_searched = bool(origin_market or dest_market)
    market_result = pd.DataFrame()

    if market_searched:
        market_result = carriers[
            carriers.apply(lambda r: match_market_to_market(r, origin_market, dest_market, item, shape), axis=1)
        ]

    if market_searched and not market_result.empty:
        return market_result, "market"

    # 2. 市場で当たらなければ都道府県→都道府県で検索
    pref_result = carriers[
        carriers.apply(lambda r: match_pref_to_pref(r, origin_pref, dest_pref, item, shape), axis=1)
    ]

    return pref_result, "pref_fallback" if market_searched else "pref"


def render_badges(values, red=False):
    cls = "badge badge-red" if red else "badge"
    return " ".join([f"<span class='{cls}'>{v}</span>" for v in values])


def render_card(row, detail=False):
    has_fare = str(row.get("has_fare_table", "")).lower() in ["true", "1", "yes", "あり"]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='company'>{row.get('name', '')}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='small'>📍 {row.get('base', '') or '—'}　👤 {row.get('contact', '') or '—'}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='small'>📄 運賃表：{'あり' if has_fare else 'なし'}</div>", unsafe_allow_html=True)

    if detail:
        if split_values(row.get("origin_markets", "")) or split_values(row.get("dest_markets", "")):
            st.markdown("**市場対応**")
            st.markdown("発：" + (render_badges(split_values(row.get("origin_markets", ""))) or "—"), unsafe_allow_html=True)
            st.markdown("着：" + (render_badges(split_values(row.get("dest_markets", "")), red=True) or "—"), unsafe_allow_html=True)

        st.markdown("**対応エリア**")
        st.markdown("発：" + render_badges(split_values(row.get("origin_areas", ""))), unsafe_allow_html=True)
        st.markdown("着：" + render_badges(split_values(row.get("dest_areas", "")), red=True), unsafe_allow_html=True)

        st.markdown("**ルート**")
        st.markdown(render_badges(split_values(row.get("routes", ""))), unsafe_allow_html=True)

        st.markdown("**品目 / 荷姿**")
        st.markdown(render_badges(split_values(row.get("items", ""))) + render_badges(split_values(row.get("shapes", ""))), unsafe_allow_html=True)

        st.markdown("**運賃情報**")
        st.info(row.get("fare_note", "") or "—")

        st.markdown("**メモ・注意点**")
        st.markdown(f"<div class='note'>{row.get('memo', '') or '—'}</div>", unsafe_allow_html=True)
    else:
        route = " / ".join(split_values(row.get("routes", ""))[:2])
        if route:
            st.caption(route)
        memo = row.get("memo", "")
        if memo:
            st.markdown(f"<div class='small'>📝 {memo[:80]}{'…' if len(memo) > 80 else ''}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ===================== UI =====================
st.markdown("""
<div class="route-hero">
  <div class="route-title">ASSIST ROUTE FINDER</div>
  <div class="route-main">市場から探す、運送会社検索。</div>
  <div class="route-sub">市場→市場で検索。該当がなければ、都道府県→都道府県で自動検索します。</div>
</div>
""", unsafe_allow_html=True)

tab_search, tab_all, tab_market = st.tabs(["🔍 検索", "📋 一覧", "🏪 市場"])

with tab_search:
    mtp = market_to_pref_map()
    prefs = pref_options()

    st.subheader("発地")
    origin_pref = st.selectbox("発地 都道府県", prefs, key="origin_pref")
    origin_market = st.selectbox("発地 市場", market_options(origin_pref), key="origin_market")
    if origin_market and origin_market in mtp:
        origin_pref = mtp[origin_market]

    st.subheader("着地")
    dest_pref = st.selectbox("着地 都道府県", prefs, key="dest_pref")
    dest_market = st.selectbox("着地 市場", market_options(dest_pref), key="dest_market")
    if dest_market and dest_market in mtp:
        dest_pref = mtp[dest_market]

    st.subheader("条件")
    item = st.selectbox("品目", get_unique_list("items"), key="item")
    shape = st.selectbox("荷姿", get_unique_list("shapes"), key="shape")

    has_condition = any([origin_pref, origin_market, dest_pref, dest_market, item, shape])
    if not has_condition:
        st.info("発地・着地・市場・品目・荷姿を選択してください。")
    else:
        result, mode = search_carriers(origin_pref, origin_market, dest_pref, dest_market, item, shape)

        c1, c2 = st.columns(2)
        with c1:
            st.metric("該当", f"{len(result)} 社")
        with c2:
            if mode == "market":
                st.metric("検索方式", "市場→市場")
            elif mode == "pref_fallback":
                st.metric("検索方式", "都道府県 fallback")
            else:
                st.metric("検索方式", "都道府県")

        if mode == "pref_fallback":
            st.warning("市場単位では該当なし。都道府県単位で候補を表示しています。")
        elif mode == "market":
            st.success("市場単位で該当しました。")

        if result.empty:
            st.error("条件に合う運送会社が見つかりません。")
        else:
            for _, row in result.iterrows():
                with st.expander(f"{row['name']}｜詳細を見る"):
                    render_card(row, detail=True)

with tab_all:
    st.subheader(f"全運送会社：{len(carriers)}社")
    keyword = st.text_input("会社名・メモ検索")
    df = carriers
    if keyword:
        mask = carriers.apply(lambda r: keyword in " ".join(map(str, r.values)), axis=1)
        df = carriers[mask]
    for _, row in df.iterrows():
        with st.expander(f"{row['name']}｜詳細を見る"):
            render_card(row, detail=True)

with tab_market:
    st.subheader("市場一覧")
    if markets.empty:
        st.info("markets.csv を入れると市場一覧を表示できます。")
    else:
        q = st.text_input("市場名検索")
        dfm = markets
        if q:
            dfm = dfm[dfm["market"].astype(str).str.contains(q, na=False)]
        for pref, group in dfm.groupby("pref"):
            st.markdown(f"**{pref}**")
            st.markdown(render_badges(group["market"].astype(str).tolist()), unsafe_allow_html=True)
