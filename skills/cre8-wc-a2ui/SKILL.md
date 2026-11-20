---
name: cre8-wc-a2ui
description: 'The cre8-wc web component catalog (https://cre8.dev/a2ui/v1_0/catalogs/cre8-wc/3.0.1)
  for A2UI v1.0: every component''s signature, plus worked examples. Use when generating
  cre8 UIs with A2UI Express.'
---

## Positional Component Signatures

Use these exact positional signatures to instantiate components. Do not output property keys:
• Cre8Accordion(items?, borderType?, hasDivider?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-accordion> — The component is a vertically stacked list of headers that reveal or hide sections of related content on a page.
  - items: Panels for a data-driven accordion.
  - borderType: borderType Must be one of: 'rectangle', 'rounded-bottom', 'rounded', 'none'
  - hasDivider: When it is true, the inner dividers are displayed;
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8AccordionItem(size?, heading?, isActive?, iconBefore?, tertiaryIcon?, headingTagVariant?, brandHeader?, accordionItemId?, slot_default?, slot_heading?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-accordion-item> — The accordion item component delivers large amounts of content in a small space
  - size: Users can choose between two header sizes:  'sm' [title-default] or 'lg' [title-large]. Must be one of: 'sm', 'lg'
  - heading: Controls the text content of the Accordion Item heading.
  - isActive: When true, the Accordion Item is opens, when false it closes;
  - iconBefore: Controls the positioning of the dropdown icon in relation to the text, true puts the icon before the text
  - tertiaryIcon: Controls the appearance  of dropdown icon as being an icon-only button.
  - headingTagVariant: Purely meant to help the user structure the HTML page hierarchy. Must be one of: 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
  - brandHeader: Controls whether the header takes on the theme's 'brand-strong' color
  - accordionItemId: Optional custom id for the accordion item, if one is not set, a random id is generated for you.
  - slot_default: A list of components for the "default" slot, even if there is only one. The body of the accordion item will be any valid html
  - slot_heading: A list of components for the "heading" slot, even if there is only one. Custom heading content, used when the `heading` property is not set.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Alert(status?, variant?, emphasis?, dismissed?, iconAlert?, iconTitle?, headerText?, ctaBody?, notDismissible?, slot_default?, slot_cta?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-alert> — The general purpose of an alert or notification is to draw the user’s attention
  - status: The alert type. Must be one of: 'error', 'info', 'notification', 'neutral', 'warning', 'success'
  - variant: The alert variant. Must be one of: 'standalone', 'banner'
  - emphasis: The alert emphasis. Must be one of: 'subtle', 'strong'
  - dismissed: Dismissed property
  - iconAlert: Overrides the default status icon.
  - iconTitle: Icon title used for the icon alt text
  - headerText: The alert heading text.
  - ctaBody: Text content for the call-to-action area.
  - notDismissible: Dismissable property
  - slot_default: A list of components for the "default" slot, even if there is only one. The alert body content
  - slot_cta: A list of components for the "cta" slot, even if there is only one. Container for a call-to-action button or link
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Badge(text?, status?, variant?, svg?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-badge> — Status badges are used most often in tables or fat rows in a list.
  - text: The badge text
  - status: Status (a color variant prop) Must be one of: 'error', 'info', 'warning', 'success', 'attention'
  - variant: Background Style Variant Must be one of: 'light', 'white'
  - svg: SVG as a raw string
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Band(variant?, fullHeight?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-band> — Band component.
  - variant: Gradient variant
  - fullHeight: Full height variant
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Breadcrumbs(items?, navAriaLabel?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-breadcrumbs> — The breadcrumbs component is a secondary navigation pattern that helps a user understand where the user is located.
  - items: Crumbs for a data-driven trail.
  - navAriaLabel: aria-label attribute to designate at name for the nav.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8BreadcrumbsItem(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-breadcrumbs-item> — Breadcrumbs Item component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Button(text?, variant?, neutral?, inverse?, href?, target?, rel?, svg?, size?, loading?, type?, name?, disabled?, required?, value?, iconName?, iconRotateDegree?, iconFlipDirection?, iconPosition?, hideText?, fullWidth?, loadingComplete?, ariaLive?, splitButtonType?, buttonAriaExpanded?, isError?, isSuccess?, slot_before?, slot_after?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-button> — The size and state of buttons on the screen serve as visual cues for the user
  - text: The button text.
  - variant: Style variant Must be one of: 'primary', 'secondary', 'tertiary'
  - neutral: This property is for a neutral button propery mainly used for the secondary or tertiary button variant.
  - inverse: Inverse attribute
  - href: Provide this property if you intend to use button styles for an anchor tag (`<a>`).
  - target: Target attribute for a link if providing `href` to style a link as a button Must be one of: '_blank', '_self', '_parent', '_top'
  - rel: Rel if this is an <a> element - this swaps <button> for <a>
  - svg: svg as a raw string
  - size: Size variants add another way to increase or decrease visual priority of a button. Must be one of: 'sm', 'lg', 'md'
  - type: Type of button. Must be one of: 'button', 'submit', 'reset'
  - name: The name of the form field
  - disabled: Disabled attribute
  - required: Whether the field is required
  - value: The value of the form field.
  - iconName: Deprecated: iconName, use svg instead
  - iconRotateDegree: iconRotateDegree is used for <cre8-icon> to set the arrow in the correct direction
  - iconFlipDirection: iconFlipDirection is used for <cre8-icon> to set the icon in the correct direction
  - iconPosition: Icon position. Must be one of: 'before', 'after'
  - hideText: Visually hide button text.
  - fullWidth: Full width button
  - ariaLive: Controls whether your loading status update to voiceover users will occur Must be one of: 'polite', 'assertive'
  - splitButtonType: These two subvariants of the split button style the two seperate buttons to style as a singular button Must be one of: 'text', 'caret'
  - buttonAriaExpanded: Button aria expanded attribute
  - isError: Whether the field is in an error state
  - isSuccess: Whether the field is in a success state
  - slot_before: A list of components for the "before" slot, even if there is only one. Content rendered before the button text, such as an icon
  - slot_after: A list of components for the "after" slot, even if there is only one. Content rendered after the button text, such as an icon
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8ButtonGroup(orientation?, gap?, fullWidth?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-button-group> — Button Group component.
  - orientation: Responsive Button Group (for modals)
  - gap: Gap between buttons
  - fullWidth: Stretch button group to fill its container width
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Card(variant?, align?, fullHeight?, slot_default?, slot_header?, slot_footer?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-card> — The card component acts a general container element sectioned off by slots: `header`, `body`, `footer`.
  - variant: Style variants Must be one of: 'bare', 'compact', 'horizontal', 'horizontal-bare'
  - align: Alignment variant
  - fullHeight: Full height
  - slot_default: A list of components for the "default" slot, even if there is only one. The card's body content
  - slot_header: A list of components for the "header" slot, even if there is only one. (Optional) Content in the card's header
  - slot_footer: A list of components for the "footer" slot, even if there is only one. (Optional) Content in the card's footer
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Chart(type?, width?, height?, maintainAspectRatio?, responsive?, loading?, ariaLabel?, showLegend?, legendPosition?, enableAnimation?, animationDuration?, data?, options?, colors?, on_chart_click? (static), on_chart_hover? (static), on_chart_ready? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-chart> — A flexible chart component built on Chart.js that supports multiple chart types
  - type: The type of chart to render. Must be one of: 'line', 'bar', 'pie', 'doughnut', 'radar', 'polarArea', 'bubble', 'scatter'
  - width: Width of the chart container in pixels.
  - height: Height of the chart container in pixels.
  - maintainAspectRatio: Whether the chart should maintain aspect ratio when resizing.
  - responsive: Whether the chart should be responsive to container size.
  - loading: Display a loading indicator instead of the chart.
  - ariaLabel: Accessible label for the chart.
  - showLegend: Whether to show the legend.
  - legendPosition: Position of the legend. Must be one of: 'top', 'bottom', 'left', 'right'
  - enableAnimation: Whether to animate chart updates.
  - animationDuration: Animation duration in milliseconds.
  - data: The chart data including labels and datasets.
  - options: Chart.js configuration options.
  - colors: Default colors for datasets (uses cre8 design token colors).
  - on_chart_click: Fires on the "chart-click" event.
  - on_chart_hover: Fires on the "chart-hover" event.
  - on_chart_ready: Fires on the "chart-ready" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8CheckboxField(label?, items?, name?, fieldNote?, ariaDescribedBy?, fieldNoteIconName?, fieldNoteKnockout?, fieldNoteIsSuccess?, fieldNoteIsError?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-checkbox-field> — Checkbox Field is the parent container for `checkbox-field-item`.
  - label: Checkbox container legend label
  - items: Checkboxes for a data-driven field.
  - name: Form control name shared by every generated item.
  - fieldNote: Checkbox container fieldnote
  - ariaDescribedBy: Checkbox container fieldnote aria describe by
  - fieldNoteIconName: Checkbox container fieldnote icon name
  - fieldNoteKnockout: Checkbox container fieldnote knockout
  - fieldNoteIsSuccess: Checkbox container fieldnote isSuccess
  - fieldNoteIsError: Checkbox container fieldnote isError
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8CheckboxFieldItem(label?, checked?, name?, disabled?, required?, value?, errorText?, errorNote?, successText?, successNote?, fieldId?, fieldNote?, ariaDescribedBy?, validationAriaDescribedBy?, fieldNoteIconName?, isError?, isSuccess?, type?, slot_fieldNote?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-checkbox-field-item> — Checkbox Field Item is the combination of a checkbox input, label and field note.
  - label: The checkbox label
  - checked: Checked State
  - name: The name of the form field
  - disabled: Disabled State
  - required: Required property
  - value: The value of the form field.
  - errorText: Visually hidden text that always signifies that this is an error for screen reader usage
  - errorNote: The error field note that appears below the default field note
  - successText: Visually hidden text that always signifies that this is successful for screen reader usage
  - successNote: The success field note that appears below the default field note
  - fieldId: Checkbox FieldId
  - fieldNote: Checkbox FieldNote
  - ariaDescribedBy: Checkbox fieldnote ariaDescribeBy
  - validationAriaDescribedBy: Additional aria-describedby connection to id for additional success and error notes to be accessible
  - fieldNoteIconName: Checkbox fieldnote icon name
  - isError: Changes the component's treatment to represent an error state
  - isSuccess: Changes the component's treatment to represent a success state
  - type: The type of form control (text, checkbox, radio, etc.)
  - slot_fieldNote: A list of components for the "fieldNote" slot, even if there is only one. Container for optional field note content
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Container(type?, name?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-container> — `cre8-container` establishes a CSS containment context so anything slotted
  - type: Containment type Must be one of: 'inline-size', 'size', 'normal'
  - name: Container name
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8ContainerGrid(variant?, gap?, break?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-container-grid> — `cre8-container-grid` is `cre8-grid`'s layout vocabulary - stacked to
  - variant: Style variant Must be one of: 'side-by-side', '2up', '3up', '1-3up', '4up', '1-4up', '1-2-4up', '2-4-6up'
  - gap: Style variant Must be one of: 'sm', 'lg', 'none'
  - break: Break variant Must be one of: 'faster', 'slower'
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8DangerButton(text?, variant?, href?, target?, rel?, svg?, size?, loading?, inverted?, type?, name?, disabled?, required?, value?, iconRotateDegree?, iconFlipDirection?, iconPosition?, hideText?, fullWidth?, loadingComplete?, ariaLive?, buttonAriaExpanded?, isError?, isSuccess?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-danger-button> — The size and state of buttons on the screen serve as visual cues for the user
  - text: The button text.
  - variant: Style variant Must be one of: 'primary', 'secondary', 'tertiary'
  - href: Provide this property if you intend to use button styles for an anchor tag (`<a>`).
  - target: Target attribute for a link if providing `href` to style a link as a button Must be one of: '_blank', '_self', '_parent', '_top'
  - rel: Rel if this is an <a> element - this swaps <button> for <a>
  - svg: SVG raw string if including an icon within a button.
  - size: Size variants add another way to increase or decrease visual priority of a button. Must be one of: 'sm', 'lg'
  - inverted: Inverted colors Danger Button (onDark)
  - type: Type of button. Must be one of: 'button', 'submit', 'reset'
  - name: The name of the form field
  - disabled: Disabled attribute
  - required: Whether the field is required
  - value: The value of the form field.
  - iconRotateDegree: rotate is used for <cre8-icon> to set the arrow in the correct direction
  - iconFlipDirection: flip is used for <cre8-icon> to set the icon in the correct direction
  - iconPosition: Icon position. Must be one of: 'before', 'after'
  - hideText: Visually hide button text.
  - fullWidth: Full width button
  - ariaLive: Controls whether your loading status update to voiceover users will occur Must be one of: 'polite', 'assertive'
  - buttonAriaExpanded: Button aria expanded attribute
  - isError: Whether the field is in an error state
  - isSuccess: Whether the field is in a success state
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8DatePicker(autocomplete?, pattern?, placeholder?, label?, max?, min?, maxlength?, readonly?, type?, name?, disabled?, required?, value?, hasShortcuts?, fieldId?, fieldNote?, ariaLive?, ariaDescribedBy?, errorText?, errorNote?, validationAriaDescribedBy?, successText?, successNote?, isError?, isSuccess?, showCalendar?, slot_fieldNote?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-date-picker> — The Date Picker component renders a form group with label, control, help text and validation styling much
  - autocomplete: Autocomplete attribute that allows input to expect certain types of information.
  - pattern: Pattern attribute defines a regular expression to validate against input
  - placeholder: The placeholder text that appears inside the input
  - label: The label text for the date picker field.
  - max: The max attribute defines the maximum value that is acceptable and valid for the input containing the attribute.
  - min: The min attribute defines the minimum value that is acceptable and valid for the input containing the attribute.
  - maxlength: The maxlength is an integer above 0 that indicates the maximum allowed characters to be entered.
  - readonly: Readonly attribute
  - type: Type variants
  - name: The name of the form field
  - disabled: The disabled attribute on the input
  - required: The required attribute on the input
  - value: The value of the form field.
  - hasShortcuts: Quick Shortcuts Variant
  - fieldId: The unique id of the field
  - fieldNote: The text that displays below in text field input
  - ariaLive: Controls how the voiceover will experience the new information when field note changes, Must be one of: 'polite', 'assertive'
  - ariaDescribedBy: Used to connect the field note in text field to the text menu for accessibility
  - errorText: Visually hidden text that always signifies that this is an error for screen reader usage
  - errorNote: The error field note that appears below the default field note
  - validationAriaDescribedBy: Additional aria-describedby connection to id for additional success and error notes to be accessible
  - successText: Visually hidden text that always signifies that this is successful for screen reader usage
  - successNote: The success field note that appears below the default field note
  - isError: Changes the component's treatment to represent an error state
  - isSuccess: Changes the component's treatment to represent a success state
  - slot_fieldNote: A list of components for the "fieldNote" slot, even if there is only one. Container for optional field note content
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Divider(variant?, status?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-divider> — The divider component is a separator between sections of content or groups of items.
  - variant: Divider variants Must be one of: 'horizontal', 'vertical'
  - status: Status (a color variant prop) Must be one of: 'brand', 'knockout'
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Dropdown(items?, buttonText?, maxHeight?, dropdownWithLink?, open?, dropdownContent?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-dropdown> — The Dropdown menu itself is a container that can host multiple interactive items, commonly formatted as a list
  - items: Items for a data-driven dropdown.
  - buttonText: Dropdown header
  - maxHeight: Enables scrolling once content reached to specified height, the height should mention in px units, ex: 100px
  - dropdownWithLink: button text represents as a link
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8DropdownItem(ariaLabel?, children?, on_dropdown_item_select? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-dropdown-item> — The Dropdown item component is designed to be used with Dropdown component, each item represents a
  - ariaLabel: The accessible label for the item.
  - children: A list of child components, in order, even if there is only one.
  - on_dropdown_item_select: Fires on the "dropdown-item-select" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Feature(inverted?, imgSrc?, imgAlt?, aspectRatio?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-feature> — Feature component.
  - inverted: Inverted variant
  - imgSrc: Image source
  - imgAlt: Image alt text
  - aspectRatio: CSS aspect-ratio for the image (e.g.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Field(autocomplete?, pattern?, placeholder?, label?, max?, min?, maxlength?, readonly?, type?, name?, disabled?, required?, value?, fieldId?, fieldNote?, ariaLive?, ariaDescribedBy?, errorText?, errorNote?, validationAriaDescribedBy?, successText?, successNote?, isError?, isSuccess?, slot_fieldNote?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-field> — The Field component renders a form group with label, control, help text and validation styling.
  - autocomplete: Autocomplete attribute that allows input to expect certain types of information.
  - pattern: Pattern attribute defines a regular expression to validate against input
  - placeholder: The placeholder text that appears inside the input
  - label: The required label that appears above the input
  - max: The max attribute defines the maximum value that is acceptable and valid for the input containing the attribute.
  - min: The min attribute defines the minimum value that is acceptable and valid for the input containing the attribute.
  - maxlength: The maxlength is an integer above 0 that indicates the maximum allowed characters to be entered.
  - readonly: Readonly attribute
  - type: Type variants
  - name: The name of the form field
  - disabled: The disabled attribute on the input
  - required: The required attribute on the input
  - value: The value of the form field.
  - fieldId: The unique id of the field
  - fieldNote: The text that displays below in text field input
  - ariaLive: Controls how the voiceover will experience the new information when field note changes, Must be one of: 'polite', 'assertive'
  - ariaDescribedBy: Used to connect the field note in text field to the text menu for accessibility
  - errorText: Visually hidden text that always signifies that this is an error for screen reader usage
  - errorNote: The error field note that appears below the default field note
  - validationAriaDescribedBy: Additional aria-describedby connection to id for additional success and error notes to be accessible
  - successText: Visually hidden text that always signifies that this is successful for screen reader usage
  - successNote: The success field note that appears below the default field note
  - isError: Changes the component's treatment to represent an error state
  - isSuccess: Changes the component's treatment to represent a success state
  - slot_fieldNote: A list of components for the "fieldNote" slot, even if there is only one. Container for optional field note content
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8FieldNote(isError?, isSuccess?, iconName?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-field-note> — Field Note gives direction on how to fill out a form field and to alert users of form errors and successes.
  - isError: Changes the component's treatment to represent an error
  - isSuccess: Changes the component's treatment to represent a success
  - iconName: DEPRECATED: Icon name used for the icon before to the field note
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Footer(slot_default?, slot_top?, slot_bottom?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-footer> — Footer component.
  - slot_default: A list of components for the "default" slot, even if there is only one. The footer content
  - slot_top: A list of components for the "top" slot, even if there is only one. The top content (above the default slot)
  - slot_bottom: A list of components for the "bottom" slot, even if there is only one. The bottom content (below the default slot)
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Form(novalidate?, disabled?, controls?, values?, children?, on_form_submit? (static), on_form_reset? (static), on_form_invalid? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-form> — The form component groups form-associated Cre8 controls, aggregates their
  - novalidate: Skips aggregate validation on submit.
  - disabled: Disables every control in the form, for example while submitting.
  - controls: Every form-associated Cre8 control owned by this form, in document order.
  - values: The form's current values, derived from FormData.
  - children: A list of child components, in order, even if there is only one.
  - on_form_submit: Fires on the "form-submit" event.
  - on_form_reset: Fires on the "form-reset" event.
  - on_form_invalid: Fires on the "form-invalid" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8GlobalNav(inverted?, behavior?, navAriaLabel?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-global-nav> — Global Nav component.
  - inverted: Inverted variant
  - behavior: Behavior variant
  - navAriaLabel: aria-label attribute to designate at name for the nav.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8GlobalNavItem(text?, href?, iconName?, megaMenu?, isActive?, slot_default?, slot_itemBefore?, slot_itemAfter?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-global-nav-item> — Global Nav Item component.
  - text: Primary nav item text
  - href: Primary nav item href
  - iconName: Icon name
  - megaMenu: Append to the class name.
  - isActive: Append to the class name.
  - slot_default: A list of components for the "default" slot, even if there is only one. The label for the navigation item
  - slot_itemBefore: A list of components for the "itemBefore" slot, even if there is only one. Content rendered before the item label, such as an icon
  - slot_itemAfter: A list of components for the "itemAfter" slot, even if there is only one. Content rendered after the item label, such as an icon
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Grid(variant?, gap?, break?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-grid> — Grid component.
  - variant: Style variant Must be one of: 'side-by-side', '2up', '3up', '1-3up', '4up', '1-4up', '1-2-4up', '2-4-6up'
  - gap: Style variant Must be one of: 'sm', 'lg', 'none'
  - break: Break variant Must be one of: 'faster', 'slower'
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8GridItem(fullHeight?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-grid-item> — Grid Item component.
  - fullHeight: Full height
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Header(isActive?, slot_default?, slot_top?, slot_bottom?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-header> — Header component.
  - isActive: Is active state
  - slot_default: A list of components for the "default" slot, even if there is only one. The header content
  - slot_top: A list of components for the "top" slot, even if there is only one. Content rendered above the main header row
  - slot_bottom: A list of components for the "bottom" slot, even if there is only one. Content rendered below the main header row
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Heading(type?, inverted?, tagVariant?, brandColor?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-heading> — HTML headings are titles or subtitles that you want to display on a webpage.
  - type: Heading type Must be one of: 'display-default', 'display-small', 'headline-large', 'headline-default', 'headline-small', 'title-xlarge', 'title-large', 'title-default', 'title-small', 'label-large', 'label-default', 'label-small', 'meta-large', 'meta-default', 'meta-small'
  - inverted: Invert the color of the font from dark to light.
  - tagVariant: Dynamic tag name for the component Must be one of: 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
  - brandColor: Apply the brand color to the heading text.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Hero(align?, imgSrc?, imgAlt?, hasOverlay?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-hero> — Hero component.
  - align: Position variant. Must be one of: 'center', 'left', 'right', 'top-left', 'top-center', 'bottom-center', 'top-right', 'bottom-right'
  - imgSrc: Image source
  - imgAlt: Image alt text
  - hasOverlay: Renders a dark overlay between the background image and the content for legibility.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Icon(focusable?, name?, svg?, iconUrl?, iconTitle?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-icon> — <svg> is a web component, which can be used with any frontend framework and use any svg.
  - focusable: Focusable
  - name: Icon name (this method of passing in svgs is to be deprecated)
  - svg: Raw SVG markup to render.
  - iconUrl: Icon path
  - iconTitle: Icon Title, this string is used for the aira-label of the svg
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8InlineAlert(variant?, status?, iconName?, fullWidth?, iconTitle?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-inline-alert> — In cases when it is necessary to alert the user but a less strong message that cannot be dismissed is desired,
  - variant: Variant Must be one of: 'subtle', 'transparent'
  - status: Status Must be one of: 'error', 'info', 'neutral', 'warning', 'success', 'attention', 'help'
  - iconName: DEPRECATED: Icon name used for the icon before to the field note
  - fullWidth: Full width Inline Alert
  - iconTitle: Icon title used for the icon alt text
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Layout(variant?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-layout> — Layout component.
  - variant: Style variants
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8LayoutContainer(fullHeight?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-layout-container> — Layout Container component.
  - fullHeight: Full height variant
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8LayoutSection(behavior?, top?, fullHeight?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-layout-section> — Layout Section component.
  - behavior: Behavioral variants
  - top: Top style
  - fullHeight: Full height
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8LinelengthContainer(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-linelength-container> — Linelength Container component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Link(href?, rel?, target?, svg?, size?, inverted?, iconName?, iconRotateDegree?, iconFlipDirection?, iconPosition?, ctaIcon?, ctaLink?, noUnderline?, slot_default?, slot_badge?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-link> — Link Component are strictly used in the case where the component will take
  - href: Href attribute of the anchor tag
  - rel: Rel attribute of the anchor tag
  - target: Target attribute for a link (i.e. Must be one of: '_blank', '_self', '_parent', '_top'
  - svg: svg as a raw string
  - size: Size variant (default is medium) Must be one of: 'sm', 'lg'
  - inverted: Inverted colors Link (onDark)
  - iconName: DEPRECATED: Icon name, use svg instead
  - iconRotateDegree: iconRotateDegree is used for <cre8-icon> to set the arrow in the correct direction
  - iconFlipDirection: iconFlipDirection is used for <cre8-icon> to set the icon in the correct direction
  - iconPosition: Icon position Must be one of: 'before', 'after'
  - ctaIcon: Call To Action Icon
  - ctaLink: Call To Action Link
  - noUnderline: Link with no underline
  - slot_default: A list of components for the "default" slot, even if there is only one. The link text content
  - slot_badge: A list of components for the "badge" slot, even if there is only one. Container for an optional badge displayed alongside the link
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8LinkList(behavior?, inverted?, size?, spacing?, variant?, items?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-link-list> — Link List component.
  - behavior: Behavioral variant Must be one of: 'horizontal', 'responsive'
  - inverted: Inverted variant
  - size: Size variants
  - spacing: Spacing between link list items
  - variant: Style variants Must be one of: 'secondary', 'display'
  - items: Links for a data-driven list.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8LinkListItem(text?, href?, isActive?, slot_default?, slot_itemBefore?, slot_itemAfter?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-link-list-item> — Link List Item component.
  - text: The link text
  - href: The link URL
  - isActive: Active link
  - slot_default: A list of components for the "default" slot, even if there is only one. The default slot to put badges or other Components
  - slot_itemBefore: A list of components for the "itemBefore" slot, even if there is only one. Content rendered before the link text, such as an icon
  - slot_itemAfter: A list of components for the "itemAfter" slot, even if there is only one. Content rendered after the link text, such as an icon
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8List(variant?, spacing?, items?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-list> — List component.
  - variant: Style variants
  - spacing: Spacing variants Must be one of: 'condensed', 'padded'
  - items: Items for a data-driven list.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8ListItem(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-list-item> — List Item component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8LoadingSpinner(determinate?, inverse?, neutral?, label?, progress?, size?, buttonVariant?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-loading-spinner> — A loading spinner notifies the user that their request is being processed while the front end is retrieving data
  - determinate: Mode of the spinner, defaults to indeterminate.
  - inverse: Inverse property used for dark backgrounds.
  - neutral: Neutral property used for secondary neutral loading button.
  - label: Label to show along with progress indicator.
  - progress: Progress to display, between 0 and 100.
  - size: Size of the progress indicator and position of the label, if a label has been defined using the label property. Must be one of: 'large', 'small'
  - buttonVariant: Property that specifies which button variant is using the loading spinner Must be one of: 'primary', 'secondary', 'tertiary'
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Logo(href?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-logo> — Logo component.
  - href: Logo link
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Main(fullHeight?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-main> — Main component.
  - fullHeight: Full height variant
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Modal(status?, isActive?, utilityModalTitle?, notDismissible?, closeButtonText?, closeButtonIcon?, ariaLabel?, mapStatusToIconModal?, slot_default?, slot_header?, slot_footer?, on_modal_close? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-modal> — Modal component should be used in all modal situations.
  - status: Status Types Must be one of: 'error', 'info', 'warning', 'success', 'help'
  - isActive: Is Active attribute
  - utilityModalTitle: Utility Modal Heading (String)
  - notDismissible: Not dismissible modal
  - closeButtonText: Close Button Text
  - closeButtonIcon: Close Button Icon
  - ariaLabel: Modal Aria Label - This is required for accessibility and provides context of the entire modal!
  - mapStatusToIconModal: Maps modal icons and modal status variants to what the alt text of the related icon should be
  - slot_default: A list of components for the "default" slot, even if there is only one. The component content
  - slot_header: A list of components for the "header" slot, even if there is only one. Custom header content for the modal
  - slot_footer: A list of components for the "footer" slot, even if there is only one. Custom footer content for the modal
  - on_modal_close: Fires on the "modal-close" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8MultiSelect(items?, label?, disabled?, preselectedItems?, fieldId?, fieldNote?, ariaDescribedBy?, validationAriaDescribedBy?, isError?, errorNote?, isSuccess?, successNote?, selectedTagItems?, dropdownOpen?, slot_fieldNote?, on_multi_select_change? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-multi-select> — Multiselect is used when multiple options can be chosen from a static dropdown
  - items: The list of string items the user can choose in the dropdown
  - label: The required label that appears above the multiselect
  - disabled: The disabled attribute on the select
  - preselectedItems: The list of string items that are initially in the selected list of tags
  - fieldId: The unique id of the select
  - fieldNote: Optional field note text can be added to provide additional field guidance.
  - ariaDescribedBy: Used to connect the field note in text field to the text menu for accessibility
  - validationAriaDescribedBy: Additional aria-describedby connection to id for additional success and error notes to be accessible
  - isError: Changes the component's treatment to represent an error state
  - errorNote: The error field note that appears below the default field note
  - isSuccess: Changes the component's treatment to represent a success state
  - successNote: The success field note that appears below the default field note
  - slot_fieldNote: A list of components for the "fieldNote" slot, even if there is only one. Container for optional field note content
  - on_multi_select_change: Fires on the "multi-select-change" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8NavContainer(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-nav-container> — Nav Container component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8PageHeader(heading?, slot_default?, slot_titleAfter?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-page-header> — Page Header component.
  - heading: Page header title
  - slot_default: A list of components for the "default" slot, even if there is only one. The page header content
  - slot_titleAfter: A list of components for the "titleAfter" slot, even if there is only one. Content rendered after the heading text, inside the title element
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Pagination(display?, totalResults?, pageSize?, visiblePages?, hideLastAndFirstButtons?, currentPage?, elementDefinitions?, windowWidth?, buttons?, maxVisiblePages?, children?, on_pagination_change? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-pagination> — The Pagination component is used to split up a large amount of results
  - display: (optional) prop that allows for a compact and icon-only variant both Must be one of: 'compact', 'icon-only', 'default'
  - totalResults: Input the total number of elements are returned from consuming app e.g.
  - pageSize: how many elements will displayVariant per page, indicated by business to typically be 20
  - visiblePages: Controls how many page buttons are displayVarianted on the page
  - currentPage: The currently active page (1-based).
  - children: A list of child components, in order, even if there is only one.
  - on_pagination_change: Fires on the "pagination-change" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8PercentBar(value?, max?, disableActionLeft?, on_percent_bar_left_action_click? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-percent-bar> — The percent bar visually indicates a user's current progress and has a few features: a basic display bar with
  - value: The current step the user is on.
  - max: The total number of steps in the multistep process.
  - disableActionLeft: The action-left icon-only tertiary button in the percent bar controls can be disabled.
  - on_percent_bar_left_action_click: Fires on the "percent-bar-left-action-click" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Popover(heading?, position?, isVisibleOnScroll?, isDynamic?, isActiveDynamic?, isActive?, isRTL?, handleOnClickOutside?, removeActiveOnScroll?, removeActive?, slot_default?, slot_trigger?, slot_header?, slot_footer?, on_popover_open? (static), on_popover_close? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-popover> — The Popover is for progressive disclosure of relevant content often hidden behind a help or info icon.
  - heading: The heading text that appears at the top of the popover panel.
  - position: Positions the popover panel absolutely to the trigger Must be one of: 'top', 'left', 'right'
  - isVisibleOnScroll: Set to prevent the popover panel from hiding on scroll
  - isDynamic: The dynamic state for the popover
  - isActiveDynamic: The dynamic active state
  - isActive: The active state for the popover
  - isRTL: Query the document direction value
  - handleOnClickOutside: Handle click outside the component
  - removeActiveOnScroll: Remove Active State on Scroll
  - removeActive: Remove Active State
  - slot_default: A list of components for the "default" slot, even if there is only one. The component content
  - slot_trigger: A list of components for the "trigger" slot, even if there is only one. The element that toggles the popover open and closed
  - slot_header: A list of components for the "header" slot, even if there is only one. Custom header content for the popover panel
  - slot_footer: A list of components for the "footer" slot, even if there is only one. Custom footer content for the popover panel
  - on_popover_open: Fires on the "popover-open" event.
  - on_popover_close: Fires on the "popover-close" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8PrimaryNav(inverted?, behavior?, navAriaLabel?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-primary-nav> — Primary Nav component.
  - inverted: Inverted variant
  - behavior: Behavior variant
  - navAriaLabel: aria-label attribute to designate at name for the nav.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8PrimaryNavItem(text?, href?, iconName?, megaMenu?, isActive?, slot_default?, slot_itemBefore?, slot_itemAfter?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-primary-nav-item> — Primary Nav Item component.
  - text: Primary nav item text
  - href: Primary nav item href
  - iconName: Icon name
  - megaMenu: Append to the class name.
  - isActive: Append to the class name.
  - slot_default: A list of components for the "default" slot, even if there is only one. The label for the navigation item
  - slot_itemBefore: A list of components for the "itemBefore" slot, even if there is only one. Content rendered before the item label, such as an icon
  - slot_itemAfter: A list of components for the "itemAfter" slot, even if there is only one. Content rendered after the item label, such as an icon
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8ProgressMeter(status?, knockout?, max?, value?, name?, label?, fieldId?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-progress-meter> — A progress meter provides feedback that the system is working and gives
  - status: Progress Status Must be one of: 'error', 'warning', 'success'
  - knockout: Determines if the progress meter is displayed on a dark background (uses knockout colors for contrast)
  - max: The max number for the progress bar (defaulted to 100 to match percentages)
  - value: The the percentage of the bar that is filled in (defaulted to match percentages)
  - name: Progress Meter name
  - label: Progress Meter label
  - fieldId: Progress Meter FieldId
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8ProgressSteps(steps?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-progress-steps> — The Progress Steps component is used to display where a user is in a multistep process.
  - steps: Steps for a data-driven progress indicator.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8ProgressStepsItem(state?, message?, name?, svg?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-progress-steps-item> — The Progress Steps Item component is used to display a single step in a multi-step process.
  - state: The state of the step. Must be one of: 'error', 'warning', 'complete', 'current', 'incomplete'
  - message: Optional message to display under the step name.
  - name: The name of the step.
  - svg: An SVG string to use as the step icon.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8RadioField(label?, items?, name?, fieldNote?, ariaDescribedBy?, fieldNoteIconName?, fieldNoteKnockout?, isSuccess?, isError?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-radio-field> — Radio Field is the parent container for `radio-field-item`.
  - label: Radio field legend label
  - items: Options for a data-driven radio field.
  - name: Form control name shared by every generated option.
  - fieldNote: Radio Field Note
  - ariaDescribedBy: Radio container fieldnote aria describe by
  - fieldNoteIconName: Radio container fieldnote icon name
  - fieldNoteKnockout: Radio container fieldnote knockout
  - isSuccess: Radio container fieldnote isSuccess
  - isError: Radio container fieldnote isError
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8RadioFieldItem(checked?, label?, name?, disabled?, required?, value?, ariaDescribedBy?, fieldId?, fieldNote?, fieldNoteIconName?, fieldNoteKnockout?, fieldNoteIsError?, isError?, isSuccess?, type?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-radio-field-item> — A Radio Field Item adds a radio button to a Radio Field.
  - checked: A Boolean attribute which, if present, sets the radio button as selected.
  - label: The label attribute is used to assign a value to the label element corresponding to this radio button.
  - name: The name of the form field
  - disabled: The Boolean disabled attribute, when present, makes the element not mutable, focusable, or even submitted with
  - required: Required attribute
  - value: The value of the form field.
  - ariaDescribedBy: Identifies the element that provides a detailed, extended description for the object.
  - fieldId: The fieldId attribute is assigned to the HTML input element of the radio button and the for attribute of the
  - fieldNote: A FieldNote can be placed to provide guidance.
  - fieldNoteIconName: Sets the item fieldnote icon.
  - fieldNoteKnockout: Radio item fieldnote knockout
  - fieldNoteIsError: Sets the error state of the fieldnote.
  - isError: The isError attribute is used to indicate an error state related to the radio button.
  - isSuccess: The isSuccess attribute is used to indicate a success state related to the radio button.
  - type: The type of form control (text, checkbox, radio, etc.)
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8RemoveTag(text?, color?, shape?, disabled?, on_remove_tag_click? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-remove-tag> — Clicking a Remove Tag causes it to disappear from the page or field (in the case of Multi-Select).
  - text: The tag text
  - color: The tag color scheme Must be one of: 'neutral', 'branded', 'neutral-hybrid'
  - shape: The tag shape Must be one of: 'round', 'square'
  - disabled: Disabled state for remove tag
  - on_remove_tag_click: Fires on the "remove-tag-click" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Section(headline?, slot_default?, slot_header?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-section> — The section component acts as a block level HTML element that takes a 'headline' property
  - headline: The Headline will be rendered as the Section Headline with the correct brand styling applied
  - slot_default: A list of components for the "default" slot, even if there is only one. The content of the section should go here.
  - slot_header: A list of components for the "header" slot, even if there is only one. Custom header content, rendered in place of the `headline` property
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Select(items?, label?, name?, disabled?, required?, value?, fieldId?, fieldNote?, ariaDescribedBy?, validationAriaDescribedBy?, errorNote?, successNote?, isError?, isSuccess?, type?, slot_fieldNote?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-select> — The Select control is designed and built to be used for selecting between choices in a form.
  - items: A mix of Cre8SelectOption and Cre8SelectOptionGroup definitions:
  - label: The required label that appears above the select
  - name: The name of the form field
  - disabled: The disabled attribute on the select
  - required: The required attribute on the select
  - value: The value of the form field.
  - fieldId: The unique id of the select
  - fieldNote: Optional field note text can be added to provide additional field guidance.
  - ariaDescribedBy: Used to connect the field note in text field to the text menu for accessibility
  - validationAriaDescribedBy: Additional aria-describedby connection to id for additional success and error notes to be accessible
  - errorNote: The error field note that appears below the default field note
  - successNote: The success field note that appears below the default field note
  - isError: Changes the component's treatment to represent an error state
  - isSuccess: Changes the component's treatment to represent a success state
  - type: The type of form control (text, checkbox, radio, etc.)
  - slot_fieldNote: A list of components for the "fieldNote" slot, even if there is only one. Container for optional field note content
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8SelectTile(variant?, align?, checked?, type?, name?, disabled?, required?, value?, variantBreakToVertical?, checkPosition?, radioVariant?, fieldId?, isError?, isSuccess?, shadowRootOptions?, defaultChecked?, slot_default?, slot_header?, slot_footer?, slot_title?, slot_body?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-select-tile> — The Select Tile component is a short block of content inside a visual
  - variant: Style variants Must be one of: 'bare', 'horizontal', 'horizontal-bare'
  - align: Align variants
  - checked: Checked State.
  - type: Should this Select Tile behave as a radio button or a checkbox? Must be one of: 'checkbox', 'radio'
  - name: The name of the form field
  - disabled: Disabled State
  - required: Required attribute
  - value: The value of the form field.
  - variantBreakToVertical: Which breakpoint, if any, to switch to verticial. Must be one of: 'sm', 'lg', 'none', 'md', 'sm-2', 'xl', 'xxl'
  - checkPosition: Where does the checkmark or radio button go? Must be one of: 'none', 'left', 'right', 'top-right'
  - radioVariant: In radio mode, whether to use the circle with the dot, or the rounded check. Must be one of: 'dot', 'check'
  - fieldId: Select Tile FieldId
  - isError: Error State
  - isSuccess: Radio item fieldnote isSuccess
  - defaultChecked: The default checked state when the element first renders or is reset.
  - slot_default: A list of components for the "default" slot, even if there is only one. The default slot goes into the center, main part of the Select Tile.
  - slot_header: A list of components for the "header" slot, even if there is only one. The top or left part of the Select Tile
  - slot_footer: A list of components for the "footer" slot, even if there is only one. The bottom or right part of the Select Tile
  - slot_title: A list of components for the "title" slot, even if there is only one. The title part of the Select Tile, use with body slot and
  - slot_body: A list of components for the "body" slot, even if there is only one. The "body" part of the Select Tile, which appears under
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8SelectTileList(variant?, label?, fieldNote?, ariaDescribedBy?, fieldNoteIconName?, fieldNoteKnockout?, fieldNoteIsSuccess?, fieldNoteIsError?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-select-tile-list> — Select Tile List is a container design to hold multiple Select Tile Components.
  - variant: Whether to show the tiles side by side (columns) or stacked vertically (rows). Must be one of: 'columns', 'rows'
  - label: Select Tile container label
  - fieldNote: Select Tile container fieldnote
  - ariaDescribedBy: Select Tile container fieldnote aria describe by
  - fieldNoteIconName: Select Tile container fieldnote icon name
  - fieldNoteKnockout: Select Tile container fieldnote knockout
  - fieldNoteIsSuccess: Select Tile container fieldnote isSuccess
  - fieldNoteIsError: Select Tile container fieldnote isError
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8SkeletonLoader(variant?, height?, width?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-skeleton-loader> — Skeleton Loader allows for the ability to create placeholder UI loading states.
  - variant: Style variant Must be one of: 'rectangle', 'square', 'circle'
  - height: Height inline style
  - width: Width inline style
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8SplitButton(disabled?, size?, buttonText?, dropdownOpen?, children?, on_split_button_text_click? (static), on_split_button_dropdown_click? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-split-button> — Split Button component.
  - disabled: Disables both the main button and the dropdown toggle.
  - size: Size variant Must be one of: 'sm', 'lg'
  - buttonText: Display text on the button
  - children: A list of child components, in order, even if there is only one.
  - on_split_button_text_click: Fires on the "split-button-text-click" event.
  - on_split_button_dropdown_click: Fires on the "split-button-dropdown-click" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Submenu(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-submenu> — Submenu component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8SubmenuItem(href?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-submenu-item> — Submenu Item component.
  - href: The link URL
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Tab(size?, index?, isActive?, ariaLabelledBy?, children?, on_tab_select? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tab> — Tab component.
  - size: Tab sizes
  - index: Used to align the tab with the tab panel
  - isActive: If is true, tab has active state and cooresponding tab panel is visible.
  - ariaLabelledBy: Used to connect tab trigger and tab panel for accessibility
  - children: A list of child components, in order, even if there is only one.
  - on_tab_select: Fires on the "tab-select" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TabPanel(index?, skipFocusOnPanel?, isActive?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tab-panel> — Tab Panel component.
  - index: Used to align the tab panel with the tab
  - skipFocusOnPanel: This will remove focus on panel element
  - isActive: Indicates if the panel is active
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Table(columns?, rows?, caption?, behavior?, variant?, isHoverable?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table> — Table component.
  - columns: Columns for a data-driven table.
  - rows: Rows for a data-driven table.
  - caption: Specifies the caption/title of the table, visible to all users.
  - behavior: Behavior variants
  - variant: Style variants
  - isHoverable: Hoverable rows variant
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TableBody(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table-body> — Table Body component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TableCell(colspan?, variant?, dataHeader?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table-cell> — Table Cell component.
  - colspan: Colspan attribute on td
  - variant: Style variants
  - dataHeader: Column header text for cell to display when table is using responsive variant
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TableHeader(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table-header> — Table Header component.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TableHeaderCell(colspan?, width?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table-header-cell> — Table Header Cell component.
  - colspan: Colspan attribute on th
  - width: Adds inline width style to th
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TableObject(slot_default?, slot_header?, slot_footer?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table-object> — Table Object component.
  - slot_default: A list of components for the "default" slot, even if there is only one. The component content
  - slot_header: A list of components for the "header" slot, even if there is only one. Content rendered in the table object header
  - slot_footer: A list of components for the "footer" slot, even if there is only one. Content rendered in the table object footer
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TableRow(variant?, isExpanded?, isExpandable?, expandedButtonText?, collapsedButtonText?, slot_default?, slot_expandableContent?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-table-row> — Table Row component.
  - variant: Style variants
  - isExpanded: Visually show additional expandable content
  - isExpandable: Indicates row has additional visually hidden related content
  - expandedButtonText: Expanded button text
  - collapsedButtonText: Expand button text
  - slot_default: A list of components for the "default" slot, even if there is only one. The component content
  - slot_expandableContent: A list of components for the "expandableContent" slot, even if there is only one. Content revealed when the row is expanded
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Tabs(size?, items?, fullWidth?, activeIndex?, isStart?, isEnd?, activeTab?, isRTL?, handleScroll?, handleResize?, setIsStart?, setIsEnd?, emitEvent?, tabId?, slot_default?, slot_panel?, on_tab_change? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tabs> — Tabs are used to quickly navigate back and forth between views.
  - size: Tab sizes
  - items: Tabs for a data-driven tab set.
  - fullWidth: Displays a set of tabs with a spanning the width of the element
  - activeIndex: Sets the initial active tab (e.g.
  - isStart: If position from left is greater than 0, set isStart to false.
  - isEnd: If last child is fully in the viewport, set isEnd to true.
  - activeTab: The active tab
  - isRTL: Query the document direction value
  - tabId: Auto Increment id to sync tab and tab panel
  - slot_default: A list of components for the "default" slot, even if there is only one. Default, unnamed slot container for each `cre8-tab` button
  - slot_panel: A list of components for the "panel" slot, even if there is only one. Container for each `cre8-tab-panel` content item
  - on_tab_change: Fires on the "tab-change" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Tag(text?, variant?, shape?, type?, name?, disabled?, required?, value?, isDisabled?, isSelected?, fieldId?, isError?, isSuccess?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tag> — The tag component allows you to make selections, filter content, or trigger actions.
  - text: The text label displayed inside the tag.
  - variant: Color variant Must be one of: 'neutral', 'branded', 'neutral-hybrid'
  - shape: shape of the tag, supports square and round, and default not mentioned its a square Must be one of: 'square', 'round'
  - type: Type of tag Must be one of: 'checkbox', 'radio'
  - name: The name of the form field
  - disabled: Whether the field is disabled
  - required: Whether the field is required
  - value: The value of the form field.
  - isDisabled: Disabled attribute
  - isSelected: Selected attribute
  - fieldId: The fieldId attribute is assigned to the HTML input element of the radio button and the for attribute of the
  - isError: Whether the field is in an error state
  - isSuccess: Whether the field is in a success state
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TagList(label?, tags?, fieldId?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tag-list> — Tag List must have children which are Tag components that are of type `checkbox` or `radio`.
  - label: Tag list legend label
  - tags: Tags for a data-driven tag list.
  - fieldId: The unique id of the select
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TertiaryNav(fullWidth?, navAriaLabel?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tertiary-nav> — Tertiary Nav component.
  - fullWidth: Allows the tertiary nav to take up the full width of it parent container
  - navAriaLabel: aria-label attribute to designate at name for the nav.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TertiaryNavItem(href?, isCurrent?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tertiary-nav-item> — Tertiary Nav Item component.
  - href: The href value of the tertiary nav link
  - isCurrent: The current state of the tertiary nav link
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TextLink(href?, variant?, size?, inverted?, slot_default?, slot_linkAfter?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-text-link> — Text Link component.
  - href: The link URL
  - variant: Style variant Must be one of: 'secondary', 'display'
  - size: Size variant
  - inverted: Inverted variant
  - slot_default: A list of components for the "default" slot, even if there is only one. The component content
  - slot_linkAfter: A list of components for the "linkAfter" slot, even if there is only one. Content rendered after the link text, such as an icon
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8TextPassage(inverted?, size?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-text-passage> — The text-passage component acts a general wrapper element
  - inverted: Inverted variant
  - size: Size variant Must be one of: 'large', 'small', 'default'
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8Tooltip(position?, knockout?, svg?, isDynamic?, isActiveDynamic?, isActive?, ariaDescribes?, iconRotateDegree?, iconFlipDirection?, isRTL?, removeActive?, slot_default?, slot_trigger?, on_tooltip_open? (static), on_tooltip_close? (static), on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-tooltip> — The purpose of tooltips is to provide a tip or hint about what a tool, icon, link, or other interaction does.
  - position: Positions the tooltip panel absolutely to the icon. Must be one of: 'default', 'top', 'left', 'right'
  - knockout: The knockout variant for the tooltip
  - svg: svg as a raw string
  - isDynamic: The dynamic state for the tooltip.
  - isActiveDynamic: The dynamic active state
  - isActive: The active state for the tooltip
  - ariaDescribes: Accepts the ID string of the item the tooltip is referencing
  - iconRotateDegree: iconRotateDegree is used for <cre8-icon> to set the arrow in the correct direction
  - iconFlipDirection: iconFlipDirection is used for <cre8-icon> to set the icon in the correct direction
  - isRTL: Query the document direction value
  - removeActive: Remove Active State
  - slot_default: A list of components for the "default" slot, even if there is only one. Default, unnamed slot container for Tooltip text
  - slot_trigger: A list of components for the "trigger" slot, even if there is only one. Named slot container for Tooltip element to trigger showing/hiding the Tooltip text
  - on_tooltip_open: Fires on the "tooltip-open" event.
  - on_tooltip_close: Fires on the "tooltip-close" event.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8UtilityNav(inverted?, navAriaLabel?, children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-utility-nav> — Utility Nav component.
  - inverted: Inverted variant
  - navAriaLabel: aria-label attribute to designate at name for the nav.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• Cre8UtilityNavItem(href?, text?, hideText?, iconName?, iconPosition?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static))
  - Description: <cre8-utility-nav-item> — Utility Nav Item component.
  - href: URL of the utility nav item
  - text: Text of the utility nav item
  - hideText: Hide text toggle
  - iconName: Icon name
  - iconPosition: Icon position Must be one of: 'before', 'after'
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
• HtmlArticle(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <article> — A self-contained composition, e.g. a card or post.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• HtmlAside(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <aside> — Content tangential to its surroundings, e.g. a sidebar.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• HtmlDiv(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <div> — Generic layout container; use display/direction/gap/columns.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• HtmlFooter(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <footer> — Closing content for its section.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• HtmlHeader(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <header> — Introductory content for its section.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• HtmlNav(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <nav> — A group of navigation links (the links themselves are cre8 components).
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• HtmlSection(children?, on_click? (static), on_keydown? (static), on_focus? (static), on_blur? (static), on_input? (static), on_change? (static), on_submit? (static), padding? (static), paddingX? (static), paddingY? (static), margin? (static), marginX? (static), marginY? (static), display? (static), direction? (static), gap? (static), align? (static), justify? (static), wrap? (static), columns? (static), background? (static), radius? (static), border? (static), width? (static), maxWidth? (static), textAlign? (static))
  - Description: <section> — A thematic grouping of content.
  - children: A list of child components, in order, even if there is only one.
  - on_click: Fires on the native "click" event.
  - on_keydown: Fires on the native "keydown" event.
  - on_focus: Fires on the native "focus" event.
  - on_blur: Fires on the native "blur" event.
  - on_input: Fires on the native "input" event.
  - on_change: Fires on the native "change" event.
  - on_submit: Fires on the native "submit" event.
  - padding: Padding on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingX: Horizontal (inline) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - paddingY: Vertical (block) padding. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - margin: Margin on all sides. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginX: Horizontal (inline) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - marginY: Vertical (block) margin. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - display: CSS display. Must be one of: 'block', 'inline', 'inline-block', 'flex', 'inline-flex', 'grid', 'none'
  - direction: Flex direction; implies display flex. Must be one of: 'row', 'column'
  - gap: Space between children of a flex or grid box. Must be one of: '0', '4', '8', '12', '16', '24', '32', '48', '64', '96'
  - align: Cross-axis alignment (align-items). Must be one of: 'start', 'center', 'end', 'stretch', 'baseline'
  - justify: Main-axis distribution (justify-content). Must be one of: 'start', 'center', 'end', 'between', 'around', 'evenly'
  - wrap: Let flex children wrap.
  - columns: Equal grid columns; implies display grid.
  - background: Background colour token. Must be one of: 'default', 'subtle', 'brand'
  - radius: Corner radius token. Must be one of: 'none', 'small', 'field', 'large', 'container', 'pill'
  - border: A 1px border in this colour token. Must be one of: 'default', 'strong', 'brand'
  - width: auto, 100% (full) or fit-content. Must be one of: 'auto', 'full', 'fit'
  - maxWidth: sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch. Must be one of: 'sm', 'md', 'lg', 'xl', 'prose', 'none'
  - textAlign: Text alignment. Must be one of: 'start', 'center', 'end'
• Text(text (static))
  - Description: A plain text node inside a cre8 component. Wrap it in Cre8Heading or Cre8TextPassage for typography.
  - text: The literal text.

## Positional Function Signatures

Use these exact positional signatures to instantiate check rules or logic functions:


## Catalog Instructions

Every component is a cre8 web component; `x-cre8-tag` on each definition names the element it renders.
Text content is a separate `Text` component referenced from `children` or a `slot_*` property, never a string in a ChildList.
Content goes through EITHER `children` OR `slot_*` properties; the definition says which. Button labels are the `text` property.
Any non-static property can be bound to the data model, and lists of children can be generated from a data model list with a template.
Events: `on_<event>` properties take an Action whose event.name is reported back to the agent.
Every component accepts token spacing: padding, paddingX, paddingY, margin, marginX, marginY ("0"-"96"; 16 = 1rem).
Html* components are structural HTML containers (div, section, article, aside, header, footer, nav) for grouping and layout only. They take display, direction, gap, align, justify, wrap, columns, background, radius, border, width, maxWidth and textAlign, all as cre8 token enums. All content (text, headings, lists, links, images) is cre8 components.

### Examples:

<a2ui>
surface("example_agency_overview")
root = Cre8LayoutSection(_, _, _, [body])
body = HtmlDiv([title, intro, kpis, charts, accounts], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "24")
title = Cre8Heading("headline-large", _, "h1", _, [title_text])
title_text = Text("Client performance")
intro = Cre8TextPassage(_, _, [intro_text])
intro_text = Text("Paid media across all active clients, last 7 days. Sample data.")
kpis__text_1 = Text("This week")
kpis__cre8heading_1 = Cre8Heading("title-large", _, "h2", _, [kpis__text_1])
kpis__cre8griditem_1 = Cre8GridItem(_, [spend])
kpis__cre8griditem_2 = Cre8GridItem(_, [roas])
kpis__cre8griditem_3 = Cre8GridItem(_, [conversions])
kpis__cre8griditem_4 = Cre8GridItem(_, [cpa])
kpis__cre8grid_1 = Cre8Grid("4up", "lg", _, [kpis__cre8griditem_1, kpis__cre8griditem_2, kpis__cre8griditem_3, kpis__cre8griditem_4])
kpis = HtmlSection([kpis__cre8heading_1, kpis__cre8grid_1], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "12")
spend__text_1 = Text("Spend")
spend__cre8heading_1 = Cre8Heading("label-default", _, _, _, [spend__text_1])
spend__text_2 = Text("$84.3k")
spend__cre8heading_2 = Cre8Heading("headline-default", _, _, _, [spend__text_2])
spend__cre8badge_1 = Cre8Badge("+4.2%", "error")
spend__htmldiv_1 = HtmlDiv([spend__cre8heading_1, spend__cre8heading_2, spend__cre8badge_1], _, _, _, _, _, _, _, "16", _, _, _, _, _, "flex", "column", "4")
spend = Cre8Card(_, _, _, [spend__htmldiv_1])
roas__text_1 = Text("ROAS")
roas__cre8heading_1 = Cre8Heading("label-default", _, _, _, [roas__text_1])
roas__text_2 = Text("3.8x")
roas__cre8heading_2 = Cre8Heading("headline-default", _, _, _, [roas__text_2])
roas__cre8badge_1 = Cre8Badge("+0.4x", "success")
roas__htmldiv_1 = HtmlDiv([roas__cre8heading_1, roas__cre8heading_2, roas__cre8badge_1], _, _, _, _, _, _, _, "16", _, _, _, _, _, "flex", "column", "4")
roas = Cre8Card(_, _, _, [roas__htmldiv_1])
conversions__text_1 = Text("Conversions")
conversions__cre8heading_1 = Cre8Heading("label-default", _, _, _, [conversions__text_1])
conversions__text_2 = Text("2,914")
conversions__cre8heading_2 = Cre8Heading("headline-default", _, _, _, [conversions__text_2])
conversions__cre8badge_1 = Cre8Badge("+11%", "success")
conversions__htmldiv_1 = HtmlDiv([conversions__cre8heading_1, conversions__cre8heading_2, conversions__cre8badge_1], _, _, _, _, _, _, _, "16", _, _, _, _, _, "flex", "column", "4")
conversions = Cre8Card(_, _, _, [conversions__htmldiv_1])
cpa__text_1 = Text("Cost per acquisition")
cpa__cre8heading_1 = Cre8Heading("label-default", _, _, _, [cpa__text_1])
cpa__text_2 = Text("$28.93")
cpa__cre8heading_2 = Cre8Heading("headline-default", _, _, _, [cpa__text_2])
cpa__cre8badge_1 = Cre8Badge("-6%", "success")
cpa__htmldiv_1 = HtmlDiv([cpa__cre8heading_1, cpa__cre8heading_2, cpa__cre8badge_1], _, _, _, _, _, _, _, "16", _, _, _, _, _, "flex", "column", "4")
cpa = Cre8Card(_, _, _, [cpa__htmldiv_1])
charts = HtmlDiv([trend, channels], _, _, _, _, _, _, _, _, _, _, _, _, _, "grid", _, "16", _, _, _, 2)
trend__cre8chart_1 = Cre8Chart("line", _, 280.0, _, true, _, "Spend and revenue by day", true, _, _, _, {labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], datasets: [{label: "Spend", data: [11.2, 12.5, 12.1, 13.0, 12.8, 11.0, 11.7]}, {label: "Revenue", data: [41.0, 47.3, 45.2, 50.1, 49.4, 40.2, 43.9]}]})
trend__text_1 = Text("Revenue in thousands of dollars.")
trend__cre8textpassage_1 = Cre8TextPassage(_, "small", [trend__text_1])
trend__htmldiv_1 = HtmlDiv([trend__cre8chart_1, trend__cre8textpassage_1], _, _, _, _, _, _, _, "16", _, _, _, _, _, "flex", "column", "12")
trend__text_2 = Text("Spend and revenue by day")
trend__cre8heading_1 = Cre8Heading("title-default", _, "h3", _, [trend__text_2])
trend__htmldiv_2 = HtmlDiv([trend__cre8heading_1], _, _, _, _, _, _, _, _, "16", "12")
trend = Cre8Card(_, _, _, [trend__htmldiv_1], [trend__htmldiv_2])
channels__cre8chart_1 = Cre8Chart("doughnut", _, 280.0, _, true, _, "Spend by channel", true, _, _, _, {labels: ["Search", "Social", "Display", "Video"], datasets: [{label: "Spend", data: [38.0, 27.0, 12.0, 7.0]}]})
channels__htmldiv_1 = HtmlDiv([channels__cre8chart_1], _, _, _, _, _, _, _, "16", _, _, _, _, _, "flex", "column", "12")
channels__text_1 = Text("Spend by channel")
channels__cre8heading_1 = Cre8Heading("title-default", _, "h3", _, [channels__text_1])
channels__htmldiv_2 = HtmlDiv([channels__cre8heading_1], _, _, _, _, _, _, _, _, "16", "12")
channels = Cre8Card(_, _, _, [channels__htmldiv_1], [channels__htmldiv_2])
accounts__text_1 = Text("Needs attention")
accounts__cre8heading_1 = Cre8Heading("title-large", _, "h2", _, [accounts__text_1])
accounts = HtmlSection([accounts__cre8heading_1, alert], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "12")
alert = Cre8Alert("warning", _, _, _, _, _, _, _, true, [alert_text])
alert_text = Text("Northwind's social campaign is 18% over its weekly budget.")
</a2ui>

<a2ui>
surface("example_contact_form")
$/form/email = ""
$/form/full_name = ""
$/form/notes = ""
$/form/plan = ""
root = Cre8LayoutSection(_, _, _, [form_body])
text = Text("A contact form")
title = Cre8Heading("headline-large", _, "h1", _, [text])
text_2 = Text("Demo mode: these fields are canned, the pathway is real.")
intro = Cre8TextPassage(_, _, [text_2])
field_full_name = Cre8Field(_, _, _, "Full name", _, _, _, _, "text", "full_name", _, true, $/form/full_name, _, _, _, _, _, "", _, _, _, false)
field_email = Cre8Field(_, _, _, "Email", _, _, _, _, "email", "email", _, true, $/form/email, _, _, _, _, _, "", _, _, _, false)
field_plan = Cre8Select([{label: "Starter", value: "Starter"}, {label: "Team", value: "Team"}, {label: "Enterprise", value: "Enterprise"}], "Plan", "plan", _, _, $/form/plan, _, _, _, _, "", _, false)
field_notes = Cre8Field(_, _, _, "Notes", _, _, _, _, "text", "notes", _, _, $/form/notes, _, _, _, _, _, "", _, _, _, false)
submit = Cre8Button("Submit", "primary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Event("submit", {full_name: $/form/full_name, email: $/form/email, plan: $/form/plan, notes: $/form/notes}))
form_body = HtmlDiv([title, intro, field_full_name, field_email, field_plan, field_notes, submit], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "16")
</a2ui>

<a2ui>
surface("example_pricing")
root = Cre8LayoutSection(_, _, _, [intro, plans_grid, footnote])
intro = HtmlDiv([page_title, page_intro], _, _, _, _, _, _, _, _, _, "48", _, _, _, "flex", "column", "12", "center", _, _, _, _, _, _, _, _, "center")
page_title = Cre8Heading("display-small", _, "h1", _, [page_title_text])
page_title_text = Text("Simple, transparent pricing")
page_intro = Cre8TextPassage(_, "large", [page_intro_text])
page_intro_text = Text("Pick the plan that fits your team. Upgrade, downgrade or cancel at any time.")
plans_grid = Cre8Grid("3up", "lg", _, [grid_basic, grid_pro, grid_ent])
grid_basic = Cre8GridItem(true, [card_basic])
card_basic = Cre8Card(_, _, true, [basic_body], [basic_header], [basic_btn])
basic_header = HtmlDiv([basic_name], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "row", _, "center", "between")
basic_name = Cre8Heading("title-large", _, "h2", _, [basic_name_text])
basic_name_text = Text("Basic")
basic_body = HtmlDiv([basic_price_row, basic_desc, basic_divider, basic_list], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
basic_price_row = HtmlDiv([basic_price, basic_period], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "4", "baseline")
basic_price = Cre8Heading("display-small", _, "h3", _, [basic_price_text])
basic_price_text = Text("$9")
basic_period = Cre8TextPassage(_, "small", [basic_period_text])
basic_period_text = Text("/ month")
basic_desc = Cre8TextPassage(_, "small", [basic_desc_text])
basic_desc_text = Text("Everything you need to get started on your own.")
basic_divider = Cre8Divider("horizontal")
basic_list = Cre8List(_, "condensed", _, [basic_f1, basic_f2, basic_f3, basic_f4])
basic_f1 = Cre8ListItem([basic_f1_t])
basic_f1_t = Text("1 user")
basic_f2 = Cre8ListItem([basic_f2_t])
basic_f2_t = Text("Up to 10 projects")
basic_f3 = Cre8ListItem([basic_f3_t])
basic_f3_t = Text("5 GB storage")
basic_f4 = Cre8ListItem([basic_f4_t])
basic_f4_t = Text("Email support")
basic_btn = Cre8Button("Choose Basic", "secondary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, true, _, _, _, _, _, _, _, _, Event("choose_plan", {plan: "basic"}), _, _, _, _, _, _, _, _, _, "24")
grid_pro = Cre8GridItem(true, [card_pro])
card_pro = Cre8Card(_, _, true, [pro_body], [pro_header], [pro_btn])
pro_header = HtmlDiv([pro_name, pro_badge], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "row", _, "center", "between")
pro_name = Cre8Heading("title-large", _, "h2", true, [pro_name_text])
pro_name_text = Text("Pro")
pro_badge = Cre8Badge("Most popular", "info")
pro_body = HtmlDiv([pro_price_row, pro_desc, pro_divider, pro_list], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
pro_price_row = HtmlDiv([pro_price, pro_period], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "4", "baseline")
pro_price = Cre8Heading("display-small", _, "h3", _, [pro_price_text])
pro_price_text = Text("$29")
pro_period = Cre8TextPassage(_, "small", [pro_period_text])
pro_period_text = Text("/ month")
pro_desc = Cre8TextPassage(_, "small", [pro_desc_text])
pro_desc_text = Text("For growing teams that need more room to collaborate.")
pro_divider = Cre8Divider("horizontal", "brand")
pro_list = Cre8List(_, "condensed", _, [pro_f1, pro_f2, pro_f3, pro_f4])
pro_f1 = Cre8ListItem([pro_f1_t])
pro_f1_t = Text("Up to 10 users")
pro_f2 = Cre8ListItem([pro_f2_t])
pro_f2_t = Text("Unlimited projects")
pro_f3 = Cre8ListItem([pro_f3_t])
pro_f3_t = Text("100 GB storage")
pro_f4 = Cre8ListItem([pro_f4_t])
pro_f4_t = Text("Priority support")
pro_btn = Cre8Button("Choose Pro", "primary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, true, _, _, _, _, _, _, _, _, Event("choose_plan", {plan: "pro"}), _, _, _, _, _, _, _, _, _, "24")
grid_ent = Cre8GridItem(true, [card_ent])
card_ent = Cre8Card(_, _, true, [ent_body], [ent_header], [ent_btn])
ent_header = HtmlDiv([ent_name], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "row", _, "center", "between")
ent_name = Cre8Heading("title-large", _, "h2", _, [ent_name_text])
ent_name_text = Text("Enterprise")
ent_body = HtmlDiv([ent_price_row, ent_desc, ent_divider, ent_list], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
ent_price_row = HtmlDiv([ent_price, ent_period], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "4", "baseline")
ent_price = Cre8Heading("display-small", _, "h3", _, [ent_price_text])
ent_price_text = Text("$99")
ent_period = Cre8TextPassage(_, "small", [ent_period_text])
ent_period_text = Text("/ month")
ent_desc = Cre8TextPassage(_, "small", [ent_desc_text])
ent_desc_text = Text("Advanced security and control for large organizations.")
ent_divider = Cre8Divider("horizontal")
ent_list = Cre8List(_, "condensed", _, [ent_f1, ent_f2, ent_f3, ent_f4])
ent_f1 = Cre8ListItem([ent_f1_t])
ent_f1_t = Text("Unlimited users")
ent_f2 = Cre8ListItem([ent_f2_t])
ent_f2_t = Text("1 TB storage")
ent_f3 = Cre8ListItem([ent_f3_t])
ent_f3_t = Text("Single sign-on (SSO)")
ent_f4 = Cre8ListItem([ent_f4_t])
ent_f4_t = Text("Dedicated account manager")
ent_btn = Cre8Button("Choose Enterprise", "secondary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, true, _, _, _, _, _, _, _, _, Event("choose_plan", {plan: "enterprise"}), _, _, _, _, _, _, _, _, _, "24")
footnote = HtmlDiv([footnote_text], _, _, _, _, _, _, _, _, _, "32", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, "center")
footnote_text = Cre8TextPassage(_, "small", [footnote_t])
footnote_t = Text("All prices in USD, billed monthly. Taxes may apply.")
</a2ui>

<a2ui>
surface("example_product_launch")
$/demo/company = ""
$/demo/email = ""
$/demo/name = ""
root = Cre8LayoutSection(_, _, _, [body])
body = HtmlDiv([hero, plans, demo], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "48")
hero__text_1 = Text("Reports your clients actually read")
hero__cre8heading_1 = Cre8Heading("display-default", _, "h1", _, [hero__text_1])
hero__text_2 = Text("Live dashboards for every account, branded and ready in minutes.")
hero__cre8textpassage_1 = Cre8TextPassage(_, _, [hero__text_2])
hero__cre8button_1 = Cre8Button("Start free trial", "primary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Event("start_trial", {}))
hero__cre8button_2 = Cre8Button("See pricing", "secondary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Event("see_pricing", {}))
hero__htmldiv_2 = HtmlDiv([hero__cre8button_1, hero__cre8button_2], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "12", _, "center", true)
hero__htmldiv_1 = HtmlDiv([hero__cre8heading_1, hero__cre8textpassage_1, hero__htmldiv_2], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "16", _, _, _, _, _, _, _, _, "lg", "center")
hero = Cre8Hero("center", _, _, _, [hero__htmldiv_1])
plans__text_1 = Text("Pricing")
plans__cre8heading_1 = Cre8Heading("title-large", _, "h2", _, [plans__text_1])
plans = HtmlSection([plans__cre8heading_1, plan_grid], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "24")
plan_grid = HtmlDiv([starter, growth, agency], _, _, _, _, _, _, _, _, _, _, _, _, _, "grid", _, "16", _, _, _, 3)
starter__text_1 = Text("$49")
starter__cre8heading_1 = Cre8Heading("display-small", _, "h3", _, [starter__text_1])
starter__text_2 = Text("/ month")
starter__cre8textpassage_1 = Cre8TextPassage(_, "small", [starter__text_2])
starter__htmldiv_2 = HtmlDiv([starter__cre8heading_1, starter__cre8textpassage_1], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "4", "baseline")
starter__cre8divider_1 = Cre8Divider()
starter__text_3 = Text("5 client dashboards")
starter__cre8listitem_1 = Cre8ListItem([starter__text_3])
starter__text_4 = Text("Weekly email reports")
starter__cre8listitem_2 = Cre8ListItem([starter__text_4])
starter__cre8list_1 = Cre8List(_, _, _, [starter__cre8listitem_1, starter__cre8listitem_2])
starter__htmldiv_1 = HtmlDiv([starter__htmldiv_2, starter__cre8divider_1, starter__cre8list_1], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
starter__text_5 = Text("Starter")
starter__cre8heading_2 = Cre8Heading("title-large", _, "h2", false, [starter__text_5])
starter__htmldiv_3 = HtmlDiv([starter__cre8heading_2], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "row", _, "center", "between")
starter__cre8button_1 = Cre8Button("Choose Starter", "secondary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, true, _, _, _, _, _, _, _, _, Event("choose_plan", {plan: "starter"}), _, _, _, _, _, _, _, _, _, "24")
starter = Cre8Card(_, _, true, [starter__htmldiv_1], [starter__htmldiv_3], [starter__cre8button_1])
growth__text_1 = Text("$149")
growth__cre8heading_1 = Cre8Heading("display-small", _, "h3", _, [growth__text_1])
growth__text_2 = Text("/ month")
growth__cre8textpassage_1 = Cre8TextPassage(_, "small", [growth__text_2])
growth__htmldiv_2 = HtmlDiv([growth__cre8heading_1, growth__cre8textpassage_1], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "4", "baseline")
growth__cre8divider_1 = Cre8Divider()
growth__text_3 = Text("25 client dashboards")
growth__cre8listitem_1 = Cre8ListItem([growth__text_3])
growth__text_4 = Text("Custom branding")
growth__cre8listitem_2 = Cre8ListItem([growth__text_4])
growth__text_5 = Text("Daily refresh")
growth__cre8listitem_3 = Cre8ListItem([growth__text_5])
growth__cre8list_1 = Cre8List(_, _, _, [growth__cre8listitem_1, growth__cre8listitem_2, growth__cre8listitem_3])
growth__htmldiv_1 = HtmlDiv([growth__htmldiv_2, growth__cre8divider_1, growth__cre8list_1], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
growth__text_6 = Text("Growth")
growth__cre8heading_2 = Cre8Heading("title-large", _, "h2", true, [growth__text_6])
growth__cre8badge_1 = Cre8Badge("Most popular", "info")
growth__htmldiv_3 = HtmlDiv([growth__cre8heading_2, growth__cre8badge_1], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "row", _, "center", "between")
growth__cre8button_1 = Cre8Button("Choose Growth", "primary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, true, _, _, _, _, _, _, _, _, Event("choose_plan", {plan: "growth"}), _, _, _, _, _, _, _, _, _, "24")
growth = Cre8Card(_, _, true, [growth__htmldiv_1], [growth__htmldiv_3], [growth__cre8button_1])
agency__text_1 = Text("$399")
agency__cre8heading_1 = Cre8Heading("display-small", _, "h3", _, [agency__text_1])
agency__text_2 = Text("/ month")
agency__cre8textpassage_1 = Cre8TextPassage(_, "small", [agency__text_2])
agency__htmldiv_2 = HtmlDiv([agency__cre8heading_1, agency__cre8textpassage_1], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "row", "4", "baseline")
agency__cre8divider_1 = Cre8Divider()
agency__text_3 = Text("Unlimited dashboards")
agency__cre8listitem_1 = Cre8ListItem([agency__text_3])
agency__text_4 = Text("White-label domain")
agency__cre8listitem_2 = Cre8ListItem([agency__text_4])
agency__text_5 = Text("Priority support")
agency__cre8listitem_3 = Cre8ListItem([agency__text_5])
agency__cre8list_1 = Cre8List(_, _, _, [agency__cre8listitem_1, agency__cre8listitem_2, agency__cre8listitem_3])
agency__htmldiv_1 = HtmlDiv([agency__htmldiv_2, agency__cre8divider_1, agency__cre8list_1], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
agency__text_6 = Text("Agency")
agency__cre8heading_2 = Cre8Heading("title-large", _, "h2", false, [agency__text_6])
agency__htmldiv_3 = HtmlDiv([agency__cre8heading_2], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "row", _, "center", "between")
agency__cre8button_1 = Cre8Button("Choose Agency", "secondary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, true, _, _, _, _, _, _, _, _, Event("choose_plan", {plan: "agency"}), _, _, _, _, _, _, _, _, _, "24")
agency = Cre8Card(_, _, true, [agency__htmldiv_1], [agency__htmldiv_3], [agency__cre8button_1])
demo__htmldiv_1 = HtmlDiv([name, email, company], _, _, _, _, _, _, _, _, "24", _, _, _, _, "flex", "column", "16")
demo__text_1 = Text("Request a demo")
demo__cre8heading_1 = Cre8Heading("title-large", _, "h2", _, [demo__text_1])
demo__text_2 = Text("We reply within one business day.")
demo__cre8textpassage_1 = Cre8TextPassage(_, "small", [demo__text_2])
demo__htmldiv_2 = HtmlDiv([demo__cre8heading_1, demo__cre8textpassage_1], _, _, _, _, _, _, _, _, "24", "16", _, _, _, "flex", "column", "4")
demo__cre8button_1 = Cre8Button("Request demo", "primary", _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Event("request_demo", {name: $/demo/name, email: $/demo/email, company: $/demo/company}))
demo__htmldiv_3 = HtmlDiv([demo__cre8button_1], _, _, _, _, _, _, _, "24")
demo = Cre8Card(_, _, _, [demo__htmldiv_1], [demo__htmldiv_2], [demo__htmldiv_3])
name = Cre8Field(_, _, _, "Name", _, _, _, _, "text", _, _, true, $/demo/name)
email = Cre8Field(_, _, _, "Work email", _, _, _, _, "email", _, _, true, $/demo/email)
company = Cre8Field(_, _, _, "Company", _, _, _, _, "text", _, _, _, $/demo/company)
</a2ui>

<a2ui>
surface("example_sales_dashboard")
root = Cre8LayoutSection(_, _, _, [dashboard_body])
text = Text("A sales dashboard for an online")
title = Cre8Heading("headline-large", _, "h1", _, [text])
text_2 = Text("Demo mode: sample data for the last 30 days.")
subtitle = Cre8TextPassage(_, _, [text_2])
text_3 = Text("Revenue")
metric_label = Cre8Heading("label-default", _, _, _, [text_3])
text_4 = Text("$48.2k")
metric_value = Cre8Heading("headline-default", _, _, _, [text_4])
metric_delta = Cre8Badge("+6.1%", "success")
metric_card = Cre8Card(_, _, _, [metric_label, metric_value, metric_delta])
metric_cell = Cre8GridItem(_, [metric_card])
text_5 = Text("Orders")
metric_label_2 = Cre8Heading("label-default", _, _, _, [text_5])
text_6 = Text("1,204")
metric_value_2 = Cre8Heading("headline-default", _, _, _, [text_6])
metric_delta_2 = Cre8Badge("+3.0%", "success")
metric_card_2 = Cre8Card(_, _, _, [metric_label_2, metric_value_2, metric_delta_2])
metric_cell_2 = Cre8GridItem(_, [metric_card_2])
text_7 = Text("Refund rate")
metric_label_3 = Cre8Heading("label-default", _, _, _, [text_7])
text_8 = Text("1.9%")
metric_value_3 = Cre8Heading("headline-default", _, _, _, [text_8])
metric_delta_3 = Cre8Badge("+0.4%", "error")
metric_card_3 = Cre8Card(_, _, _, [metric_label_3, metric_value_3, metric_delta_3])
metric_cell_3 = Cre8GridItem(_, [metric_card_3])
text_9 = Text("Avg. order")
metric_label_4 = Cre8Heading("label-default", _, _, _, [text_9])
text_10 = Text("$40.03")
metric_value_4 = Cre8Heading("headline-default", _, _, _, [text_10])
metric_card_4 = Cre8Card(_, _, _, [metric_label_4, metric_value_4])
metric_cell_4 = Cre8GridItem(_, [metric_card_4])
metrics = Cre8Grid("4up", "lg", _, [metric_cell, metric_cell_2, metric_cell_3, metric_cell_4])
text_11 = Text("Top products")
section_title = Cre8Heading("title-large", _, "h2", _, [text_11])
text_12 = Text("Product")
th = Cre8TableHeaderCell(_, _, [text_12])
text_13 = Text("Units")
th_2 = Cre8TableHeaderCell(_, _, [text_13])
text_14 = Text("Revenue")
th_3 = Cre8TableHeaderCell(_, _, [text_14])
header_row = Cre8TableRow(_, _, _, _, _, [th, th_2, th_3])
text_15 = Text("Ceramic mug")
td = Cre8TableCell(_, _, _, [text_15])
text_16 = Text("320")
td_2 = Cre8TableCell(_, _, _, [text_16])
text_17 = Text("$6,400")
td_3 = Cre8TableCell(_, _, _, [text_17])
row = Cre8TableRow(_, _, _, _, _, [td, td_2, td_3])
text_18 = Text("Linen apron")
td_4 = Cre8TableCell(_, _, _, [text_18])
text_19 = Text("210")
td_5 = Cre8TableCell(_, _, _, [text_19])
text_20 = Text("$8,190")
td_6 = Cre8TableCell(_, _, _, [text_20])
row_2 = Cre8TableRow(_, _, _, _, _, [td_4, td_5, td_6])
text_21 = Text("Tea set")
td_7 = Cre8TableCell(_, _, _, [text_21])
text_22 = Text("96")
td_8 = Cre8TableCell(_, _, _, [text_22])
text_23 = Text("$7,680")
td_9 = Cre8TableCell(_, _, _, [text_23])
row_3 = Cre8TableRow(_, _, _, _, _, [td_7, td_8, td_9])
table_header = Cre8TableHeader([header_row])
table_body = Cre8TableBody([row, row_2, row_3])
table = Cre8Table(_, _, _, _, "striped", _, [table_header, table_body])
section = HtmlSection([section_title, table], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "12")
text_24 = Text("Quarterly goals")
section_title_2 = Cre8Heading("title-large", _, "h2", _, [text_24])
text_25 = Text("Revenue")
progress_label = Cre8Heading("label-default", _, _, _, [text_25])
progress = Cre8PercentBar(62.0, 100.0, true)
progress_item = HtmlDiv([progress_label, progress], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "4")
text_26 = Text("New customers")
progress_label_2 = Cre8Heading("label-default", _, _, _, [text_26])
progress_2 = Cre8PercentBar(81.0, 100.0, true)
progress_item_2 = HtmlDiv([progress_label_2, progress_2], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "4")
section_2 = HtmlSection([section_title_2, progress_item, progress_item_2], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "12")
dashboard_body = HtmlDiv([title, subtitle, metrics, section, section_2], _, _, _, _, _, _, _, _, _, _, _, _, _, "flex", "column", "24")
</a2ui>
