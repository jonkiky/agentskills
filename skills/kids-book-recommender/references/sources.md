# Source registry and routing

Use current public search or browser access, open the relevant page and capture the title, author, source URL, list/review date, evidence type and the reason it supports the pick. Do not assume that a listed source is accessible in the current runtime.

| Source | Evidence and access | URL |
| --- | --- | --- |
| ALA / ALSC | Librarian-curated thematic lists, Newbery, Caldecott, Geisel, Sibert and notable books; public web | https://www.ala.org/alsc/book-lists ; https://libguides.ala.org/recommended-reading/children |
| Reading Rockets Book Finder | Curated age/format/topic filters and children's literacy recommendations; public web | https://www.readingrockets.org/books-and-authors/books |
| NPR Books We Love | Editorial/critic recommendations; filter Kids' Books, year and theme; public web | https://apps.npr.org/best-books/ |
| Book Riot | Children's, middle-grade and themed editorial lists; public web | https://bookriot.com/category/childrens/ |
| The Horn Book | Children's literature reviews and curated selections; public portions only | https://www.hbook.com/ |
| NY Times Books | Sales rankings, not quality judgments; use public lists or keyed Books API | https://www.nytimes.com/books/best-sellers/ ; https://developer.nytimes.com/ |
| LibraryThing | ISBN-based read-alikes; public work pages or keyed Multi-Recommendations API | https://www.librarything.com/developer/documentation/multirecommendations |
| NoveList K-8 Plus | Librarian read-alikes, appeal factors, award/age lists; licensed access only | https://about.ebsco.com/novelist |
| Goodreads | Public reader opinions and lists; no new developer API keys; no automated scraping | https://www.goodreads.com/ |
| Reddit | Secondary anecdotal recommendations from accessible public threads; not professional evidence | https://www.reddit.com/r/suggestmeabook/ |
| TasteDive | Optional read-alike lead via public pages; legacy API deferred pending authorization and terms review | https://tastedive.com/read/api |
| Google Books | Bibliographic metadata; optional API; not a recommendation endorsement | https://developers.google.com/books/docs/v1/using |
| Open Library | Work/edition identity, author, ISBN, subject; low-volume API lookup; not a recommendation endorsement | https://openlibrary.org/dev/docs/api/search |

## Routing by intent

- General browsing/weekly picks: ALSC + Reading Rockets + NPR or Book Riot.
- Preschool or beginning readers: Reading Rockets age/format filters + ALSC Geisel/Caldecott + another relevant curated list.
- Middle grade/chapter books: ALSC Newbery/notables + Reading Rockets + Horn Book/NPR/Book Riot.
- STEM/nonfiction: ALSC Sibert/thematic lists + Reading Rockets topic lists + publisher or independent professional review.
- New releases: dated NPR/Book Riot/Horn Book lists + NYT category when relevant; confirm publication dates.
- Read-alikes: LibraryThing or authorized NoveList; supplement with professional thematic lists and public reader discussion. Resolve seed ISBN before API calls. Verify child appropriateness independently.
- Bilingual, reluctant readers or particular interests: Reading Rockets + ALSC thematic lists + targeted professional or library booklists. Avoid assuming English titles are translated.
- If a source is unavailable, substitute a relevant independent public librarian or professional booklist; report gaps. Never count syndicated copies as independent sources.

## Optional API helper

Run from the skill directory using Python 3 (standard library only). One request per invocation; avoid repeated/bulk requests. Use environment variables NYT_BOOKS_API_KEY, LIBRARYTHING_API_KEY or GOOGLE_BOOKS_API_KEY where needed. Open Library needs no key; set OPEN_LIBRARY_CONTACT to an application contact email for regular use. Never print or commit credentials. Read provider terms before enabling API access. The script emits provider JSON for agent analysis, not a final recommendation list.

    python scripts/book_api.py openlibrary 'The Wild Robot Peter Brown'
    python scripts/book_api.py google 'intitle:The Wild Robot inauthor:Peter Brown'
    python scripts/book_api.py nyt names
    python scripts/book_api.py nyt childrens-middle-grade-hardcover
    python scripts/book_api.py librarything 9780316381994

For NYT use the list names response to confirm the current list slug; treat rankings as popularity. LibraryThing accepts comma-separated ISBNs; keep within its published limits. Resolve returned ISBNs through metadata before making recommendations. Open Library requests should not exceed 1/sec without identification; use human-driven low-volume lookups, not a bulk backend. Google Books quota/key requirements may vary. If any request fails, use authorized web sources instead; no retries around access blocks. TasteDive and NoveList are not implemented API adapters in V1.

## Library fulfillment

Use the reader's chosen public library; never assume location. For Montgomery County, Maryland, start at https://mcpl.aspendiscovery.org/ and https://mcplmd.overdrive.com/ for ebooks/audiobooks. MCPL's https://mcpl.aspendiscovery.org/WebBuilder/ResourcesList also lists NoveList K-8 Plus; use it only if access is authorized. Public catalog access may be blocked in some environments. No authenticated catalog API is assumed. Use only actually observed record links; if a catalog cannot be reached, return its homepage plus title/author and label status unknown.
