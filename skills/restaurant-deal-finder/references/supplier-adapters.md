# Supplier adapter contract

A supplier adapter is a non-secret profile describing how to enter, contextualize, search, and interpret one supplier site. It isolates site-specific behavior from the shared matching, normalization, history, and comparison rules.

## Profile fields

Use JSON or YAML. Omit optional fields that are unknown rather than inventing them.

| Field | Required | Purpose |
|---|---|---|
| `id` | Yes | Stable lowercase ID used in observations and history, such as `restaurant-depot`. |
| `display_name` | Yes | Supplier name shown to the user. |
| `allowed_domains` | Yes | Exact user-approved domains; do not follow product research onto unrelated domains. |
| `start_url` | Yes | User-approved storefront or catalog entry URL. |
| `auth_mode` | Yes | `none` or `user_sign_in`; the user always handles credentials and MFA. |
| `location_context` | Yes | Visible location/account label required before prices are read, or `none`. |
| `fulfillment_channels` | Yes | Supported channel labels and which one is active. Keep distinct price contexts separate. |
| `search` | Yes | Visible search label and optional user-confirmed category/deals navigation hints. |
| `result_fields` | Yes | Where the site visibly provides name, pack, price, product ID, availability, and promotion data. These are semantic hints, not guaranteed selectors. |
| `price_semantics` | Yes | Whether displayed price is per pack, per unit, weight-variable, member price, or otherwise qualified. |
| `limits` | Yes | Per-supplier page/result and time bounds. |
| `notes` | No | Non-secret caveats, seller rules, minimums, or known missing fields. |

Example shape:

```yaml
suppliers:
  - id: example-supplier
    display_name: Example Supplier
    allowed_domains: [shop.example.com]
    start_url: https://shop.example.com/
    auth_mode: user_sign_in
    location_context:
      required: true
      visible_label: Delivery location
    fulfillment_channels:
      allowed: [Delivery, Pickup]
      active: Delivery
    search:
      visible_label: Search products
      deals_label: Specials
    result_fields:
      required: [name, pack, price, source_url]
      optional: [brand, product_id, regular_price, promo_end, availability]
    price_semantics: displayed price is for the full sell pack
    limits:
      pages: 5
      minutes: 20
```

## Add or update a supplier

1. Confirm the user-approved domain, start URL, supplier ID, intended channel/location, and scan limits.
2. Open only the configured start URL. If authentication is required, let the user complete it.
3. Run one representative product query. Observe the visible context, result structure, product identity, pack, price meaning, availability, and canonical product URL.
4. Keep only non-secret navigation and interpretation details in the profile. Save it to disk only when the user asked to add, update, or persist the supplier. Never save credentials, cookies, tokens, membership/account numbers, or payment data.
5. Validate with at least two representative products when practical: one straightforward packaged item and one item with a different pack or pricing pattern. Confirm both can be mapped to the shared observation schema.
6. Mark unsupported or unreliable fields explicitly. An adapter is usable for comparison only when product identity, total comparable quantity, effective price, currency, channel/location context, and source evidence can be established.

Do not encode ranking, match classification, unit normalization, or recommendation logic in a supplier profile. Those rules remain shared so a new site participates in the same comparison fairly.

## Runtime contract

For each query, the adapter workflow must yield zero or more observations conforming to [data-schema.md](data-schema.md), plus a coverage note. Reject or quarantine an offer when its price meaning or pack quantity is ambiguous. Site-specific promotions, loyalty requirements, minimum orders, and marketplace sellers belong in observation fields or notes, not in hidden adjustments.

When a site changes, re-validate the smallest affected profile section with a representative query. Update semantic hints or caveats without changing historical supplier IDs or shared comparison rules.
