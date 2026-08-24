# Resume — Prahadhesvaryaa K S

`resume.pdf` is the current resume (single page, A4).

## Files

| File | Purpose |
| --- | --- |
| `resume.pdf` | Generated output — the file to share/submit |
| `resume_content.py` | All resume text and section order. **Edit this to change the resume.** |
| `build_resume.py` | Renders the content into `resume.pdf` |

## Rebuilding the PDF

```bash
python3 build_resume.py            # writes resume.pdf
```

No third-party packages are required — `build_resume.py` writes the PDF directly and
measures text using the Adobe base-14 font metrics shipped with groff
(`/usr/share/groff/*/font/devps/`), so line breaking and justification are exact.

## Editing tips

Each entry in `CONTENT` (in `resume_content.py`) is one block:

- `section` — blue section heading with a rule above it
- `paragraph` — justified body text
- `bullet` — bulleted, hanging-indent paragraph
- `entry` — single line, optionally with a right-aligned date
- `columns` — evenly spaced bulleted columns (used for Skills, Languages)
- `labeled` — `Label : value` line
- `space` — extra vertical gap

Text is styled per run: `("some text", B)` is bold, `R` is regular, `I` is italic.
