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

PREF_ORDER = [
    "北海道",
    "青森", "岩手", "宮城", "秋田", "山形", "福島",
    "茨城", "栃木", "群馬", "埼玉", "千葉", "東京", "神奈川",
    "新潟", "富山", "石川", "福井", "山梨", "長野",
    "岐阜", "静岡", "愛知", "三重",
    "滋賀", "京都", "大阪", "兵庫", "奈良", "和歌山",
    "鳥取", "島根", "岡山", "広島", "山口",
    "徳島", "香川", "愛媛", "高知",
    "福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄",
]

# ===================== CSS =====================
st.markdown("""
<style>
:root{
  --bg:#07111f;
  --navy:#0d1b2a;
  --navy2:#15314d;
  --blue:#5bc4f5;
  --muted:#9fb2c7;
  --line:rgba(91,196,245,.26);
  --green:#18d72c;
  --red:#ef233c;
}

/* page */
html, body, .stApp, [data-testid="stAppViewContainer"]{
  background:
    radial-gradient(circle at 18% 0%, rgba(38,105,157,.55), transparent 34%),
    linear-gradient(145deg,#07111f 0%,#0b1a2b 52%,#07111f 100%) !important;
  color:#fff !important;
  overflow-x:hidden !important;
}
.block-container{
  max-width:760px !important;
  padding:.55rem .72rem 1.2rem !important;
}
[data-testid="stHeader"]{background:transparent !important;}
#MainMenu, footer, [data-testid="stToolbar"]{visibility:hidden !important;}
*{box-sizing:border-box !important;}
p, div, span, label{
  font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif !important;
}

/* header */
.header{
  background:linear-gradient(135deg,#0d1b2a,#173a59 62%,#1e5f8e);
  border:1px solid rgba(91,196,245,.35);
  border-radius:22px;
  padding:12px 14px;
  margin:0 0 8px;
  box-shadow:0 12px 30px rgba(0,0,0,.30);
}
.header-row{
  display:flex;
  justify-content:space-between;
  gap:10px;
  align-items:flex-start;
}
.brand{
  font-size:.62rem;
  letter-spacing:.23em;
  color:var(--blue);
  font-weight:900;
  white-space:nowrap;
}
.title{
  margin-top:5px;
  font-size:1.14rem;
  line-height:1.15;
  font-weight:900;
  color:#fff;
}
.count{
  color:#c7dff2;
  text-align:right;
  font-size:.68rem;
  white-space:nowrap;
}
.count strong{
  display:block;
  color:var(--blue);
  font-size:1.75rem;
  line-height:1;
}

/* tabs */
div[data-testid="stTabs"] [data-baseweb="tab-list"]{
  gap:4px !important;
  border-bottom:1px solid rgba(255,255,255,.08) !important;
}
div[data-testid="stTabs"] button{
  color:rgba(255,255,255,.70) !important;
  padding:8px 9px !important;
  font-size:.84rem !important;
}
div[data-testid="stTabs"] button[aria-selected="true"]{
  color:#0d1b2a !important;
  background:#fff !important;
  border-radius:12px 12px 0 0 !important;
  border-bottom:none !important;
  font-weight:900 !important;
}

/* search panel */
.search-card{
  width:100%;
  background:linear-gradient(135deg,rgba(9,23,40,.98),rgba(22,57,87,.96));
  border:1px solid rgba(91,196,245,.28);
  border-radius:22px;
  padding:14px 14px 12px;
  margin-top:9px;
  box-shadow:0 16px 36px rgba(0,0,0,.30);
  overflow:hidden;
}
.search-title{
  font-size:1.02rem;
  font-weight:900;
  color:#fff;
  margin-bottom:12px;
}

/* Streamlit columns - no overflow */
[data-testid="stHorizontalBlock"]{
  width:100% !important;
  max-width:100% !important;
  display:flex !important;
  flex-direction:row !important;
  flex-wrap:nowrap !important;
  gap:10px !important;
  align-items:stretch !important;
  overflow:visible !important;
}
[data-testid="column"]{
  min-width:0 !important;
  flex:1 1 0 !important;
  width:0 !important;
  max-width:100% !important;
}

/* select widgets */
[data-testid="stWidgetLabel"]{
  min-height:auto !important;
  margin-bottom:0 !important;
}
[data-testid="stWidgetLabel"] p{
  color:#cfe7fb !important;
  font-size:.64rem !important;
  font-weight:800 !important;
  line-height:1.1 !important;
}
div[data-baseweb="select"]{
  width:100% !important;
  min-width:0 !important;
}
div[data-baseweb="select"] > div{
  background:#fff !important;
  min-height:39px !important;
  height:39px !important;
  border-radius:12px !important;
  border:1.5px solid rgba(255,255,255,.75) !important;
  box-shadow:0 2px 10px rgba(0,0,0,.16) !important;
  min-width:0 !important;
}
div[data-baseweb="select"] span{
  color:#111827 !important;
  font-size:.82rem !important;
  overflow:hidden !important;
  text-overflow:ellipsis !important;
  white-space:nowrap !important;
}
[data-testid="stVerticalBlock"]{
  gap:.35rem !important;
}

/* visual blocks */
.route-head{
  display:flex;
  align-items:center;
  gap:7px;
  color:#fff;
  font-size:.92rem;
  font-weight:900;
  margin:2px 0 7px;
}
.dot{
  width:18px;
  height:18px;
  border-radius:50%;
  display:inline-block;
  box-shadow:inset 0 1px 2px rgba(255,255,255,.55),0 0 12px rgba(0,0,0,.36);
}
.green{background:radial-gradient(circle at 35% 30%,#75ff7b,#06b61e 65%);}
.red{background:radial-gradient(circle at 35% 30%,#ff8585,#e10d1a 65%);}
.route-inner{
  background:rgba(255,255,255,.075);
  border:1px solid rgba(255,255,255,.05);
  border-radius:16px;
  padding:10px 9px 9px;
  min-width:0;
}
.divider{
  height:1px;
  background:rgba(255,255,255,.13);
  margin:12px 0 10px;
}
.result-row{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
  margin-top:9px;
}
.result-main{
  color:var(--blue);
  font-weight:900;
  font-size:.94rem;
}
.result-sub{
  color:#cbd5e1;
  font-size:.74rem;
  white-space:nowrap;
}

/* result cards */
.card{
  background:#fff;
  color:#0d1b2a;
  border:1px solid #dbe4ef;
  border-radius:16px;
  padding:13px;
  margin-bottom:9px;
  box-shadow:0 5px 18px rgba(0,0,0,.14);
}
.company{
  color:#0d1b2a;
  font-size:1rem;
  font-weight:900;
  margin-bottom:4px;
}
.small{font-size:.78rem;color:#64748b;}
.badge{
  display:inline-block;
  padding:3px 9px;
  margin:3px 4px 3px 0;
  border-radius:999px;
  background:#edf6ff;
  border:1px solid #c9def2;
  color:#17324e;
  font-size:.74rem;
}
.badge-red{
  background:#fff0f0;
  border-color:#f3c5c5;
  color:#7f1d1d;
}
.note{
  background:#fff8e6;
  border-left:4px solid #f39c12;
  color:#5f4300;
  padding:9px 11px;
  border-radius:10px;
  font-size:.84rem;
}

/* mobile: keep 2 columns, compress */
@media(max-width:430px){
  .block-container{padding-left:.62rem !important;padding-right:.62rem !important;}
  .header{padding:10px 11px;border-radius:20px;}
  .brand{font-size:.52rem;letter-spacing:.18em;}
  .title{font-size:1.02rem;}
  .count{font-size:.62rem;}
  .count strong{font-size:1.48rem;}
  div[data-testid="stTabs"] button{font-size:.78rem !important;padding:7px 7px !important;}
  .search-card{padding:12px 10px;border-radius:20px;}
  .search-title{font-size:.94rem;margin-bottom:9px;}
  [data-testid="stHorizontalBlock"]{gap:7px !important;}
  .route-inner{padding:8px 7px 8px;border-radius:14px;}
  .route-head{font-size:.78rem;margin-bottom:6px;}
  .dot{width:16px;height:16px;}
  [data-testid="stWidgetLabel"] p{font-size:.58rem !important;}
  div[data-baseweb="select"] > div{min-height:36px !important;height:36px !important;border-radius:11px !important;}
  div[data-baseweb="select"] span{font-size:.74rem !important;}
  .result-main{font-size:.86rem;}
  .result-sub{font-size:.66rem;}
}
</style>
""", unsafe_allow_html=True)


# ===================== DATA =====================
def split_values(value):
    if pd.isna(value) or str(value).strip() == "":
        return []
    return [x.strip() for x in str(value).replace(",", "、").split("、") if x.strip()]


@st.cache_data
def load_data():
    carriers = pd.read_csv(CARRIERS_CSV).fillna("")
    markets = pd.read_csv(MARKETS_CSV).fillna("") if MARKETS_CSV.exists() else pd.DataFrame(columns=["pref", "market"])
    for col in ["origin_areas", "dest_areas", "origin_markets", "dest_markets", "items", "shapes", "routes", "memo", "fare_note"]:
        if col not in carriers.columns:
            carriers[col] = ""
    return carriers, markets


carriers, markets = load_data()


# ===================== LOGIC =====================
def market_to_pref_map():
    if markets.empty:
        return {}
    return dict(zip(markets["market"].astype(str), markets["pref"].astype(str)))


def market_options(pref=""):
    if markets.empty:
        return [""]
    df = markets
    if pref:
        df = df[df["pref"] == pref]
    return [""] + df["market"].dropna().astype(str).tolist()


def get_unique_list(col):
    vals = set()
    for v in carriers[col].tolist():
        vals.update(split_values(v))
    return [""] + sorted(vals)


def match_market(row, origin_market, dest_market, item, shape):
    if not (split_values(row.get("origin_markets", "")) or split_values(row.get("dest_markets", ""))):
        return False
    if origin_market and origin_market not in split_values(row.get("origin_markets", "")):
        return False
    if dest_market and dest_market not in split_values(row.get("dest_markets", "")):
        return False
    if item and item not in split_values(row.get("items", "")):
        return False
    if shape and shape not in split_values(row.get("shapes", "")):
        return False
    return True


def match_pref(row, origin_pref, dest_pref, item, shape):
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
    if origin_market or dest_market:
        market_result = carriers[carriers.apply(lambda r: match_market(r, origin_market, dest_market, item, shape), axis=1)]
        if not market_result.empty:
            return market_result, "market"
    pref_result = carriers[carriers.apply(lambda r: match_pref(r, origin_pref, dest_pref, item, shape), axis=1)]
    return pref_result, "pref_fallback" if (origin_market or dest_market) else "pref"


def render_badges(values, red=False):
    cls = "badge badge-red" if red else "badge"
    return " ".join([f"<span class='{cls}'>{v}</span>" for v in values])


def render_card(row, detail=False):
    has_fare = str(row.get("has_fare_table", "")).lower() in ["true", "1", "yes", "あり"]
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='company'>{row.get('name', '')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small'>📍 {row.get('base', '') or '—'}　👤 {row.get('contact', '') or '—'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small'>📄 運賃表：{'あり' if has_fare else 'なし'}</div>", unsafe_allow_html=True)

    if detail:
        if split_values(row.get("origin_markets", "")) or split_values(row.get("dest_markets", "")):
            st.markdown("**市場対応**")
            st.markdown("発：" + (render_badges(split_values(row.get("origin_markets", ""))) or "—"), unsafe_allow_html=True)
            st.markdown("着：" + (render_badges(split_values(row.get("dest_markets", "")), True) or "—"), unsafe_allow_html=True)

        st.markdown("**対応エリア**")
        st.markdown("発：" + render_badges(split_values(row.get("origin_areas", ""))), unsafe_allow_html=True)
        st.markdown("着：" + render_badges(split_values(row.get("dest_areas", "")), True), unsafe_allow_html=True)

        st.markdown("**ルート**")
        st.markdown(render_badges(split_values(row.get("routes", ""))), unsafe_allow_html=True)

        st.markdown("**品目 / 荷姿**")
        st.markdown(render_badges(split_values(row.get("items", ""))) + render_badges(split_values(row.get("shapes", ""))), unsafe_allow_html=True)

        st.markdown("**運賃情報**")
        st.info(row.get("fare_note", "") or "—")

        st.markdown("**メモ・注意点**")
        st.markdown(f"<div class='note'>{row.get('memo', '') or '—'}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ===================== UI =====================
st.markdown(f"""
<div class="header">
  <div class="header-row">
    <div>
      <div class="brand">ASSIST Co., Ltd. — INTERNAL TOOL</div>
      <div class="title">🚛 運送会社リスト検索ツール</div>
    </div>
    <div class="count">登録運送会社<strong>{len(carriers)}</strong>社</div>
  </div>
</div>
""", unsafe_allow_html=True)

tab_search, tab_all, tab_market = st.tabs(["🔍 運賃検索", "📋 会社一覧", "🏪 市場一覧"])

with tab_search:
    mtp = market_to_pref_map()

    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.markdown('<div class="search-title">🔍 発地・着地から運送会社を検索</div>', unsafe_allow_html=True)

    origin_col, dest_col = st.columns(2)

    with origin_col:
        st.markdown('<div class="route-inner">', unsafe_allow_html=True)
        st.markdown('<div class="route-head"><span class="dot green"></span>発地</div>', unsafe_allow_html=True)
        origin_pref = st.selectbox("メイン　都道府県", [""] + PREF_ORDER, key="origin_pref")
        origin_market = st.selectbox("サブ　市場名", market_options(origin_pref), key="origin_market")
        if origin_market and origin_market in mtp:
            origin_pref = mtp[origin_market]
        st.markdown('</div>', unsafe_allow_html=True)

    with dest_col:
        st.markdown('<div class="route-inner">', unsafe_allow_html=True)
        st.markdown('<div class="route-head"><span class="dot red"></span>着地</div>', unsafe_allow_html=True)
        dest_pref = st.selectbox("メイン　都道府県", [""] + PREF_ORDER, key="dest_pref")
        dest_market = st.selectbox("サブ　市場名", market_options(dest_pref), key="dest_market")
        if dest_market and dest_market in mtp:
            dest_pref = mtp[dest_market]
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    item_col, shape_col = st.columns(2)

    with item_col:
        item = st.selectbox("品目（任意）", get_unique_list("items"), key="item")
    with shape_col:
        shape = st.selectbox("荷姿（任意）", get_unique_list("shapes"), key="shape")

    has_condition = any([origin_pref, origin_market, dest_pref, dest_market, item, shape])

    if has_condition:
        result, mode = search_carriers(origin_pref, origin_market, dest_pref, dest_market, item, shape)
        label = "市場→市場" if mode == "market" else "都道府県"
        st.markdown(f'<div class="result-row"><div class="result-main">{len(result)} 社が見つかりました</div><div class="result-sub">検索方式：{label}</div></div>', unsafe_allow_html=True)
    else:
        result = pd.DataFrame()
        mode = ""
        st.markdown('<div class="result-row"><div class="result-main">条件を入力してください</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if has_condition:
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
        df = carriers[carriers.apply(lambda r: keyword in " ".join(map(str, r.values)), axis=1)]
    for _, row in df.iterrows():
        with st.expander(f"{row['name']}｜詳細を見る"):
            render_card(row, detail=True)

with tab_market:
    st.subheader("市場・卸売センター一覧")
    q = st.text_input("市場名で検索")
    dfm = markets
    if q:
        dfm = dfm[dfm["market"].astype(str).str.contains(q, na=False)]
    for pref in PREF_ORDER:
        group = dfm[dfm["pref"] == pref]
        if not group.empty:
            st.markdown(f"**{pref}**")
            st.markdown(render_badges(group["market"].astype(str).tolist()), unsafe_allow_html=True)
