# S-BaXIT lab website

This repository contains the S-BaXIT website maintained by the OptImaTo group. Most updates only require editing Markdown files. Website content is in English.

## How the website works

**Zensical** is the program that turns our Markdown files into a website, adding navigation, search, styling and a blog. You do not need to learn Zensical to update the text.

1. Edit the source files in this repository.
2. Preview the result on your computer.
3. Publish through the manual GitHub Actions workflow when the changes are ready.

Saving or pushing changes does **not** automatically publish them. The generated HTML is written to `site/`. Never edit that folder directly: it is rebuilt from the sources.

## Where to make changes

| Content | Source |
| --- | --- |
| Homepage and featured news | [docs/index.md](docs/index.md) |
| Research | [docs/research.md](docs/research.md) |
| Team biographies and portraits | [docs/our-team.md](docs/our-team.md) |
| Publications | [docs/publications.md](docs/publications.md) |
| Addresses and contacts | [docs/contacts.md](docs/contacts.md) |
| Job announcements | [docs/jobs.md](docs/jobs.md) |
| News articles | [docs/news/posts/](docs/news/posts/) |
| Blog title and introduction | [docs/news/index.md](docs/news/index.md) |
| Images, videos and PDFs | [docs/assets/](docs/assets/) |
| Menu, site name, logo and blog settings | [zensical.toml](zensical.toml) |
| Colours, spacing and portrait styles | [docs/stylesheets/extra.css](docs/stylesheets/extra.css) |
| Shared funding acknowledgement and footer | [overrides/main.html](overrides/main.html) |

## Edit an existing page

Edit its `.md` file and preview the result. Keep one `#` title per page and use `##` and `###` for sections: Zensical uses these headings to create the table of contents. Preserve scientific references, photographic credits and the ERC funding acknowledgement.

Some pages include small HTML blocks or attributes such as `{ .portrait }`. These control layout; leave them in place when only updating text.

Link to pages through their Markdown paths, relative to the file you are editing. From a page directly inside `docs/`:

```markdown
[Our research](research.md)
[Latest news](news/index.md)
```

Zensical converts these to website URLs. Avoid renaming published files unless you update their incoming links: filenames normally determine public URLs.

## Add a normal page

1. Create a file such as `docs/facilities.md` with a title and content.
2. To include it in the main menu, add an entry inside the existing `nav = [...]` list in `zensical.toml`:

   ```toml
   { "Facilities" = "facilities.md" },
   ```

3. Link to it from relevant pages and preview the website.

Menu paths are relative to `docs/`, and their order in `nav` determines the menu order. A page can be linked from another page without having a menu entry.

Removing a menu entry does not hide the page from the website or search. To omit a page entirely, add its path to `exclude_docs`, preserving existing exclusions. Fabio’s personal page is currently excluded this way; its source remains available.

## Add a news article

Create `docs/news/posts/new-experiment.md`:

```markdown
---
date: 2026-10-14
slug: new-experiment
---

# A new experiment at the lab

A short introduction displayed in the news listing.

<!-- more -->

The full article goes here.

![Experimental setup](../../assets/news/new-experiment.jpg)
```

The block between `---` lines is **metadata**, used to organise the article:

- `date`: publication date in YYYY-MM-DD format; replace the example date.
- `slug`: unique final part of the URL, here `/news/new-experiment/`. Use lowercase words separated by hyphens and keep it unchanged after publication.
- `<!-- more -->`: separates the preview text from the full article.
- Optional `draft: true`: includes the article in local preview but excludes it from publication. Remove it when ready.
- Optional `categories`: a YAML list of categories. Reuse existing category names consistently.

**Do not add individual posts to the menu or manually list them in `docs/news/index.md`.** The blog creates the chronological list, annual archives and pagination automatically, with six posts per page.

The featured news items on the homepage are **manually curated** in `docs/index.md`; they do not change automatically when a post is added.

From a post, use these relative paths:

```markdown
[Research](../../research.md)
[Another article](new-umpa-published.md)
[All news](../index.md)
```

From the homepage, link to `news/posts/new-experiment.md`.

In the current Zensical version, some post-to-post links are rewritten incorrectly inside previews. Put those links after `<!-- more -->`, or use the published root-relative URL before it, such as `/news/new-experiment/`. The link checker also checks the generated archives.

## Images and other media

Media are stored locally in this repository, not loaded from the old website. Choose the relevant folder under `docs/assets/`:

| Folder | Contents |
| --- | --- |
| `people/` | Portraits and placeholder image |
| `research/` | Scientific figures and imaging examples |
| `news/` | Event photos and article illustrations |
| `logos/` | Project, institution and software logos |
| `videos/` | Scientific animations |
| `documents/` | Downloadable PDFs |
| `backgrounds/` | Decorative backgrounds |

Use descriptive filenames, preferably lowercase with hyphens. Resize unnecessarily large photographs before adding them, provide meaningful image descriptions, and retain credits where required.

On the team page:

```markdown
![Giovanni Lemma](assets/people/giovanni-lemma.png){ .portrait .grayscale }
```

`.portrait` sets size and placement. `.grayscale` displays the photo in black and white without changing its original file; omit that class for colour.

The browser icon is `docs/assets/favicon.svg`. It embeds its own copy of the logo, so changing the header logo does not automatically change the favicon.

## Local preview

Install **Python 3.11 or later**. Open a terminal in the repository root (the folder containing `zensical.toml`).

### First-time setup

Create a project-local Python environment and install the pinned dependencies. This keeps the website tools separate from other Python projects.

**Windows — PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS / Linux:**

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Start the preview

**Windows:**

```powershell
.\.venv\Scripts\zensical.exe serve
```

**macOS / Linux:**

```sh
.venv/bin/zensical serve
```

Open the address printed in the terminal, normally http://127.0.0.1:8000/. Keep the terminal running: saving a source file rebuilds the preview. Stop it with **Ctrl+C**. This preview stays on your computer and does not publish anything.

## Check and share changes

Review affected pages, images and links, including at a narrow browser width. Stop the preview before running the final build and link check.

**Windows:**

```powershell
.\.venv\Scripts\zensical.exe build --clean
.\.venv\Scripts\python.exe scripts/validate_site.py
```

**macOS / Linux:**

```sh
.venv/bin/zensical build --clean
.venv/bin/python scripts/validate_site.py
```

The checker verifies local links, media and anchors in the generated HTML. It does not check external websites or scientific accuracy. Draft posts are excluded from the production build; avoid linking to them from published pages.

Commit changed sources and new media, push your branch and open a pull request for review. Small text edits can also be made through GitHub’s file editor; local preview is recommended for layout and media changes.

## Publishing — manual workflow

The [Documentation workflow](.github/workflows/docs.yml) runs **only when manually requested**, never automatically on push or pull request. Running it builds, validates and deploys the selected branch to GitHub Pages; it is not just a preview check.

Once Pages is configured, a maintainer with repository access can publish through **Actions → Documentation → Run workflow**, selecting the branch to publish. The workflow must exist on the default branch for the manual trigger to appear. Follow the run to completion; the deployment job provides the published URL.

Before the first publication, configure GitHub Pages to use GitHub Actions and set `site_url` in `zensical.toml` to the public website URL. It currently points to localhost. A custom domain also needs GitHub Pages and DNS configuration; changing page content does not configure it.

## Supporting and generated files

- `requirements.txt`: pinned Zensical version; change only for an intentional tooling upgrade.
- `scripts/validate_site.py`: standalone link checker.
- `.github/workflows/docs.yml`: manual publication workflow.
- `.venv/`, `site/` and `.cache/`: generated locally and ignored by Git.
- Old migration snapshots, import scripts, reports and QA screenshots may exist locally, but are ignored and are not needed to maintain the website.
- `.git/`: internal Git data; leave it alone.

If changes do not appear, check that you edited a source file in `docs/`, saved it, and still have the preview running. For a cached favicon, close and reopen the browser tab. For missing pages or images, check relative paths and filename capitalisation: the GitHub build environment is case-sensitive.
