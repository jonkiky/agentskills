# Configuration

Keep user-provided, non-secret inputs here or in a user-selected local configuration document. Never store usernames, passwords, MFA codes, cookies, access tokens, membership numbers, payment data, or other secrets.

Resolve only the placeholders required for the active mode. Values below are examples, not defaults. Store one supplier profile per site using the adapter contract in [supplier-adapters.md](supplier-adapters.md).

| Placeholder | Required? | Meaning | Safe example |
|---|---|---|---|
| `{{TEST_ZIP_CODE}}` | Required for location-sensitive live research | ZIP code used to set delivery, pickup, or warehouse context. | `20850` |
| `{{ACTIVE_SUPPLIERS}}` | Required for multi-supplier comparison | Stable supplier IDs to research, matching configured supplier profiles. | `["sysco", "costco"]` |
| `{{SUPPLIER_PROFILES_FILE}}` | Required when using reusable or newly added supplier profiles | User-selected local JSON or YAML document containing only non-secret site configuration. | `./supplier-profiles.yaml` |
| `{{SYSCO_START_URL}}` | Required for Sysco live research | User-approved starting page for the signed-in Sysco storefront. | `https://shop.sysco.com/` |
| `{{SYSCO_ACCOUNT_LOCATION_LABEL}}` | Required when Sysco prices depend on the account or delivery location | Exact non-secret location label expected in the signed-in storefront. | `Rockville, MD` |
| `{{SYSCO_DEALS_LABEL}}` | Optional | Visible navigation label that opens current promotions; confirm it exists rather than assuming. | `Deals` |
| `{{COSTCO_CHANNEL}}` | Required for Costco live research | Exact fulfillment channel being researched. Use `Costco.com`, or the site's exact label. | `pick up` |
| `{{COSTCO_WAREHOUSE_LOCATION}}` | Required for warehouse-specific research; otherwise optional | City/store label for the selected Costco warehouse or delivery area. Do not store a membership number. | `frederick, MD` |
| `{{PREFERRED_CATEGORIES}}` | Optional | Bounded categories relevant to the restaurant. | `["Beef","Dairy and eggs","Chicken","Pantry and cooking staples","Fresh produce","Pork","Bakery","Prepared sides and desserts","Seafood"]` |
| `{{ORDER_HISTORY_FILE}}` | Optional | Local CSV, JSON, or XLSX file containing purchase history. Confirm columns before using it. | `./history/purchased_items.json` |
| `{{PRODUCT_CATALOG_BY_CATEGORY_FILE}}` | Optional | Local catalog index used with order history to identify relevant categories, related products, and search terms for open-ended deal discovery. | `./history/product_catalog_by_category.json` |
| `{{PRICE_HISTORY_FILES}}` | Required for historical assessment | One or more local CSV, JSON, or XLSX files containing prior price observations. | `["./history/prices-2026.csv"]` |
| `{{SCAN_PAGE_LIMIT}}` | Required for deal discovery | Maximum category/search result pages to inspect per supplier or explicit scope. Set it high enough to inspect at least three pages and aim for four when relevant multi-page results exist. | `10` |
| `{{SCAN_TIME_LIMIT_MINUTES}}` | Required for deal discovery | Total live browsing time budget; stop when reached and report coverage. | `100` |
| `{{PRINT_OUTPUT_DIRECTORY}}` | Required only when saving a printable list | User-selected local output directory. Confirm it before writing and do not overwrite an existing file without approval. | `./shopping-lists` |

## Mode-specific minimums

- **Compare a shopping list:** the list itself, `{{ACTIVE_SUPPLIERS}}`, and each active supplier's start URL plus any location or fulfillment context that its profile requires.
- **Discover deals:** at least one of `{{ORDER_HISTORY_FILE}}` or `{{PREFERRED_CATEGORIES}}`, plus active supplier profiles and both scan limits. For an open-ended request for the best deals, also use `{{PRODUCT_CATALOG_BY_CATEGORY_FILE}}` when it is available to expand order-history items into relevant categories and related search concepts.
- **Assess or compare history:** `{{PRICE_HISTORY_FILES}}` and a product key or filters such as supplier, location, channel, and date.
- **Add a supplier:** a user-approved start URL/domain, a stable supplier ID, permitted fulfillment context, and one representative product query for validation. Follow [supplier-adapters.md](supplier-adapters.md).

If a value cannot be confirmed, leave the token unresolved and label the resulting limitation. Do not guess an account location, fulfillment channel, ZIP code, or a new site's pricing semantics.
