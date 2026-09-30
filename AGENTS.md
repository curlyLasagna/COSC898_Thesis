# Agent Guidelines & Repository Instructions

## Building and Compiling the Thesis

To compile the entire thesis/dissertation, always run:

```bash
latexmk Dissertation.tex
```

> **Note**: A custom `latexmkrc` configuration is already set up in the user's environment (`~/.latexmkrc` managed via Home Manager), which configures LuaLaTeX, auxiliary directories, and outputs to `./out/`. Do **not** pass custom engine flags or manual output directory parameters—simply execute `latexmk Dissertation.tex`.

---

## Diagram Authoring & Recompilation (D2 & Vector PDFs)

Diagrams in this project are authored in [D2](https://d2lang.com) located under `Figures/` and compiled to standalone vector PDFs embedded via `\includegraphics`:

1. **Compile D2 to Vector SVG**:
   ```bash
   nix run nixpkgs#d2 -- Figures/<filename>.d2 Figures/<filename>.svg
   ```

2. **Convert SVG to Vector PDF (via `librsvg`)**:
   ```bash
   nix run nixpkgs#librsvg -- -f pdf -o Figures/<filename>.pdf Figures/<filename>.svg
   ```

---

## Project Structure Overview

- **`Dissertation.tex`**: Master document entry point.
- **`TUgrad.cls`**: Towson University Graduate Thesis/Dissertation document class.
- **`Pages/`**:
  - `A-Preliminary/`: Approval sheet, acknowledgments, abstract, abbreviations.
  - `B-Text/`: Core chapters (`intro.tex`, `litreview.tex`, `body.tex`, `conclusion.tex`).
  - `C-Supplemental/`: Appendices.
- **`Figures/`**: Contains vector PDFs (`.pdf`), source D2 diagrams (`.d2`), and SVGs (`.svg`).
- **`References/`**: BibTeX bibliography files (`ref.bib`, `mine.bib`).
  - **Important**: Do **not** touch or edit `References/ref.bib` under any circumstances. It is exported directly from Zotero. Ignore any warnings/errors originating from within it.
- **`out/`**: Output directory for generated PDF and build cache (`out/Dissertation.pdf`).

