# Test report

All tests below ran in real Chromium (Playwright) in the final pass, after the last code change.

| Suite | Checks | Passed |
|---|---|---|
| Whole site: 17 pages EN/EL x 6 widths (1920-375), Greek leak scan, navigation, CTAs, mobile menu, previews (desktop/phone, no reload, Escape), "Open full website" (new tab, right language), all demos in both languages | 455 | 455 |
| Demo translation (Olive & Oak, THE CUT): switching mid-booking keeps choices, filters, live totals, Greek dates, previews follow site language | 50 | 50 |
| AI assistant widget: 23 questions across 4 businesses in EN/EL (desktop + phone), guided website plan, keyboard, screen-reader roles, phone layout, booking buttons never covered, LIVE mode through the real engine with a fake AI, missing key and unreachable engine | 180 | 180 |
| claude.ai test copy: "Open full website" opens the real demo full-screen (EN/EL, desktop/phone), back button, browser Back, menu button, assistant inside the copy | 64 + 8 | 64 + 8 |
| AI engine (Node, fake AI provider): isolation, injection, limits, daily cap, streaming, usage, CORS, errors | 16 | 16 |

Greek on every agency page and in both demos is checked by a detector that flags any English word
left in visible text or labels (brand names and common loanwords like SEO are allowed).

## Bugs found and fixed in this round
- Mobile menu "Get a quote" button showed as a blank light square (text and background both ivory).
- Phone homepage headline broke one word per line: a CSS class name clash (`split`), renamed `wsplit`.
- "Open full website" in the claude.ai test copy used blob: links that the sandbox blocks; it now opens the demo full-screen in the page. On the real site it opens /demos/... in a new tab (tested).
- Greek project pages opened the English demo.
- Demo translation: input labels were skipped; "Email" missing from the dictionary.
- Assistant: Greek word endings (επικοινωνώ vs επικοινωνία) did not match; "πότε" matched the drinks keyword; "Are you a real person?" not recognised; Greek package price said "from €750"; suggestion buttons squeezed the conversation on desktop.
- Olive & Oak phone hero: the plate illustration made the intro text hard to read.

## Not tested
- Real phones, Safari and Firefox; a deployed Cloudflare site.
- Real AI answers: no API key exists, so live mode was tested with a fake AI provider behind the real engine.
- Greek has not been reviewed by a native speaker.
