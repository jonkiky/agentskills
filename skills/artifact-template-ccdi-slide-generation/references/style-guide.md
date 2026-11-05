# CCDI visual style

Use this guide with the retained PowerPoint, not instead of inspecting it. Measurements below describe the bundled reference. If the user supplies a different template, inspect that template and follow it.

## Retained reference

- `../assets/reference.pptx`: unchanged copy of the user-provided **CCDI MCP Use Cases v4 (1).pptx**.
- `../assets/preview.png`: rendered first slide for the template preview.
- `../assets/layout-reference.png`: rendered interior diagram slide for visual styling only. Its text and subject are not default content.

The source contains 23 slides. That is a source property, not a slide-count requirement.

## Design tokens

| Element | Reference treatment |
| --- | --- |
| Canvas | 16:9, 13⅓ × 7½ inches; 1280 × 720 at 96 dpi |
| Type | Montserrat body; Montserrat SemiBold for titles and emphasis |
| Main blue | `#2D6483` for strong labels and takeaway strips |
| Medium blue | `#508BAC` for slide titles, number tabs, and connectors |
| Pale blue | `#E7F1F6` for light visual grouping |
| Blue border | `#C9DDE8` for fine rules and node outlines |
| Main text | `#343F47` |
| Secondary text | `#657381` |
| Green accent | `#4E8F72`, with `#E8F3ED` as the light fill |
| Background | White; `#F5F7F8` for occasional subtle contrast |

Use blue as the primary color and green for one meaningful distinction. Keep category meanings consistent throughout a deck and supplement color with labels. Retain original logo colors and proportions.

## Page structure

### Cover and section slides

Reuse the building photograph, blue overlay, and original white Frederick logo. Preserve the upper-left logo and right-side title composition. On the cover, retain the institutional header treatment while updating the title, subtitle, and date to the current request. Section and closing slides can reuse the same photographic treatment when they are needed.

### Content slides

Preserve the white background, blue number tab at the upper left, centered blue title, Frederick logo at the upper right, and thin horizontal rule below the header. The body should be more visual and less wordy than many of the original slides.

At the reference's 1280 × 720 coordinate scale:

- The number tab is approximately `x=0, y=30, w=72, h=39`.
- The title region is approximately `x=98, y=29, w=1018, h=50`. Typical title size is 25 px (18.75 pt).
- The header rule sits near `y=101`. Body content generally starts around `x=74, y=122` and extends to `x=1206`.
- Body text is commonly 17–21 px (12.75–15.75 pt), with stronger node headings around 23–25 px. Preserve the hierarchy, reduce wording, and give labels room.
- A bottom takeaway strip, when useful, is approximately `x=74, y=616, w=1132, h=62`, using white text on the main blue. The original also uses pale green for selected callouts. Omit a redundant takeaway instead of filling the strip with repeated text.

These are alignment guides, not mandatory boxes. Reclaim unused subtitle or callout space for the diagram. A question banner is optional content and should not appear merely because the original layout contains one.

## Choosing the visual

| Main idea | Useful visual form |
| --- | --- |
| Sequence or process | A flow diagram with short step labels and a clear start and outcome |
| Roles and handoffs | A small number of lanes, with actions placed by responsibility |
| System structure | A component diagram with explicit boundaries and labeled relationships |
| Options or differences | Aligned parallel diagrams or a concise comparison matrix |
| Change over time | A timeline or before-and-after visual with the same scale and structure |
| Selection or decision | A branching diagram, with conditions on the branches |
| Quantity or distribution | A data chart with units and a clearly stated population |
| Part-to-whole organization | A hierarchy or grouping diagram supported by the source |

Choose the form that explains the material. Do not force every slide into the same flow or box layout. Covers, brief dividers, or a simple numerical finding may need little or no diagram.

## Diagram treatment

Use restrained rounded rectangles or simple shapes for meaningful entities, thin blue connectors, pale blue fills, and a limited green accent. Keep arrows aligned and use orthogonal routing when it makes relationships easier to follow. Prefer left-to-right flow for short processes; use vertical flow when the content needs it. Label a connector when the relationship would otherwise be ambiguous.

Keep labels brief without replacing necessary terms with unexplained abbreviations. Use a small number of visually distinct groups and generous white space. Avoid shadows, 3D effects, dense panel grids, repeated ornamental icons, or paragraphs inside every node. Adapt the reference's diagram language to make the current idea easier to understand.
