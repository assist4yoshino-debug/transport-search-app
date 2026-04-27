import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="ASSIST ROUTE FINDER", page_icon="🚛", layout="centered", initial_sidebar_state="collapsed")

APP_DIR = Path(__file__).parent
CARRIERS_CSV = APP_DIR / "carriers.csv"
MARKETS_CSV = APP_DIR / "markets.csv"

PREF_ORDER = [
    "北海道", "青森", "岩手", "宮城", "秋田", "山形", "福島",
    "茨城", "栃木", "群馬", "埼玉", "千葉", "東京", "神奈川",
    "新潟", "富山", "石川", "福井", "山梨", "長野",
    "岐阜", "静岡", "愛知", "三重", "滋賀", "京都", "大阪", "兵庫", "奈良", "和歌山",
    "鳥取", "島根", "岡山", "広島", "山口", "徳島", "香川", "愛媛", "高知",
    "福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄",
]

st.markdown("""
<style>
:root{--blue:#38bdf8;--muted:#94a3b8;--gold:#fbbf24;}
html,body,[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#16324f 0,#070b12 36%,#05070c 100%)!important;color:#e5eef8;}
[data-testid="stHeader"]{background:transparent}.block-container{padding-top:.5rem;padding-bottom:1.2rem;max-width:760px;padding-left:.8rem;padding-right:.8rem}
h1,h2,h3{margin-top:.15rem!important;margin-bottom:.25rem!important}h1{font-size:1.1rem!important}h3{font-size:.88rem!important}
p,label,span,div{font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif}label{font-size:.72rem!important;color:#b7c4d6!important;margin-bottom:0!important}
[data-testid="stTabs"] button{color:#cbd5e1;padding:7px 8px;font-size:.86rem}[data-testid="stTabs"] button[aria-selected="true"]{color:white;border-bottom-color:var(--blue)}
div[data-baseweb="select"]>div,input{background:rgba(255,255,255,.98)!important;border-radius:12px!important;min-height:40px!important}div[data-baseweb="select"] span{font-size:.9rem!important}
[data-testid="stVerticalBlock"]{gap:.25rem!important}div[data-testid="column"]{padding:0 .12rem!important}.stSelectbox{margin-bottom:.12rem!important}
.hero{border:1px solid rgba(125,211,248,.22);background:linear-gradient(135deg,rgba(15,23,36,.96),rgba(18,29,45,.92));border-radius:16px;padding:10px 12px;margin-bottom:6px;box-shadow:0 10px 34px rgba(0,0,0,.32)}
.hero .k{font-size:.64rem;color:var(--blue);letter-spacing:.18em;font-weight:800}.hero .t{font-size:1rem;font-weight:900;color:white;margin-top:1px}.hero .s{font-size:.7rem;color:var(--muted);margin-top:2px}
.panel{border:1px solid rgba(125,211,248,.22);background:linear-gradient(135deg,rgba(15,23,36,.96),rgba(18,29,45,.92));border-radius:16px;padding:10px;margin-bottom:9px}.title{font-size:.9rem;font-weight:900;color:white;margin-bottom:3px}
.card{background:linear-gradient(135deg,rgba(15,23,36,.98),rgba(17,24,39,.94));border:1px solid rgba(148,163,184,.18);border-radius:16px;padding:13px;margin-bottom:9px;box-shadow:0 8px 24px rgba(0,0,0,.22)}
.company{font-size:1rem;font-weight:900;color:white;margin-bottom:4px}.small{font-size:.8rem;color:var(--muted)}.badge{display:inline-block;padding:3px 9px;margin:3px 4px 3px 0;border-radius:999px;background:rgba(56,189,248,.13);border:1px solid rgba(56,189,248,.25);color:#dff6ff;font-size:.74rem}.badge-red{background:rgba(248,113,113,.12);border-color:rgba(248,113,113,.26)}
.note{background:rgba(251,191,36,.10);border-left:4px solid var(--gold);color:#fff7d6;padding:9px 11px;border-radius:10px;font-size:.84rem}div[data-testid="stMetric"]{background:rgba(15,23,36,.75);border:1px solid rgba(56,189,248,.20);border-radius:14px;padding:8px 10px}div[data-testid="stMetricValue"]{color:white;font-size:1.15rem}
@media(max-width:640px){.hero .s{display:none}.block-container{padding-left:.65rem;padding-right:.65rem}.panel{padding:9px}.title{font-size:.86rem}}
</style>
""", unsafe_allow_html=True)

def split_values(value):
    if pd.isna(value) or str(value).strip() == "": return []
    return [x.strip() for x in str(value).replace(",", "、").split("、") if x.strip()]

@st.cache_data
def load_data():
    carriers = pd.read_csv(CARRIERS_CSV).fillna("")
    markets = pd.read_csv(MARKETS_CSV).fillna("") if MARKETS_CSV.exists() else pd.DataFrame(columns=["pref","market"])
    for col in ["origin_areas","dest_areas","origin_markets","dest_markets","items","shapes","routes","memo","fare_note"]:
        if col not in carriers.columns: carriers[col] = ""
    return carriers, markets

carriers, markets = load_data()

def market_to_pref_map(): return dict(zip(markets["market"].astype(str), markets["pref"].astype(str))) if not markets.empty else {}
def pref_options(): return [""] + PREF_ORDER
def market_options(pref=""):
    if markets.empty: return [""]
    df = markets[markets["pref"] == pref] if pref else markets
    return [""] + df["market"].astype(str).tolist()
def get_unique_list(col):
    vals=set()
    for v in carriers[col].tolist(): vals.update(split_values(v))
    return [""] + sorted(vals)
def has_market_data(row): return bool(split_values(row.get("origin_markets","")) or split_values(row.get("dest_markets","")))
def match_market(row, om, dm, item, shape):
    if not has_market_data(row): return False
    if om and om not in split_values(row.get("origin_markets","")): return False
    if dm and dm not in split_values(row.get("dest_markets","")): return False
    if item and item not in split_values(row.get("items","")): return False
    if shape and shape not in split_values(row.get("shapes","")): return False
    return True
def match_pref(row, op, dp, item, shape):
    if op and op not in split_values(row.get("origin_areas","")): return False
    if dp and dp not in split_values(row.get("dest_areas","")): return False
    if item and item not in split_values(row.get("items","")): return False
    if shape and shape not in split_values(row.get("shapes","")): return False
    return True
def search_carriers(op, om, dp, dm, item, shape):
    if om or dm:
        mr = carriers[carriers.apply(lambda r: match_market(r, om, dm, item, shape), axis=1)]
        if not mr.empty: return mr, "市場→市場"
    pr = carriers[carriers.apply(lambda r: match_pref(r, op, dp, item, shape), axis=1)]
    return pr, "都道府県"
def badges(values, red=False):
    cls="badge badge-red" if red else "badge"
    return " ".join([f"<span class='{cls}'>{v}</span>" for v in values])
def render_card(row, detail=False):
    has_fare=str(row.get("has_fare_table","")).lower() in ["true","1","yes","あり"]
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='company'>{row.get('name','')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small'>📍 {row.get('base','') or '—'}　👤 {row.get('contact','') or '—'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small'>📄 運賃表：{'あり' if has_fare else 'なし'}</div>", unsafe_allow_html=True)
    if detail:
        if split_values(row.get("origin_markets","")) or split_values(row.get("dest_markets","")):
            st.markdown("**市場対応**")
            st.markdown("発："+(badges(split_values(row.get("origin_markets",""))) or "—"), unsafe_allow_html=True)
            st.markdown("着："+(badges(split_values(row.get("dest_markets","")), True) or "—"), unsafe_allow_html=True)
        st.markdown("**対応エリア**")
        st.markdown("発："+badges(split_values(row.get("origin_areas",""))), unsafe_allow_html=True)
        st.markdown("着："+badges(split_values(row.get("dest_areas","")), True), unsafe_allow_html=True)
        st.markdown("**ルート**")
        st.markdown(badges(split_values(row.get("routes",""))), unsafe_allow_html=True)
        st.markdown("**品目 / 荷姿**")
        st.markdown(badges(split_values(row.get("items","")))+badges(split_values(row.get("shapes",""))), unsafe_allow_html=True)
        st.markdown("**運賃情報**"); st.info(row.get("fare_note","") or "—")
        st.markdown("**メモ・注意点**")
        st.markdown(f"<div class='note'>{row.get('memo','') or '—'}</div>", unsafe_allow_html=True)
    else:
        memo=row.get("memo","")
        if memo: st.markdown(f"<div class='small'>📝 {memo[:80]}{'…' if len(memo)>80 else ''}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""<div class="hero"><div class="k">ASSIST Co., Ltd. — INTERNAL TOOL</div><div class="t">🚛 運送会社リスト検索ツール</div><div class="s">市場→市場。なければ都道府県→都道府県で検索。</div></div>""", unsafe_allow_html=True)

tab_search, tab_all, tab_market = st.tabs(["🔍 運賃検索", "📋 会社一覧", "🏪 市場一覧"])
with tab_search:
    mtp=market_to_pref_map(); prefs=pref_options()
    st.markdown("<div class='panel'><div class='title'>🔍 発地・着地から検索</div>", unsafe_allow_html=True)
    co, cd = st.columns(2)
    with co:
        st.markdown("### 🟢 発地")
        origin_pref=st.selectbox("都道府県", prefs, key="origin_pref")
        origin_market=st.selectbox("市場", market_options(origin_pref), key="origin_market")
        if origin_market and origin_market in mtp: origin_pref=mtp[origin_market]
    with cd:
        st.markdown("### 🔴 着地")
        dest_pref=st.selectbox("都道府県", prefs, key="dest_pref")
        dest_market=st.selectbox("市場", market_options(dest_pref), key="dest_market")
        if dest_market and dest_market in mtp: dest_pref=mtp[dest_market]
    ci, cs = st.columns(2)
    with ci: item=st.selectbox("品目", get_unique_list("items"), key="item")
    with cs: shape=st.selectbox("荷姿", get_unique_list("shapes"), key="shape")
    has_condition=any([origin_pref,origin_market,dest_pref,dest_market,item,shape])
    if not has_condition:
        st.markdown("<div style='color:#67e8f9;font-weight:900;margin-top:4px;'>条件を入力してください</div>", unsafe_allow_html=True)
    else:
        result, mode=search_carriers(origin_pref,origin_market,dest_pref,dest_market,item,shape)
        m1,m2=st.columns(2)
        with m1: st.metric("該当", f"{len(result)} 社")
        with m2: st.metric("検索方式", mode)
        if mode=="都道府県" and (origin_market or dest_market): st.warning("市場単位では該当なし。都道府県単位で候補を表示しています。")
    st.markdown("</div>", unsafe_allow_html=True)
    if has_condition:
        if result.empty: st.error("条件に合う運送会社が見つかりません。")
        else:
            for _, row in result.iterrows():
                with st.expander(f"{row['name']}｜詳細を見る"):
                    render_card(row, True)
with tab_all:
    st.subheader(f"全運送会社：{len(carriers)}社")
    keyword=st.text_input("会社名・メモ検索")
    df=carriers
    if keyword: df=carriers[carriers.apply(lambda r: keyword in " ".join(map(str,r.values)), axis=1)]
    for _, row in df.iterrows():
        with st.expander(f"{row['name']}｜詳細を見る"):
            render_card(row, True)
with tab_market:
    st.subheader("市場・卸売センター一覧")
    q=st.text_input("市場名で検索")
    dfm=markets
    if q: dfm=dfm[dfm["market"].astype(str).str.contains(q, na=False)]
    for pref in PREF_ORDER:
        group=dfm[dfm["pref"]==pref]
        if not group.empty:
            st.markdown(f"**{pref}**")
            st.markdown(badges(group["market"].astype(str).tolist()), unsafe_allow_html=True)
