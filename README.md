# BookLib

Static site generator for an Obsidian-based digital bookshelf. Turns markdown notes with `categories: [[Books]]` into a searchable, filterable card-grid website.

## What it does

- Scans your Obsidian vault for book notes
- Parses YAML frontmatter (title, author, genre, pages, year, scoreGr, cover, read status)
- Strips wikilinks (`[[Author Name]]` → `Author Name`)
- Maps `read: "true"` → **Read**, `read: "false"` → **Want to Read**
- Generates a single `index.html` with all data embedded as JSON
- Serves it via Caddy on Termux

## Files

| File | Purpose |
|------|---------|
| `generate.py` | Main generator script (Python 3 + PyYAML) |
| `update.sh` | Termux wrapper: `git pull` → regenerate site |
| `Caddyfile` | Caddy config for serving `~/obsidian/BookLib/site` |

## Termux Setup

### 1. Clone this repo

```bash
cd ~/obsidian/BookLib
git clone <repo-url> BookLib
```

Result: `~/obsidian/BookLib/BookLib/` contains `.git/`, `generate.py`, `update.sh`, etc.

### 2. Install dependencies

```bash
pkg install python-pip
pip install pyyaml
```

### 3. Configure Caddy

```bash
pkg install caddy
cp ~/obsidian/BookLib/BookLib/Caddyfile ~/.config/caddy/Caddyfile
caddy start
```

Site will be available at `http://<tailscale-ip>:9090`

### 4. Run manually

```bash
~/obsidian/BookLib/BookLib/update.sh
```

### 5. Automate with Tasker / Termux:Tasker

Create a Tasker task that runs the shell command:

```bash
/data/data/com.termux/files/home/obsidian/BookLib/BookLib/update.sh
```

Trigger on a schedule (e.g., every 30 minutes) or on-demand.

## Desktop Usage (testing)

```bash
python3 generate.py --vault /home/malik/Documents/obsidian --output /tmp/bookshelf/index.html
```

## Frontmatter Fields Used

| Field | Type | Used for |
|-------|------|----------|
| `categories` | list | Must contain `Books` |
| `title` | string | Book title |
| `author` | list | Authors |
| `genre` | list | Genre filter & tags |
| `pages` | int | Display & sort |
| `year` | int | Display & sort |
| `scoreGr` | float | Goodreads rating (stars + modal) |
| `cover` | string | Cover image URL |
| `read` | string | `"true"` = Read, `"false"` = Want to Read |

All other fields are ignored.

## How it works

1. `update.sh` pulls the latest vault from GitHub
2. `generate.py` walks all `.md` files, parses frontmatter with PyYAML
3. Filters for notes where `categories` includes `Books`
4. Strips wikilinks recursively from all values
5. Injects the book array into a self-contained HTML template
6. Caddy serves the static `index.html` from `~/obsidian/BookLib/site/`
