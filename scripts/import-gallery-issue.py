#!/usr/bin/env python3
"""Import approved GitHub issue attachments into a series gallery.

A public user opens the Gallery photo issue form and attaches images.
A maintainer approves by commenting /approve-gallery on that issue.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.request
from pathlib import Path

BODY = os.environ.get("ISSUE_BODY", "")
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER", "0")

SERIES = {
    "Al & Sloppy": "al-and-sloppy",
    "Channel 86": "channel-86",
    "That Time Again Records": "that-time-again-records",
}

ALLOWED_HOSTS = ("github.com/user-attachments/assets/", "private-user-images.githubusercontent.com/")
URL_RE = re.compile(r"https://[^\\s)]+")
MAX_BYTES = 15 * 1024 * 1024


def section_value(title: str) -> str:
    match = re.search(rf"###\\s+{re.escape(title)}\\s*\\n+([^\\n]+)", BODY, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extension(content_type: str, url: str) -> str:
    low = content_type.lower()
    if "png" in low:
        return ".png"
    if "webp" in low:
        return ".webp"
    if "gif" in low:
        return ".gif"
    if "avif" in low:
        return ".avif"
    if "jpeg" in low or "jpg" in low:
        return ".jpg"
    suffix = Path(url.split("?", 1)[0]).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"} else ".jpg"


def main() -> int:
    selected = section_value("Series")
    slug = SERIES.get(selected)
    if not slug:
        print(f"Unknown or missing series: {selected!r}", file=sys.stderr)
        return 2

    urls = [
        url.rstrip(".,>")
        for url in URL_RE.findall(BODY)
        if any(host in url for host in ALLOWED_HOSTS)
    ]
    if not urls:
        print("No supported GitHub image attachments found.", file=sys.stderr)
        return 3

    target = Path("public/gallery") / slug
    target.mkdir(parents=True, exist_ok=True)

    saved = []
    for index, url in enumerate(urls[:12], start=1):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "That-Time-Again-Gallery-Importer"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read(MAX_BYTES + 1)

        if len(data) > MAX_BYTES:
            print(f"Skipping oversized attachment: {url}", file=sys.stderr)
            continue
        if not content_type.lower().startswith("image/"):
            print(f"Skipping non-image attachment: {url} ({content_type})", file=sys.stderr)
            continue

        ext = extension(content_type, url)
        filename = f"submission-{ISSUE_NUMBER}-{index:02d}{ext}"
        (target / filename).write_bytes(data)
        saved.append(str(target / filename))

    if not saved:
        return 4

    print("\\n".join(saved))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
