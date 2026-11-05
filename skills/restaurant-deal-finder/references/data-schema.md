# Price observation schema and historical assessment

Read supplied CSV, JSON, or spreadsheet observations with appropriate local data or spreadsheet tools. Preserve the original files unless the user explicitly asks to update them. Historical files must contain no credentials, cookies, tokens, membership/account numbers, or payment data.

## Observation fields

Every row is timestamped and should include:

| Field | Meaning |
|---|---|
| `observed_at` | ISO 8601 retrieval timestamp with timezone. |
| `supplier` | Stable supplier ID from its profile, such as `sysco`, `costco`, or `restaurant-depot`. Do not change the ID when the display name changes. |
| `account_location_label` | Non-secret visible account/location or warehouse label. |
| `fulfillment_channel` | Exact visible channel, e.g. `Account Delivery`, `Shipped`, `Warehouse Pickup`, `Business Delivery`, or `Same-Day`. |
| `product_id` | Supplier-visible SKU/item ID, if available. |
| `normalized_product_key` | Stable local comparison key such as `canola-oil|refined|gal`. |
| `name`, `brand` | Displayed product identity. |
| `pack_count` | Number of containers/units in the sell pack. |
| `unit_size`, `unit_size_unit` | Size of each container plus its unit. |
| `total_quantity`, `total_quantity_unit` | Pack quantity converted to a comparison base unit. |
| `regular_price`, `deal_price`, `currency` | Displayed monetary values. Leave unavailable values null. |
| `normalized_unit_price`, `normalized_price_unit` | Effective price per base unit using deal price when present, otherwise regular price. |
| `promo_start`, `promo_end` | Displayed promotion dates, if any. |
| `availability` | Displayed stock/availability statement. |
| `source_url` | Exact product or result URL used as evidence. |
| `retrieval_coverage` | Bounded context, such as search term, category, page number, and scan limit. |
| `notes` | Non-secret assumptions, fees/tax status, or match caveats. |

Preserve any existing row ID or creation timestamp, but neither is required for comparison.

## Normalize before comparison

Compute `total_quantity = pack_count × unit_size`, then convert compatible measurements to one base unit. Suitable bases include ounces or pounds for weight, fluid ounces or gallons for volume, and each for counts. Do not convert between weight and volume without a product-specific conversion supplied by the user or authoritative packaging.

Compute the effective unit price from the available deal price, otherwise regular price. Keep fees and tax outside this value unless they are known and consistently applicable; state whether they were included.

## Comparable history

Historical rows are comparable only when `normalized_product_key`, currency, normalized price unit, materially equivalent fulfillment context and account/location, and product specification all match. Use supplier-specific history by default; compare across suppliers only when the product match and fulfillment basis remain comparable.

The conservative default requires at least three prior comparable observations. With enough history, compare the current normalized unit price with the historical median:

- `good`: at least 10% below median;
- `fair`: within 10% below through 10% above median;
- `poor`: more than 10% above median.

These thresholds are a repeatable heuristic, not proof of market value. Always show sample count, date range, median, and threshold. When filters are missing, units differ, or fewer than the minimum rows exist, return `insufficient history`.

## Historical assessment

1. Open only the relevant supplied history file or sheet and identify its columns.
2. Filter rows to the same product key, supplier, account/location, fulfillment channel, currency, normalized price unit, and materially equivalent product specification.
3. Exclude the current observation from the historical sample. Disclose invalid or excluded rows rather than repairing them by assumption.
4. Sort the remaining normalized unit prices. For an odd count, use the middle value; for an even count, average the two middle values.
5. Calculate `(current price - median) / median × 100`, then apply the thresholds above.
6. Report the source filename or sheet, sample count, date range, median, current price, percentage difference, and assessment.

Do not modify a history file unless the user explicitly asks to record the new observation. When recording is requested, preserve the existing format and columns and make the smallest direct file or spreadsheet edit needed.
