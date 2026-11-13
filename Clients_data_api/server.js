/*
 * ============================================================
 * DEPRECATED — DO NOT RUN THIS ALONGSIDE app.py
 * ============================================================
 *
 * This file is no longer used. Flask (app.py) now fully owns
 * weekly_schedule.json:
 *
 *   - GET  /api/calendar/schedule  (calendar_manager.get_current_week)
 *   - POST /api/calendar/save      (calendar_manager.save_schedule)
 *
 * The old /api/calendar/save route below wrote the WHOLE file
 * as one flat object every time it was called, with no
 * per-week key at all. Flask's version keys the file by week
 * (e.g. "2026-08-31") and nests each week's days under a
 * "week" key alongside "savedAt" — a different, incompatible
 * format.
 *
 * If this Node server is ever started on port 3000 while
 * Flask is also running on port 5000, and something posts to
 * this server's /api/calendar/save instead of Flask's, it
 * will silently overwrite weekly_schedule.json with the old
 * flat format and corrupt every saved week Flask has stored.
 *
 * The route below is disabled for that reason. If you need a
 * separate Node process for something else in the future,
 * copy just what you need from here rather than re-enabling
 * this route as-is.
 * ============================================================
 */

const express = require("express");
const path = require("path");

const app = express();

const PORT = 3000;

app.use(express.json());

app.use(express.static(__dirname));

/*
 * SAVE WEEKLY SCHEDULE — DISABLED.
 * See the deprecation notice at the top of this file.
 */
app.post("/api/calendar/save", (req, res) => {
  res.status(410).json({
    success: false,
    message:
      "This endpoint is disabled. Weekly schedule saving is handled " +
      "by the Flask app (app.py) on port 5000, not this Node server.",
  });
});

/*
 * START SERVER
 */
app.listen(PORT, () => {
  console.log(
    `Deprecated calendar server running at http://localhost:${PORT} ` +
      `(schedule saving is disabled — see comments at the top of this file)`,
  );
});
