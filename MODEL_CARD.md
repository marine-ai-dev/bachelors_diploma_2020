# Model Card

## Overview

- **Task**: Multi-class image classification of agricultural plant
  disease/health status from a single leaf photo.
- **Architecture**: AlexNet (5 conv + 3 fully-connected layers), transfer
  learning from ImageNet-pretrained weights, fine-tuned end-to-end.
- **Classes**: 38 (26 disease classes + 12 healthy classes across 14 crop
  species).
- **Framework**: PyTorch 1.5.0 / torchvision 0.6.0 (as recorded for the final
  training run — see [`docs/results.md`](docs/results.md)).
- **Training hardware**: CPU only, 16 GB RAM.
- **Best reported accuracy**: 0.987833 on the PlantVillage test split
  (80/20 split, segmented image variant).

## Training data

[PlantVillage dataset](data/README.md) — 54,306 images, segmented variant.
Not redistributed in this repository; see `data/README.md` for how to obtain
it.

## Intended use (as originally scoped)

A student thesis prototype demonstrating automated crop-disease
identification via a web application: a user uploads a leaf photo, the model
classifies it, and — for diseased classes — the application looks up
suggested treatments from a MySQL database.

## Known limitations

- Trained and evaluated only on PlantVillage — a dataset of clean,
  single-leaf, mostly lab-quality photos. Real-world field photos (variable
  background, lighting, multiple leaves, disease co-occurrence) were not part
  of formal evaluation.
- No precision/recall/F1/confusion-matrix breakdown was produced — only
  overall accuracy.
- CPU-only training in 2020 limited experimentation (only 4 configurations
  were tried; the largest run took ~16 hours).
- The trained weights (`alexnet__pytorch_new_last.pth`, ~228 MB) are not
  committed to this repository due to size — see
  [`docs/future-deployment.md`](docs/future-deployment.md) and the main
  README for how to obtain or reconstruct them.

## Ethical / deployment considerations

This was never deployed as a production agronomy tool and should not be
treated as one — a 2020 undergraduate thesis prototype evaluated on a single
public benchmark is not sufficient validation for real farming decisions.
