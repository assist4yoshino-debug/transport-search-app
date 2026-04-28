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

st.markdown("""
<style>
:root {
  --navy: #07111f;
  --navy2: #0d1b2a;
  --blue: #5bc4f5;
  --line: rgba(91,196,245,.28);
  --muted: #b9c7d8;
  --green: #16d72c;
  --red: #ef233c;
}

/* 全体を濃紺に固定。白背景化を防ぐ */
html, body, [data-testid="stAppViewContainer"], .stApp {
  background:
    radial-gradient(circle at top left, rgba(32,92,140,.45), transparent 35%),
    linear-gradient(135deg, #07111f 0%, #0d1b2a 55%, #07111f 100%) !important;
  color: #ffffff !important;
}

.block-container {
  padding: .55rem .75rem 1.4rem !important;
  max-width: 760px !important;
}

[data-testid="stHeader"] {background: transparent !important;}
#MainMenu, footer, [data-testid="stToolbar"] {visibility: hidden !important;}

p, label, span, div {
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Noto Sans JP", sans-serif !important;
}

/* ヘッダー */
.header-box {
  border: 1px solid var(--line);
  background: linear-gradient(135deg, #0d1b2a 0%, #163a5a 70%, #1e5f8e 100%);
  border-radius: 22px;
  padding: 12px 14px;
  color: #fff;
  box-shadow: 0 10px 30px rgba(0,0,0,.28);
  margin-bottom: 10px;
}
.header-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.brand {
  font-size: .62rem;
  letter-spacing: .22em;
  color: var(--blue);
  font-weight: 900;
  white-space: nowrap;
}
.title {
  margin-top: 5px;
  font-size: 1.15rem;
  line-height: 1.15;
  font-weight: 900;
}
.count {
  text-align: right;
  font-size: .7rem;
  color: #d4e8f7;
  white-space: nowrap;
}
.count strong {
  display: block;
  font-size: 1.8rem;
  line-height: .95;
  color: var(--blue);
}

/* タブ */
div[data-testid="stTabs"] button {
  color: rgba(255,255,255,.72) !important;
  padding: 8px 7px !important;
  font-size: .83rem !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: #07111f !important;
  background: #ffffff !important;
  border-radius: 10px 10px 0 0 !important;
  font-weight: 900 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap: 3px !important;
}

/* 検索パネル */
.search-panel {
  border: 1px solid var(--line);
  background: linear-gradient(135deg, rgba(8,22,38,.98), rgba(21,56,86,.98));
  border-radius: 22px;
  padding: 13px 12px 12px;
  box-shadow: 0 14px 34px rgba(0,0,0,.30);
  margin-top: 8px;
  margin-bottom: 12px;
}
.search-title {
  color: #fff;
  font-size: 1rem;
  font-weight: 900;
  margin-bottom: 10px;
}

/* iPhoneでも列を強制的に横並びにする */
[data-testid="stHorizontalBlock"] {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  gap: 8px !important;
  align-items: stretch !important;
}
[data-testid="column"] {
  flex: 1 1 0 !important;
  width: auto !important;
  min-width: 0 !important;
}

/* 発地・着地ボックス風 */
.route-label {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #fff;
  font-size: .9rem;
  font-weight: 900;
  margin: 4px 0 7px;
}
.dot {
  width: 19px;
  height: 19px;
  border-radius: 50%;
  display: inline-block;
  box-shadow: inset 0 1px 2px rgba(255,255,255,.5), 0 0 10px rgba(0,0,0,.3);
}
.green {background: radial-gradient(circle at 35% 30%, #77ff7b, #05b51b 65%);}
.red {background: radial-gradient(circle at 35% 30%, #ff8585, #e10d1a 65%);}
.arrow {
  color: rgba(255,255,255,.35);
  text-align: center;
  font-size: 1.35rem;
  padding-top: 58px;
}
.divider {
  height: 1px;
  background: rgba(255,255,255,.14);
  margin: 11px 0 9px;
}

/* ラベルとセレクト */
label, [data-testid="stWidgetLabel"] {
  color: #dbeafe !important;
  font-size: .62rem !important;
  font-weight: 700 !important;
  opacity: 1 !important;
}
[data-testid="stWidgetLabel"] p {
  color: #dbeafe !important;
  font-size: .62rem !important;
  font-weight: 700 !important;
}
div[data-baseweb="select"] > div {
  background: #ffffff !important;
  border: 1.5px solid rgba(255,255,255,.65) !important;
  border-radius: 12px !important;
  min-height: 38px !important;
  box-shadow: 0 1px 8px rgba(0,0,0,.12);
}
div[data-baseweb="select"] span {
  font-size: .82rem !important;
  color: #111827 !important;
}
[data-testid="stVerticalBlock"] {
  gap: .30rem !important;
}

/* 結果 */
.result-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 8px;
}
.result-main {
  color: var(--blue);
  font-weight: 900;
  font-size: .9rem;
}
.result-sub {
  color: #cbd5e1;
  font-size: .72rem;
}

/* カード */
.card {
  background: rgba(255,255,255,.98);
  color: #0d1b2a;
  border: 1px solid #dbe4ef;
  border-radius: 16px;
  padding: 13px;
  margin-bottom: 9px;
  box-shadow: 0 5px 18px rgba(0,0,0,.16);
}
.company {
  color: #0d1b2a;
  font-size: 1rem;
  font-weight: 900;
  margin-bottom: 4px;
}
.small {font-size:.78rem;color:#64748b;}
.badge {
  display: inline-block;
  padding: 3px 9px;
  margin: 3px 4px 3px 0;
  border-radius: 999px;
  background: #edf6ff;
  border: 1px solid #c9def2;
  color: #17324e;
  font-size: .74rem;
}
.badge-red {
  background: #fff0f0;
  border-color: #f3c5c5;
  color:#7f1d1d;
}
.note {
  background: #fff8e6;
  border-left: 4px solid #f39c12;
  color:#5f4300;
  padding: 9px 11px;
  border-radius: 10px;
  font-size: .84rem;
}

/* 画面が細い時の圧縮 */
@media (max-width: 430px) {
  .block-container {padding-left: .62rem !important; padding-right: .62rem !important;}
  .header-box {padding: 10px 11px;}
  .brand {font-size: .54rem; letter-spacing: .18em;}
  .title {font-size: 1.02rem;}
  .count strong {font-size: 1.55rem;}
  .search-panel {padding: 11px 9px;}
  [data-testid="stHorizontalBlock"] {gap: 6px !important;}
  .route-label {font-size: .78rem;}
  .dot {width: 16px; height: 16px;}
  .arrow {font-size: 1rem; padding-top: 55px;}
  div[data-baseweb="select"] > div {min-height: 36px !important;}
  div[data-baseweb="select"] span {font-size: .76rem !important;}
}
</style>
""", unsafe_allow_html=True)


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


st.markdown(f"""
<div class="header-box">
  <div class="header-top">
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

    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.markdown('<div class="search-title">🔍 発地・着地から運送会社を検索</div>', unsafe_allow_html=True)

    left, arrow, right = st.columns([1, .10, 1])

    with left:
        st.markdown('<div class="route-label"><span class="dot green"></span>発地</div>', unsafe_allow_html=True)
        origin_pref = st.selectbox("メイン　都道府県", [""] + PREF_ORDER, key="origin_pref")
        origin_market = st.selectbox("サブ　市場名", market_options(origin_pref), key="origin_market")
        if origin_market and origin_market in mtp:
            origin_pref = mtp[origin_market]

    with arrow:
        st.markdown('<div class="arrow">→</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="route-label"><span class="dot red"></span>着地</div>', unsafe_allow_html=True)
        dest_pref = st.selectbox("メイン　都道府県", [""] + PREF_ORDER, key="dest_pref")
        dest_market = st.selectbox("サブ　市場名", market_options(dest_pref), key="dest_market")
        if dest_market and dest_market in mtp:
            dest_pref = mtp[dest_market]

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
        st.markdown(f'<div class="result-line"><div class="result-main">{len(result)} 社が見つかりました</div><div class="result-sub">検索方式：{label}</div></div>', unsafe_allow_html=True)
    else:
        result = pd.DataFrame()
        mode = ""
        st.markdown('<div class="result-line"><div class="result-main">条件を入力してください</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

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
