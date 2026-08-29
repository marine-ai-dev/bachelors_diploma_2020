# Plant Disease AI Detection

An intelligent web application that identifies agricultural plant diseases
from a leaf photo using a fine-tuned AlexNet convolutional neural network,
with a Flask + MySQL backend for treatment recommendations and case history.

> **Bachelor's Diploma Project, 2020.** Originally built and defended by
> Maryna Antonevych at Taras Shevchenko National University of Kyiv. This
> repository was reorganized and documented in 2026 for archival and
> portfolio purposes — see [Historical Context](docs/historical-context.md)
> for exactly what that does and doesn't mean.

## Overview

Crop disease is a major threat to global food security, disproportionately
affecting smallholder farmers who produce most of the world's food. This
project applies deep learning to automate what is normally a slow, expert-
dependent diagnostic step: given a photo of a plant leaf, classify it into
one of 38 classes (26 diseases across 14 crop species, plus healthy) and
surface relevant treatment information.

**What it does:**
1. A user uploads a leaf photo through a web interface.
2. A fine-tuned AlexNet model classifies the image.
3. For diseased classes, the app queries a MySQL database for the pathogen,
   disease description, and recommended treatment products.
4. The classification and any subsequent treatments are logged for later
   review (case history, treatment history, statistics).

## System Architecture

See [`docs/architecture.md`](docs/architecture.md) for the full breakdown and
a data-flow diagram. In short: Flask app → PyTorch model (inference) → MySQL
(disease/drug lookup and logging) → server-rendered HTML pages.

## Machine Learning Pipeline

- **Model**: AlexNet, transfer-learned (fine-tuned) from ImageNet weights.
- **Dataset**: [PlantVillage](data/README.md) — 54,306 images, 38 classes.
- **Best result**: 0.987833 accuracy on the test split (see
  [`docs/results.md`](docs/results.md) for the full comparison across 4
  training configurations, and [`MODEL_CARD.md`](MODEL_CARD.md) for scope and
  limitations).
- Full methodology: [`docs/methodology.md`](docs/methodology.md).

## Application

A Flask web app (`app/web/`) with 9 pages: home, upload & analyze, case
history, add/view treatment, statistics, about, and privacy policy. A
separate, partial Kivy mobile prototype also exists (`app/kivy/`) — an early
UI experiment with no model or database wiring.

## Tech Stack

| Layer | Technology |
|---|---|
| Model | PyTorch, AlexNet (transfer learning) |
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| Mobile prototype | Kivy |

Original environment: Python 3.6, Windows, CPU-only training. See
[`requirements-legacy.txt`](requirements-legacy.txt) for what could and
could not be confirmed from surviving artifacts.

## Repository Structure

```text
app/
├── web/            Flask application (main product)
└── kivy/           Partial Kivy mobile UI prototype
scripts/
├── training/       Model training (train_alexnet.py)
├── evaluation/      Accuracy/loss plotting
└── data/           Dataset sampling/splitting
database/           MySQL schema + connectivity script
docs/
├── thesis/         Final thesis PDF
├── presentation/   English adaptation of the defense presentation
├── architecture.md, methodology.md, results.md, historical-context.md,
└── future-deployment.md
data/               Dataset documentation (not the dataset itself)
archive/            Superseded/experimental scripts, kept for reference
MODEL_CARD.md
```

## Results

| Model | Method | Epochs | Accuracy |
|---|---|---|---|
| 1 | feature extraction | 15 | did not finish (interrupted) |
| 2 | feature extraction | 13 | 0.884045 |
| 3 | feature extraction | 20 | 0.897594 |
| 4 (deployed) | fine-tuning | 40 | **0.987833** |

Full table with hardware/timing: [`docs/results.md`](docs/results.md).

## Running the Historical Project

This is a 2020 codebase with no pinned dependency versions and CPU-only
training assumptions. To attempt a local run:

1. Obtain the [PlantVillage dataset](data/README.md) and the trained model
   weights (not included in this repo — see [`MODEL_CARD.md`](MODEL_CARD.md)
   and [`docs/future-deployment.md`](docs/future-deployment.md)).
2. Set up MySQL and apply [`database/plant_disease_sql_script.sql`](database/plant_disease_sql_script.sql).
3. Set environment variables: `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`,
   `MYSQL_DATABASE`, `FLASK_SECRET_KEY`.
4. Install dependencies per [`requirements-legacy.txt`](requirements-legacy.txt)
   (only `torch==1.5.0`/`torchvision==0.6.0` are confirmed-accurate; others
   are unpinned in the original project).
5. Run `app/web/web_application.py`.

**Compatibility note**: modern PyTorch/Flask versions may not load a model
pickled with PyTorch 1.5 without adjustment, and Flask's API has changed in
several places since 2020. This has not been re-verified against a current
environment as part of this restoration — see
[`MODEL_CARD.md`](MODEL_CARD.md) for the honest run-status assessment.

## Thesis

Full thesis (Ukrainian, PDF): [`docs/thesis/Antonevych_diploma_thesis_2020_final.pdf`](docs/thesis/Antonevych_diploma_thesis_2020_final.pdf)

## Presentation

The original Ukrainian defense presentation and an English adaptation of its
full content: [`docs/presentation/`](docs/presentation/README.md).

## Historical Context

See [`docs/historical-context.md`](docs/historical-context.md) for what
"2020" and "2026" each mean in this repository, and why some material from
the original source was intentionally excluded.

## Limitations

- Evaluated only on the PlantVillage benchmark — no field-condition
  validation.
- No precision/recall/F1/confusion-matrix breakdown, only overall accuracy.
- CPU-only training constrained experimentation to 4 configurations.
- The trained model weights (~228 MB) are not included in this repository.

## What I'd Improve Today

Not part of the original 2020 work — noted separately per the restoration
scope: a modern re-implementation would likely use a more modern backbone
(e.g. EfficientNet or a ViT) with GPU training, add real precision/recall/F1
evaluation and a held-out field-photo test set, containerize the app, and
move image storage off local disk.

## Author

**Maryna Antonevych** — [github.com/marine-ai-dev](https://github.com/marine-ai-dev)

## License

MIT (see [LICENSE](LICENSE)) for the original author's own code. The
PlantVillage dataset is third-party and not covered by this license — see
[`data/README.md`](data/README.md).
