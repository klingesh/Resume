# Resume — Samyuktha Ajay

Source for `../Samyuktha_Ajay_Resume.pdf` (single page, A4, selectable text).

| File | Purpose |
| --- | --- |
| `resume.html` | All content and styling. **Edit this to change the resume.** |
| `build.sh` | Renders `resume.html` into `../Samyuktha_Ajay_Resume.pdf` |
| `preview.png` | Screen render of the current resume, for quick review on GitHub |
| `assets/photo.png` | Profile photo, cropped from the original Canva export |
| `assets/icon-*.png` | Contact icons (phone, mail, LinkedIn, location), also from the original |

## Rebuilding

```bash
./build.sh                 # writes ../Samyuktha_Ajay_Resume.pdf
CHROME=/path/to/chrome ./build.sh
```

The build uses headless Chromium's print-to-PDF, so the PDF matches what the browser shows.

## Notes

- The original `../RESUME 2205.pdf` was a single flat image, so its text could not be
  edited or read by applicant tracking systems. This version is real text on a
  re-created layout, so it is searchable and ATS-readable.
- The layout was measured off the original export (colours, column widths, font sizes),
  and set in Noto Sans because the original Canva font is not available here.
- Page geometry: A4 at 96 dpi = 794 x 1123 px, sidebar 290 px wide.
