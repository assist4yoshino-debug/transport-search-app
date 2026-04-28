import json
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path).fillna("")


carriers_df = load_csv(CARRIERS_CSV)
markets_df = load_csv(MARKETS_CSV)

for col in [
    "id", "name", "base", "contact", "has_fare_table", "routes",
    "origin_areas", "dest_areas", "origin_markets", "dest_markets",
    "items", "shapes", "fare_note", "memo",
]:
    if col not in carriers_df.columns:
        carriers_df[col] = ""

if markets_df.empty:
    markets_df = pd.DataFrame(columns=["pref", "market"])

carriers = carriers_df.to_dict(orient="records")
markets = markets_df.to_dict(orient="records")

carriers_json = json.dumps(carriers, ensure_ascii=False)
markets_json = json.dumps(markets, ensure_ascii=False)
pref_json = json.dumps(PREF_ORDER, ensure_ascii=False)

st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
  background:#07111f !important;
}
.block-container {
  padding:0 !important;
  max-width:100% !important;
}
[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"] {
  display:none !important;
}
iframe {
  width:100% !important;
}
</style>
""",
    unsafe_allow_html=True,
)

html_code = f"""
<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<style>
:root {{
  --bg:#07111f;
  --panel:#0d1b2a;
  --panel2:#15314d;
  --blue:#5bc4f5;
  --muted:#aebfd2;
  --line:rgba(91,196,245,.30);
  --green:#16d72c;
  --red:#ef233c;
  --white:#ffffff;
  --ink:#0d1b2a;
}}
* {{
  box-sizing:border-box;
  -webkit-tap-highlight-color: transparent;
}}
html, body {{
  margin:0;
  padding:0;
  background:
    radial-gradient(circle at 18% 0%, rgba(38,105,157,.48), transparent 32%),
    linear-gradient(145deg,#07111f 0%,#0b1a2b 52%,#07111f 100%);
  color:white;
  font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;
  overflow-x:hidden;
}}
.app {{
  width:100%;
  max-width:760px;
  margin:0 auto;
  padding:10px 10px 28px;
}}
.header {{
  background:linear-gradient(135deg,#0d1b2a,#173a59 64%,#1e5f8e);
  border:1px solid rgba(91,196,245,.34);
  border-radius:22px;
  padding:12px 14px;
  box-shadow:0 12px 32px rgba(0,0,0,.32);
}}
.header-row {{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:10px;
}}
.brand {{
  color:var(--blue);
  font-size:10px;
  font-weight:900;
  letter-spacing:.22em;
  white-space:nowrap;
}}
.title {{
  margin-top:5px;
  font-size:22px;
  line-height:1.12;
  font-weight:900;
}}
.count {{
  text-align:right;
  color:#d4e8f7;
  font-size:12px;
  white-space:nowrap;
}}
.count strong {{
  display:block;
  color:var(--blue);
  font-size:36px;
  line-height:.95;
}}
.tabs {{
  display:flex;
  gap:4px;
  margin:8px 0 8px;
  border-bottom:1px solid rgba(255,255,255,.10);
}}
.tab {{
  appearance:none;
  border:0;
  background:transparent;
  color:rgba(255,255,255,.68);
  padding:9px 10px;
  font-size:15px;
  border-radius:12px 12px 0 0;
  font-weight:700;
}}
.tab.active {{
  background:white;
  color:#0d1b2a;
  font-weight:900;
}}
.panel {{
  display:none;
}}
.panel.active {{
  display:block;
}}
.search-card {{
  background:linear-gradient(135deg,rgba(9,23,40,.98),rgba(22,57,87,.96));
  border:1px solid rgba(91,196,245,.30);
  border-radius:22px;
  padding:14px;
  box-shadow:0 16px 36px rgba(0,0,0,.32);
}}
.search-title {{
  font-size:18px;
  font-weight:900;
  margin-bottom:12px;
}}
.route-grid {{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
}}
.route-box {{
  min-width:0;
  background:rgba(255,255,255,.075);
  border:1px solid rgba(255,255,255,.055);
  border-radius:17px;
  padding:10px 9px 9px;
}}
.route-head {{
  display:flex;
  align-items:center;
  gap:7px;
  font-size:16px;
  font-weight:900;
  margin-bottom:8px;
}}
.dot {{
  width:18px;
  height:18px;
  border-radius:50%;
  display:inline-block;
  box-shadow:inset 0 1px 2px rgba(255,255,255,.55),0 0 12px rgba(0,0,0,.36);
}}
.green {{ background:radial-gradient(circle at 35% 30%,#75ff7b,#06b61e 65%); }}
.red {{ background:radial-gradient(circle at 35% 30%,#ff8585,#e10d1a 65%); }}
.field {{
  margin-bottom:7px;
}}
.field label {{
  display:block;
  color:#dbeafe;
  font-size:11px;
  font-weight:800;
  margin-bottom:3px;
  line-height:1.1;
}}
select, input {{
  width:100%;
  height:38px;
  border:0;
  border-radius:12px;
  background:white;
  color:#111827;
  padding:0 30px 0 10px;
  font-size:14px;
  font-weight:500;
  outline:none;
  box-shadow:0 2px 10px rgba(0,0,0,.16);
}}
select {{
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}}
.divider {{
  height:1px;
  background:rgba(255,255,255,.13);
  margin:12px 0 10px;
}}
.sub-grid {{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
}}
.result-line {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
  margin-top:10px;
}}
.result-main {{
  color:var(--blue);
  font-weight:900;
  font-size:17px;
}}
.result-sub {{
  color:#cbd5e1;
  font-size:12px;
  white-space:nowrap;
}}
.notice {{
  margin-top:10px;
  padding:10px 12px;
  border-radius:14px;
  background:rgba(251,191,36,.13);
  color:#ffe9a6;
  border:1px solid rgba(251,191,36,.26);
  font-size:14px;
  line-height:1.5;
}}
.success {{
  background:rgba(34,197,94,.12);
  color:#bbf7d0;
  border-color:rgba(34,197,94,.26);
}}
.results {{
  margin-top:10px;
}}
.company-card {{
  background:rgba(255,255,255,.98);
  color:#0d1b2a;
  border:1px solid #dbe4ef;
  border-radius:16px;
  padding:12px;
  margin-bottom:8px;
  box-shadow:0 5px 18px rgba(0,0,0,.16);
}}
.company-title {{
  font-size:17px;
  font-weight:900;
  margin-bottom:4px;
}}
.company-meta {{
  font-size:12px;
  color:#64748b;
  line-height:1.45;
}}
.detail-btn {{
  margin-top:8px;
  width:100%;
  border:0;
  border-radius:12px;
  background:#0d1b2a;
  color:white;
  font-weight:900;
  padding:9px 10px;
  font-size:14px;
}}
.detail {{
  display:none;
  margin-top:10px;
  border-top:1px solid #e2e8f0;
  padding-top:9px;
}}
.detail.open {{
  display:block;
}}
.section-title {{
  font-size:13px;
  font-weight:900;
  color:#0f172a;
  margin:8px 0 4px;
}}
.badge {{
  display:inline-block;
  padding:3px 9px;
  margin:3px 4px 3px 0;
  border-radius:999px;
  background:#edf6ff;
  border:1px solid #c9def2;
  color:#17324e;
  font-size:12px;
}}
.badge-red {{
  background:#fff0f0;
  border-color:#f3c5c5;
  color:#7f1d1d;
}}
.note {{
  background:#fff8e6;
  border-left:4px solid #f39c12;
  color:#5f4300;
  padding:9px 10px;
  border-radius:10px;
  font-size:13px;
  line-height:1.55;
}}
.list-card {{
  background:white;
  color:#0d1b2a;
  border-radius:18px;
  padding:14px;
  margin-top:8px;
}}
.search-input {{
  height:42px;
  border:1px solid #dbe4ef;
  margin-bottom:12px;
}}
.pref-title {{
  display:inline-block;
  background:#e8f0fa;
  color:#173a59;
  border-radius:10px;
  padding:5px 10px;
  font-weight:900;
  margin:12px 0 6px;
}}
.market-chip {{
  display:inline-block;
  border:1px solid #ccd7e6;
  border-radius:999px;
  padding:5px 11px;
  margin:4px 4px 4px 0;
  color:#1f2937;
  background:#fff;
  font-size:14px;
}}
.empty {{
  color:#cbd5e1;
  font-size:14px;
  padding:16px 0;
}}
@media(max-width:430px){{
  .app {{ padding:8px 9px 24px; }}
  .header {{ padding:10px 11px; border-radius:20px; }}
  .brand {{ font-size:8.5px; letter-spacing:.18em; }}
  .title {{ font-size:18px; }}
  .count {{ font-size:10px; }}
  .count strong {{ font-size:28px; }}
  .tab {{ font-size:13px; padding:8px 7px; }}
  .search-card {{ padding:12px 10px; border-radius:20px; }}
  .search-title {{ font-size:16px; margin-bottom:9px; }}
  .route-grid {{ gap:7px; }}
  .route-box {{ padding:8px 7px; border-radius:14px; }}
  .route-head {{ font-size:14px; margin-bottom:6px; }}
  .dot {{ width:16px; height:16px; }}
  .field label {{ font-size:10px; }}
  select, input {{ height:35px; border-radius:11px; font-size:12.5px; padding-left:8px; padding-right:24px; }}
  .sub-grid {{ gap:7px; }}
  .result-main {{ font-size:15px; }}
  .result-sub {{ font-size:11px; }}
}}
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <div class="header-row">
      <div>
        <div class="brand">ASSIST Co., Ltd. — INTERNAL TOOL</div>
        <div class="title">🚛 運送会社リスト検索ツール</div>
      </div>
      <div class="count">登録運送会社<strong id="carrierCount">0</strong>社</div>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="search">🔍 運賃検索</button>
    <button class="tab" data-tab="companies">📋 会社一覧</button>
    <button class="tab" data-tab="markets">🏪 市場一覧</button>
  </div>

  <section id="search" class="panel active">
    <div class="search-card">
      <div class="search-title">🔍 発地・着地から運送会社を検索</div>

      <div class="route-grid">
        <div class="route-box">
          <div class="route-head"><span class="dot green"></span>発地</div>
          <div class="field">
            <label>メイン　都道府県</label>
            <select id="originPref"></select>
          </div>
          <div class="field">
            <label>サブ　市場名</label>
            <select id="originMarket"></select>
          </div>
        </div>

        <div class="route-box">
          <div class="route-head"><span class="dot red"></span>着地</div>
          <div class="field">
            <label>メイン　都道府県</label>
            <select id="destPref"></select>
          </div>
          <div class="field">
            <label>サブ　市場名</label>
            <select id="destMarket"></select>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="sub-grid">
        <div class="field">
          <label>品目（任意）</label>
          <select id="item"></select>
        </div>
        <div class="field">
          <label>荷姿（任意）</label>
          <select id="shape"></select>
        </div>
      </div>

      <div class="result-line">
        <div id="resultMain" class="result-main">条件を入力してください</div>
        <div id="resultSub" class="result-sub"></div>
      </div>

      <div id="notice"></div>
    </div>

    <div id="results" class="results"></div>
  </section>

  <section id="companies" class="panel">
    <div class="list-card">
      <input class="search-input" id="companyKeyword" placeholder="会社名・メモで検索..." />
      <div id="companyList"></div>
    </div>
  </section>

  <section id="markets" class="panel">
    <div class="list-card">
      <input class="search-input" id="marketKeyword" placeholder="市場名で検索..." />
      <div id="marketList"></div>
    </div>
  </section>
</div>

<script>
const CARRIERS = {carriers_json};
const MARKETS = {markets_json};
const PREF_ORDER = {pref_json};

const $ = (id) => document.getElementById(id);

function splitValues(v) {{
  if (v === null || v === undefined) return [];
  return String(v).replaceAll(",", "、").split("、").map(x => x.trim()).filter(Boolean);
}}

function escapeHtml(str) {{
  return String(str ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}}

function optionHtml(value, label) {{
  return `<option value="${{escapeHtml(value)}}">${{escapeHtml(label)}}</option>`;
}}

function fillSelect(el, values, placeholder="すべて") {{
  el.innerHTML = optionHtml("", placeholder) + values.map(v => optionHtml(v, v)).join("");
}}

function marketToPrefMap() {{
  const m = {{}};
  MARKETS.forEach(x => m[String(x.market)] = String(x.pref));
  return m;
}}

const MTP = marketToPrefMap();

function marketsByPref(pref) {{
  return MARKETS
    .filter(x => !pref || String(x.pref) === pref)
    .map(x => String(x.market));
}}

function uniqueFromCarriers(col) {{
  const s = new Set();
  CARRIERS.forEach(c => splitValues(c[col]).forEach(v => s.add(v)));
  return Array.from(s).sort();
}}

function init() {{
  $("carrierCount").textContent = CARRIERS.length;

  fillSelect($("originPref"), PREF_ORDER, "選択してください");
  fillSelect($("destPref"), PREF_ORDER, "選択してください");
  fillSelect($("originMarket"), marketsByPref(""), "市場を選択...");
  fillSelect($("destMarket"), marketsByPref(""), "市場を選択...");
  fillSelect($("item"), uniqueFromCarriers("items"), "すべて");
  fillSelect($("shape"), uniqueFromCarriers("shapes"), "すべて");

  ["originPref","destPref","originMarket","destMarket","item","shape"].forEach(id => {{
    $(id).addEventListener("change", handleSearch);
  }});

  $("originPref").addEventListener("change", () => {{
    fillSelect($("originMarket"), marketsByPref($("originPref").value), "市場を選択...");
  }});
  $("destPref").addEventListener("change", () => {{
    fillSelect($("destMarket"), marketsByPref($("destPref").value), "市場を選択...");
  }});

  $("originMarket").addEventListener("change", () => {{
    const m = $("originMarket").value;
    if (m && MTP[m]) $("originPref").value = MTP[m];
  }});
  $("destMarket").addEventListener("change", () => {{
    const m = $("destMarket").value;
    if (m && MTP[m]) $("destPref").value = MTP[m];
  }});

  document.querySelectorAll(".tab").forEach(btn => {{
    btn.addEventListener("click", () => {{
      document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      $(btn.dataset.tab).classList.add("active");
    }});
  }});

  $("companyKeyword").addEventListener("input", renderCompanyList);
  $("marketKeyword").addEventListener("input", renderMarketList);

  renderCompanyList();
  renderMarketList();
}}

function hasMarketData(c) {{
  return splitValues(c.origin_markets).length || splitValues(c.dest_markets).length;
}}

function matchMarket(c, originMarket, destMarket, item, shape) {{
  if (!hasMarketData(c)) return false;
  if (originMarket && !splitValues(c.origin_markets).includes(originMarket)) return false;
  if (destMarket && !splitValues(c.dest_markets).includes(destMarket)) return false;
  if (item && !splitValues(c.items).includes(item)) return false;
  if (shape && !splitValues(c.shapes).includes(shape)) return false;
  return true;
}}

function matchPref(c, originPref, destPref, item, shape) {{
  if (originPref && !splitValues(c.origin_areas).includes(originPref)) return false;
  if (destPref && !splitValues(c.dest_areas).includes(destPref)) return false;
  if (item && !splitValues(c.items).includes(item)) return false;
  if (shape && !splitValues(c.shapes).includes(shape)) return false;
  return true;
}}

function search() {{
  let originPref = $("originPref").value;
  let destPref = $("destPref").value;
  const originMarket = $("originMarket").value;
  const destMarket = $("destMarket").value;
  const item = $("item").value;
  const shape = $("shape").value;

  if (originMarket && MTP[originMarket]) originPref = MTP[originMarket];
  if (destMarket && MTP[destMarket]) destPref = MTP[destMarket];

  const hasCondition = !!(originPref || destPref || originMarket || destMarket || item || shape);
  if (!hasCondition) return {{ hasCondition:false, result:[], mode:"" }};

  if (originMarket || destMarket) {{
    const marketResult = CARRIERS.filter(c => matchMarket(c, originMarket, destMarket, item, shape));
    if (marketResult.length) return {{ hasCondition:true, result:marketResult, mode:"market" }};
  }}

  const prefResult = CARRIERS.filter(c => matchPref(c, originPref, destPref, item, shape));
  return {{ hasCondition:true, result:prefResult, mode:(originMarket || destMarket) ? "pref_fallback" : "pref" }};
}}

function handleSearch() {{
  const s = search();
  const notice = $("notice");
  const results = $("results");
  notice.innerHTML = "";
  results.innerHTML = "";

  if (!s.hasCondition) {{
    $("resultMain").textContent = "条件を入力してください";
    $("resultSub").textContent = "";
    return;
  }}

  $("resultMain").textContent = `${{s.result.length}} 社が見つかりました`;
  $("resultSub").textContent = "検索方式：" + (s.mode === "market" ? "市場→市場" : "都道府県");

  if (s.mode === "pref_fallback") {{
    notice.innerHTML = `<div class="notice">市場単位では該当なし。都道府県単位で候補を表示しています。</div>`;
  }} else if (s.mode === "market") {{
    notice.innerHTML = `<div class="notice success">市場単位で該当しました。</div>`;
  }}

  if (!s.result.length) {{
    results.innerHTML = `<div class="empty">条件に合う運送会社が見つかりません。</div>`;
    return;
  }}

  results.innerHTML = s.result.map(renderCarrierCard).join("");
  bindDetailButtons();
}}

function badges(values, red=false) {{
  const cls = red ? "badge badge-red" : "badge";
  return splitValues(values).map(v => `<span class="${{cls}}">${{escapeHtml(v)}}</span>`).join("") || "—";
}}

function fareText(c) {{
  const v = String(c.has_fare_table).toLowerCase();
  return ["true","1","yes","あり"].includes(v) ? "あり" : "なし";
}}

function renderCarrierCard(c) {{
  const safeName = escapeHtml(c.name || "");
  return `
    <div class="company-card">
      <div class="company-title">${{safeName}}</div>
      <div class="company-meta">📍 ${{escapeHtml(c.base || "—")}}　👤 ${{escapeHtml(c.contact || "—")}}</div>
      <div class="company-meta">📄 運賃表：${{fareText(c)}}</div>
      ${{c.memo ? `<div class="company-meta">📝 ${{escapeHtml(String(c.memo).slice(0, 80))}}${{String(c.memo).length > 80 ? "…" : ""}}</div>` : ""}}
      <button class="detail-btn" type="button">詳細を見る</button>
      <div class="detail">
        ${{(splitValues(c.origin_markets).length || splitValues(c.dest_markets).length) ? `
          <div class="section-title">市場対応</div>
          <div>発：${{badges(c.origin_markets)}}</div>
          <div>着：${{badges(c.dest_markets, true)}}</div>
        ` : ""}}
        <div class="section-title">対応エリア</div>
        <div>発：${{badges(c.origin_areas)}}</div>
        <div>着：${{badges(c.dest_areas, true)}}</div>
        <div class="section-title">ルート</div>
        <div>${{badges(c.routes)}}</div>
        <div class="section-title">品目 / 荷姿</div>
        <div>${{badges(c.items)}}${{badges(c.shapes)}}</div>
        <div class="section-title">運賃情報</div>
        <div class="note">${{escapeHtml(c.fare_note || "—")}}</div>
        <div class="section-title">メモ・注意点</div>
        <div class="note">${{escapeHtml(c.memo || "—")}}</div>
      </div>
    </div>
  `;
}}

function bindDetailButtons() {{
  document.querySelectorAll(".detail-btn").forEach(btn => {{
    btn.onclick = () => {{
      const detail = btn.nextElementSibling;
      detail.classList.toggle("open");
      btn.textContent = detail.classList.contains("open") ? "閉じる" : "詳細を見る";
    }};
  }});
}}

function renderCompanyList() {{
  const q = $("companyKeyword").value.trim();
  const list = q
    ? CARRIERS.filter(c => JSON.stringify(c).includes(q))
    : CARRIERS;
  $("companyList").innerHTML = list.map(renderCarrierCard).join("");
  bindDetailButtons();
}}

function renderMarketList() {{
  const q = $("marketKeyword").value.trim();
  const wrap = $("marketList");
  let html = "";
  PREF_ORDER.forEach(pref => {{
    const items = MARKETS.filter(m => String(m.pref) === pref && (!q || String(m.market).includes(q)));
    if (!items.length) return;
    html += `<div class="pref-title">${{escapeHtml(pref)}}</div><div>`;
    html += items.map(m => `<span class="market-chip">${{escapeHtml(m.market)}}</span>`).join("");
    html += `</div>`;
  }});
  wrap.innerHTML = html || `<div class="empty" style="color:#64748b;">見つかりませんでした。</div>`;
}}

init();
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
