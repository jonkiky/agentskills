# Browser workflows

Use these procedures only for live supplier research. The user controls the signed-in browser and completes sign-in and MFA. Never copy or persist credentials, cookies, tokens, membership identifiers, or payment data.

## Shared navigation discipline

1. Load the supplier profile described in [supplier-adapters.md](supplier-adapters.md), then open its configured start URL in the user's browser.
2. If sign-in or MFA is required, pause and ask the user to complete it. Continue only after the browser visibly shows an authenticated state.
3. Establish location and fulfillment context before reading prices. Record the visible label.
4. Navigate by visible text, accessible role/name, form label, or stable product identifier. Do not depend on screen coordinates or visual position alone.
5. After each navigation or filter change, verify supplier, page heading, location/channel, result count or product identity, and visible price state.
6. Capture product evidence without entering checkout: product name, brand, item/product ID, pack details, regular/deal price, promotion dates, availability, page URL, retrieval time, and coverage note. Map it to the shared schema before comparison.
7. For relevant multi-page listings, inspect at least pages 1–3 and aim to include page 4 when it exists and remains within the configured page/time limits. Stop earlier only when results end, relevance is exhausted, access is blocked, or a configured limit is reached. Record pages/categories/searches checked and the reason for any shorter scan.

Prices and availability are volatile. Re-verify items selected for the final list near the end of the session.

## Bounded semantic search expansion

Before searching a requested item, create a small concept set appropriate to its breadth and intended use:

- Start with the user's exact wording and direct spelling or terminology variants.
- For a broad category, add common subtypes, cuts, forms, and menu-use terms that a supplier may index separately. For example, `beef` may expand to `steak`, `ground beef`, `beef roast`, `beef patties`, and `stew beef`; `chicken` may expand to breasts, thighs, drumsticks, tenders, patties, and diced chicken.
- Use visible category labels, suggested searches, product taxonomy, and relevant terms found on the supplier site to refine the concept set. Do not invent unrelated categories merely to increase result count.
- When the user specifies a cut, grade, dietary requirement, brand, preparation, or storage state, treat it as a constraint. Search direct synonyms and equivalent supplier terminology, but place materially different results under possible substitutes or omit them.
- Keep the number of expanded searches proportional to the page and time limits. For a very broad category, prioritize representative, commercially useful subtypes and disclose what was and was not searched.

Record every search term and category page checked. Group results by subtype or intended use before matching across suppliers; compare steak with comparable steak, ground beef with comparable ground beef, and so on.

## Sysco

- Begin at `{{SYSCO_START_URL}}`; do not derive or probe alternate account URLs.
- Confirm the visible `{{SYSCO_ACCOUNT_LOCATION_LABEL}}` before collecting observations. If it differs, stop and ask whether to switch or update the configuration.
- Use `{{SYSCO_DEALS_LABEL}}` only when that visible label exists. Otherwise use bounded searches for shopping-list/watchlist items.
- Treat assortment, contract pricing, minimum quantities, and availability as specific to the visible account/location.
- If price is hidden, says “contact representative,” or requires a cart quantity, record it as unavailable rather than manipulating the cart.

## Costco

- Confirm `{{TEST_ZIP_CODE}}`, `{{COSTCO_CHANNEL}}`, and `{{COSTCO_WAREHOUSE_LOCATION}}` when applicable before gathering evidence.
- Keep `Costco.com`, `Warehouse Pickup`, `Business Delivery`, and `Same-Day` distinct. Store the exact channel on every observation.
- Do not treat a shipped price as a warehouse price. Same-Day prices may differ from warehouse pricing and may include channel-specific markups.
- Record delivery fees, service fees, minimum-order constraints, or member-only price visibility only when exposed. Never infer them.

## Other configured suppliers

- Use the supplier profile's user-approved domain, entry URL, context requirements, and search procedure.
- First validate the profile with one representative query and confirm product identity, pack quantity, price meaning, fulfillment context, and source URL can be observed reliably.
- Prefer semantic labels and stable product identifiers. Treat selectors, URL patterns, and page layouts as hints that must be re-verified, not permanent truths.
- If the site exposes multiple sellers or marketplaces, record the actual seller as part of the supplier identity or notes. Do not merge offers from different sellers under one supplier implicitly.
- If a required field cannot be extracted reliably, keep it null where the schema allows or exclude the offer from price comparison. Never repair missing pack or price data by guessing.

## Shopping-list comparison

For each requested item:

1. Build the bounded concept set described above, then search both suppliers using relevant product terms, brand, grade/specification, intended use, and needed quantity.
2. Group candidates by product subtype or intended use before comparing suppliers.
3. Label each candidate `exact`, `close_equivalent`, or `possible_substitute`.
4. Normalize quantities and unit prices before deciding. Only exact or close equivalents within the same product group can win the cheaper-option comparison.
5. If no comparable candidate exists, say so; keep useful substitutes in a separate section.

### Match rules

- `exact`: same product identity/specification, brand where material, grade/form, and materially equivalent pack; quantity may differ if reliably normalized.
- `close_equivalent`: functionally equivalent specification and quality with no material purchasing difference, but brand or pack configuration differs. State the difference.
- `possible_substitute`: uncertain equivalence or a meaningful difference in formulation, quality, grade, cut, size, packaging, or use. Never use it to declare a supplier cheaper.

## Deal discovery

Build the scope from, in priority order, the current shopping list, watchlist, order history, preferred categories, and preferred brands. For an open-ended `best deals` request, inspect both `{{ORDER_HISTORY_FILE}}` and `{{PRODUCT_CATALOG_BY_CATEGORY_FILE}}` when available: use purchase recency and frequency to identify likely needs, then use the category catalog to add relevant related products and supplier search terms. Treat this as a relevance signal, not proof of deal quality.

Expand broad items into the bounded concept set above, then visit only relevant category/search/deal pages within `{{SCAN_PAGE_LIMIT}}` and `{{SCAN_TIME_LIMIT_MINUTES}}`. When pagination is available, scan at least the first three relevant pages and aim for four before ranking, unless fewer pages exist or a documented stopping condition applies.

Rank candidates using relevance, normalized savings, needed quantity and likely consumption, purchase history, and waste/spoilage/storage risk. Explain the strongest factors and material penalties rather than presenting false precision.

Describe results as “best among categories/pages checked” and include the coverage note.

## Fail safely

Stop and report the limitation when authentication expires, location/channel is unclear, anti-automation controls appear, prices cannot be verified, or the authorized scan bound is reached. Do not bypass controls, broaden the crawl, or claim unobserved coverage.
