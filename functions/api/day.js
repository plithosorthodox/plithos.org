/* The calendar's answer for one day, as JSON, to anyone who asks.
 *
 * A parish that wants the day's saints and fast on its own site should not
 * have to embed a page or scrape one. This is the same reckoning the calendar
 * itself runs - Pascha, the Julian offset, the menaion, the movable cycle, the
 * fast, the lectionary, and what each of the ten Churches adds - copied out of
 * index.html by tools/build_calendar_engine.py and never written twice.
 *
 *   /api/day                                  today, Greek, in English
 *   /api/day?date=2026-12-25&juris=russian    a day, a Church
 *   /api/day?lang=el&scope=all                a language, every Church's saints
 *
 *   date   YYYY-MM-DD, default today in UTC
 *   juris  greek antiochian romanian ukrainian russian serbian oca western
 *          georgian bulgarian
 *   cal    new or old, to override the Church's own reckoning
 *   lang   any of the twenty-two
 *   scope  church (default) or all
 *
 * Open to any origin, because a calendar is not a secret and this is the whole
 * point of publishing it.
 */
import { calendar } from "../../assets/plithos-calendar.v1.js";

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, OPTIONS",
  "access-control-max-age": "86400",
};

/* Built once per isolate and kept: the tables are 243 KB and the names 200 KB
   apiece, and fetching them per request would be the slowest thing here. */
let TABLES = null;
const NAMES = {};

async function asset(env, url, path) {
  const r = await env.ASSETS.fetch(new URL(path, url.origin));
  if (!r.ok) return null;
  const ct = (r.headers.get("content-type") || "").toLowerCase();
  /* A path that does not exist is answered with the whole of index.html and a
     200. Five bugs on this site began by trusting r.ok alone. */
  if (ct.indexOf("json") < 0) return null;
  return r.json();
}

function bad(message, status) {
  return new Response(JSON.stringify({ error: message }, null, 1) + "\n", {
    status: status || 400,
    headers: Object.assign({ "content-type": "application/json; charset=utf-8" }, CORS),
  });
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method === "OPTIONS") return new Response(null, { headers: CORS });
  if (request.method !== "GET") return bad("Only GET.", 405);

  const url = new URL(request.url);
  const q = url.searchParams;

  const date = q.get("date") || new Date().toISOString().slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return bad("date must be YYYY-MM-DD.");

  const lang = q.get("lang") || "en";
  if (!/^[a-z]{2,3}$/.test(lang)) return bad("lang must be a language code.");

  if (!TABLES) TABLES = await asset(env, url, "/data/calendar-tables.v1.json");
  if (!TABLES) return bad("The calendar tables are not available.", 503);

  if (NAMES[lang] === undefined) {
    NAMES[lang] = lang === "en"
      ? null
      : await asset(env, url, "/data/calendar-names.v1." + lang + ".json");
  }

  const juris = q.get("juris") || "greek";
  if (!TABLES.JURISDICTIONS[juris]) {
    return bad("Unknown jurisdiction. One of: " +
               Object.keys(TABLES.JURISDICTIONS).join(", ") + ".");
  }

  let out;
  try {
    const day = calendar(TABLES, NAMES[lang], lang);
    out = day(date, {
      juris: juris,
      lang: lang,
      cal: q.get("cal") || undefined,
      scope: q.get("scope") || undefined,
    });
  } catch (e) {
    return bad("The calendar could not answer for that day.", 500);
  }
  if (!out) return bad("That is not a date the calendar can read.");

  out.source = "https://plithos.org/";
  return new Response(JSON.stringify(out, null, 1) + "\n", {
    headers: Object.assign({
      "content-type": "application/json; charset=utf-8",
      /* A day's answer does not change; an hour lets a correction through. */
      "cache-control": "public, max-age=3600, must-revalidate",
    }, CORS),
  });
}
