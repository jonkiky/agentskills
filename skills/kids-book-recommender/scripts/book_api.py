#!/usr/bin/env python3
"""One-shot, read-only book API helper. No dependencies beyond Python 3."""
import argparse
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def required_key(name):
    value = os.getenv(name)
    if not value:
        raise ValueError("Set " + name + " in the environment first.")
    return value


def build_request(source, query):
    if not query.strip() or len(query) > 400:
        raise ValueError("Supply a nonempty query of at most 400 characters.")
    headers = {"Accept": "application/json", "User-Agent": "KidsBookRecommender/1.0"}
    if source == "openlibrary":
        url = "https://openlibrary.org/search.json"
        params = {"q": query, "limit": 12, "fields": "key,title,author_name,isbn,first_publish_year"}
        contact = os.getenv("OPEN_LIBRARY_CONTACT")
        if contact:
            headers["User-Agent"] += " (" + contact + ")"
    elif source == "google":
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": query, "maxResults": 12, "printType": "books"}
        if os.getenv("GOOGLE_BOOKS_API_KEY"):
            params["key"] = os.environ["GOOGLE_BOOKS_API_KEY"]
    elif source == "nyt":
        if query != "names" and not re.fullmatch(r"[a-z0-9-]{1,80}", query):
            raise ValueError("Use names or a verified NYT list slug.")
        base = "https://api.nytimes.com/svc/books/v3/lists/"
        url = base + ("names.json" if query == "names" else "current/" + query + ".json")
        params = {"api-key": required_key("NYT_BOOKS_API_KEY")}
    elif source == "librarything":
        if not re.fullmatch(r"(?:[0-9]{9}[0-9Xx]|[0-9]{13})(?:,(?:[0-9]{9}[0-9Xx]|[0-9]{13})){0,4}", query):
            raise ValueError("Supply 1-5 comma-separated ISBN-10 or ISBN-13 values.")
        url = "https://www.librarything.com/api/multirecommendations.php"
        params = {"apiKey": required_key("LIBRARYTHING_API_KEY"), "isbns": query, "maxItems": 12, "maxPerAuthor": 2}
    else:
        raise ValueError("Unknown source.")
    return Request(url + "?" + urlencode(params), headers=headers)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", choices=["openlibrary", "google", "nyt", "librarything"])
    parser.add_argument("query", help="Public book query, list slug or ISBNs; no personal data")
    args = parser.parse_args()
    try:
        request = build_request(args.source, args.query)
        with build_opener(NoRedirect()).open(request, timeout=15) as response:
            data = response.read(2_000_001)
            if len(data) > 2_000_000:
                raise ValueError("Response exceeds the size limit.")
            result = json.loads(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except HTTPError as exc:
        print("Provider returned HTTP " + str(exc.code) + "; use authorized web sources instead.", file=sys.stderr)
    except (URLError, TimeoutError, OSError):
        print("Provider unavailable; use authorized web sources instead.", file=sys.stderr)
    except (ValueError, TypeError):
        print("Invalid input, missing API key or invalid provider response; see --help and sources.md.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
