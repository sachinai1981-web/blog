# sachinai.com — Audit Task Tracker

8-agent audit run 2026-05-11. 47 issues found, 39 prioritized below.
Check off as completed. Tell Claude what's done → it will mark them.

---

## Sprint 1 — This Week (Priorities 1–14)

- [x] **1. Subscribe form — broken action** — form POSTs to `#` placeholder; wire to real email platform (Mailchimp / ConvertKit) or remove
- [x] **2. Analytics — no tracking** — no GA4 / Plausible / Fathom tag found; add privacy-first analytics before launch
- [x] **3. Fake metrics copy** — "500+ readers" and similar hardcoded numbers with no real backing; replace with real data or remove
- [x] **4. Featured post — 404** — hero "featured" card links to a post that returns 404; fix the slug or swap the card
- [x] **5. llms.txt — incomplete** — file exists but tool name / description placeholders not filled in; complete it
- [x] **6. robots.txt — missing sitemap ref** — `robots.txt` does not point to `sitemap.xml`; add `Sitemap:` directive
- [x] **7. sitemap.xml — stale / incomplete** — posts missing or lastmod dates wrong; regenerate
- [x] **8. ops@ placeholder** — `ops@sachinai.com` appears in footer/contact; confirm mailbox is live or swap address
- [x] **9. 404.html — missing** — no custom 404 page; add one so dead links have a branded recovery path
- [x] **10. Favicon — missing or broken** — no `<link rel="icon">` or file returns 404; add favicon (SVG preferred)
- [x] **11. OG image — missing** — no `og:image` meta tag; share previews are blank on Twitter/LinkedIn
- [x] **12. Defer non-critical scripts** — render-blocking `<script>` tags found in `<head>`; move to `defer` or bottom of body
- [x] **13. Font crossorigin — missing** — `<link rel="preload">` for fonts missing `crossorigin` attribute; causes double-fetch
- [x] **14. Accessibility landmarks — missing** — page lacks `<main>`, `<nav aria-label>`, `<footer>` landmarks; screen readers can't navigate

---

## Sprint 2 — This Month (Priorities 15–30)

- [ ] **15. Cloudflare security headers** — missing `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`, `Permissions-Policy`; add via Cloudflare Transform Rules
- [x] **16. Schema.org structured data** — no `Article` or `Person` JSON-LD; Google can't surface rich results
- [x] **17. RSS feed — missing** — no `/feed.xml`; readers and aggregators can't subscribe
- [x] **18. SRI hashes — missing** — CDN-loaded assets lack `integrity` + `crossorigin`; add Subresource Integrity
- [x] **19. /about.html — missing or stub** — page either missing or placeholder; write real About content
- [x] **20. /tools.html — missing or stub** — tools page linked in nav returns 404 or is empty; build it
- [x] **21. Broken post meta** — author, date, or read-time missing on several post cards; standardize post frontmatter
- [x] **22. Twitter OG tags** — `twitter:card`, `twitter:title`, `twitter:description` missing; Twitter previews are blank
- [x] **23. Privacy policy — missing** — no privacy policy page; required if analytics or email capture is live
- [ ] **24. Email platform — not wired** — no ConvertKit / Mailchimp / Buttondown integration; subscribe form has nowhere to send
- [x] **25. Font reduction** — more than 2 font families loading; audit and cut to ≤2 per performance rules
- [x] **26. focus-visible — missing** — keyboard focus rings absent or invisible; fails WCAG 2.1 AA
- [ ] **27. aria-label on nav** — `<nav>` element missing `aria-label="Main navigation"`
- [x] **28. Heading hierarchy** — `<h2>` or `<h3>` used before `<h1>` on some pages; fix ordering
- [ ] **29. Broken post links** — several post card hrefs resolve to 404; fix slugs or remove cards
- [ ] **30. CLS from dynamic content** — layout shifts detected when hero or post images load without explicit dimensions; add `width` + `height`

---

## Sprint 3 — This Quarter (Priorities 31–39+)

- [x] **31. Three.js tree-shake** — full Three.js bundle imported; import only used modules to cut JS size
- [x] **32. Hero human hook** — hero headline is abstract/generic; rewrite with specific, human, conversational angle
- [x] **33. Archive page** — no `/archive` or `/posts` index listing all articles; add one for discoverability
- [x] **34. Hero polygon replacement** — Three.js polygon visual is generic; replace with something distinctly Sachin
- [ ] **35. Grain texture** — design system calls for grain/atmosphere; not applied consistently across sections
- [x] **36. Mobile slam typography** — "it's unfair." slam text overflow still present at some breakpoints; verify fix across 320–768px
- [x] **37. S2 static-first state** — S2 section uses JS-dependent state; ensure static/no-JS version renders correctly
- [ ] **38. Cross-post links** — no "you might also like" or related-post links at bottom of posts; add navigation
- [x] **39. Real CWV analytics** — CrUX / Cloudflare Analytics not configured; can't track real Core Web Vitals improvements

---

- [x] **40. BreadcrumbList JSON-LD** — added to all 8 posts; Google can surface breadcrumb rich results
- [x] **41. Reading progress bar** — red bar at top of every post, tracks scroll through article
- [x] **42. Submit sitemap to Search Console** — user action required (no API; must be done in browser)
- [x] **43. Pagefind search** — static index (31 files, 16 pages, 2556 words); brand-matched UI (red accent, square corners, JetBrains Mono); loads from GitHub Pages origin, no CDN
- [x] **45. X handle site-wide** — @sachinrai → @sachinrai01 across nav, footer, twitter:site meta on index, archive, about, tools
- [x] **44. Cookie consent banner** — needed before EU traffic matters

## Completed

*(move items here when done)*

---

## Notes

- Blog files: `/Volumes/ORICO/Claude/blog-deploy/` (deployed) · `/Volumes/ORICO/Claude/blog/` (working copy)
- Audit date: 2026-05-11
- Audited file: `index.html` + all linked assets
- Tell Claude "mark #N complete" or paste a list and it will update this file
