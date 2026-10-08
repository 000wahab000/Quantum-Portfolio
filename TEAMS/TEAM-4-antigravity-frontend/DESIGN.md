# Design: "Sunset Navy" palette (dark theme, chosen by the team)

Read this before PROMPT-1. Every colour in the app comes from this file.

| Token | Hex | Use |
|---|---|---|
| `--color-ink` | #161E2F | page background |
| `--color-panel` | #242F49 | cards, form panels, header |
| `--color-line` | #384358 | borders, gridlines, disabled, muted fills |
| `--color-peach` | #FFA586 | primary accent: Run button, QAOA series, links, focus ring, "optimal" bars |
| `--color-red` | #B51A2B | infeasible bars, error banners (fill only), cancel button |
| `--color-wine` | #541A2E | hover or pressed state of red; danger panel background |
| `--color-text` | #F4EFEA | main text (derived; not in the image) |
| `--color-muted` | #A9B3C9 | secondary text, axis labels (derived) |
| `--color-slate` | #8FA3C8 | feasible-but-not-optimal bars, relaxation series (derived) |

**Hero band:** the page header uses the image's gradient, top to bottom: #541A2E → #B51A2B → #FFA586 → #384358 → #161E2F. It may also run left to right on a thin bar. Use it only in the header, never behind body text.

**Chart series (fixed for every chart and the frontier):**

| Series | Colour |
|---|---|
| QAOA standard | #FFA586 |
| QAOA XY | #FFD2C2 |
| Brute force (exact) | #F4EFEA |
| Relaxation | #8FA3C8 |
| Simulated annealing | #C9566A |
| NIFTY 50 benchmark | #A9B3C9, dashed |

**Bitstring histogram:** optimal #FFA586, feasible #8FA3C8, infeasible #B51A2B. Add a legend that says each one in words.

**Contrast rules:**
- Text sits only on ink or panel, in text, muted or peach.
- Never put red #B51A2B text on navy (contrast too low). For error text use #FF8A8A on #541A2E.
- Every colour meaning also has a text label or icon, so colour is never the only signal.

**Shapes:** rounded-2xl cards (the pill shapes in the image), soft shadow `0 10px 30px rgb(0 0 0 / .35)`, 16px mobile side gutter, system font stack.

**Tailwind v4:** declare tokens in `@theme { --color-ink: #161E2F; ... }` in `src/index.css` after `@import "tailwindcss";`, then use classes like `bg-ink`, `bg-panel`, `text-peach`.
