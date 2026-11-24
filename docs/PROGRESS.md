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
- Social share image (assets/og/og-en.jpg, og-el.jpg, 1200×630) on every page. It uses the live address https://pn-digital-website.pages.dev in the og:image and canonical tags.

## Language guarantee
- Homepage and Services (English and Greek) now have a "Language guarantee" section: websites in any language, including right-to-left languages, with a scrolling strip of language names in their own scripts (stops for reduced-motion users).
- Each package lists its languages: Starter up to 2, Business up to 3, Premium up to 5 (all of the client's choosing), Maintenance covers every language on the site. Extra languages are "quoted separately" with no published price. These counts were proposed by Claude and can be changed in the four page files and in ai-assistant/businesses/pn-digital.json.
- Homepage FAQ and the P&N assistant's knowledge say the same thing. The "Plan my website" flow now has a "Three or more languages" option, which moves a one-page plan up to Business.

## AI assistants (this round)
- One shared widget (`assets/assistant/assistant.js`) and one public pack per business (`assets/assistant/packs/`), on every agency page and in all three demos, in English and Greek.
- It runs in clearly labelled DEMO MODE: answers come only from the website's own information and nothing is sent. Real AI needs the separate engine (ai-assistant zip) deployed with an API key, which needs your approval and has usage costs. Steps: ai-assistant/README.md.
- To change what an assistant knows, edit ai-assistant/businesses/<id>.json and run `node tools/export-public.mjs`; do not edit the packs by hand.
- The P&N Digital assistant is set to Google Gemini 3.5 Flash-Lite (free tier), capped at 400 requests a day. Its live-mode note says Google may keep messages. The three demo assistants stay on Claude (paid) and remain in demo mode until a Claude key is added. Nothing is switched on yet: it needs a Gemini key and a Cloudflare account, both with your approval.

## Published (2026-11-23)
- Website live on Cloudflare Pages: https://pn-digital-website.pages.dev (connected to GitHub; every push to `main` deploys).
- AI assistant engine deployed by the owner as the Worker `pn-digital-assistant` (https://pn-digital-assistant.tsiopou3.workers.dev) with the GEMINI_API_KEY secret. The P&N Digital chat is live; the three demos stay in demo mode (no Claude key). The USAGE KV namespace (400/day cap) is NOT set up yet.

## Hotel and salon demos, privacy page (2026-11-24)
- Two new demos, each one self-contained file with hash pages, English + Greek (EN | ΕΛ switcher, ?lang=el, follows the portfolio language in previews) and the AI widget:
  - Halcyon Bay, seaside hotel (`demos/halcyon-bay/`): rooms with view/feature filters and detail pop-ups, gallery pop-ups, experiences page with a sample day, 10-question FAQ, 7-step booking + confirmation with a month calendar (stays up to 14 nights), guests (max 4 per room), rooms that fit the group (some "not available" as demo data), rate (room only / B&B / half board, children under 12 half price), extras, details, review. The total appears once dates and a room are chosen.
  - Myrtle Beauty Studio, beauty salon (`demos/myrtle/`): treatment categories, treatment filters (category, under 1 hour, no patch test), add-ons, team with days off, a three-question treatment finder, gift vouchers (nothing sold), 10-question FAQ, 7-step booking + confirmation where add-ons and specialists follow the treatment, closed Sunday/Monday, patch-test reminders.
- Project pages (EN + EL) with "How we built it": images from `tools/wire.py`, stats from the new `tools/measure_demo.py`. The three older project pages were re-measured with the same tool (their demos had grown since: CSS rules and Greek strings changed slightly).
- Work page, homepage (now "five concept websites", counter 5, two new feature cards), previews (`js/projects.js`), sitemap, test copy builder and README updated. Next-project chain: Olive & Oak → THE CUT → Nexora → Halcyon Bay → Myrtle → Olive & Oak.
- Privacy page `/privacy/` + `/el/privacy/`, linked from every footer. It says only what the site really does: no cookies/analytics/trackers, the contact form and calculator open the visitor's own app, the quote estimate stays in the browser for one visit, Cloudflare hosting, the P&N chat uses the Gemini free tier (Google may keep messages, P&N stores nothing), demos send nothing, GDPR rights and the Cyprus data protection commissioner. Owner to confirm the sentence about keeping messages "for our business records".
- AI assistants: `halcyon-bay` and `myrtle` business files in the engine repo (rooms/rates/extras, treatments/add-ons/team, FAQs). The widget's demo mode answers rooms, rates, extras, treatment categories and "who does…" questions. Only businesses with `"live": true` (P&N Digital) get the engine address in their pack, so every demo stays in demo mode and sends nothing (before this, the first demo message went to the engine and came back "not switched on").

## NOT done
- Owner decision (2026-11-23): no founder photo. The photo placeholder and its note were removed from the "One person" section (EN + EL); the section is now one column. The owner is a native Greek speaker and will review the Greek, including the two new demos.
- Real client reviews and photos: only when real clients exist.
- The 400-a-day cap for the live chat needs the `USAGE` KV namespace (engine repo README, step 3).
- Optional: a custom domain instead of pn-digital-website.pages.dev; Google Business Profile and Search Console.

## Tests
`tests/`: test_site, test_contact_quote, test_demo_i18n (now includes a Greek sweep of every page and booking step of the two new demos), test_assistant, test_hosted. Engine: `cd ../pn-digital-ai-assistant/engine && npm test`. Not tested: real touch devices, other browsers, the live chat on the deployed site.

## Exact next steps
1. Owner: read the Greek of the new demos and pages and send corrections.
2. Owner: confirm the privacy page wording, then add the USAGE KV namespace for the daily cap.
3. Optional: custom domain, Google Business Profile, Search Console.
