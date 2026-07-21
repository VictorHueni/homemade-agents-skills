---
type: rule
paths:
  - "**/*.vue"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/nuxt.config.*"
  - "**/app/**"
---

# Frontend (Nuxt UI v4 / Vue 3.5 / Reka UI)

## Component choice

- Prefer Nuxt UI v4 built-ins (`UAccordion`, `UTable`, `UPagination`, `USlideover`, `UInput`, `UBadge`, `UCard`, `UButton`) before writing custom components.
- For domain-specific layouts (cards, stat panels), compose Nuxt UI primitives; do not replace them.
- `UButton` with a `to` prop renders as `<a>` (role=link); without `to` it renders as `<button>` (role=button). In E2E tests, use `getByRole('link')` for navigation buttons and `getByRole('button')` for action buttons.

## SSR hydration (Reka UI 2.9.2 bug)

- All interactive Reka UI primitives must be wrapped in `<ClientOnly>`. Lazy hydration, `default-value`, `:unmount-on-hide`, and re-mount keys all fail to fix the underlying event-delegation reconnect bug.
- Every `<ClientOnly>` MUST have a `#fallback` slot, chosen by content type:
  - **Interactive widgets** (SearchBar, UButton toggles): render a `disabled` clone in `#fallback` — zero CLS, visually identical from first paint.
  - **Content-heavy sections** (UTabs with paragraphs, partner cards, legal text): render the actual default content as static HTML in `#fallback` — preserves SEO + LCP. Reference pattern: Nuxt UI's own `ColorModeSwitch.vue`.
- Non-interactive components (UBadge, UCard, UIcon) do not need `ClientOnly`.

## Event handling

- `UInput @focus`/`@blur` are unreliable during hydration and during Playwright `fill()` operations. Use `@focusin`/`@focusout` on a wrapper `<div>` and check `relatedTarget` + `contains()` in the handler to avoid false triggers when focus moves within the component.

## Error pages

- `clearError({ redirect })` does NOT navigate in dev mode when the Nuxt DevTools overlay is active. In E2E tests for error CTAs, assert button presence/enablement only; assert navigation only against production builds (`npm run build && npm run preview`).

## Number / date formatting (SSR-safe)

- Never use `toLocaleString()` / `Intl.NumberFormat` / `Intl.DateTimeFormat` in SSR-rendered templates. Node and browser ICU data may diverge → hydration mismatch (e.g. `U+2019` vs `U+0027` for Swiss thousands separator, or silent fallback to `en` if a locale is missing server-side).
- For single-locale formatting: use a manual deterministic formatter (regex-based string replacement; insert the typographic apostrophe `U+2019` directly).
- For multi-locale formatting: use `@nuxtjs/i18n` `useI18n().n()` which handles SSR serialization.
- Last resort: `data-allow-mismatch="text"` (Vue 3.5+) suppresses the warning but allows a visual flash.
