# Output formats

Keep evidence compact and make unknowns explicit.

## Mandatory offer links

- Every specific observed or recommended offer must be a clickable Markdown link to the supplier source used for its price, availability, or description. Apply this rule in prose, comparison tables, deal-quality tables, recommendations, and printable lists. Generic requested items or categories do not require links.
- Prefer a stable product-detail URL. Preserve meaningful supplier product IDs or SKUs in the visible text or evidence column.
- If no stable detail URL exists, use the exact search, listing, offer, or order-history URL and label it `fallback source`; include the product ID and the search term needed to locate the product again.
- Do not present a specific observed or recommended offer without a traceable link. If no usable source URL can be captured, omit the offer-specific claim and explain that it could not be traced reliably.

## Comparison table

Use a long-form table so the output supports any number of suppliers without adding site-specific columns.

| Needed item / quantity | Supplier / channel | Linked candidate and pack | Match | Normalized price | Fees/tax | Evidence |
|---|---|---|---|---|---|---|

Link each candidate name to its supplier source. Add a short recommendation after each item's candidate rows. Show total quantity, effective unit price, currency/unit, and whether fees/tax are included. Name the cheaper supplier only for `exact` or `close_equivalent` matches. Put possible substitutes in a separate table with material differences.

## Deal-quality table

| Linked product | Supplier / channel | Current normalized price | History | Assessment | Why it matters |
|---|---|---|---|---|---|

For history, show comparable sample count, observed date range, and median. Use only `good`, `fair`, `poor`, or `insufficient history`. Include deal relevance, needed quantity, purchase-history signal, and waste risk in the explanation.

## Coverage and assumptions

State:

- retrieval date/time and ZIP/location/account label;
- exact supplier, fulfillment channel, and account/location context for every source;
- categories, searches, and pages checked plus elapsed/allowed limits;
- expanded search terms and product subtypes checked, including any relevant subtypes omitted because of the page or time limit;
- inaccessible areas or unavailable prices;
- conversions, fees/tax treatment, and match assumptions;
- the honest claim, normally “best among categories/pages checked.”

## Printable supplier-grouped list

Produce plain, print-friendly Markdown or a user-requested printable format. Avoid wide tables.

```markdown
# Restaurant Shopping List
Purchase date: YYYY-MM-DD
Location/channel context: ...

## <Supplier name> — <account/location and channel>
- [ ] <quantity> × [<product name and pack>](<supplier product or fallback source URL>) — <expected price> — <product ID>
  Needed for: <shopping-list item>; unit price: <currency/base unit>

Supplier subtotal (before unknown fees/tax): ...

## <Next supplier name> — <account/location and channel>
- [ ] <quantity> × [<product name and pack>](<supplier product or fallback source URL>) — <expected price> — <product ID>
  Needed for: <shopping-list item>; unit price: <currency/base unit>

Supplier subtotal (before unknown fees/tax): ...

## Verify before purchase
- Prices and availability retrieved at <timestamp>.
- <known assumptions, promotion expiry, fees/tax not included, or stock caveats>
```

Group by supplier first, then optional aisle/category. Include purchase quantity, pack description, expected price, product ID when available, and a checkbox. Keep possible substitutes out unless the user explicitly selects them.

When writing a file, use `{{PRINT_OUTPUT_DIRECTORY}}`, a descriptive date-based filename, and confirm the exact path. Do not overwrite an existing list without approval.
