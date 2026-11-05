---
name: restaurant-deal-finder
description: Find the best actionable restaurant-supply deals across Sysco, Costco, and additional configured supplier sites; compare current offers with other suppliers or local price history, and produce supplier-grouped shopping lists. Use for bounded purchasing research in a user-controlled browser and for adding a new product-search source; not for checkout, payment, or broad site crawling.
---

# Restaurant Deal Finder

Find the best actionable deals for the user's purchasing needs and support each recommendation with traceable evidence, without placing orders. Deal discovery—not merely listing available products—is the primary objective.

## Start safely

1. Read [references/configuration.md](references/configuration.md). Ask only for required missing values. Never request or persist credentials, cookies, MFA codes, or payment data.
2. Select one or more modes: compare a shopping list, discover relevant deals, assess deal quality, compare observations by date or supplier, or generate a printable supplier-grouped list.
3. For live research, read [references/browser-workflows.md](references/browser-workflows.md). The user signs in and completes MFA. Use a user-controlled browser, interact through visible labels or semantic page elements, and verify the page state after navigation.
4. When a requested supplier is not already configured, read [references/supplier-adapters.md](references/supplier-adapters.md) and construct a non-secret supplier profile before researching it. Persist the profile only when the user asks to save or add the supplier. Do not change the comparison rules for each site.
5. For historical assessment, read [references/data-schema.md](references/data-schema.md) and analyze the supplied CSV, JSON, or spreadsheet data directly.
6. For the response or printable artifact, read [references/output-formats.md](references/output-formats.md).

## Core decision rules

- Lead with verified deal candidates. A product counts as a deal only when supported by visible promotion evidence, a current-versus-regular price reduction, a favorable comparison with a close equivalent from another supplier, or a meaningful reduction versus comparable local history. A low current unit price without one of these signals is a `value candidate`, not a verified deal.
- Prefer the deal that produces the best practical purchasing outcome, not automatically the largest advertised percentage. Rank verified deals by product relevance, normalized savings, final unit cost, needed quantity, purchase history, pack usability, and waste or spoilage risk.
- When the available evidence does not establish a worthwhile deal, say so clearly. Do not pad the response with ordinary-priced products or present market prices as promotions; list useful non-deal alternatives separately only when they help the decision.
- For an open-ended request for the `best deals`, inspect the configured order-history data and `product_catalog_by_category` file when available before live searching. Use recurring purchases, recent purchases, preferred categories, and catalog relationships to build a bounded watchlist of products and related search concepts the user is likely to need. Do not restrict discovery to exact historical product names, and do not treat past purchase frequency as proof that a current offer is a deal.
- Bound research to the shopping list, order history, watchlist, preferred categories or brands, plus configured page and time limits. Do not crawl any supplier site by default.
- When a relevant result or deal listing has multiple pages, inspect at least the first three pages and aim for four pages per relevant query or category, provided those pages exist and the configured page and time limits allow it. Stop earlier only when results end, the scope becomes irrelevant, access is blocked, or a configured limit is reached. Report the exact pages checked and the reason for any shorter scan.
- Expand broad requested items into a bounded set of relevant supplier search concepts instead of relying on one literal keyword. Include common synonyms, cuts, forms, and menu uses that remain within the user's intent; for example, a broad `beef` request can include steak, ground beef, roasts, patties, and stew meat. Preserve narrow constraints: a request specifically for ribeye, halal beef, or ground beef must not silently broaden to materially different products.
- Keep site-specific navigation in supplier profiles. Convert every observed offer into the shared observation schema before matching, normalizing, ranking, or comparing it.
- Report coverage precisely, such as “best among categories/pages checked.” Never claim “best on the site” without complete, authorized coverage.
- Treat prices and availability as account-, location-, and channel-specific whenever the supplier does. Always identify the visible context used.
- Keep each supplier's shipping, delivery, pickup, warehouse, and same-day channels distinct; never silently compare one as another.
- Classify product matches as `exact`, `close_equivalent`, or `possible_substitute`. Only exact and close-equivalent matches may determine which supplier is cheaper. Present possible substitutes separately.
- Keep related product families distinct after search expansion. Do not compare or rank different cuts, forms, grades, storage states, or intended uses as though they were the same product merely because they share a parent category.
- Normalize pack size and quantity to a shared base unit before comparing unit prices. Show the math or normalized quantities. Include fees and tax only when available; label omissions and assumptions.
- Record source evidence and retrieval coverage with each timestamped observation. Do not infer unavailable regular prices, promotions, taxes, fees, or inventory.
- Capture a traceable source URL for every specific offer used as evidence or recommended in the response. Prefer the supplier's direct product-detail URL and render the offer name as a clickable Markdown link wherever it appears in prose, tables, or printable lists. If the supplier does not expose a stable product URL, link the exact search, listing, offer, or order-history page used, label it as a fallback source link, and include the product ID and search term needed to find it again. Generic shopping-list items and product categories do not require links.
- Rate a price `good`, `fair`, or `poor` only when sufficient comparable local history exists. Otherwise state `insufficient history`.
- Do not add items to carts, submit orders, or perform checkout unless the user separately and explicitly authorizes that action at the time.

## Finish with evidence

Lead the response with the strongest verified deals and why they win. Then provide useful value candidates or “no verified deal found” results separately, followed by supplier-neutral comparisons, historical assessment where supported, coverage, and assumptions. When requested, include a printable list grouped by supplier. Make every specific observed or recommended offer clickable using its traceable supplier source URL, and preserve retrieval times so the user can re-check volatile prices and availability.
