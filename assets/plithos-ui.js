/* Plithos: recovery for a page kept past its replacement.
 *
 * Nothing published now asks for this file. It is here for pages a browser
 * held on to from an earlier day, which still name it. Those pages predate
 * the build stamp, so reaching this code is itself the signal that the page
 * in front of the reader is not the page on the site: refetch it past the
 * cache and show the current one.
 *
 * Runs once per visit, and does nothing where it cannot tell. Leave this file
 * in place; the pages that need it are exactly the ones that cannot be
 * updated to stop asking for it.
 */
(function () {
  "use strict";

  var KEY = "plithos.recovered";

  if (document.querySelector('meta[name="plithos-build"]')) return;
  if (!window.fetch) return;
  try {
    if (sessionStorage.getItem(KEY)) return;
    sessionStorage.setItem(KEY, "1");
  } catch (e) {}

  function reload() { location.reload(); }
  fetch(location.href, { cache: "reload" }).then(reload, reload);
})();
