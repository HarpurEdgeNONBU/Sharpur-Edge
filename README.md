# Sharpur Edge Magazine Archive

This project is the static website for the Sharpur Edge magazine archive. It has:

- `index.html`: the archive/library page where visitors browse all issues.
- `reader.html`: the flipbook reader for one issue.
- `Admin Library.bat`: double-click launcher for the admin app (Windows).
- `library/pdfs/`: the original PDF files.
- `library/pages/`: generated WebP page images used by the flipbook.
- `library/covers/`: generated WebP cover images used on the archive page.
- `library/magazines.json`: the list of issues shown on the site.
- `library/page-text/{issue-id}.json`: page-by-page readable text and captions for the reader side panel and text-to-speech.

The website is static, which means there is no server database. Updating the archive mostly means adding files, editing JSON, testing locally, and pushing to GitHub.

## The Big Picture

When you add a new PDF, the PDF itself is not what the flipbook displays. The script converts the PDF into browser-friendly WebP images:

```text
library/pdfs/my-issue.pdf
library/pages/my-issue/page-1.webp
library/pages/my-issue/page-2.webp
library/covers/my-issue.webp
library/page-text/my-issue.json
```

Then you add one entry to `library/magazines.json` so the archive knows the issue exists.

## First-Time Setup

### 1. Install VS Code

Download and install Visual Studio Code:

```text
https://code.visualstudio.com/
```

### 2. Install Python

Download and install Python:

```text
https://www.python.org/downloads/
```

During installation on Windows, check the box that says `Add python.exe to PATH`.

To confirm Python works, open a terminal and run:

```bash
python --version
```

If that does not work, try:

```bash
py --version
```

### 3. Install Git

Download and install Git:

```text
https://git-scm.com/downloads
```

To confirm Git works:

```bash
git --version
```

### 4. Install Script Dependencies

The PDF conversion script needs two Python packages:

```bash
pip install PyMuPDF Pillow
```

If `pip` does not work, try:

```bash
python -m pip install PyMuPDF Pillow
```

## Opening The Project In VS Code

1. Open VS Code.
2. Click `File` > `Open Folder...`.
3. Select the `magazine-archive` folder.
4. Click `Select Folder`.

You should see files like `index.html`, `reader.html`, `README.md`, and folders like `library`, `manager`, and `scripts`.

## Opening A Terminal In VS Code

Most maintenance work happens in the terminal.

In VS Code:

1. Click `Terminal` in the top menu.
2. Click `New Terminal`.
3. A terminal panel opens at the bottom of the window.

Make sure the terminal is in the project root. You should be able to run:

```bash
dir
```

On Windows, or:

```bash
ls
```

On Mac/Linux.

You should see `index.html`, `reader.html`, `library`, and `scripts`.

If you are in the wrong folder, move into the project folder:

```bash
cd path/to/magazine-archive
```

## Basic Computer And Terminal Syntax

This section explains the notation used in this guide. If you are not used to code projects, this is the part that makes the rest less mysterious.

### Files And Folders

A folder is a container that holds files or other folders. A file is one specific item, such as a PDF, image, HTML file, or JSON file.

Example:

```text
library/pdfs/mentor-magic-fall-2026.pdf
```

This means:

- Open the `library` folder.
- Inside it, open the `pdfs` folder.
- Inside `pdfs`, find the file named `mentor-magic-fall-2026.pdf`.

The slash `/` means "inside this folder." So this:

```text
library/page-text/mentor-magic-fall-2026.json
```

Means:

- Open the `library` folder.
- Inside `library`, open the `page-text` folder.
- Inside `page-text`, find `mentor-magic-fall-2026.json`.

On Windows, File Explorer may show paths with backslashes like this:

```text
library\page-text\mentor-magic-fall-2026.json
```

That is the same idea. In this project's code and JSON files, use forward slashes `/`.

### The Project Root

The "project root" means the main `magazine-archive` folder. It is the folder that directly contains:

```text
index.html
reader.html
README.md
Admin Library.bat
library/
manager/
scripts/
```

When this guide says "run this from the project root," your terminal should already be inside the `magazine-archive` folder.

To check where your terminal is, run:

```bash
pwd
```

On Windows PowerShell, this also works:

```bash
Get-Location
```

To list what is inside the current folder, run:

```bash
dir
```

If you see `index.html`, `reader.html`, `library`, and `scripts`, you are in the right place.

### Commands

A command is something you type into the terminal and run by pressing Enter.

Example:

```bash
python -m http.server 8000
```

Do not paste the surrounding triple backticks. Only paste the command text inside the box.

When a command contains a filename, replace the example filename with your real filename.

Example command from this guide:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf
```

If your PDF is named `dream-big-spring-2027.pdf`, use:

```bash
python scripts/generate-webp.py library/pdfs/dream-big-spring-2027.pdf
```

### Placeholders

Sometimes this guide uses placeholder names to mean "put your real value here."

If you see something like `XXX`, `your-file-name`, `path/to/...`, or `{issue-id}`, that is usually not something to type literally. It is a stand-in for the real folder name, file name, or issue ID you are working with.

For example:

```text
{issue-id}
```

Means the ID for a real issue, such as:

```text
mentor-magic-fall-2026
```

So this placeholder path:

```text
library/page-text/{issue-id}.json
```

Would become:

```text
library/page-text/mentor-magic-fall-2026.json
```

Another example:

```bash
cd path/to/magazine-archive
```

Means "replace `path/to/magazine-archive` with wherever the folder actually is on your computer." On Windows, that might look like:

```bash
cd C:\Users\YourName\Documents\magazine-archive
```

If a path contains spaces, put quotes around it:

```bash
cd "C:\Users\YourName\Documents\Magazine Archive"
```

### Common File Types In This Project

| Ending | What it is |
| --- | --- |
| `.pdf` | The original magazine PDF. |
| `.webp` | A web image generated from the PDF. |
| `.json` | Structured data that tells the site what magazines and page text exist. |
| `.html` | A website page. |
| `.css` | Website styling. |
| `.py` | A Python script. |

### Editing Versus Running

Some instructions ask you to edit a file. That means open the file in VS Code and change its text.

Example:

```text
Open library/magazines.json and add the new magazine entry.
```

Other instructions ask you to run a command. That means type or paste the command into the VS Code terminal and press Enter.

Example:

```bash
git status
```

## Before You Start Editing

Get the latest version from GitHub before making changes:

```bash
git pull
```

This reduces the chance that two people edit old versions of the same files.

## Adding A New Magazine PDF

Use this checklist every time a new issue is added.

### 1. Name The PDF Carefully

Use lowercase words separated by hyphens. Include the semester and year.

Good:

```text
mentor-magic-fall-2026.pdf
dream-big-spring-2027.pdf
```

Avoid:

```text
Mentor Magic FINAL final version.pdf
Spring_2027!!.pdf
```

The filename becomes the issue ID. For example:

```text
library/pdfs/mentor-magic-fall-2026.pdf
```

Becomes:

```text
mentor-magic-fall-2026
```

That ID is used in page folders, cover filenames, JSON files, and shareable URLs.

### 2. Put The PDF In `library/pdfs/`

Drag the PDF into:

```text
library/pdfs/
```

Example:

```text
library/pdfs/mentor-magic-fall-2026.pdf
```

### 3. Run The WebP Generation Script

From the project root terminal, run:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf
```

Replace the PDF name with the actual file you added.

If your computer uses `py` instead of `python`, run:

```bash
py scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf
```

### What The Script Does

The script:

- Reads the PDF from `library/pdfs/`.
- Creates one WebP image for each page in `library/pages/{issue-id}/`.
- Creates a cover image at `library/covers/{issue-id}.webp`.
- Creates `library/page-text/{issue-id}.json` if it does not already exist.
- Preserves existing page text and captions by default.
- Prints a JSON snippet that should be added to `library/magazines.json`.

Example output files:

```text
library/pages/mentor-magic-fall-2026/page-1.webp
library/pages/mentor-magic-fall-2026/page-2.webp
library/covers/mentor-magic-fall-2026.webp
library/page-text/mentor-magic-fall-2026.json
```

### Script Options

Usually, use the default command. It is designed to balance quality and file size:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf
```

If tiny text looks blurry, generate larger images:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf --page-dpi 450 --cover-dpi 300 --quality 90
```

If you need artifact-free images and do not mind larger files:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf --lossless
```

If you intentionally want to reset the page text template:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf --overwrite-page-data
```

Be careful with `--overwrite-page-data`. It replaces the existing readable text/caption JSON for that issue.

## Adding The Magazine To The Archive

After the script runs, it prints a block that looks like this:

```json
{
  "id": "mentor-magic-fall-2026",
  "title": "Your Title Here",
  "year": "2026",
  "category": "Spring Issue",
  "pageCount": 18,
  "pdf": "library/pdfs/mentor-magic-fall-2026.pdf",
  "cover": "library/covers/mentor-magic-fall-2026.webp",
  "description": "Short description."
}
```

Copy that object into `library/magazines.json`.

### Editing `library/magazines.json`

`library/magazines.json` is a list of magazine objects inside square brackets:

```json
[
  {
    "id": "take-charge-fall-2023",
    "title": "Take Charge, Fall 2023",
    "year": "2023",
    "category": "Fall Issue",
    "pageCount": 16,
    "pdf": "library/pdfs/take-charge-fall-2023.pdf",
    "cover": "library/covers/take-charge-fall-2023.webp",
    "description": "Take Charge issue."
  },
  {
    "id": "mentor-magic-fall-2026",
    "title": "Mentor Magic, Fall 2026",
    "year": "2026",
    "category": "Fall Issue",
    "pageCount": 18,
    "pdf": "library/pdfs/mentor-magic-fall-2026.pdf",
    "cover": "library/covers/mentor-magic-fall-2026.webp",
    "description": "Stories and resources about mentorship."
  }
]
```

Important JSON rules:

- Every object needs `{` and `}`.
- The whole file needs one opening `[` and one closing `]`.
- Put a comma between magazine objects.
- Do not put a comma after the final object.
- Use double quotes, not single quotes.
- `id` must match the generated folder and file names.
- `pageCount` must match the number of pages in the PDF.
- `cover` should end in `.webp`.

## Adding Readable Page Text And Captions

The recommended way to add this text is the **Page Text editor** in the admin app (see `HOW_TO_RUN.md`):

1. Open the admin app (double-click `Admin Library.bat`, or run `py manager/run.py`).
2. Go to the **Page Text** view (or click **Edit text** on an issue's card on the Dashboard).
3. Pick the issue, then step through its pages. Each page shows the page image on the left and editable **Text** and **Captions** boxes on the right.
4. Type the readable text and any caption/image description, then click **Save**. Saving writes the file described below for you — no manual JSON editing needed.

Each issue has a matching file behind the scenes:

```text
library/page-text/{issue-id}.json
```

Example:

```text
library/page-text/mentor-magic-fall-2026.json
```

The reader uses this file for:

- The side panel page text.
- Text-to-speech.
- Accessibility support.
- Captions or image descriptions.

Each page object looks like this:

```json
{
  "title": "Page 1",
  "text": "Readable text from this page.",
  "captions": "Description of important images or layout on this page."
}
```

**Fallback (hand-editing):** if you prefer, or the admin app isn't available, you can edit `library/page-text/{issue-id}.json` directly in a text editor. If the script creates empty text fields, fill them in when you have the final copy. Captions can describe photos, illustrations, QR codes, charts, or anything important that is not obvious from the text.

## Testing The Website Locally

Do not open `index.html` directly by double-clicking it. The site uses `fetch()` to load JSON, and browsers often block that when files are opened directly.

Instead, run a local web server from the project root:

```bash
python -m http.server 8000
```

Then open this in a browser:

```text
http://localhost:8000
```

To test a specific issue, use:

```text
http://localhost:8000/reader.html?id=mentor-magic-fall-2026
```

To stop the local server, click the terminal and press:

```text
Ctrl + C
```

## What To Check Before Publishing

Before pushing to GitHub, check:

- The new issue appears on the archive page.
- The cover image loads.
- The reader opens without an error.
- All pages flip correctly.
- The PDF download/open links work.
- The page count is correct.
- The side panel text appears where available.
- No JSON syntax errors appear in the browser console.

You can also check changed files in the terminal:

```bash
git status
```

To check that every JSON file is readable by the website:

```bash
python -c "import json, pathlib; [json.load(open(p, encoding='utf-8-sig')) for p in pathlib.Path('library').rglob('*.json')]; print('All JSON files are valid')"
```

## Publishing Changes To GitHub

GitHub Pages updates from the files in the GitHub repository. To publish changes, commit and push them.

### 1. Check What Changed

```bash
git status
```

You should see the new or modified files, such as:

```text
library/pdfs/mentor-magic-fall-2026.pdf
library/pages/mentor-magic-fall-2026/
library/covers/mentor-magic-fall-2026.webp
library/page-text/mentor-magic-fall-2026.json
library/magazines.json
```

### 2. Review Changes

For text files, you can run:

```bash
git diff
```

Large generated image files and PDFs will not show useful text diffs. That is normal.

### 3. Stage The Files

To stage everything changed:

```bash
git add .
```

Or stage specific files:

```bash
git add library/pdfs/mentor-magic-fall-2026.pdf
git add library/pages/mentor-magic-fall-2026
git add library/covers/mentor-magic-fall-2026.webp
git add library/page-text/mentor-magic-fall-2026.json
git add library/magazines.json
```

### 4. Commit The Files

Write a clear commit message:

```bash
git commit -m "Add Mentor Magic Fall 2026 issue"
```

### 5. Push To GitHub

```bash
git push
```

After pushing, GitHub Pages may take a minute or two to update.

## Updating Your Local Copy Later

If someone else has changed the website on GitHub, bring those changes down before starting new work:

```bash
git pull
```

If Git says your local changes would be overwritten, stop and ask a maintainer before continuing.

## Updating An Existing Magazine

If a PDF is replaced with a corrected version:

1. Replace the PDF in `library/pdfs/`.
2. Run the converter again:

```bash
python scripts/generate-webp.py library/pdfs/existing-issue.pdf
```

By default, the script preserves existing `library/page-text/{issue-id}.json` text and captions.

Then test locally, commit, and push.

## Shareable Issue URLs

Each magazine can be linked directly with its issue ID:

```text
https://your-site-url/reader.html?id=mentor-magic-spring-2025
```

The ID after `?id=` must match an entry in `library/magazines.json`.

## Updating A Cover Only

The usual cover is generated from page 1 of the PDF. If you need a custom cover:

1. Export or create a WebP cover.
2. Save it here:

```text
library/covers/{issue-id}.webp
```

3. Confirm `library/magazines.json` points to that file:

```json
"cover": "library/covers/{issue-id}.webp"
```

## File Structure

```text
/
|-- index.html                  Archive page
|-- reader.html                 Flipbook reader
|-- Admin Library.bat           Double-click launcher for the admin app (Windows)
|-- README.md                   This guide
|-- PROJECT_CONTEXT.md          Technical handoff notes
|-- assets/
|   |-- style.css               Shared colors, fonts, and components
|   |-- sharpur-edge-logo.svg
|   |-- pips/
|   |-- icons/
|   `-- fonts/
|-- library/
|   |-- magazines.json          Magazine list and metadata
|   |-- pdfs/
|   |   `-- {issue-id}.pdf      Source PDFs
|   |-- covers/
|   |   `-- {issue-id}.webp     Generated cover images
|   |-- pages/
|   |   `-- {issue-id}/
|   |       |-- page-1.webp
|   |       |-- page-2.webp
|   |       `-- ...
|   `-- page-text/
|       `-- {issue-id}.json     Per-page text and captions
|-- manager/                    Admin app (Dashboard, Add Issue, Page Text, Explorer, Git)
|-- scripts/
|   |-- generate-webp.py        Main PDF-to-WebP converter
|   |-- generate-pages.py       Older wrapper that calls generate-webp.py
|   `-- generate-jpg.py         Legacy JPG converter
`-- docs/                       Additional project documentation
```

## What To Edit

| File | When to edit |
| --- | --- |
| `library/magazines.json` | Add, remove, rename, sort, or describe magazine issues. |
| `library/page-text/{issue-id}.json` | Add readable text and captions for each page (prefer the admin app's **Page Text** editor over hand-editing this file). |
| `README.md` | Update this guide when the workflow changes. |
| `assets/style.css` | Change site-wide colors, spacing, typography, or layout. |

## What Not To Edit By Hand

| Path | Why |
| --- | --- |
| `library/pages/{issue-id}/page-N.webp` | Generated by the converter. Regenerate from the PDF instead. |
| `library/covers/{issue-id}.webp` | Usually generated by the converter. Replace only when intentionally using a custom cover. |
| `index.html` | Core archive logic. Edit only when changing the website behavior. |
| `reader.html` | Core reader logic. Edit only when changing the reader behavior. |

## Common Problems And Fixes

### `python` Is Not Recognized

Try:

```bash
py --version
```

If `py` works, use `py` instead of `python` in the commands.

If neither works, install Python and make sure it is added to PATH.

### `fitz` Or `Pillow` Is Missing

Install the dependencies:

```bash
python -m pip install PyMuPDF Pillow
```

### The Site Says It Could Not Load Magazines

Check:

- You are using `http://localhost:8000`, not opening `index.html` directly.
- `library/magazines.json` exists.
- `library/magazines.json` is valid JSON.
- There are no missing commas or extra trailing commas.

### A New Issue Does Not Show Up

Check:

- The issue was added to `library/magazines.json`.
- The JSON file was saved.
- The browser was refreshed.
- The issue is not hidden by a search or filter.
- The local server is running from the project root.

### Pages Do Not Appear In The Reader

Check:

- `library/pages/{issue-id}/page-1.webp` exists.
- The `id` in `library/magazines.json` matches the folder name in `library/pages/`.
- `pageCount` matches the number of page images.
- `reader.html?id={issue-id}` uses the same ID.

### Cover Does Not Appear

Check:

- `library/covers/{issue-id}.webp` exists.
- `library/magazines.json` has the correct cover path.
- The path uses forward slashes:

```json
"cover": "library/covers/mentor-magic-fall-2026.webp"
```

### Git Push Fails

First, make sure you have the latest version:

```bash
git pull
```

Then try:

```bash
git push
```

If Git reports a conflict, ask a supervisor or another maintainer before resolving it unless you are comfortable with merge conflicts.

## Reader Keyboard Shortcuts

| Key | Action |
| --- | --- |
| Right arrow or Space | Next page |
| Left arrow or Shift+Space | Previous page |
| `+` | Zoom in |
| `-` | Zoom out |
| `F` | Fit to screen |

## Quick Command Reference

Install dependencies:

```bash
python -m pip install PyMuPDF Pillow
```

Generate WebP files for a new PDF:

```bash
python scripts/generate-webp.py library/pdfs/mentor-magic-fall-2026.pdf
```

Run the local test server:

```bash
python -m http.server 8000
```

Check changed files:

```bash
git status
```

Commit and publish:

```bash
git add .
git commit -m "Add Mentor Magic Fall 2026 issue"
git push
```
