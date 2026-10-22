# bridgewebs.com/jbf → jordanbridgefederation.com

Audit of every menu entry on https://www.bridgewebs.com/jbf (checked 22 Oct 2026).

| Bridgewebs page | Content there | On the new site |
|---|---|---|
| Home Page | Condolence for Issam Salfiti | Memorial section |
| | Jordan Cup 26 results + schedule (.xlsx) | National Leagues & Cup, Archive |
| | Festival 2026 posters (JOR261, JOR_262) | Posters |
| | Sponsors (Tejari, Etihad, Capital, National Paints) | Sponsors strip |
| | Special message from HRH Prince Feisal + Olympic logo | Olympic patronage block |
| | President, committee and manager with photos | Executive Board |
| | Contact details, Facebook, tourist links | Contact Details (`#contact`) |
| | Latest results list | Results (`#results`) |
| Bulletin Section | Pre_Bulletin.pdf | Archive (`public/archive/Pre_Bulletin.pdf`) |
| Pictures Album | 2 albums, 46 distinct image files | Gallery, same 2 albums (`public/data/gallery_albums.json`). Files that are just smaller copies of the same photo are shown once |
| Results → Results Calendar | 83 events, 2019–2026 | Results (`public/data/results/`) |
| 2021 / By-Laws documents | Arabic statutes 2021 PDF, By-Laws KP 220821 PDF | Archive (byte-identical files) |
| | "2021.pdf" | Broken on Bridgewebs itself ("document no longer exists"), nothing to copy |

## Not copied, and why

- **Where & When, How to Find Us, Constitution**: still the default Bridgewebs sample text ("£xx per person", "Objects (Sample)", a placeholder map). The federation never filled them in.
- **Committee (Information menu), Calendar, Calendar Month, Competitions**: empty on Bridgewebs.
- **Contact Us, Find a Partner, Personal Analysis, Member Area**: Bridgewebs features that need a member login (contact form, partner bookings, personal score analysis). They hold no public content.
- **EBU Information (EBU News, Best Behaviour, Law Change 2017, Announcing Rules)**: the English Bridge Union's own pages that Bridgewebs inserts into every club site. This is not JBF content.
- **Administration, BridgeWebs**: the platform's admin and directory pages.

## Excel files in public/archive (checked 23 Oct 2026)

| File | What it holds | On the site |
|---|---|---|
| Jordan Cups 26 Final.xlsx | 8 teams × 7 rounds (VP + IMP), penalties, totals, rosters | Jordan Cup 2026 table and team rosters. Roster spelling now follows the file ("Azza Qauah") |
| Jordan Cups 26 schedule.xlsx | Rosters and the 7 rounds of pairings | Jordan Cup 2026 schedule. Every match's VPs add up to 20 and its IMPs to 0 |
| Jordan Cups 2025 Final.xlsx | 7 teams: result after round 7, rounds 8–14, totals, rosters | Jordan Cup 2025 table |
| JORDAN CUP 2025 AFTER ROUND 11.xlsx | An earlier copy of the same table, stopped after round 11 | Covered by the final file: every round value matches. Its King Hussein roster also lists Zafer Jarrar and Mona Al Zbein, who are not in the final roster |
| MIX SELECTION FINAL.xlsx, sheet "BYE" | 7 pairs × 11 rounds (IMP + VP), totals, "Top 9 VP" and the final ranking | Mixed Selection 2025 table. Fixed: the site used to show only the first 5 rounds (Sheet1), so its ranking was wrong |
| MIX SELECTION FINAL.xlsx, Sheet1/Sheet2/Sheet3 | Interim working sheets (after 5 and after 8 rounds) | Covered by the final sheet. Two cells differ from it (Maya/Rageed R2 3.98 vs 3.89, Rana/Jamal R3 4.92 vs 5.4); the final sheet's values are used |
| MIX Selection 2025 V.P.xlsx | Group A after 3 rounds | Covered by the final sheet |
