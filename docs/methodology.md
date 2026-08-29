# Methodology

Source: the final thesis, `docs/thesis/Antonevych_diploma_thesis_2020_final.pdf`
(sections 1–3.5). Claims below are what the thesis states; nothing here is
invented or extrapolated beyond the document.

## Problem

Automated identification of agricultural plant diseases from leaf images,
motivated by the economic weight of agriculture in Ukraine and the global
food-security risk posed by crop disease, especially for smallholder farmers.

## Literature review (as cited in the thesis)

- Mohanty et al. — AlexNet / GoogLeNet on PlantVillage, ~85–99% accuracy.
- Honcharov et al. — Siamese networks for grape disease detection, >99%
  accuracy on some classes.
- Mendu — CNN ("PlantNet"), 95.4% overall accuracy.
- A 2019 study comparing AlexNet vs. a custom "MyNet" across RGB/grayscale/
  segmented PlantVillage variants.

## Approach taken

1. **Architecture choice: AlexNet** (5 convolutional layers + 3 fully
   connected layers + softmax), selected as an established, comparatively
   simple CNN baseline suited to the available (CPU-only) compute.
2. **Transfer learning** from ImageNet-pretrained weights, with two training
   modes compared: feature extraction (freeze backbone, retrain final layer
   only) and fine-tuning (retrain all layers).
3. **Preprocessing**: images resized to ≥224×224, RGB, scaled to [0,1],
   normalized with ImageNet mean/std (`[0.485, 0.456, 0.406]` /
   `[0.229, 0.224, 0.225]`).
4. **System design**: DFD diagrams (Gane–Sarson notation, ERwin Process
   Modeler) and a structural/function-tree diagram were produced before
   implementation; database designed in MySQL Workbench.
5. **Empirical model selection**: 4 candidate training configurations were
   run and compared on loss/accuracy curves (see
   [`docs/results.md`](results.md)); the best-performing configuration
   (fine-tuning, 40 epochs) was deployed in the final application.

## Evaluation methodology

Accuracy and loss were tracked across training and validation splits for each
of the 4 configurations. No precision/recall/F1/confusion-matrix breakdown
was found in the extracted thesis content — the thesis's own evaluation is
limited to overall accuracy per configuration.

## What is NOT covered by this document

The thesis's Conclusions section (page ~87) and reference list were not fully
recovered during content extraction from the source PDF and are not
summarized here to avoid guessing their content. Read the original PDF
directly for that material.
