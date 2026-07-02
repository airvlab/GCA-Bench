#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
README = ROOT / "README.md"

REQUIRED_LINKS = [
    "https://scholar.google.com/citations?hl=zh-CN&authuser=2&user=1VOV3lsAAAAJ",
    "https://scholar.google.com/citations?hl=zh-CN&authuser=2&user=gEbaF0sAAAAJ",
    "https://scholar.google.com/citations?hl=zh-CN&authuser=2&user=8SLtiQgAAAAJ",
    "https://scholar.google.com/citations?hl=zh-CN&authuser=2&user=unbPvWAAAAAJ",
]

REQUIRED_TEXT = [
    "Beyond Visual Grasping: Benchmarking Complex Grasping from Detection to Execution",
    "GCA-Bench",
    "IROS 2026",
    "102 grasping tasks",
    "Detection Success Rate",
    "Task Success Rate",
    "GCA-Bench-Beyond-Visual-Grasping.pdf",
    "Real-world Setup",
    "Real-world Collection",
]

REQUIRED_ASSETS = [
    "static/images/paper/gca-overview.png",
    "static/images/paper/gca-scenario-design.png",
    "static/images/paper/gca-task-metrics.png",
    "static/images/paper/gca-simulation-setup.png",
    "static/images/paper/gca-real-world-setup.png",
    "static/images/paper/gca-real-world-collection.png",
    "static/images/paper/gca-action-complexity.png",
    "static/images/paper/gca-baseline-comparison.png",
    "static/images/paper/gca-scenario-results.png",
    "static/images/paper/gca-instruction-results.png",
    "static/images/paper/gca-real-world-results.png",
]


class LocalReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.external_links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in {"href", "src"} or not value:
                continue
            if value.startswith(("http://", "https://", "#", "mailto:", "data:")):
                if value.startswith(("http://", "https://")):
                    self.external_links.append(value)
                continue
            self.references.append(value)


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    failures = []

    for text in REQUIRED_TEXT:
        if text not in html:
            failures.append(f"missing text: {text}")

    for asset in REQUIRED_ASSETS:
        if asset not in html:
            failures.append(f"missing reference: {asset}")
        if not (ROOT / asset).is_file():
            failures.append(f"missing asset file: {asset}")

    if "GVLA" in html or "Gripper-aware Vision Language Action Models" in html:
        failures.append("stale GVLA content remains in index.html")

    if "IROS26_0382_MS.pdf" in html:
        failures.append("stale source PDF filename remains in index.html")

    for stale_ref in [
        "bulma-carousel",
        "bulma-slider",
        "fontawesome.all.min.js",
        "static/js/index.js",
        "ajax.googleapis.com",
        "academicons",
    ]:
        if stale_ref in html:
            failures.append(f"stale template dependency remains: {stale_ref}")

    if 'class="paper-figure figure-compact"' not in html:
        failures.append("simulation setup figure is not using compact layout")

    parser = LocalReferenceParser()
    parser.feed(html)
    for link in REQUIRED_LINKS:
        if link not in parser.external_links:
            failures.append(f"missing external link: {link}")

    for reference in parser.references:
        path = ROOT / reference.lstrip("./")
        if not path.exists():
            failures.append(f"broken local reference: {reference}")

    readme = README.read_text(encoding="utf-8")
    for stale_readme_text in ["GVLA", "MiGA", "G-VLA", "nerfies"]:
        if stale_readme_text in readme:
            failures.append(f"stale README content remains: {stale_readme_text}")

    if failures:
        print("Static site check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Static site check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
