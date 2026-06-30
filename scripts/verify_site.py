#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

EXPECTED_TEXT = [
    "MiGA Dataset",
    "GVLA Method",
    "Results",
    "103K",
    "5 gripper types",
    "36 tasks",
    "Multi-gripper tokenization",
    "Dual Mixture-of-Adapters",
    "Real-world Validation",
]

EXPECTED_ASSETS = [
    "5218_Gripper_aware_Vision_Lang_副本.pdf",
    "static/images/introduction.png",
    "static/images/paper/fig-03-task-categories.png",
    "static/images/paper/fig-04-dataset-statistics.png",
    "static/images/paper/fig-05-architecture.png",
    "static/images/paper/fig-08-cross-object-generalization.png",
    "static/images/paper/fig-09-adaptation.png",
    "static/images/paper/fig-10-real-world-validation.png",
    "static/images/paper/table-01-dataset-comparison.png",
    "static/images/paper/table-02-baseline-comparison.png",
    "static/videos/GVLA Video.mp4",
]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.videos = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img" and "src" in attrs:
            self.images.append(attrs["src"])
        if tag == "source" and "src" in attrs:
            self.videos.append(attrs["src"])


def local_path(reference):
    if reference.startswith(("http://", "https://", "mailto:", "#")):
        return None
    return ROOT / reference.removeprefix("./")


def main():
    failures = []
    html = INDEX.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)

    for text in EXPECTED_TEXT:
        if text not in html:
            failures.append(f"Missing expected page text: {text}")

    if "RobotDesign1M" in html:
        failures.append("Stale RobotDesign1M text remains in index.html")

    for href in parser.links:
        if href == "#":
            failures.append("Found dead href=\"#\" link")

    for asset in EXPECTED_ASSETS:
        if not (ROOT / asset).is_file():
            failures.append(f"Missing expected asset: {asset}")

    for reference in parser.images + parser.videos + parser.links:
        path = local_path(reference)
        if path is not None and not path.exists():
            failures.append(f"Referenced local asset does not exist: {reference}")

    if failures:
        print("Site verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
