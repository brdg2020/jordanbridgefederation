# JBF website – admin guide
# دليل إدارة الموقع

Admin page: **https://jordanbridgefederation.com/admin/**
It is not linked from the site menu and search engines are told not to index it.

## Signing in · الدخول
- Enter the admin password and press **Sign in**. There is one admin account (`admin@jordanbridgefederation.com`); only the password is typed.
- After 3 wrong passwords the form locks for 30 seconds, and the lock doubles after every further failure (up to 1 hour). Firebase also blocks repeated attempts on its side.
- You are signed out after 30 minutes without activity, or when the browser tab is closed.
- To change the password: Firebase console → project **jbf-portal** → Authentication → Users → the admin user → *Reset password*.

## Announcements · الإعلانات
1. Open the **Announcements** tab → **+ New announcement**.
2. Write the title and text in English, Arabic, or both. Add a date, an optional link, and tick **Pin to top** to keep it first.
3. Tick **Published** and press **Save**. It appears on the home page within seconds in the "Announcements & Latest Results" section (the section is hidden while there is nothing published).
4. Untick **Published** to hide it again without deleting it.

## Results tables · جداول النتائج
Two ways to add a table:

**A. From Excel (recommended for tournaments calculated in Excel)**
1. **Results tables** tab → **⬆ Import Excel / CSV**, choose the file (.xlsx, .xls, .csv, .ods). The file is read only inside your browser; it is not uploaded anywhere.
2. Pick the sheet. The page guesses where the table starts and ends; click a row to set the **header row** or the **last row** if the guess is wrong. Use *Title rows* when the header spans 2–3 rows.
3. Check the preview, then **Use this table**. The text above the table becomes the title and the lines under it become the note — edit them freely.
4. Set the date and category, tick **Published**, **Save**.

**B. By hand or copy–paste**
- **+ Blank table**, then use the grid: **+ Row**, **+ Column**, click a cell to type. You can also copy a block of cells in Excel and paste it into the first cell.

The first column is shown with gold/silver/bronze badges for 1, 2 and 3.

## Good to know
- Everything published is public. Do not publish phone numbers or private data of players.
- The 83 historical events from Bridgewebs and the Festival / Jordan Cup tables are part of the site's code; changing those needs the developer.
- Technical details: the data is stored in Firebase Firestore (project `jbf-portal`). Security rules in `firebase/firestore.rules` allow the public to read published items only, and only the account with the `admin` permission can write.
