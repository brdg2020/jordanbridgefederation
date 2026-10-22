# Jordan Bridge Federation (JBF) — Portal Administration & Data Entry Guide
# الاتحاد الأردني للبريدج — دليل إدارة وتحديث بيانات البوابة الإلكترونية

This guide provides simple, step-by-step instructions for JBF officials and tournament directors (e.g. Tournament Director Raad Otoom, President Feisal Hamdan, General Assembly staff) to update scores, player rosters, and documents on **jordanbridgefederation.com**.

---

## Method 1: Instant In-Browser Data Entry (Zero-Coding)
## الطريقة الأولى: إدخال البيانات المباشر عبر المتصفح (بدون أي برمجة)

1. Open **[jordanbridgefederation.com](https://jordanbridgefederation.com/)** in any web browser.
2. Click the **"Admin Portal"** or **"Admin Data Entry"** button located at the top banner or website footer.
3. Enter the Federation Admin PIN:
   * **PIN:** `jbf2026`
4. Fill in the simple form:
   * **Target Tournament:** Jordan Cup 2026 or Festival
   * **Team Name:** e.g., `AL Nashama`
   * **Rank (#):** e.g., `1`
   * **Total V.P Score:** e.g., `90.90`
   * **Total IMP:** e.g., `+79`
   * **Player Roster (comma-separated):** e.g., `Abdlah Ajlouni, Zaid Bitar, Samer Haddad, Luai Al Hussari`
5. Click **"Apply Live Preview"** to see your updates reflect immediately on the page!
6. Click **"Export Clean JSON"** to copy the updated dataset for permanent archiving.

---

## Method 2: Direct GitHub Data Update (Takes 30 Seconds)
## الطريقة الثانية: التحديث المباشر عبر ملفات البيانات

All live datasets are structured in clean JSON files inside `public/data/`:
* **Complete Federation Master Data:** `public/data/jbf_master_data.json`
  * Contains Jordan Cup matrix with rosters, 4 historical festivals (2026, 2025, 2024, 2023), Mixed Selection 2025, and Document catalog.
* **Festival Round Matches:** `public/data/festival2026.json`
* **Executive Committee Members:** `public/data/committee.json`

### To update via GitHub web interface:
1. Open repository `https://github.com/brdg2020/jordanbridgefederation`
2. Navigate to `public/data/jbf_master_data.json`
3. Click the **Edit (Pencil)** icon.
4. Modify scores, team names, or add new tournament records.
5. Click **"Commit changes"**.
6. GitHub Pages will automatically build and publish the live site within 30 seconds!

---

## Method 3: Adding New Tournament Documents, Posters & Photos
## الطريقة الثالثة: إضافة وثائق جديدة، ملصقات أو صور

* **PDF Bulletins & Regulations:** Place the PDF inside `public/archive/` and add the filename to the document catalog in `generate_master_data.py`.
* **Festival Posters:** Place image files inside `public/images/` (`JOR261.jpg`, `JOR_262.jpg`).
* **Tournament Gallery Photos:** Add `.jpg` files to `public/gallery/`. They will automatically appear in the gallery grid with full Lightbox Zoom support.

---

## Technical Summary
* **Domain:** `jordanbridgefederation.com` / `www.jordanbridgefederation.com`
* **Hosting:** GitHub Pages (SSL / TLS automated by Let's Encrypt)
* **DNS Provider:** Squarespace Domains (Standard A Records & CNAME configured)
* **Frontend:** Modern Single Page Application (Tailwind CSS, Lucide Icons, Vanilla JS, Zero heavy dependencies)
* **Language Support:** Full English & Arabic RTL reactive toggle.
