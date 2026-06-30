# GVLA Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the existing static GVLA template into a complete standard paper homepage using assets extracted from the local paper PDF.

**Architecture:** Keep the site as a plain static project. Add a small Python verification script for repeatable checks, extract paper visuals into `static/images/paper/`, then update `index.html`, `static/css/index.css`, `static/js/index.js`, and `README.md` to present the approved sections.

**Tech Stack:** HTML, CSS, Bulma, vanilla JavaScript, Python standard library, Poppler CLI tools (`pdftoppm`, `pdfimages`, `pdfinfo`) and macOS `sips` for image inspection/cropping.

---

### Task 1: Add Site Verification Script

**Files:**
- Create: `scripts/verify_site.py`
- Test: `python3 scripts/verify_site.py`

- [ ] **Step 1: Write the failing verification script**

Create `scripts/verify_site.py`:

```python
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
```

- [ ] **Step 2: Run verification to confirm it fails for missing implementation**

Run: `python3 scripts/verify_site.py`

Expected: FAIL with messages about missing GVLA sections, missing `static/images/paper/*` assets, stale `RobotDesign1M`, and dead `href="#"` links.

- [ ] **Step 3: Commit the verification script**

Run:

```bash
git add scripts/verify_site.py
git commit -m "Add static site verification"
```

Expected: commit succeeds and only `scripts/verify_site.py` is included.

### Task 2: Extract Paper Visual Assets

**Files:**
- Create: `static/images/paper/*.png`
- Use: `5218_Gripper_aware_Vision_Lang_副本.pdf`
- Test: `python3 scripts/verify_site.py`

- [ ] **Step 1: Render PDF pages at high resolution**

Run:

```bash
mkdir -p /private/tmp/gvla-pages static/images/paper
pdftoppm -png -r 260 "5218_Gripper_aware_Vision_Lang_副本.pdf" /private/tmp/gvla-pages/page
```

Expected: `/private/tmp/gvla-pages/page-01.png` through `/private/tmp/gvla-pages/page-18.png` exist.

- [ ] **Step 2: Create the first pass of cropped assets**

Use `sips` crops from rendered pages and save the following files:

```bash
sips -c 1200 1900 --cropOffset 240 130 /private/tmp/gvla-pages/page-06.png --out static/images/paper/fig-03-task-categories.png
sips -c 1220 1900 --cropOffset 1440 130 /private/tmp/gvla-pages/page-06.png --out static/images/paper/fig-04-dataset-statistics.png
sips -c 880 1700 --cropOffset 170 220 /private/tmp/gvla-pages/page-04.png --out static/images/paper/table-01-dataset-comparison.png
sips -c 1060 1900 --cropOffset 120 120 /private/tmp/gvla-pages/page-08.png --out static/images/paper/fig-05-architecture.png
sips -c 820 1750 --cropOffset 120 120 /private/tmp/gvla-pages/page-12.png --out static/images/paper/table-02-baseline-comparison.png
sips -c 930 1750 --cropOffset 1320 120 /private/tmp/gvla-pages/page-12.png --out static/images/paper/fig-08-cross-object-generalization.png
sips -c 860 1850 --cropOffset 1260 90 /private/tmp/gvla-pages/page-13.png --out static/images/paper/fig-09-adaptation.png
sips -c 920 1800 --cropOffset 130 120 /private/tmp/gvla-pages/page-14.png --out static/images/paper/fig-10-real-world-validation.png
```

Expected: each output file exists. If a crop is visibly wrong, adjust only the crop dimensions/offsets for that file and rerun the affected command.

- [ ] **Step 3: Inspect asset dimensions**

Run:

```bash
sips -g pixelWidth -g pixelHeight static/images/paper/*.png
```

Expected: all assets have non-zero dimensions and are large enough to read on desktop when displayed at full container width.

- [ ] **Step 4: Run verification and expect remaining page-content failures**

Run: `python3 scripts/verify_site.py`

Expected: FAIL still reports missing sections/dead links/stale text, but no longer reports missing `static/images/paper/*` files.

### Task 3: Implement Homepage Structure and Content

**Files:**
- Modify: `index.html`
- Test: `python3 scripts/verify_site.py`

- [ ] **Step 1: Remove stale commented RobotDesign1M sections**

Delete the large commented dataset pipeline/statistics/samples block in `index.html`.

Expected: `rg -n "RobotDesign1M|Dataset Samples|robot design image" index.html` returns no matches.

- [ ] **Step 2: Replace dead resource links**

In `index.html`, keep the Paper link as `./5218_Gripper_aware_Vision_Lang_副本.pdf` and remove the arXiv, Code, and MiGA Dataset button blocks until real URLs are available.

Expected: `rg -n 'href="#"' index.html` returns no matches.

- [ ] **Step 3: Add MiGA Dataset section**

Add a section after Abstract/Video with:

```html
<section class="section section-alt" id="miga-dataset">
  <div class="container is-max-desktop">
    <h2 class="title is-3">MiGA Dataset</h2>
    <p>
      MiGA is a multi-gripper-aware dataset with 103K demonstrations across 36 tasks, five gripper types, and both simulation and real-world robot setups. It captures how identical task objectives require different contact choices, approach directions, and execution strategies across gripper embodiments.
    </p>
    <div class="metric-grid">
      <div class="metric-card"><strong>103K</strong><span>Trajectories</span></div>
      <div class="metric-card"><strong>5</strong><span>Gripper types</span></div>
      <div class="metric-card"><strong>36</strong><span>Tasks</span></div>
      <div class="metric-card"><strong>Real + Sim</strong><span>Domains</span></div>
    </div>
    <figure class="paper-figure">
      <img src="./static/images/paper/fig-03-task-categories.png" alt="Gripper-specific strategy variations across MiGA task categories">
      <figcaption>Gripper-specific strategy variation across singulated, stacked, constrained, and semantic tasks.</figcaption>
    </figure>
    <div class="figure-grid">
      <figure class="paper-figure">
        <img src="./static/images/paper/fig-04-dataset-statistics.png" alt="MiGA dataset statistics">
        <figcaption>MiGA balances task categories and gripper coverage across the dataset.</figcaption>
      </figure>
      <figure class="paper-figure">
        <img src="./static/images/paper/table-01-dataset-comparison.png" alt="Comparison of MiGA with existing VLA datasets">
        <figcaption>Compared with prior VLA datasets, MiGA explicitly covers gripper-specific solutions across real and simulated domains.</figcaption>
      </figure>
    </div>
  </div>
</section>
```

- [ ] **Step 4: Add GVLA Method section**

Add a method section after the dataset section with:

```html
<section class="section" id="method">
  <div class="container is-max-desktop">
    <h2 class="title is-3">GVLA Method</h2>
    <p>
      GVLA conditions a VLA backbone on gripper embodiment through multi-gripper tokenization and a dual Mixture-of-Adapters. Platform-, type-, and instance-level gripper tokens provide structured conditioning, while gripper and platform adapter pools route computation toward embodiment-specific policies.
    </p>
    <div class="method-points">
      <div><strong>Multi-gripper tokenization</strong><span>Encodes robot platform, gripper type, and gripper instance as learnable tokens.</span></div>
      <div><strong>Dual Mixture-of-Adapters</strong><span>Routes action generation through platform- and gripper-aware adapter experts.</span></div>
    </div>
    <figure class="paper-figure">
      <img src="./static/images/paper/fig-05-architecture.png" alt="GVLA architecture overview">
      <figcaption>GVLA injects gripper-aware tokens and adapter routing into the VLA action-generation pipeline.</figcaption>
    </figure>
  </div>
</section>
```

- [ ] **Step 5: Add Results section**

Add a results section after the method section with:

```html
<section class="section section-alt" id="results">
  <div class="container is-max-desktop">
    <h2 class="title is-3">Results</h2>
    <p>
      Across simulation and real-world evaluations, GVLA improves gripper-aware manipulation, zero-shot object generalization, and few-shot adaptation to new tasks or grippers.
    </p>
    <div class="figure-grid">
      <figure class="paper-figure">
        <img src="./static/images/paper/table-02-baseline-comparison.png" alt="Baseline comparison across GVLA task categories">
        <figcaption>GVLA outperforms gripper-agnostic baselines across task categories.</figcaption>
      </figure>
      <figure class="paper-figure">
        <img src="./static/images/paper/fig-08-cross-object-generalization.png" alt="Cross-object generalization success rates">
        <figcaption>GVLA maintains stronger zero-shot transfer across unseen objects and grippers.</figcaption>
      </figure>
      <figure class="paper-figure">
        <img src="./static/images/paper/fig-09-adaptation.png" alt="Task, gripper, and mixed-data adaptation results">
        <figcaption>Gripper-aware conditioning enables more efficient few-shot task and gripper adaptation.</figcaption>
      </figure>
      <figure class="paper-figure">
        <img src="./static/images/paper/fig-10-real-world-validation.png" alt="Real-world robotic validation setup and results">
        <figcaption>Real-world validation shows improved adaptation on a UR5 robot with a Robotiq 2F-85 gripper.</figcaption>
      </figure>
    </div>
  </div>
</section>
```

- [ ] **Step 6: Run verification and expect CSS/readability work only if content is present**

Run: `python3 scripts/verify_site.py`

Expected: PASS for text/link/asset checks.

### Task 4: Style the New Homepage Sections

**Files:**
- Modify: `static/css/index.css`
- Test: local visual inspection and `python3 scripts/verify_site.py`

- [ ] **Step 1: Add section, metric, method, and figure styles**

Append CSS:

```css
.section-alt {
  background: #f8fafc;
}

.section p {
  color: var(--muted);
  line-height: 1.7;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  margin: 1.75rem 0;
}

.metric-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.1rem;
  text-align: center;
  box-shadow: 0 10px 26px -20px rgba(15, 23, 42, 0.35);
}

.metric-card strong {
  display: block;
  color: #111827;
  font-size: 1.75rem;
  line-height: 1.1;
}

.metric-card span {
  display: block;
  color: var(--muted);
  font-size: 0.95rem;
  margin-top: 0.35rem;
}

.method-points {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin: 1.75rem 0;
}

.method-points > div {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-left: 4px solid #2563eb;
  border-radius: 8px;
  padding: 1rem 1.1rem;
}

.method-points strong,
.method-points span {
  display: block;
}

.method-points strong {
  color: #111827;
  margin-bottom: 0.4rem;
}

.method-points span {
  color: var(--muted);
  line-height: 1.55;
}

.figure-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
  margin-top: 1.5rem;
}

.paper-figure {
  margin: 1.5rem 0 0;
}

.paper-figure img {
  display: block;
  width: 100%;
  height: auto;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 12px 30px -22px rgba(15, 23, 42, 0.45);
}

.paper-figure figcaption {
  color: var(--muted);
  font-size: 0.95rem;
  line-height: 1.55;
  margin-top: 0.65rem;
}

@media screen and (max-width: 768px) {
  .metric-grid,
  .method-points,
  .figure-grid {
    grid-template-columns: 1fr;
  }

  .metric-card strong {
    font-size: 1.45rem;
  }
}
```

- [ ] **Step 2: Run verification**

Run: `python3 scripts/verify_site.py`

Expected: PASS.

### Task 5: Clean JavaScript, README, and Final Verification

**Files:**
- Modify: `static/js/index.js`
- Modify: `README.md`
- Test: `python3 scripts/verify_site.py`, local static server

- [ ] **Step 1: Trim unused interpolation and carousel logic if unused**

If `index.html` no longer contains `.carousel`, `#interpolation-slider`, or `#interpolation-image-wrapper`, replace `static/js/index.js` with:

```javascript
window.HELP_IMPROVE_VIDEOJS = false;

$(document).ready(function() {
  $(".navbar-burger").click(function() {
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });
});
```

- [ ] **Step 2: Update README wording**

Change `If you find RobotDesign1M useful for your work please cite:` to:

```markdown
If you find GVLA or MiGA useful for your work, please cite:
```

- [ ] **Step 3: Run automated verification**

Run: `python3 scripts/verify_site.py`

Expected: PASS with `Site verification passed.`

- [ ] **Step 4: Start local static server**

Run: `python3 -m http.server 8000`

Expected: server starts and serves `http://localhost:8000/`.

- [ ] **Step 5: Inspect in browser or with local fetch**

Run: `curl -I http://localhost:8000/`

Expected: HTTP 200 response.

- [ ] **Step 6: Commit implementation**

Run:

```bash
git add index.html static/css/index.css static/js/index.js README.md static/images/paper scripts/verify_site.py "5218_Gripper_aware_Vision_Lang_副本.pdf"
git commit -m "Build GVLA standard paper homepage"
```

Expected: commit includes the homepage, extracted assets, PDF, README update, and verification script.

