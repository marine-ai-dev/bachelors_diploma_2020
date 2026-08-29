# Dataset

## What was used

**PlantVillage dataset** — 54,306 leaf images across 14 crop species and 38 classes
(12 healthy, 26 diseased), published by the PlantVillage project at Penn State
University. The thesis used the **segmented** variant (leaf isolated from
background) with an 80/20 train/test split.

Crops covered: Apple, Blueberry, Cherry, Corn (Maize), Grape, Orange, Peach,
Pepper (Bell), Potato, Raspberry, Soybean, Squash, Strawberry, Tomato.

## Is it included in this repository?

No. The raw dataset (tens of thousands of images, multiple GB across the
color/grayscale/segmented variants) is not committed here. PlantVillage is a
third-party public research dataset — it is not this project's original work,
and redistributing the full image set adds size without benefit given it is
already publicly available upstream.

## How to obtain it

The PlantVillage dataset is publicly available (search "PlantVillage dataset"
or "spMohanty/PlantVillage-Dataset" on GitHub). Download it and arrange it as
an `ImageFolder`-compatible directory (one subfolder per class) to reproduce
the training pipeline in [`scripts/training/train_alexnet.py`](../scripts/training/train_alexnet.py).

## Author's own test images

The original project also included a small set of personal photos used for
manual/ad-hoc testing of the trained model (`datasets/my_test/` in the
original source tree). These are not included in this repository — they carry
no reproducibility value beyond what the PlantVillage test split already
provides.
