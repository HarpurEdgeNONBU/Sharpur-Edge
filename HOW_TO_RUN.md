# How to Run the Archive Manager

A desktop app for adding and deleting magazine issues — no terminal knowledge needed once it's set up. You do the two setup steps once; after that you just double-click to launch.

---

## What you need (one-time)

1. **Python 3.11 or newer** — https://www.python.org/downloads/
   - On **Windows**, during install, check the box **"Add python.exe to PATH"**.
2. The project folder (the one that contains `index.html`, `library/`, and the `manager/` folder).

---

## First-time setup (do this once)

You need a terminal for these two commands **only once**. After this, you never need the terminal again.

### Windows

1. Open the project folder in File Explorer.
2. Click the address bar, type `cmd`, and press **Enter** (a black terminal opens in this folder).
3. Install the app's requirements — type this and press Enter:

   ```
   py -m pip install -r manager/requirements.txt
   ```

4. Wait until it finishes (it downloads a few packages).

### Mac

1. Open **Terminal**.
2. Drag the project folder onto the Terminal window after typing `cd ` (with a space), then press Enter. For example:

   ```
   cd /Users/you/Downloads/Sharpur-Edge-Archive-main/Sharpur-Edge-Archive-main
   ```

3. Install the requirements:

   ```
   python3 -m pip install -r manager/requirements.txt
   ```

---

## Running the app

### The simplest way (Windows)

1. Open the project folder in File Explorer.
2. Double-click **`Admin Library.bat`**.

A terminal window flashes open and the app window appears. Leave the little terminal window open in the background while you use the app; closing the app window ends the session.

### Another way (Windows, terminal)

1. Open the project folder.
2. Open the address bar (click it), type `cmd`, press **Enter**.
3. Type this and press Enter:

   ```
   py manager/run.py
   ```

The app window opens. Leave the little terminal window open in the background while you use the app; closing the app window ends the session.

### Mac

From a Terminal that is inside the project folder (see setup above):

```
python3 manager/run.py
```

---

## Using the admin app

- **Dashboard** — see every issue with its cover. Click the trash icon on a card to delete an issue; you'll be asked to confirm by typing the issue's title. Deleting removes the PDF, cover, page images, page text file, and the entry from `library/magazines.json` — all together. Click **Edit text** on a card to jump straight into that issue's Page Text editor.
- **Add Issue** — drag a PDF onto the drop area (or click **Browse**). Fill in the title, year, category, and (optionally) a description. The `issue_id` is filled in automatically from the file name. Click **Generate**. A progress bar shows: Reading PDF → Rendering pages → Exporting cover → Writing JSON. When it finishes, the new issue appears on the Dashboard.
- **Page Text** — pick an issue, then step through its pages one at a time. The page image is shown on the left; editable **Text** and **Captions** boxes are on the right. Type the readable text and any caption/image description, then click **Save** to write it to that page's entry. This is the recommended way to add or fix reader text — no manual JSON editing needed.
- **Explorer** — a read-only health check. It flags any issue missing a cover, page images, or its text file, or whose page count doesn't match.
- **Git** *(not optional)* — Pull / Commit / Push buttons for publishing changes, you MUST push something onto GitHub (this is where the main website is hosted).

---

## Settings (optional)

You can change output folders, image quality/DPI, and the category list by editing:

```
manager/config/config.yaml
```

No code changes needed — just edit the values and restart the app.

---

## If something goes wrong

- **"python is not recognized" (Windows):** Python wasn't added to PATH. Reinstall Python and check the **"Add python.exe to PATH"** box, or use `py` instead of `python`.
- **"No module named customtkinter" (or similar):** the one-time install step didn't complete. Re-run:
  `py -m pip install -r manager/requirements.txt`
- **The app window doesn't appear:** make sure you ran it from inside the project folder (the folder that contains the `manager/` folder).
- **Covers look blank on the Dashboard:** that issue may be missing its cover image — check the **Explorer** tab. 
- Also contact me at williamx9455@gmail.com or +13473254401 if you need further assistance

---

## The terminal script still works

The old command-line converter is still available and now uses the same engine as the app:

```
py scripts/generate-webp.py library/pdfs/your-issue.pdf
```

But you no longer need it — the app does everything.
