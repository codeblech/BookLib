HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{SITE_TITLE}}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:         #111111;
  --bg2:        #191919;
  --bg3:        #212121;
  --bg4:        #2a2a2a;
  --bg5:        #323232;
  --border:     #2e2e2e;
  --border2:    #444;
  --text:       #e0e0e0;
  --text-muted: #888;
  --text-dim:   #505050;
  --accent:     #e8613a;
  --accent2:    #c94f2a;
  --accent-glow:rgba(232,97,58,0.15);
  --green:      #4caf72;
  --green-dim:  rgba(76,175,114,0.1);
  --blue:       #5b9bd5;
  --yellow:     #d4a853;
  --card-w:     175px;
  --img-h:      255px;
  --radius:     5px;
  --mono:       'DM Mono', monospace;
  --serif:      'Libre Baskerville', Georgia, serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--mono);
  font-size: 15px;
  min-height: 100vh;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--bg5); border-radius: 3px; }

/* ── HEADER ── */
header {
  padding: 20px 32px 0;
  border-bottom: 1px solid var(--border);
  background: rgba(17,17,17,0.94);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.header-top {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 12px;
}

h1 {
  font-family: var(--serif);
  font-size: 26px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: -0.4px;
}

.count-badge {
  font-size: 12px;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 2px 9px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding-bottom: 11px;
  flex-wrap: wrap;
}

.search-wrap {
  position: relative;
  flex: 1;
  min-width: 160px;
  max-width: 260px;
}

.search-wrap svg {
  position: absolute;
  left: 9px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
  pointer-events: none;
}

#search {
  width: 100%;
  padding: 7px 10px 7px 30px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: var(--mono);
  font-size: 14px;
  outline: none;
  transition: border-color .15s, box-shadow .15s;
}
#search:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
#search::placeholder { color: var(--text-dim); }

select, .btn {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: var(--mono);
  font-size: 14px;
  padding: 8px 12px;
  cursor: pointer;
  outline: none;
  transition: border-color .15s, background .15s;
  appearance: none;
  -webkit-appearance: none;
  white-space: nowrap;
}
select:focus, .btn:hover { border-color: var(--border2); background: var(--bg4); }

.select-wrap { position: relative; }
.select-wrap::after {
  content: '▾';
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
  pointer-events: none;
  font-size: 11px;
}
.select-wrap select { padding-right: 22px; }

.divider { width: 1px; height: 22px; background: var(--border); margin: 0 2px; flex-shrink: 0; }
.btn-clear { color: var(--text-muted); font-size: 13px; }

/* ── MAIN GRID ── */
main { padding: 28px 32px 80px; }

#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, var(--card-w));
  gap: 28px 20px;
  justify-content: center;
}

/* ── CARD ── */
.card {
  width: var(--card-w);
  cursor: pointer;
  animation: fadeIn .22s ease both;
}
@keyframes fadeIn { from { opacity:0; transform: translateY(6px); } to { opacity:1; transform: translateY(0); } }

.cover-wrap {
  width: var(--card-w);
  height: var(--img-h);
  border-radius: 2px 5px 5px 2px;
  overflow: hidden;
  background: var(--bg3);
  border: 1px solid var(--border);
  position: relative;
  margin-bottom: 10px;
  transition: transform .18s ease, box-shadow .18s ease;
  box-shadow:
    inset 2px 0 0 rgba(255,255,255,0.06),
    -3px 2px 5px rgba(0,0,0,0.35),
    -7px 8px 22px rgba(0,0,0,0.22);
}

.cover-wrap::before {
  content: "";
  background-image: linear-gradient(to right,
    rgba(0,0,0,0.22), rgba(255,255,255,0.28) 1%,
    transparent 6%, rgba(0,0,0,0.12) 8%,
    rgba(255,255,255,0.15) 9%, transparent 22%);
  position: absolute; inset: 0;
  z-index: 2; pointer-events: none;
}

.card:hover .cover-wrap {
  transform: translateY(-5px) scale(1.026);
  box-shadow:
    inset 2px 0 0 rgba(255,255,255,0.06),
    -4px 5px 10px rgba(0,0,0,0.4),
    -12px 18px 34px rgba(0,0,0,0.28);
}

.cover-img { width:100%; height:100%; object-fit:cover; display:block; position:relative; z-index:1; }

.cover-placeholder {
  width:100%; height:100%;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:16px; text-align:center; gap:10px;
  background: linear-gradient(145deg, var(--bg3) 0%, var(--bg4) 100%);
  position:relative; z-index:1;
}
.cover-placeholder .ph-title { font-family:var(--serif); font-size:13px; color:var(--text-muted); line-height:1.4; font-style:italic; }
.cover-placeholder .ph-icon { font-size:24px; opacity:.25; }

.card-info { padding:0 2px; }
.card-title {
  font-family:var(--serif); font-size:14px; font-weight:700;
  color:var(--text); line-height:1.35; margin-bottom:5px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
}
.card-authors { color:var(--accent); font-size:13px; margin-bottom:4px;
  display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden; }
.card-meta { color:var(--text-dim); font-size:12px; margin-bottom:4px; }
.rating-stars { color:var(--text-muted); font-size:12px; margin-top:3px; }

/* ── EMPTY ── */
#empty { display:none; text-align:center; padding:100px 20px; color:var(--text-muted); }
#empty .big { font-size:48px; margin-bottom:14px; opacity:.3; }
#empty p { font-size:15px; }

/* ── FULL-SCREEN DETAIL ── */
#detail-overlay {
  display:none;
  position:fixed; inset:0; z-index:300;
  background:var(--bg);
  overflow-y:auto;
}
#detail-overlay.open { display:block; animation: detailIn .2s ease; }
@keyframes detailIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }

.detail-nav {
  position:sticky; top:0; z-index:10;
  background:rgba(17,17,17,0.92);
  backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px);
  border-bottom:1px solid var(--border);
  padding:12px 24px;
  display:flex; align-items:center; gap:12px;
}

.back-btn {
  display:inline-flex; align-items:center; gap:7px;
  background:var(--bg3); border:1px solid var(--border);
  border-radius:var(--radius);
  color:var(--text-muted); font-family:var(--mono); font-size:14px;
  padding:8px 15px; cursor:pointer;
  transition:color .12s, border-color .12s, background .12s;
  flex-shrink:0;
}
.back-btn:hover { color:var(--text); border-color:var(--border2); background:var(--bg4); }

.detail-nav-title {
  font-family:var(--serif); font-size:15px; color:var(--text-muted);
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}

/* Content */
.detail-content {
  max-width: 820px;
  margin: 0 auto;
  padding: 44px 32px 100px;
}

.detail-hero {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 44px;
  margin-bottom: 44px;
  align-items: start;
}

/* Large cover */
.detail-cover {
  width:220px; height:320px;
  border-radius:2px 7px 7px 2px;
  overflow:hidden;
  background:var(--bg3);
  border:1px solid var(--border);
  position:relative;
  box-shadow:
    inset 2px 0 0 rgba(255,255,255,0.07),
    -6px 4px 12px rgba(0,0,0,0.45),
    -14px 16px 40px rgba(0,0,0,0.28);
  flex-shrink:0;
}
.detail-cover::before {
  content:"";
  background-image: linear-gradient(to right,
    rgba(0,0,0,0.22), rgba(255,255,255,0.28) 1%,
    transparent 6%, rgba(0,0,0,0.12) 8%,
    rgba(255,255,255,0.15) 9%, transparent 22%);
  position:absolute; inset:0; z-index:2; pointer-events:none;
}
.detail-cover img { width:100%; height:100%; object-fit:cover; position:relative; z-index:1; display:block; }
.detail-cover .cover-placeholder { height:100%; position:relative; z-index:1; }

/* Info column */
.detail-info { display:flex; flex-direction:column; }

.detail-title {
  font-family:var(--serif);
  font-size:30px; font-weight:700;
  line-height:1.25; color:var(--text);
  margin-bottom:8px; letter-spacing:-0.3px;
}

.detail-authors {
  color:var(--accent); font-size:16px; margin-bottom:22px;
}

/* ── READING LINKS — most important ── */
.reading-links { margin-bottom:22px; }

.section-label {
  font-size:11px; text-transform:uppercase; letter-spacing:1.4px;
  color:var(--text-dim); margin-bottom:9px; font-family:var(--mono);
}

.read-link {
  display:flex; align-items:center; gap:10px;
  padding:10px 14px;
  background:var(--green-dim);
  border:1px solid rgba(76,175,114,0.2);
  border-radius:var(--radius);
  color:var(--green); font-family:var(--mono); font-size:14px;
  text-decoration:none; margin-bottom:6px;
  transition:background .14s, border-color .14s, transform .12s;
  word-break:break-all;
}
.read-link:hover {
  background:rgba(76,175,114,0.18);
  border-color:rgba(76,175,114,0.4);
  transform:translateX(3px);
}
.read-link-icon { font-size:16px; flex-shrink:0; }
.read-link-text { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.read-link-arrow { flex-shrink:0; opacity:.55; }

/* Meta */
.detail-meta {
  display:grid; grid-template-columns:auto 1fr;
  gap:7px 20px; margin-bottom:18px;
}
.meta-k { color:var(--text-dim); font-size:13px; white-space:nowrap; padding-top:1px; }
.meta-v { color:var(--text); font-size:14px; }
.meta-link { color:var(--accent); font-size:14px; word-break:break-all; }

/* Status badge */
.sbadge {
  display:inline-flex; align-items:center; gap:5px;
  padding:3px 10px 3px 7px; border-radius:999px; font-size:12px;
}
.sbadge.read    { background:rgba(76,175,114,0.1); color:var(--green); border:1px solid rgba(76,175,114,0.22); }
.sbadge.reading { background:rgba(91,155,213,0.1); color:var(--blue);  border:1px solid rgba(91,155,213,0.22); }
.sbadge.want    { background:rgba(212,168,83,0.1); color:var(--yellow);border:1px solid rgba(212,168,83,0.22); }
.sbadge::before { content:''; width:6px; height:6px; border-radius:50%; background:currentColor; flex-shrink:0; }

.dscore { font-size:13px; color:var(--text-dim); }

/* Genre tags */
.gtags { display:flex; flex-wrap:wrap; gap:5px; margin-bottom:18px; }
.gtag {
  background:var(--bg4); border:1px solid var(--border);
  border-radius:3px; padding:4px 9px;
  font-size:12px; color:var(--text-muted);
}

/* Description */
.detail-body {
  border-top:1px solid var(--border);
  padding-top:28px; margin-top:4px;
}
.detail-desc {
  font-size:16px; line-height:1.82; color:var(--text-muted);
  font-family:var(--serif); font-style:italic;
  white-space:pre-wrap;
}

/* Extra props */
.extra-props { border-top:1px solid var(--border); padding-top:22px; margin-top:28px; }
.props-table { width:100%; border-collapse:collapse; font-size:13px; }
.props-table td { padding:6px 0; border-bottom:1px solid var(--border); vertical-align:top; }
.props-table td:first-child { color:var(--text-dim); white-space:nowrap; padding-right:22px; width:1%; }
.props-table td:last-child { color:var(--text); word-break:break-word; }

/* Footer stamp */
.updated { position:fixed; bottom:14px; right:18px; font-size:11px; color:var(--text-dim); pointer-events:none; }

/* ── RESPONSIVE — TABLET ── */
@media (max-width:780px) {
  :root { --card-w:160px; --img-h:232px; }
  header { padding:16px 20px 0; }
  main { padding:22px 20px 80px; }
  #grid { gap:22px 14px; }
  .detail-content { padding:32px 22px 80px; }
  .detail-hero { grid-template-columns:180px 1fr; gap:28px; }
  .detail-cover { width:180px; height:262px; }
  .detail-title { font-size:24px; }
}

/* ── RESPONSIVE — MOBILE ── */
@media (max-width:520px) {
  :root { --card-w:145px; --img-h:210px; }
  header { padding:12px 14px 0; }
  h1 { font-size:21px; }
  main { padding:16px 14px 80px; }
  #grid { gap:18px 10px; }
  .search-wrap { min-width:100%; max-width:100%; }

  .detail-content { padding:18px 16px 80px; }
  .detail-nav { padding:10px 16px; }

  /* Stack hero on mobile */
  .detail-hero { grid-template-columns:1fr; gap:22px; }
  .detail-cover { width:170px; height:248px; margin:0 auto; }
  .detail-info { align-items:center; text-align:center; }
  .detail-title { font-size:22px; }
  .detail-authors { font-size:15px; }
  .reading-links { width:100%; }
  .reading-links-label, .section-label { text-align:left; width:100%; }
  .gtags { justify-content:center; }
  .detail-meta { justify-items:start; }
}
</style>
</head>
<body>

<header>
  <div class="header-top">
    <h1>{{SITE_TITLE}}</h1>
    <span class="count-badge" id="countBadge">— results</span>
  </div>
  <div class="toolbar">
    <div class="search-wrap">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input id="search" type="text" placeholder="Search…" autocomplete="off">
    </div>
    <div class="select-wrap">
      <select id="sortSelect">
        <option value="title">Sort: Title</option>
        <option value="author">Sort: Author</option>
        <option value="year-desc">Sort: Year ↓</option>
        <option value="year-asc">Sort: Year ↑</option>
        <option value="pages-desc">Sort: Pages ↓</option>
        <option value="scoreGr-desc">Sort: Rating ↓</option>
      </select>
    </div>
    <div class="select-wrap">
      <select id="statusFilter">
        <option value="">All Status</option>
        <option value="read">Read</option>
        <option value="want-to-read">Want to Read</option>
      </select>
    </div>
    <div class="select-wrap" id="genreWrap" style="display:none">
      <select id="genreFilter">
        <option value="">All Genres</option>
      </select>
    </div>
    <div class="divider"></div>
    <button class="btn btn-clear" id="clearBtn" style="display:none" onclick="clearFilters()">✕ Clear</button>
  </div>
</header>

<main>
  <div id="grid"></div>
  <div id="empty">
    <div class="big">📭</div>
    <p>No books match your filters.</p>
  </div>
</main>

<div class="updated" id="updated"></div>

<!-- FULL-SCREEN DETAIL -->
<div id="detail-overlay">
  <div class="detail-nav">
    <button class="back-btn" onclick="closeDetail()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M19 12H5"/><path d="m12 5-7 7 7 7"/></svg>
      Back
    </button>
    <div class="detail-nav-title" id="detailNavTitle"></div>
  </div>
  <div class="detail-content" id="detailContent"></div>
</div>

<script>
const BOOKS = {{BOOKS_JSON}};
const GENERATED = "{{GENERATED}}";

let state = { query:"", sort:"title", status:"", genre:"" };

function init() {
  document.getElementById('updated').textContent = 'Generated ' + GENERATED;

  const allGenres = [...new Set(BOOKS.flatMap(b => b.genre))].sort();
  if (allGenres.length) {
    const sel = document.getElementById('genreFilter');
    allGenres.forEach(g => { const o=document.createElement('option'); o.value=g; o.textContent=g; sel.appendChild(o); });
    document.getElementById('genreWrap').style.display = '';
  }

  document.getElementById('grid').addEventListener('click', e => { const card = e.target.closest('.card'); if (card) openDetail(card.dataset.id); });
  document.getElementById('search').addEventListener('input', e => { state.query=e.target.value; render(); });
  document.getElementById('sortSelect').addEventListener('change', e => { state.sort=e.target.value; render(); });
  document.getElementById('statusFilter').addEventListener('change', e => { state.status=e.target.value; render(); });
  document.getElementById('genreFilter').addEventListener('change', e => { state.genre=e.target.value; render(); });
  document.addEventListener('keydown', e => {
    if (e.key==='Escape') closeDetail();
    if (e.key==='/' && !document.getElementById('detail-overlay').classList.contains('open')) {
      e.preventDefault(); document.getElementById('search').focus();
    }
  });
  render();
}

function filtered() {
  const q = state.query.toLowerCase().trim();
  return BOOKS.filter(b => {
    if (q) {
      const tg = (b.telegram||[]).join(' ').toLowerCase();
      if (!(b.title.toLowerCase().includes(q) || b.authors.join(' ').toLowerCase().includes(q) ||
            b.description.toLowerCase().includes(q) || tg.includes(q))) return false;
    }
    if (state.status) {
      const s = (b.status||'').toLowerCase().replace(/[\s_]+/g,'-');
      if (s !== state.status.replace(/[\s_]+/g,'-')) return false;
    }
    if (state.genre && !b.genre.includes(state.genre)) return false;
    return true;
  }).sort((a,b) => {
    switch(state.sort) {
      case 'author':       return (a.authors[0]||'').localeCompare(b.authors[0]||'');
      case 'year-desc':    return (parseInt(b.year)||0)-(parseInt(a.year)||0);
      case 'year-asc':     return (parseInt(a.year)||0)-(parseInt(b.year)||0);
      case 'pages-desc':   return (parseInt(b.pages)||0)-(parseInt(a.pages)||0);
      case 'scoreGr-desc': return (parseFloat(b.scoreGr)||0)-(parseFloat(a.scoreGr)||0);
      default:             return a.title.localeCompare(b.title);
    }
  });
}

function render() {
  const books = filtered();
  const grid = document.getElementById('grid');
  const empty = document.getElementById('empty');
  document.getElementById('countBadge').textContent = books.length+(books.length===1?' result':' results');
  document.getElementById('clearBtn').style.display = (state.query||state.status||state.genre)?'':'none';
  if (!books.length) { grid.innerHTML=''; empty.style.display=''; return; }
  empty.style.display='none';
  grid.innerHTML = books.map((b,i) => cardHTML(b,i)).join('');
}

function coverInner(b) {
  if (b.cover) return `<img class="cover-img" src="${esc(b.cover)}" alt="${esc(b.title)}" loading="lazy"
      onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
    <div class="cover-placeholder" style="display:none"><span class="ph-icon">📖</span><span class="ph-title">${esc(b.title)}</span></div>`;
  return `<div class="cover-placeholder"><span class="ph-icon">📖</span><span class="ph-title">${esc(b.title)}</span></div>`;
}

function starsSmall(scoreGr, rating) {
  const n = parseFloat(scoreGr||rating);
  if (isNaN(n)) return '';
  return `<div class="rating-stars">${n} / 5</div>`;
}

function cardHTML(b, i) {
  const meta = [b.year, b.pages?b.pages+' pp':''].filter(Boolean).join(' · ');
  return `<div class="card" data-id="${esc(b.id)}" style="animation-delay:${Math.min(i*11,280)}ms">
    <div class="cover-wrap">
      ${coverInner(b)}
    </div>
    <div class="card-info">
      <div class="card-title">${esc(b.title)}</div>
      ${b.authors.length?`<div class="card-authors">${esc(b.authors.join(', '))}</div>`:''}
      ${meta?`<div class="card-meta">${esc(meta)}</div>`:''}
      ${starsSmall(b.scoreGr,b.rating)}
    </div>
  </div>`;
}

// ── DETAIL VIEW ──
function openDetail(id) {
  const b = BOOKS.find(x => x.id===id);
  if (!b) return;

  document.getElementById('detailNavTitle').textContent = b.title;

  // Reading links — most prominent
  const tgLinks = b.telegram||[];
  const linksHTML = tgLinks.length ? `
    <div class="reading-links">
      <div class="section-label">Read Online</div>
      ${tgLinks.map((url,i) => `
        <a class="read-link" href="${esc(url)}" target="_blank" rel="noopener noreferrer">
          <span class="read-link-icon">${linkIcon(url)}</span>
          <span class="read-link-text">${esc(linkLabel(url,i))}</span>
          <span class="read-link-arrow">↗</span>
        </a>`).join('')}
    </div>` : '';

  // Metadata
  const sc = (b.status||'').toLowerCase().replace(/[\s_]+/g,'-');
  let sClass = sc==='read'?'read':sc==='reading'?'reading':'want';
  const metaRows = [
    b.year    ? ['Year',      `<span class="meta-v">${esc(b.year)}</span>`]                           : null,
    b.pages   ? ['Pages',     `<span class="meta-v">${esc(b.pages)} pages</span>`]                    : null,
    b.status  ? ['Status',    `<span class="sbadge ${sClass}">${esc(b.status)}</span>`]               : null,
    b.scoreGr ? ['Goodreads', `<span class="dscore">${esc(b.scoreGr)} / 5</span>`] : null,
    b.rating  ? ['My rating', `<span class="dscore">${esc(b.rating)} / 5</span>`]       : null,
    b.urlGr   ? ['Goodreads', `<a class="meta-link" href="${esc(b.urlGr)}" target="_blank" rel="noopener">${esc(b.urlGr)}</a>`] : null,
  ].filter(Boolean);

  const metaHTML = metaRows.length ? `
    <div class="detail-meta">
      ${metaRows.map(([k,v]) => `<span class="meta-k">${esc(k)}</span><span class="meta-v">${v}</span>`).join('')}
    </div>` : '';

  const genreHTML = b.genre&&b.genre.length ? `
    <div class="gtags">${b.genre.map(g=>`<span class="gtag">${esc(g)}</span>`).join('')}</div>` : '';

  const descHTML = b.description ? `
    <div class="detail-body">
      <div class="section-label">Notes</div>
      <div class="detail-desc">${esc(b.description)}</div>
    </div>` : '';

  // Extra unknown properties
  const knownKeys = new Set(['id','title','authors','genre','pages','year','scoreGr','rating','cover','status','description','telegram','urlGr']);
  const extras = Object.entries(b).filter(([k]) => !knownKeys.has(k) && b[k]!=null && b[k]!=='' && !(Array.isArray(b[k])&&!b[k].length));
  const extraHTML = extras.length ? `
    <div class="extra-props">
      <div class="section-label">All Properties</div>
      <table class="props-table">
        ${extras.map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(Array.isArray(v)?v.join(', '):String(v))}</td></tr>`).join('')}
      </table>
    </div>` : '';

  document.getElementById('detailContent').innerHTML = `
    <div class="detail-hero">
      <div class="detail-cover">${coverInner(b)}</div>
      <div class="detail-info">
        <div class="detail-title">${esc(b.title)}</div>
        ${b.authors.length?`<div class="detail-authors">${esc(b.authors.join(', '))}</div>`:''}
        ${linksHTML}
        ${metaHTML}
        ${genreHTML}
      </div>
    </div>
    ${descHTML}
    ${extraHTML}`;

  const overlay = document.getElementById('detail-overlay');
  overlay.scrollTop = 0;
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeDetail() {
  document.getElementById('detail-overlay').classList.remove('open');
  document.body.style.overflow = '';
}

function linkIcon(url) {
  if (/t\.me|telegram/i.test(url))   return '✈️';
  if (/drive\.google/i.test(url))    return '☁️';
  if (/dropbox/i.test(url))          return '📦';
  if (/archive\.org/i.test(url))     return '🏛️';
  if (/libgen|library/i.test(url))   return '📚';
  if (/epub|pdf|mobi/i.test(url))    return '📄';
  return '🔗';
}

function linkLabel(url, i) {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^www\./,'');
    const path = u.pathname.slice(0,42)+(u.pathname.length>42?'…':'');
    return host + path;
  } catch { return 'Link '+(i+1); }
}

function clearFilters() {
  state={...state,query:'',status:'',genre:''};
  document.getElementById('search').value='';
  document.getElementById('statusFilter').value='';
  document.getElementById('genreFilter').value='';
  render();
}

function esc(s) {
  return String(s==null?'':s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

init();
</script>
</body>
</html>"""
