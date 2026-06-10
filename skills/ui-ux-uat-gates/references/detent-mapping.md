# Detent concepts mapped to GSD

This mapping adapts local Detent-main methodology without importing its harness.

## Core mapping

| Detent concept | GSD-native equivalent |
|---|---|
| STYLE_PICK | `STYLE_PICK.md` artifact |
| DESIGN_DNA | `DESIGN_DNA.md` artifact |
| COMPONENT_PLAN | `COMPONENT_PLAN.md` artifact |
| browser-verification-checklist | `UI_VERIFY.md` artifact |
| gate-verdict | UI gate verdict in task/slice verification |
| final_gate.py | pre-completion validation workflow |
| audit.py | lightweight anti-slop checks |
| skill-router | existing GSD skill routing policy |
| Detent citations in code | GSD artifact evidence, not production comments |

## 15 style rows

| Style | Best for | Gate implication |
|---|---|---|
| `brutalism` | bold campaign energy | forbid safe SaaS cyan/purple defaults |
| `cinematic-product` | immersive product launches | require reduced-motion path for cinematic motion |
| `dark-luxe` | moody premium surfaces | forbid gaming/electric-blue drift |
| `dashboards` | dense SaaS/admin/operator UI | block cinematic scroll runtimes by default |
| `editorial-premium` | typographic/story-led premium pages | warn on teal/cyan CTA over cream editorial palette |
| `gallery-minimal` | image-led portfolios/showcases | require image/media evidence when promised |
| `industrial-design` | technical overlays/engineering precision | cyan only as small signal accent, not primary wash |
| `minimalism` | calm restrained clarity | warn on saturated accent overload |
| `monochrome-modern` | high-contrast reduced systems | block saturated chromatic accents unless explicit |
| `premium-bento` | modular feature storytelling | bento must not become entire page grid by default |
| `quiet-luxury` | understated premium services | warn on wellness teal/electric blue clichés |
| `soft` | friendly consumer interfaces | avoid weak blurry generic softness |
| `soft-brutalism` | playful bold product/culture UI | avoid safe-modern teal drift |
| `swiss-system` | rational grid-led systems | require grid/typographic rigor |
| `warm-modern` | warm polished services/lifestyle | warn on cold teal/cyan/electric blue inversion |

## Component and motion rules

- Router first, catalog second: decide components before reading deep component references.
- Templates are references, not finished components.
- External component patterns require kept/dropped/added adaptation notes.
- At most two external UI library tracks per task.
- Magic UI max 4 per page and restricted to data-display on utilitarian surfaces.
- GSAP max 4 plugins and blocked on dashboards/app-shell/docs/settings/internal tools unless explicitly requested.
- Lenis never-fire on utilitarian surfaces.
- Do not mix GSAP/ThreeJS with Framer Motion in the same component tree.
- ShadCN customization must alter real axes: color, radius, typography, shadow/depth, motion, variants, micro-detail.
