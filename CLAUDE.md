# P&N Digital website — notes for Claude

The owner of P&N Digital (a web design studio in Cyprus) works on this repository with Claude Code. They are a
beginner with developer tools: explain commands and technical ideas in plain words, and ask few questions.

## The project
- The agency's own website and portfolio. Plain HTML, CSS and vanilla JavaScript. **No frameworks, no npm, no build step.**
- `public/` is the website and the only folder that gets published. Everything else (docs, tests, tools) stays private.
- Every page exists in English (`public/…`) and Greek (`public/el/…`). Any text change must be made in both.
- The five demos in `public/demos/` are single self-contained files with hash routing (`#home`, `#menu`, …). Their "How we built it"
  numbers come from `python tools/measure_demo.py`.
- **Light mode** (header button, `html[data-theme=light]` in `css/styles.css`, remembered in localStorage `pn-theme`) is
  permanent: the owner wants it kept whatever the style.
- **Style refresh** (deep blue, Manrope + Inter, self-hosted in `public/fonts/`) lives only in `css/refresh.css`. If the
  owner says **"revert"**, remove the `<link rel="stylesheet" href="/css/refresh.css">` line from every page (EN, EL, 404)
  and keep light mode; the old look is git tag `style-before-refresh` (local) / commit 1d22faa.
- `public/privacy/` (and `/el/privacy/`) must stay true: if the site adds cookies, analytics or an outside service, update it first.
- The AI assistant engine is a separate repository, `pn-digital-ai-assistant`, normally cloned next to this one.
  Its exporter writes `public/assets/assistant/packs/*.js` here. Do not edit the packs by hand.

## Rules (from the owner)
1. Never deploy, publish, buy a domain, change DNS, send emails, connect accounts or sign up for paid services without
   the owner's explicit approval in the conversation.
2. Never add a backend, database, login, API or server function without approval.
3. Never invent business information: no fake reviews, testimonials, clients, awards, prices, opening hours or results.
   Demo businesses must stay clearly labelled as fictional.
4. Never put API keys or secrets in this repository or in any website file.
5. Prices are fixed by the owner: Starter €250, Business €450, Premium from €750, Maintenance €50/month; languages
   included: Starter up to 2, Business up to 3, Premium up to 5; extra languages, integrations and the AI assistant
   are "quoted separately". They appear on the homepage, services page, `public/js/forms.js` and the assistant engine.
6. Keep pages fast, accessible (keyboard, focus, contrast, reduced motion) and working on phones (check 375–390 px wide).
7. Contact: pndigitalwebsites@gmail.com, +357 94426190 (WhatsApp too). Set in `public/js/site-config.js` and in the pages.

## Checking work
Run the browser tests after changes (see README → Tests). `tests/test_site.py` includes a check that flags English
text left on Greek pages. Look at the result in a browser at phone and desktop sizes before saying something is done.

## Still to do
See `docs/PROGRESS.md`. The site is live on Cloudflare Pages at `https://pn-digital-website.pages.dev`; every push to `main`
goes live, so only push to `main` with the owner's approval. Remaining: an optional custom domain, and real client reviews
when available. The owner is a native Greek speaker and checks the Greek; no founder photo (owner's decision).
