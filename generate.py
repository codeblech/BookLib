#!/usr/bin/env python3
"""Generate a static bookshelf website from Obsidian vault notes."""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import yaml


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{SITE_TITLE}}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:         #141414;
  --bg2:        #1c1c1c;
  --bg3:        #242424;
  --bg4:        #2c2c2c;
  --border:     #333;
  --border2:    #444;
  --text:       #d4d4d4;
  --text-muted: #777;
  --text-dim:   #555;
  --accent:     #e8613a;
  --accent2:    #c94f2a;
  --green:      #4caf72;
  --blue:       #5b9bd5;
  --yellow:     #d4a853;
  --card-w:     160px;
  --img-h:      230px;
  --radius:     4px;
  --mono:       'DM Mono', monospace;
  --serif:      'Libre Baskerville', Georgia, serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--mono);
  font-size: 13px;
  min-height: 100vh;
  line-height: 1.5;
}

/* ── HEADER ── */
header {
  padding: 28px 32px 0;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.header-top {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 16px;
}

h1 {
  font-family: var(--serif);
  font-size: 26px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: -0.5px;
}

.count-badge {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 2px 10px;
  letter-spacing: 0.3px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 12px;
  flex-wrap: wrap;
}

/* ── CONTROLS ── */
.search-wrap {
  position: relative;
  flex: 1;
  min-width: 180px;
  max-width: 320px;
}

.search-wrap svg {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

#search {
  width: 100%;
  padding: 7px 10px 7px 32px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: var(--mono);
  font-size: 12px;
  outline: none;
  transition: border-color .15s;
}
#search:focus { border-color: var(--border2); }
#search::placeholder { color: var(--text-dim); }

select, .btn {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: var(--mono);
  font-size: 12px;
  padding: 7px 10px;
  cursor: pointer;
  outline: none;
  transition: border-color .15s, background .15s;
  appearance: none;
  -webkit-appearance: none;
}
select:focus, .btn:hover { border-color: var(--border2); background: var(--bg4); }

.select-wrap {
  position: relative;
}
.select-wrap::after {
  content: '▾';
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
  font-size: 10px;
}
.select-wrap select {
  padding-right: 24px;
}

.divider { width: 1px; height: 20px; background: var(--border); margin: 0 2px; }

.btn.active { border-color: var(--accent); color: var(--accent); }

/* ── MAIN ── */
main { padding: 24px 32px; }

/* ── GRID ── */
#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, var(--card-w));
  gap: 24px 18px;
}

/* ── CARD ── */
.card {
  width: var(--card-w);
  cursor: pointer;
  transition: transform .15s;
  animation: fadeIn .2s ease both;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; } }

.card:hover { transform: translateY(-2px); }
.card:hover .cover-img { box-shadow: 0 12px 32px rgba(0,0,0,.6); }

.cover-wrap {
  width: var(--card-w);
  height: var(--img-h);
  border-radius: 3px;
  overflow: hidden;
  background: var(--bg3);
  border: 1px solid var(--border);
  position: relative;
  margin-bottom: 9px;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: box-shadow .15s;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
  text-align: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--bg3) 0%, var(--bg4) 100%);
}

.cover-placeholder .ph-title {
  font-family: var(--serif);
  font-size: 12px;
  color: var(--text);
  line-height: 1.4;
  font-style: italic;
}

.cover-placeholder .ph-icon {
  font-size: 24px;
  opacity: .4;
}

.status-dot {
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1.5px solid var(--bg);
}
.status-dot.read     { background: var(--green); }
.status-dot.reading  { background: var(--blue); }
.status-dot.want     { background: var(--yellow); }

.card-info { padding: 0 1px; }

.card-title {
  font-family: var(--serif);
  font-size: 12px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.35;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-authors {
  color: var(--accent);
  font-size: 11px;
  margin-bottom: 5px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 8px;
  color: var(--text-muted);
  font-size: 11px;
}

.rating-stars {
  color: var(--yellow);
  font-size: 10px;
  margin-top: 3px;
  letter-spacing: 1px;
}

/* ── EMPTY STATE ── */
#empty {
  display: none;
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}
#empty .big { font-size: 36px; margin-bottom: 12px; }
#empty p { font-size: 13px; }

/* ── MODAL ── */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.75);
  z-index: 200;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(4px);
}
.modal-overlay.open { display: flex; }

.modal {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 8px;
  max-width: 640px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  animation: modalIn .18s ease;
}
@keyframes modalIn { from { opacity:0; transform: scale(.97); } to { opacity:1; transform:scale(1); } }

.modal-inner {
  display: flex;
  gap: 24px;
  padding: 28px;
}

.modal-cover {
  flex-shrink: 0;
  width: 120px;
  height: 175px;
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg3);
}
.modal-cover img { width: 100%; height: 100%; object-fit: cover; }
.modal-cover .cover-placeholder { height: 100%; }

.modal-body { flex: 1; min-width: 0; }

.modal-title {
  font-family: var(--serif);
  font-size: 18px;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 6px;
  color: var(--text);
}

.modal-authors {
  color: var(--accent);
  font-size: 13px;
  margin-bottom: 16px;
}

.modal-meta-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 5px 14px;
  margin-bottom: 16px;
  font-size: 12px;
}
.meta-label { color: var(--text-muted); }
.meta-value { color: var(--text); }

.modal-desc {
  font-size: 12.5px;
  color: var(--text-muted);
  line-height: 1.7;
  border-top: 1px solid var(--border);
  padding-top: 14px;
  margin-top: 14px;
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--radius);
  transition: color .1s;
}
.modal-close:hover { color: var(--text); }

.tag-list { display: flex; flex-wrap: wrap; gap: 5px; }
.tag {
  background: var(--bg4);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 2px 7px;
  font-size: 10.5px;
  color: var(--text-muted);
}

/* ── UPDATED ── */
.updated {
  position: fixed;
  bottom: 16px;
  right: 20px;
  font-size: 10px;
  color: var(--text-dim);
  font-family: var(--mono);
}

/* ── RESPONSIVE ── */
@media (max-width: 600px) {
  header { padding: 16px 16px 0; }
  main   { padding: 16px; }
  #grid  { gap: 18px 12px; }
  .modal-inner { flex-direction: column; }
  .modal-cover { width: 100%; height: 180px; }
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
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input id="search" type="text" placeholder="Search…" autocomplete="off">
    </div>

    <div class="select-wrap">
      <select id="sortSelect">
        <option value="title">Sort: Title</option>
        <option value="author">Sort: Author</option>
        <option value="year-desc">Sort: Year ↓</option>
        <option value="year-asc">Sort: Year ↑</option>
        <option value="pages-desc">Sort: Pages ↓</option>
        <option value="scoreGr-desc">Sort: Goodreads ↓</option>
      </select>
    </div>

    <div class="select-wrap" id="statusWrap">
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

    <button class="btn" id="clearBtn" style="display:none" onclick="clearFilters()">✕ Clear</button>
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

<!-- Modal -->
<div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
  <div class="modal" style="position:relative">
    <button class="modal-close" onclick="closeModalDirect()">✕</button>
    <div class="modal-inner" id="modalInner"></div>
  </div>
</div>

<script>
const BOOKS = {{BOOKS_JSON}};
const GENERATED = "{{GENERATED}}";

// ── State ──
let state = {
  query: "",
  sort: "title",
  status: "",
  genre: "",
};

// ── Boot ──
function init() {
  document.getElementById('updated').textContent = 'Generated ' + GENERATED;

  // Populate genre dropdown
  const allGenres = [...new Set(BOOKS.flatMap(b => b.genre))].sort();
  if (allGenres.length) {
    const sel = document.getElementById('genreFilter');
    allGenres.forEach(g => { const o = document.createElement('option'); o.value = g; o.textContent = g; sel.appendChild(o); });
    document.getElementById('genreWrap').style.display = '';
  }

  // Events
  document.getElementById('search').addEventListener('input', e => { state.query = e.target.value; render(); });
  document.getElementById('sortSelect').addEventListener('change', e => { state.sort = e.target.value; render(); });
  document.getElementById('statusFilter').addEventListener('change', e => { state.status = e.target.value; render(); });
  document.getElementById('genreFilter').addEventListener('change', e => { state.genre = e.target.value; render(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalDirect(); if (e.key === '/' && !document.getElementById('modalOverlay').classList.contains('open')) { e.preventDefault(); document.getElementById('search').focus(); } });

  render();
}

// ── Filter + Sort ──
function filtered() {
  const q = state.query.toLowerCase().trim();
  return BOOKS.filter(b => {
    if (q && !( b.title.toLowerCase().includes(q) || b.authors.join(' ').toLowerCase().includes(q) || b.description.toLowerCase().includes(q) )) return false;
    if (state.status) {
      const s = (b.status || '').toLowerCase().replace(/[\s_]+/g, '-');
      if (s !== state.status.replace(/[\s_]+/g, '-')) return false;
    }
    if (state.genre && !b.genre.includes(state.genre)) return false;
    return true;
  }).sort((a, b) => {
    switch (state.sort) {
      case 'author':    return (a.authors[0]||'').localeCompare(b.authors[0]||'');
      case 'year-desc': return (parseInt(b.year)||0) - (parseInt(a.year)||0);
      case 'year-asc':  return (parseInt(a.year)||0) - (parseInt(b.year)||0);
      case 'pages-desc':return (parseInt(b.pages)||0) - (parseInt(a.pages)||0);
      case 'scoreGr-desc':return (parseFloat(b.scoreGr)||0) - (parseFloat(a.scoreGr)||0);
      default:          return a.title.localeCompare(b.title);
    }
  });
}

// ── Render ──
function render() {
  const books = filtered();
  const grid  = document.getElementById('grid');
  const empty = document.getElementById('empty');
  const badge = document.getElementById('countBadge');
  const clearBtn = document.getElementById('clearBtn');

  const hasFilter = state.query || state.status || state.genre;
  clearBtn.style.display = hasFilter ? '' : 'none';

  badge.textContent = books.length + (books.length === 1 ? ' result' : ' results');

  if (books.length === 0) {
    grid.innerHTML = '';
    empty.style.display = '';
    return;
  }
  empty.style.display = 'none';

  grid.innerHTML = books.map((b, i) => cardHTML(b, i)).join('');
}

function coverHTML(b, size = 'full') {
  if (b.cover) {
    return `<img class="cover-img" src="${escHtml(b.cover)}" alt="${escHtml(b.title)}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
            <div class="cover-placeholder" style="display:none"><span class="ph-icon">📖</span><span class="ph-title">${escHtml(b.title)}</span></div>`;
  }
  return `<div class="cover-placeholder"><span class="ph-icon">📖</span><span class="ph-title">${escHtml(b.title)}</span></div>`;
}

function statusDot(status) {
  if (!status) return '';
  const s = status.toLowerCase().replace(/[\s_]+/g, '-');
  if (s.includes('read') && !s.includes('want') && !s.includes('reading')) return '<span class="status-dot read" title="Read"></span>';
  if (s.includes('reading')) return '<span class="status-dot reading" title="Currently Reading"></span>';
  if (s.includes('want')) return '<span class="status-dot want" title="Want to Read"></span>';
  return '';
}

function stars(scoreGr, rating) {
  const n = parseFloat(scoreGr || rating);
  if (isNaN(n)) return '';
  const full = Math.floor(n), half = n % 1 >= 0.5;
  return '<div class="rating-stars" title="Goodreads ' + n + '">' + '★'.repeat(full) + (half ? '½' : '') + '</div>';
}

function cardHTML(b, i) {
  const meta = [b.year, b.pages ? b.pages + ' pp' : ''].filter(Boolean).join(' · ');
  return `<div class="card" onclick="openModal(${JSON.stringify(b.id)})" style="animation-delay:${Math.min(i*15,300)}ms">
    <div class="cover-wrap">
      ${coverHTML(b)}
      ${statusDot(b.status)}
    </div>
    <div class="card-info">
      <div class="card-title">${escHtml(b.title)}</div>
      ${b.authors.length ? `<div class="card-authors">${escHtml(b.authors.join(', '))}</div>` : ''}
      ${meta ? `<div class="card-meta">${escHtml(meta)}</div>` : ''}
      ${stars(b.scoreGr, b.rating)}
    </div>
  </div>`;
}

// ── Modal ──
function openModal(id) {
  const b = BOOKS.find(x => x.id === id);
  if (!b) return;
  const meta = [
    b.year  ? ['Year', b.year] : null,
    b.pages ? ['Pages', b.pages] : null,
    b.status ? ['Status', b.status] : null,
    b.scoreGr ? ['Goodreads', b.scoreGr + ' / 5'] : null,
  ].filter(Boolean);

  document.getElementById('modalInner').innerHTML = `
    <div class="modal-cover">${coverHTML(b)}</div>
    <div class="modal-body">
      <div class="modal-title">${escHtml(b.title)}</div>
      ${b.authors.length ? `<div class="modal-authors">${escHtml(b.authors.join(', '))}</div>` : ''}
      ${meta.length ? `<div class="modal-meta-grid">${meta.map(([l,v]) => `<span class="meta-label">${escHtml(l)}</span><span class="meta-value">${escHtml(v)}</span>`).join('')}</div>` : ''}
      ${b.genre.length ? `<div class="tag-list" style="margin-bottom:10px">${b.genre.map(t=>`<span class="tag">${escHtml(t)}</span>`).join('')}</div>` : ''}
      ${b.description ? `<div class="modal-desc">${escHtml(b.description)}</div>` : ''}
    </div>`;
  document.getElementById('modalOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(e) {
  if (e.target === document.getElementById('modalOverlay')) closeModalDirect();
}
function closeModalDirect() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

function clearFilters() {
  state = {...state, query: '', status: '', genre: ''};
  document.getElementById('search').value = '';
  document.getElementById('statusFilter').value = '';
  document.getElementById('genreFilter').value = '';
  render();
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

init();
</script>
</body>
</html>"""

WIKILINK_RE = re.compile(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]')


def strip_wikilinks(value):
    """Recursively strip [[...]] wikilinks from strings/lists/dicts."""
    if isinstance(value, str):
        return WIKILINK_RE.sub(r'\1', value).strip()
    elif isinstance(value, list):
        return [strip_wikilinks(item) for item in value]
    elif isinstance(value, dict):
        return {k: strip_wikilinks(v) for k, v in value.items()}
    return value


def parse_book_file(filepath: Path) -> dict | None:
    """Parse a single markdown file and return a book dict, or None if not a book."""
    content = filepath.read_text(encoding='utf-8')

    if not content.startswith('---'):
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    if not isinstance(frontmatter, dict):
        return None

    # Strip wikilinks from all frontmatter values
    frontmatter = strip_wikilinks(frontmatter)

    # Check if this note belongs to the Books category
    categories = frontmatter.get('categories', [])
    if isinstance(categories, str):
        categories = [categories]
    if not isinstance(categories, list):
        return None

    if 'Books' not in categories:
        return None

    # Extract description (body content after frontmatter)
    body = parts[2].strip()

    # Map reading status
    read_val = str(frontmatter.get('read', '')).lower()
    if read_val == 'true':
        status = 'Read'
    else:
        status = 'Want to Read'

    # Build book object
    book = {
        'id': filepath.stem,
        'title': frontmatter.get('title') or filepath.stem,
        'authors': frontmatter.get('author', []) or [],
        'genre': frontmatter.get('genre', []) or [],
        'pages': frontmatter.get('pages'),
        'year': frontmatter.get('year'),
        'scoreGr': frontmatter.get('scoreGr'),
        'rating': frontmatter.get('rating'),
        'cover': frontmatter.get('cover', ''),
        'status': status,
        'description': body,
    }

    # Ensure list fields are actually lists
    for list_field in ('authors', 'genre'):
        val = book[list_field]
        if isinstance(val, str):
            book[list_field] = [val] if val else []
        elif not isinstance(val, list):
            book[list_field] = []

    # Clean numeric fields
    for num_field in ('pages', 'year'):
        try:
            book[num_field] = int(book[num_field]) if book[num_field] is not None else None
        except (ValueError, TypeError):
            book[num_field] = None

    # Ensure scoreGr is float or None
    try:
        book['scoreGr'] = float(book['scoreGr']) if book['scoreGr'] is not None else None
    except (ValueError, TypeError):
        book['scoreGr'] = None

    return book


def generate(vault_path: str, output_path: str, site_title: str = 'Bookshelf') -> None:
    """Generate the static site."""
    vault = Path(vault_path)
    books = []

    for md_file in vault.rglob('*.md'):
        book = parse_book_file(md_file)
        if book:
            books.append(book)

    # Default sort by title
    books.sort(key=lambda b: b['title'].lower())

    books_json = json.dumps(books, ensure_ascii=False)
    generated = datetime.now().strftime('%Y-%m-%d %H:%M')

    html = (HTML_TEMPLATE
            .replace('{{BOOKS_JSON}}', books_json)
            .replace('{{GENERATED}}', generated)
            .replace('{{SITE_TITLE}}', site_title))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding='utf-8')
    print(f'Generated {output} with {len(books)} books')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate bookshelf static site from Obsidian vault')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--output', required=True, help='Path to output index.html')
    parser.add_argument('--title', default='Bookshelf', help='Site title')
    args = parser.parse_args()
    generate(args.vault, args.output, args.title)


if __name__ == '__main__':
    main()
