# GVLA Homepage Design

Date: 2026-06-30

## Goal

Improve the existing static GVLA project page into a standard academic paper homepage while preserving the current Bulma/Nerfies-style template. The page should present the paper, dataset, method, experiments, real-robot validation, and citation clearly enough for readers arriving from ECCV, arXiv, GitHub Pages, or a lab/project link.

## Approved Direction

Use the existing single-page static site in `index.html` and enrich it with content extracted from `5218_Gripper_aware_Vision_Lang_副本.pdf`. The implementation should not introduce a build system. It should remain deployable by GitHub Pages as plain HTML, CSS, JavaScript, PDF, image, and video assets.

## Page Structure

1. Hero
   - Keep the title `GVLA: Gripper-aware Vision Language Action Models`.
   - Keep author and affiliation blocks, including Zihong Luo's Google Scholar link.
   - Keep the ECCV 2026 acceptance badge.
   - Keep the Paper button linked to the local PDF.
   - Only show arXiv, Code, and MiGA Dataset buttons when real URLs are available. Do not leave dead `#` links in the final page.
   - Keep the current `static/images/introduction.png` as the first visual because it matches the paper's GVLA/MiGA teaser.

2. Abstract and Video
   - Keep the paper abstract, lightly polish obvious grammar only where needed.
   - Keep the existing GVLA demo video as the primary video block.

3. MiGA Dataset
   - Add a dataset section centered on the paper's core dataset facts:
     - 103K trajectories.
     - 5 gripper types.
     - 36 tasks.
     - real and simulation domains.
     - multi-view RGB-D observations, proprioceptive states, and gripper-strategy annotations.
   - Include extracted figures/tables where useful:
     - Fig. 3 for gripper-specific strategy variation.
     - Fig. 4 for dataset statistics.
     - Table 1 for comparison with existing VLA datasets.

4. GVLA Method
   - Add a method section explaining the two main components:
     - multi-gripper tokenization with platform/type/instance-level tokens.
     - dual Mixture-of-Adapters for gripper and platform routing.
   - Include extracted figures:
     - Fig. 2 for token embedding structure.
     - Fig. 5 for architecture overview.
     - Fig. 6 for probing analysis if the extracted asset is readable at webpage size.

5. Results
   - Add a results section that summarizes the experimental claims without overloading the page with all paper details.
   - Include:
     - baseline comparison across task categories.
     - zero-shot cross-object generalization.
     - few-shot task and gripper adaptation.
     - real-world validation.
   - Use extracted Table 2, Fig. 8, Fig. 9, and Fig. 10 when the extracted versions are readable.
   - Add short captions that explain what each figure demonstrates.

6. Citation and Acknowledgement
   - Keep the BibTeX section.
   - Keep the Nerfies template acknowledgement.
   - Update README citation language from RobotDesign1M to GVLA/MiGA so it matches this project.

## Content and Asset Handling

Extract paper figures and tables into `static/images/paper/` with stable, descriptive filenames such as:

- `fig-01-teaser.png`
- `fig-03-task-categories.png`
- `fig-04-dataset-statistics.png`
- `fig-05-architecture.png`
- `fig-08-cross-object-generalization.png`
- `fig-09-adaptation.png`
- `fig-10-real-world-validation.png`
- `table-01-dataset-comparison.png`
- `table-02-baseline-comparison.png`

If automatic extraction produces low-quality or partial assets, render the relevant PDF page at high resolution and crop the figure/table from the rendered page. Do not recreate or fabricate paper results.

The old commented RobotDesign1M sections in `index.html` should be removed or replaced with GVLA/MiGA sections. The final HTML should not contain stale RobotDesign1M copy.

## Visual Design

Keep the page quiet, academic, and readable. Preserve the current template's overall style but reduce one-note purple/pink dominance where possible by adding restrained neutral surfaces and clearer section spacing. Use:

- compact metric cards for dataset facts.
- full-width figure blocks with captions.
- two-column layouts only when figures remain readable on desktop.
- stacked mobile layouts for all figure and text combinations.

Avoid decorative components that do not explain the paper. The site should prioritize scanning the contribution, dataset scale, model design, and experimental evidence.

## Technical Design

The site remains static:

- `index.html` owns the page structure.
- `static/css/index.css` owns page-specific styling.
- `static/js/index.js` should be trimmed if current interpolation/carousel logic is no longer used.
- `static/images/paper/` stores extracted paper assets.
- `static/videos/` keeps the existing video assets.

No frontend framework, package manager, or build step is required.

## Error Handling and Link Behavior

The final page should avoid broken user-facing links. If arXiv, Code, or Dataset URLs are not supplied, the corresponding buttons should be hidden rather than left as `href="#"`.

Images should include meaningful `alt` text. Videos should retain controls and use the existing local MP4 source. Large extracted images should be compressed only if readability is preserved.

## Verification

Before considering implementation complete:

- Check that `index.html` has no stale RobotDesign1M text.
- Check that no visible buttons link to `#`.
- Check that all referenced local image, video, and PDF assets exist.
- Open the page through a local static server and verify desktop and mobile layouts.
- Confirm that the Paper button opens the local PDF.
- Confirm that key figures are readable at normal viewport widths.

