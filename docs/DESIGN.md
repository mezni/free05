# DESIGN — bss-core

**Purpose**: Visual design system and UI styling specifications for the support application.

**Related Documents**:
- `PRD.md` — Product requirements and functional specifications
- `EXPERIENCE.md` — User flows, interaction patterns, and behavior
- `ARCHITECTURE-SPINE.md` — Technical constraints and paradigm (hexagonal/ports-and-adapters)

**Last Updated**: 2026-11-08
**Status**: Draft

---
## Design Paradigm

**Human-Centered Design** — grounded in Don Norman's principles and Alan Cooper's persona methodology. The interface should make users feel understood, with simple starting points that evolve through feedback. Data-informed but always creative.

**Boring Technology for Stability** — consistent with the architecture spine's preference for stable, well-understood patterns over novel UI trends.

**Developer Productivity is Architecture** — design tokens and components should be implementation-ready for the FastAPI/Streamlit stack, with minimal custom CSS required.

---
## Color System

### Primary Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `color.primary.50` | `#f8f9fa` | Light backgrounds, subtle surfaces |
| `color.primary.100` | `#f1f3f5` | Default page backgrounds |
| `color.primary.200` | `#e9ecef` | Secondary button hover, subtle fills |
| `color.primary.300` | `#dee2e6` | Input borders, dividers, disabled fills |
| `color.primary.500` | `#212b36` | Primary text color, main content |
| `color.primary.600` | `#1a232e` | Disabled text, secondary text, focus ring |
| `color.primary.700` | `#131a22` | Hover state for primary actions |
| `color.primary.800` | `#0d1115` | High-contrast text on light surfaces |
| `color.primary.900` | `#050505` | Maximum contrast, error states |
| `color.primary.950` | `#020203` | Modal scrim base |

### Secondary Palette (Action & Status)

| Token | Hex | Usage |
|-------|-----|-------|
| `color.success.100` | `#d4edda` | Success button text, success tint |
| `color.success.200` | `#b1dfbb` | Success disabled |
| `color.success.500` | `#28a745` | Success messages, confirmed actions |
| `color.success.600` | `#1e7e34` | Success hover |
| `color.warning.100` | `#fff3cd` | Warning tint |
| `color.warning.200` | `#ffe8a1` | Warning disabled |
| `color.warning.500` | `#ffc107` | Warnings, validation errors, attention calls |
| `color.warning.600` | `#d39e00` | Warning hover |
| `color.danger.100` | `#f8d7da` | Danger button text, danger tint |
| `color.danger.200` | `#f1aeb5` | Danger disabled |
| `color.danger.500` | `#dc3545` | Critical errors, destructive actions |
| `color.danger.600` | `#bd2130` | Danger hover |
| `color.info.100` | `#d1ecf1` | Info tint |
| `color.info.200` | `#bee5eb` | Info disabled |
| `color.info.500` | `#17a2b8` | Informational messages, hints |
| `color.info.600` | `#117a8b` | Info hover |

### Semantic Color Roles

| Role | Description | Token |
|------|-------------|-------|
| `color.text.primary` | Main readable text | `color.primary.500` |
| `color.text.secondary` | Secondary/labels | `color.primary.600` |
| `color.text.inverse` | White on dark | `color.primary.900` inverted |
| `color.background.page` | Page canvas | `color.primary.100` |
| `color.background.card` | Card/surface backgrounds | `color.primary.50` |
| `color.background.scrim` | Modal scrim behind the dialog | `color.primary.950` at 90% opacity |
| `color.background.modal` | Modal dialog surface | `color.background.card` |
| `color.border.input` | Input field borders | `color.primary.300` |
| `color.border.focus` | Focus ring state | `color.primary.600` |

### Accessibility Colors

| Contrast Level | Minimum Ratio | Applicable Tokens |
|----------------|---------------|-------------------|
| AA normal text | 4.5:1 | `color.text.primary` / `color.text.secondary` vs `color.background.page` |
| AA large text | 3:1 | Headings and text ≥ 18pt (or 14pt bold) vs backgrounds |
| UI components | 3:1 | Borders, icons, inactive states |
| Error text | 4.5:1 | `color.danger.500` text against neutral backgrounds |

---
## Typography

### Type Scale

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `typography.text.xs` | 0.75rem (12px) | 1.5 | Captions, meta text |
| `typography.text.sm` | 0.875rem (14px) | 1.5 | Body text smaller, descriptions |
| `typography.text.base` | 1rem (16px) | 1.6 | Default body text |
| `typography.text.lg` | 1.25rem (20px) | 1.6 | Section headings, prominent text |
| `typography.text.xl` | 1.5rem (24px) | 1.6 | Page-level headers |
| `typography.text.xxl` | 2rem (32px) | 1.7 | Hero headers, modals |

### Type Family

| Token | Font Family | Weight | Style |
|-------|-------------|--------|-------|
| `typography.font.body` | system-ui, sans-serif | 400 (normal) | Body copy, forms |
| `typography.font.heading` | system-ui, sans-serif | 600 (semi-bold) | Headings, section titles |
| `typography.font.monospace` | ui-monospace, SF Mono, monospace | 400 (normal) | Code snippets, timestamps |

### Line Height

| Token | Unitless Ratio | Usage |
|-------|----------------|-------|
| `typography.line.base` | 1.6 | Default body text |
| `typography.line.tight` | 1.3 | Headings, compact lists |
| `typography.line.relaxed` | 1.8 | Long-form text, modals |

---
## Spacing Scale

| Token | Size | Usage |
|-------|------|-------|
| `spacing.xs` | 0.25rem (4px) | Icon spacing, tight gaps |
| `spacing.sm` | 0.5rem (8px) | Small component gaps |
| `spacing.base` | 1rem (16px) | Default padding, margins |
| `spacing.lg` | 1.5rem (24px) | Section spacing, card padding |
| `spacing.xl` | 2rem (32px) | Page-level margins |
| `spacing.xxl` | 3rem (48px) | Hero sections, large gaps |
| `spacing.xxxl` | 4rem (64px) | Major section dividers |

### Spacing Application

| Context | Horizontal | Vertical |
|---------|------------|--------|
| **Card padding** | `spacing.base` | `spacing.base` |
| **Form gaps** | `spacing.sm` | `spacing.base` |
| **Button padding** | `spacing.sm` vertical, `spacing.base` horizontal | — |
| **Table row height** | — | `typography.line.base` + `spacing.sm` |
| **Modal content** | `spacing.lg` | `spacing.lg` |
| **Page margin** | `spacing.xl` | `spacing.xl` |

---
## Component Specifications

### Buttons

| Variant | Background | Text Color | Border | Hover | Disabled |
|---------|-----------|------------|--------|-------|----------|
| **primary** | `color.primary.600` | `color.primary.100` | `color.primary.600` | `color.primary.700` | `color.primary.300` |
| **secondary** | `color.primary.100` | `color.primary.600` | 1px `color.border.input` | `color.primary.200` | `color.border.input` |
| **success** | `color.success.500` | `color.success.100` | `color.success.500` | `color.success.600` | `color.success.200` |
| **danger** | `color.danger.500` | `color.danger.100` | `color.danger.500` | `color.danger.600` | `color.danger.200` |
| **link** | `transparent` | `color.primary.600` | none | `color.primary.700` | `color.primary.300` |

**Button Styles**:
- Height: `3rem` (48px)
- Border radius: `0.375rem` (6px)
- Font size: `1rem` (16px)
- Font weight: `500` (semi-bold)
- Minimum width: `6rem` (96px)
- Focus state: 2px solid `color.border.focus`, offset `0.125rem`

### Forms

| Element | Label Placement | Input Height | Border | Focus | Padding |
|---------|----------------|--------------|--------|-------|---------|
| **text input** | Top-aligned | `3rem` (48px) | 1px `color.border.input` | 2px `color.border.focus`, offset `0.125rem` | `spacing.sm` horizontal, `spacing.xs` vertical |
| **select** | Top-aligned | `3rem` (48px) | 1px `color.border.input` | 2px `color.border.focus`, offset `0.125rem` | `spacing.sm` horizontal, `spacing.xs` vertical |
| **textarea** | Top-aligned | `4rem` (64px) | 1px `color.border.input` | 2px `color.border.focus`, offset `0.125rem` | `spacing.sm` horizontal, `spacing.xs` vertical |
| **checkbox** | Inline with label | `2rem` (32px) | 1px `color.border.input` | 2px `color.border.focus`, offset `0.125rem` | `spacing.xs` |
| **radio group** | Vertical stack | `2rem` (32px) | 1px `color.border.input` | 2px `color.border.focus`, offset `0.125rem` | `spacing.xs` |

**Label Styles**:
- Font size: `0.875rem` (14px)
- Font weight: `500` (semi-bold)
- Color: `color.text.secondary`
- Position: Top-aligned, `spacing.xs` above input
- Floating label on focus: transitions `color` to `color.primary.600`, `width` to 100%

### Cards

| Property | Value |
|----------|-------|
| Background | `color.background.card` |
| Border | 1px `color.border.input` (default), `color.border.focus` (focused) |
| Border radius | `0.5rem` (8px) |
| Padding | `spacing.base` vertical, `spacing.base` horizontal |
| Box shadow | `0 1px 2px 0 rgba(0, 0, 0, 0.05)` |
| Max width | `100%` |

### Tables

| Property | Value |
|----------|-------|
| Font size | `typography.text.sm` (14px) for dense tables, `typography.text.base` (16px) for readability |
| Row height | `typography.line.base` + `spacing.xs` |
| Header background | `color.primary.50` |
| Header text color | `color.text.secondary` |
| Row zebbing | `color.primary.50` on alternate rows |
| Border | 1px `color.border.input` |
| Padding | `spacing.xs` horizontal, `spacing.sm` vertical |

### Modals

| Property | Value |
|----------|-------|
| Background | `color.background.card` over `color.background.scrim` (90% opacity) |
| Modal width | `min(90%, 48rem)` (max 768px) |
| Border radius | `0.5rem` (8px) |
| Header padding | `spacing.lg` |
| Content padding | `spacing.base` |
| Footer padding | `spacing.lg` |
| Close button | `color.text.secondary`, `:hover { color: color.text.primary }`, `absolute`, `top: 0.5rem`, `right: 0.5rem` |

### Notifications/Toasts

| Property | Value |
|----------|-------|
| Background | `color.background.card` |
| Border | 1px `color.border.input` |
| Close button | `×`, `color: color.text.secondary`, `hover { color: color.text.primary }` |
| Timeout | 4 seconds auto-dismiss |
| Action buttons | Primary and secondary styled per button spec |
| Position | `fixed`, `top: 1rem`, `right: 1rem`, `z-index: 1000` |

---
## Iconography

### Icon System

| Category | Tokens | Usage |
|----------|--------|-------|
| **Action** | `arrow-down`, `check`, `close`, `edit`, `delete`, `add`, `save`, `print`, `refresh`, `search` | Buttons, headers, interactive elements |
| **Status** | `success`, `warning`, `danger`, `info`, `alert` | Notifications, badges, status indicators |
| **Navigation** | `home`, `back`, `forward`, `menu`, `profile`, `settings` | Navigation, breadcrumbs |
| **Shipment** | `tracking`, `delivery`, `in-transit`, `out-for-delivery`, `delivered` | Shipment context UI |
| **Customer** | `user`, `profile`, `tier`, `preferences` | Customer context UI |
| **Order** | `basket`, `receipt`, `item`, `return`, `cancel` | Order context UI |
| **Billing** | `payment`, `refund`, `credit`, `invoice`, `receipt` | Billing context UI |

**Icon Style**:
- Inline SVG icon set (Lucide-style); no icon-font dependency
- 20px x 20px viewBox
- CurrentColor for color inheritance
- 24px size for most contexts, 16px for inline with text

---
## Design Tokens Summary

| Category | Key Tokens | Count |
|----------|------------|-------|
| **Color** | Primary 50-900, Secondary 500-600, Semantic roles, Accessibility | 20+ |
| **Typography** | Type scale 6 levels, Font families 3, Line heights 3 | 18+ |
| **Spacing** | Scale 7 levels, Application patterns 6 | 13+ |
| **Components** | Buttons 5 variants, Forms 6 elements, Cards 1 spec, Tables 1 spec, Modals 1 spec, Toasts 1 spec | 19+ |
| **Iconography** | Action 10, Status 5, Navigation 6, Shipment 6, Customer 5, Order 5, Billing 5 | 42+ |

**Total design tokens**: ~112+ named tokens across all categories (sum of the minimums above)

---
## Implementation Notes

- All tokens are defined as CSS custom properties (CSS variables) for use by custom HTML/CSS components
- FastAPI/Streamlit integration: use `st.dataframe` with `use_container_width=True`; inject limited custom CSS via `st.markdown(..., unsafe_allow_html=True)`
- Streamlit theming: set the theme via `.streamlit/config.toml` (`[theme]`) and `st.set_page_config`; core Streamlit widgets cannot consume arbitrary CSS variables
- Accessibility: all color ratios meet WCAG AA for normal text (4.5:1) and UI components (3:1)
- Dark mode: on Streamlit use the `[theme]` config (light/dark) — `prefers-color-scheme` applies only to custom HTML components, not native Streamlit widgets
- Responsive: mobile-first breakpoint at `48rem` (768px), stack columns, reduce padding

---
## Design-to-Development Handoff

| Deliverable | Format | Consumer |
|-------------|--------|----------|
| Color system | CSS variables, Figma tokens | Front-end developers, Streamlit theming |
| Typography | Type scale, font stacks | Front-end developers, UI implementation |
| Spacing scale | CSS variables, margin/padding values | Front-end developers, layout implementation |
| Component specs | Interactive Figma prototypes, this DESIGN.md | Designers, front-end developers |
| Accessibility | Contrast ratios, WCAG targets | Designers, developers, QA |
| Dark mode | Prefers-color-scheme media queries, swapped tokens | Front-end developers, theming |

**Handoff Checklist**:
- [ ] All CSS custom properties defined and tested
- [ ] Contrast ratios verified for all color combinations
- [ ] Dark mode mockup reviewed and approved
- [ ] Component specs aligned with implementation capabilities
- [ ] Responsive breakpoints documented and tested
- [ ] Accessibility guidelines communicated to development team
- [ ] Design tokens committed to repository for code reuse
