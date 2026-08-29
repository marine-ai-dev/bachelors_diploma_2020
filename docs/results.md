# Results

All figures below are taken verbatim from Table 3.1 of the thesis. Nothing
here has been re-measured or re-derived — it is a historical record.

| | Model 1 | Model 2 | Model 3 | Model 4 (deployed) |
|---|---|---|---|---|
| RAM | 8 GB | 8 GB | 16 GB | 16 GB |
| PyTorch / torchvision | 1.4.0 / 0.5.0 | 1.4.0 / 0.5.0 | 1.5.0 / 0.6.0 | 1.5.0 / 0.6.0 |
| Processor | CPU | CPU | CPU | CPU |
| Epochs | 15 | 13 | 20 | 40 |
| Batch size | 64 | 64 | 64 | 128 |
| Training method | feature extraction | feature extraction | feature extraction | fine-tuning |
| Training time | ~600 min (crashed, OOM at epoch 12) | 494 min 59 sec | 237 min 6 sec | 950 min 47 sec |
| Best accuracy | 0.8862 (incomplete run) | 0.884045 | 0.897594 | **0.987833** |

Model 4 (fine-tuning, 40 epochs, batch size 128) was selected for the
deployed web application based on its accuracy on the PlantVillage test
split.

Per-run raw accuracy/loss logs and plots are preserved in
[`scripts/evaluation/`](../scripts/evaluation/) and
[`assets/results/`](../assets/results/) (dated 20/21/24/25 April 2020,
matching the 4 configurations above).

## Caveats

- All training was CPU-only; no GPU was used or available.
- Reported accuracy is on the PlantVillage test split only — no evaluation
  against out-of-distribution field photos (e.g. real smartphone photos in
  variable lighting) is documented in the thesis beyond a small, informal set
  of personal test images that were not part of the formal evaluation.
- No precision/recall/F1 or confusion matrix is reported in the source
  document — only overall accuracy per configuration.
