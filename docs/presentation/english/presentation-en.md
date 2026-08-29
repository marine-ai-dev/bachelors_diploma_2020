# Presentation (English Adaptation)

*Adapted from the original Ukrainian defense presentation,
`Антоневич_презентація_диплом_v4.pptx` (2020). Technical claims and figures
are unchanged from the original; wording is adapted for a natural English
technical audience.*

## 1. Title

**Intelligent Application for Identifying Diseases of Agricultural Plants
Based on Deep Learning**
Maryna Antonevych, 4th-year student, group KN-41, Computer Science —
Taras Shevchenko National University of Kyiv, Faculty of Information
Technology, Department of Intelligent Technologies. Supervisor: Iryna
Domanetska, PhD. Kyiv, 2020.

## 2–4. Motivation

Plant disease is a major threat to global food security. As agriculture
strives to feed a growing population, crop disease reduces both the yield
and quality of food, fiber, and biofuel crops — and directly threatens the
livelihoods of smallholder farmers, who generate 80% of agricultural output
worldwide. Between 20% and 40% of edible-crop yield is lost every year to
pests and plant disease.

## 5. Research object, subject, and goal

- **Object**: tools for automated recognition of agricultural plant diseases
  using computer vision.
- **Subject**: methods for recognizing plant diseases from leaf images using
  convolutional neural networks.
- **Goal**: develop an intelligent application for identifying diseases of
  agricultural plants.

## 6. Approach

Plant image recognition is performed using deep artificial neural networks.

## 7. Related work

- Mohanty et al. — AlexNet and GoogLeNet on this classification problem,
  85–99% accuracy.
- Honcharov et al. — Siamese neural networks, >99% accuracy detecting
  certain grape diseases.
- Mendu — a CNN ("PlantNet") reaching 95.4% overall accuracy.

## 8–10. System design

Context-level and Level-1 Data Flow Diagrams, plus a structural (block)
diagram of the system, were produced ahead of implementation.

## 11. Database design

Designed in MySQL Workbench, running on MySQL Server.

## 12. Model architecture — AlexNet

Layers 1–5: convolutional. Layers 6–7: fully connected. Layer 8: output
(final) layer.

## 13. Dataset

**PlantVillage** — 54,306 images (RGB, grayscale, and segmented variants),
80/20 train/test split. PlantVillage is a research initiative at Penn State
University aimed at helping smallholder farmers through cheap, accessible
technology. 38 classes (12 healthy, 26 diseased) across 14 crops: Apple,
Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry,
Soybean, Squash, Strawberry, Tomato.

## 14–18. Training runs

| Model | RAM | Epochs | Batch size | Method | Time | Accuracy | Outcome |
|---|---|---|---|---|---|---|---|
| 1 | 8 GB | 15 | 64 | feature extraction | 600 min | — | did not finish (interrupted) |
| 2 | 8 GB | 13 | 64 | feature extraction | 494 min 59 s | 0.884045 | trained successfully |
| 3 | 16 GB | 20 | 64 | feature extraction | 237 min 6 s | 0.897594 | trained successfully |
| 4 | 16 GB | 40 | 128 | fine-tuning | 950 min 47 s | 0.987833 | **best result** |

## 20. Application workflow

Stack: MySQL, HTML/CSS/JavaScript, Python Flask, PyTorch.

Plant image → Flask server → neural network / database → application
interface → result.

## 21–35. Application walkthrough

- **Home** — landing page.
- **Main (upload & analyze)** — user uploads a plant photo and clicks
  "Analyze"; a warning is shown if no photo is selected. Results show the
  predicted class, probability, pathogen name, disease description, and (for
  diseased classes) a list of suggested treatment products with manufacturer,
  description, and usage instructions, retrieved from the database. Healthy
  results show only the class and probability.
- **Case History** — browse past classification results.
- **Add Treatment** — record a treatment.
- **Treatment History** — view logged treatments.
- **Statistics** — a dashboard of classification case statistics.
- **About** — project and contact information.

## 36. Conclusions

This thesis focused on developing tools for the automated, intelligent
identification of agricultural plant diseases. The design and implementation
of an intelligent application based on the AlexNet convolutional neural
network were completed, built with HTML/CSS/JavaScript on the frontend, a
Python Flask backend, and a MySQL database. Related work was published in the
proceedings of the VI International Scientific and Practical Conference
"Information Technologies and Interactions" (IT&I-2019).

## 37. Contact

Maryna Antonevych — Faculty of Information Technology, Taras Shevchenko
National University of Kyiv, Kyiv, Ukraine.
