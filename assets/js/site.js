/* Recallant site behaviour. Progressive enhancement only: every page reads fine without it. */
(function () {
  "use strict";

  var doc = document.documentElement;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------------------------------------------------------------- navigation tone and state */

  var nav = $("#nav");
  var menu = $("#menu");
  var toggle = $(".nav__toggle");
  var bands = $$(".band, .footer, .sources-band");
  var menuOpen = false;

  function toneAt(y) {
    for (var i = 0; i < bands.length; i++) {
      var r = bands[i].getBoundingClientRect();
      if (r.top <= y && r.bottom > y) {
        return bands[i].classList.contains("band--night") ? "night" : "paper";
      }
    }
    return nav ? nav.getAttribute("data-tone") : "paper";
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      if (!nav) return;
      nav.classList.toggle("is-scrolled", window.scrollY > 4);
      if (!menuOpen) {
        var mid = nav.getBoundingClientRect().top + nav.offsetHeight / 2;
        nav.setAttribute("data-tone", toneAt(mid));
      }
      progress();
    });
  }

  function setMenu(open) {
    if (!menu || !toggle) return;
    menuOpen = open;
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Menu");
    doc.style.overflow = open ? "hidden" : "";
    nav.classList.toggle("is-menu", open);
    if (open) {
      nav.setAttribute("data-tone", "paper");
      var first = $("a", menu);
      if (first) first.focus();
    } else {
      onScroll();
    }
  }

  if (toggle) {
    toggle.addEventListener("click", function () { setMenu(!menuOpen); });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menuOpen) { setMenu(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () {
      if (menuOpen && window.innerWidth > 860) setMenu(false);
    });
  }

  /* ---------------------------------------------------------------- reading progress (study page) */

  var bar = $("[data-progress]");
  var article = $("[data-article]");
  function progress() {
    if (!bar || !article) return;
    var r = article.getBoundingClientRect();
    var total = r.height - window.innerHeight * 0.6;
    var done = Math.min(1, Math.max(0, (-r.top + window.innerHeight * 0.2) / Math.max(1, total)));
    bar.style.transform = "scaleX(" + done.toFixed(4) + ")";
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------------------------------------------------------------- reveal on scroll */

  if (!reduceMotion && "IntersectionObserver" in window) {
    var fold = window.innerHeight * 0.92;
    var pending = $$(".reveal").filter(function (el) { return el.getBoundingClientRect().top > fold; });
    pending.forEach(function (el) { el.classList.add("pre"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.remove("pre"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    pending.forEach(function (el) { io.observe(el); });
  }

  /* ---------------------------------------------------------------- the answer instrument */

  var inst = $("[data-instrument]");
  if (inst) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      inst.classList.add("is-playing");
    } else {
      var io2 = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { inst.classList.add("is-playing"); io2.disconnect(); }
        });
      }, { threshold: 0.3 });
      io2.observe(inst);
    }
  }

  /* ---------------------------------------------------------------- chart tooltips */

  var tip = document.createElement("div");
  tip.className = "tip";
  tip.hidden = true;
  tip.setAttribute("role", "tooltip");
  document.body.appendChild(tip);

  function showTip(el) {
    var parts = (el.getAttribute("data-tip") || "").split("|");
    tip.innerHTML = "<strong>" + esc(parts[0]) + "</strong>" + esc(parts[1] || "");
    tip.hidden = false;
    var r = el.getBoundingClientRect();
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var x = Math.min(window.innerWidth - w - 8, Math.max(8, r.left + r.width / 2 - w / 2));
    var y = r.top - h - 10;
    if (y < 64) y = r.bottom + 10;
    tip.style.left = x + window.scrollX + "px";
    tip.style.top = y + window.scrollY + "px";
  }
  function hideTip() { tip.hidden = true; }

  $$(".db__dot[data-tip], .rangechart__dot[data-tip]").forEach(function (el) {
    el.addEventListener("mouseenter", function () { showTip(el); });
    el.addEventListener("mouseleave", hideTip);
    el.addEventListener("focus", function () { showTip(el); });
    el.addEventListener("blur", hideTip);
  });
  window.addEventListener("scroll", hideTip, { passive: true });

  /* ---------------------------------------------------------------- question explorer */

  function pips(n, total, extra) {
    var s = '<span class="pips' + (extra || "") + '" aria-hidden="true">';
    for (var i = 0; i < total; i++) s += i < n ? '<i class="on" style="--p:' + i + '"></i>' : "<i></i>";
    return s + "</span>";
  }

  function rows(pairs, n, empty) {
    if (!pairs.length) return '<ul class="rowlist"><li class="empty">' + esc(empty) + "</li></ul>";
    return '<ul class="rowlist">' + pairs.map(function (p) {
      return '<li><span class="nm">' + esc(p[0]) + "</span>" + pips(p[1], n, " pips--sm") +
        '<span class="num">' + p[1] + "/" + n + "</span></li>";
    }).join("") + "</ul>";
  }

  // Mirrors ex_result() in _build/build.py, so the server-rendered first result and these match.
  function result(item) {
    var n = item.runs, first = item.first, named = item.named, out = [];
    out.push('<p class="kicker">' + esc(item.cat) + " · " + n + " runs</p>");
    out.push('<h3 class="explorer__question">' + esc(item.q) + "</h3>");
    if (first.length) {
      var top = first[0][1];
      var leaders = first.filter(function (f) { return f[1] === top; }).map(function (f) { return f[0]; });
      var rest = first.filter(function (f) { return f[1] !== top; });
      var name = leaders.length === 1 ? leaders[0] : leaders.slice(0, -1).join(", ") + " and " + leaders[leaders.length - 1];
      var label = leaders.length === 1 ? "Recommended first" : "Recommended first, split";
      var meta = top + " of " + n + " runs" + (leaders.length > 1 ? " each" : "");
      out.push('<div class="explorer__first"><div><p class="kicker">' + label + "</p><strong>" + esc(name) +
        '</strong></div><div class="explorer__firstmeta">' + pips(top, n) + "<span>" + meta + "</span></div></div>");
      if (rest.length) {
        out.push('<p class="explorer__also">Also first: ' + rest.map(function (r) {
          return esc(r[0]) + " (" + r[1] + " of " + n + ")";
        }).join(", ") + "</p>");
      }
    } else {
      var msg = item.cat === "Comparisons" && !named.length ? "Only the two brands in the question were named"
        : !named.length ? "No helpdesk product was named in any answer" : "No single brand was recommended first";
      out.push('<div class="explorer__first is-none"><div><p class="kicker">Recommended first</p><strong>' + msg +
        "</strong></div></div>");
    }
    var emptyNamed = item.cat === "Comparisons" ? "None besides the two in the question" : "None";
    out.push('<div class="explorer__cols"><div class="explorer__col"><h4 class="kicker">Named in the answers</h4>' +
      rows(named, n, emptyNamed) + '</div><div class="explorer__col"><h4 class="kicker">Sources cited most</h4>' +
      rows(item.sources, n, "None") + "</div></div>");
    return out.join("");
  }

  $$("[data-explorer]").forEach(function (root) {
    var key = root.getAttribute("data-explorer");
    var dataEl = document.getElementById("ex-data-" + key);
    if (!dataEl) return;
    var items;
    try { items = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var byId = {};
    items.forEach(function (q) { byId[q.id] = q; });
    var out = $("[data-ex-result]", root);
    var foot = $(".explorer__foot", out);
    var footHtml = foot ? foot.outerHTML : "";
    var select = $("[data-ex-select]", root);
    var buttons = $$(".explorer__q", root);
    var tabs = $$(".explorer__tab", root);

    function show(id, fromSelect) {
      var item = byId[id];
      if (!item) return;
      out.innerHTML = result(item) + footHtml;
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-id") === id ? "true" : "false"); });
      if (select && !fromSelect) select.value = id;
      if (tabs.length) setTab(item.cat, true);
    }

    function setTab(cat, keepSelection) {
      tabs.forEach(function (t) { t.setAttribute("aria-pressed", t.getAttribute("data-cat") === cat ? "true" : "false"); });
      $$("[data-ex-list] > li", root).forEach(function (li) { li.hidden = li.getAttribute("data-cat") !== cat; });
      if (!keepSelection) {
        var firstInCat = items.filter(function (q) { return q.cat === cat; })[0];
        if (firstInCat) show(firstInCat.id);
      }
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { show(b.getAttribute("data-id")); });
    });
    if (select) select.addEventListener("change", function () { show(select.value, true); });
    tabs.forEach(function (t) {
      t.addEventListener("click", function () { setTab(t.getAttribute("data-cat"), false); });
    });
  });

  /* ---------------------------------------------------------------- scrollspy for local nav and contents */

  // The active link is the last target whose top has passed a line 30% down the viewport.
  $$("[data-spy]").forEach(function (list) {
    var links = $$("a[href^='#']", list);
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    if (targets.some(function (t) { return !t; })) return;
    var current = -2;
    var queued = false;
    function update() {
      queued = false;
      var line = window.innerHeight * 0.3;
      var best = -1;
      targets.forEach(function (t, i) { if (t.getBoundingClientRect().top <= line) best = i; });
      if (best === current) return;
      current = best;
      links.forEach(function (a, i) {
        var on = i === best;
        a.classList.toggle("is-active", on);
        if (on) a.setAttribute("aria-current", "location"); else a.removeAttribute("aria-current");
      });
      var active = links[best];
      if (active && list.scrollWidth > list.clientWidth) {
        var left = active.offsetLeft - (list.clientWidth - active.offsetWidth) / 2;
        list.scrollTo({ left: left, behavior: reduceMotion ? "auto" : "smooth" });
      }
    }
    function queue() { if (!queued) { queued = true; window.requestAnimationFrame(update); } }
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue);
    update();
  });

  /* ---------------------------------------------------------------- snapshot request form */

  /* Sent as JSON to the form's Formspree endpoint (its action). Without JavaScript the form posts there directly. */
  var EMAIL = "hello@recallant.com";
  var DEFAULT_INTEREST = "A free snapshot";

  $$("[data-snapshot-form]").forEach(function (form) {
    var endpoint = form.getAttribute("action");
    var fields = $(".snap-form__fields", form);
    var done = $(".snap-form__done", form);
    var status = $(".snap-form__status", form);
    var button = $('button[type="submit"]', form);
    var label = $("span", button);
    var required = [form.elements.email, form.elements.product];
    var sending = false;
    form.noValidate = true;

    function value(name) {
      var el = form.elements[name];
      return el ? el.value.trim() : "";
    }
    function check(input) {
      var ok = input.value.trim() !== "" && input.checkValidity();
      var err = document.getElementById(input.getAttribute("aria-describedby"));
      if (ok) input.removeAttribute("aria-invalid"); else input.setAttribute("aria-invalid", "true");
      if (err) err.hidden = ok;
      return ok;
    }
    function subject() {
      var interest = value("interest") || DEFAULT_INTEREST;
      return (interest === DEFAULT_INTEREST ? "Snapshot request" : interest + " enquiry") + ": " + value("product");
    }
    function mailto() {
      var body = "Hi Recallant,\n\n" +
        "I'm interested in: " + (value("interest") || DEFAULT_INTEREST) + "\n" +
        "Product or company: " + value("product") + "\n" +
        "Website: " + (value("website") || "-") + "\n" +
        "Competitors to compare: " + (value("competitors") || "-") + "\n";
      return "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject()) + "&body=" + encodeURIComponent(body);
    }
    function setSending(on) {
      sending = on;
      button.disabled = on;
      form.setAttribute("aria-busy", on ? "true" : "false");
      if (label) label.textContent = on ? "Sending…" : "Send my request";
    }
    function fail() {
      setSending(false);
      status.classList.add("is-error");
      status.innerHTML = "That didn’t go through. Try again, or email us at " + EMAIL + ". " +
        '<a class="text-link" href="' + esc(mailto()) + '">Open it in your email app</a>';
    }
    function succeed(email) {
      setSending(false);
      $("[data-sent-to]", form).textContent = email;
      fields.hidden = true;
      done.hidden = false;
      done.focus();
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (sending) return;
      var invalid = required.filter(function (input) { return !check(input); });
      if (invalid.length) {
        invalid[0].focus();
        return;
      }
      status.classList.remove("is-error");
      status.textContent = "";
      var email = value("email");
      if (value("_gotcha")) { succeed(email); return; }  // only bots fill the hidden field
      if (!window.fetch || !window.JSON) { form.submit(); return; }

      setSending(true);
      var ctrl = window.AbortController ? new AbortController() : null;
      var timer = window.setTimeout(function () { if (ctrl) ctrl.abort(); }, 20000);
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          email: email,
          _replyto: email,
          interest: value("interest") || DEFAULT_INTEREST,
          product: value("product"),
          website: value("website") || "-",
          competitors: value("competitors") || "-",
          page: window.location.pathname,
          _subject: subject()
        }),
        signal: ctrl ? ctrl.signal : undefined
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          window.clearTimeout(timer);
          // Formspree answers 200 {"ok": true} when it accepts a submission, and 4xx with "errors" when not
          if (res.ok && data.ok !== false && !data.error && !data.errors) succeed(email);
          else fail();
        });
      }).catch(function () {
        window.clearTimeout(timer);
        fail();
      });
    });

    required.forEach(function (input) {
      input.addEventListener("input", function () {
        if (input.getAttribute("aria-invalid")) check(input);
      });
    });

    var again = $("[data-form-reset]", form);
    if (again) {
      again.addEventListener("click", function () {
        form.reset();
        done.hidden = true;
        fields.hidden = false;
        form.elements.email.focus();
      });
    }
  });

  /* Plan and study links point at the form; preselect what the visitor asked about. */
  $$("[data-interest]").forEach(function (link) {
    link.addEventListener("click", function () {
      var select = document.getElementById("sf-interest");
      if (select) select.value = link.getAttribute("data-interest");
    });
  });

  /* ---------------------------------------------------------------- copy buttons */

  $$("[data-copy]").forEach(function (btn) {
    var label = $("span", btn);
    var original = label ? label.textContent : "";
    function done(text) {
      if (label) label.textContent = text;
      window.setTimeout(function () { if (label) label.textContent = original; }, 2200);
    }
    function selectFallback() {
      var target = btn.parentElement && $("[data-copy-text]", btn.parentElement);
      if (!target) return done("Copy failed");
      var range = document.createRange();
      range.selectNodeContents(target);
      var sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      done("Press Ctrl+C");
    }
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, selectFallback);
      } else {
        selectFallback();
      }
    });
  });
})();
