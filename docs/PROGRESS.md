# Progress (living document - read this first in any new session)

## Structure
`index.html`, `work/ services/ about/ contact/ projects/<name>/`, Greek mirror in `el/`, `404.html`, `css/styles.css`, `js/{main,fx,preview,projects,site-config}.js`,
`demos/{olive-and-oak,the-cut,nexora}/index.html` (each demo is ONE self-contained file with hash-based pages), `assets/`, `images/` (empty),
`sitemap.xml robots.txt _headers`, `README.md`, `TEST-REPORT.md`, `IMAGE-SOURCES.md`, `test-report/screenshots/`.

## How this site is maintained
The original generator scripts no longer exist. Edit the files in this folder directly; they are the source of truth.

## Done
- Agency site in English AND Greek: redesigned homepage (animated word-by-word headline, cursor-reactive hero depth, magnetic buttons, tilting project previews, price-card light, scroll progress bar, solid sticky header, industries marquee, animated counters, filling timeline, one-person section, pricing, FAQ, closing CTA). Motion is off for reduced-motion visitors; pointer effects need a real mouse; nothing essential is hidden without JavaScript.
- Pricing (EUR, provisional) in both languages, quote CTAs, central contact settings (`js/site-config.js`), central project registry (`js/projects.js`), preview modal (real iframe, desktop 1280 / phone 390, no reload on switch, loading + unavailable states). The preview passes the page language to the demo (`?lang=el` plus a postMessage), so a Greek visitor previewing Nexora sees Greek.
- Olive & Oak (English): homepage, 18-dish menu with filters, 8-step reservation, FAQ.
- THE CUT (English): homepage, services with durations, barbers, before/after slider, FAQ, 8-step booking with live price/duration.
- Nexora (English + Greek, working language switcher): homepage, services, illustrative case studies, labelled sample testimonials, 8-question FAQ, 7-step enquiry with live summary, switching language mid-enquiry keeps what you typed.

## Latest fixes
- Mobile menu: the "Get a quote" button showed as a blank light square (ivory text on ivory). Fixed.
- Phone homepage headline broke one word per line (a CSS class name clash with the two-column `.split` layout). Renamed to `wsplit`.
- Greek project pages now open the Greek demo. The claude.ai test copy opens demos full-screen in the page (a sandboxed page cannot open blob: links).
- Olive & Oak and THE CUT are now English + Greek: an EN | ΕΛ switcher, ?lang=el, and they follow the portfolio language in previews. A translation layer at the bottom of each demo file holds the Greek dictionary; add a line there when you add text.


## Contact, WhatsApp, calculator, build stories (latest)
- Real contact details on every page: pndigitalwebsites@gmail.com and +357 94426190 (also js/site-config.js). The "service area" row and setting were removed; the contact page says P&N works online.
- WhatsApp: a floating button on every agency page (bottom left; the AI chat stays bottom right), plus WhatsApp, Email and Phone cards on the contact page.
- Contact form (EN/EL) with validation. "Send on WhatsApp" and "Send by email" open the visitor's own app with the message ready. Nothing is sent or stored by the site, and no outside form service is used.
- Quote calculator on Services (#quote), linked from the homepage pricing. It only uses the published prices (Starter €250, Business €450, Premium from €750, maintenance €50/month) and the language counts. Extra languages, integrations and the AI assistant show as "quoted separately". The estimate can be sent on WhatsApp, by email, or carried into the contact form.
- "How we built it" on all six project pages: a wireframe/finished comparison slider (screenshots in images/build/, the wireframe is generated from the real page), five measured stats and a six-step build story. Stats come from the demo files; re-measure if a demo changes.
- Social share image (assets/og/og-en.jpg, og-el.jpg, 1200×630) on every page. It only works once the real domain replaces pn-digital.example in the og:image and canonical tags.

## Language guarantee
- Homepage and Services (English and Greek) now have a "Language guarantee" section: websites in any language, including right-to-left languages, with a scrolling strip of language names in their own scripts (stops for reduced-motion users).
- Each package lists its languages: Starter up to 2, Business up to 3, Premium up to 5 (all of the client's choosing), Maintenance covers every language on the site. Extra languages are "quoted separately" with no published price. These counts were proposed by Claude and can be changed in the four page files and in ai-assistant/businesses/pn-digital.json.
- Homepage FAQ and the P&N assistant's knowledge say the same thing. The "Plan my website" flow now has a "Three or more languages" option, which moves a one-page plan up to Business.

## AI assistants (this round)
- One shared widget (`assets/assistant/assistant.js`) and one public pack per business (`assets/assistant/packs/`), on every agency page and in all three demos, in English and Greek.
- It runs in clearly labelled DEMO MODE: answers come only from the website's own information and nothing is sent. Real AI needs the separate engine (ai-assistant zip) deployed with an API key, which needs your approval and has usage costs. Steps: ai-assistant/README.md.
- To change what an assistant knows, edit ai-assistant/businesses/<id>.json and run `node tools/export-public.mjs`; do not edit the packs by hand.
- The P&N Digital assistant is set to Google Gemini 3.5 Flash-Lite (free tier), capped at 400 requests a day. Its live-mode note says Google may keep messages. The three demo assistants stay on Claude (paid) and remain in demo mode until a Claude key is added. Nothing is switched on yet: it needs a Gemini key and a Cloudflare account, both with your approval.

## NOT done
- Owner decision (2026-11-23): no founder photo. The photo placeholder and its note were removed from the "One person" section (EN + EL); the section is now one column. The owner is a native Greek speaker and will review the Greek.
2. Pictures and reviews for the agency site (drawn mockups and a placeholder founder photo are used). No real photography (no internet in the build environment). Real reviews must come from real clients.
3. Native-speaker review of all Greek. Prompt extras: browser toolbar in the preview modal, Open Graph image, real domain and contact details, Cloudflare deployment (needs your login and approval).

## Tests
See `TEST-REPORT.md`: 1,269 checks, all passing in the final run, in real Chromium. Not tested: real touch devices, other browsers, the deployed site.

## Exact next steps
1. Greek for Olive & Oak, then THE CUT (Nexora pattern, leak detector, test inside Greek previews).
2. Pictures and reviews (needs internet or user-supplied licensed photos; sample reviews labelled fictional).
3. Native-speaker Greek review; then deployment with approval.
4. Re-run every suite and update this file.
