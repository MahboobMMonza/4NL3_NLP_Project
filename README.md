# Phishing and Spam Email Detection using NLP AI

This repository contains the source code, datasets, notebook experiments, and
the final research paper for an advanced Natural Language Processing (NLP)
system designed to detect phishing and spam emails.

A complementary [Codabench benchmark](https://www.codabench.org/competitions/14689/) was also created.

---

By leveraging traditional machine learning baselines and fine-tuning
state-of-the-art transformer models (such as RoBERTa and ELECTRA), this project
demonstrates high-accuracy identification of malicious email communications.

## Project Overview

Phishing remains one of the most prominent cyber threats globally. This project
systematically explores various NLP methodologies to combat this issue:

1. **Data Collection & Curation**: Aggregating, cleaning, and splitting email
   datasets into train, validation, and test subsets.
2. **Annotation Tools**: Custom Python scripts and Graphical User Interfaces
   (GUIs) to manually verify or label sample data.
3. **Baseline Modeling**: Implementing simple non-neural approaches like Random
   Baselines and Logistic Regression with Bag-of-Words (BOW).
4. **Advanced Transformers & Ensembles**: Jupyter notebooks detailing the
   fine-tuning of `roberta-base` and `electra-base`, as well as combining TF-IDF
Logistic Regression with RoBERTa, as different training approaches.
5. **Rigorous Evaluation**: Scripts evaluating model metrics via precision,
   recall, F1-score, and confusion matrices.

---

## Getting Started

### 1. Prerequisites

Ensure you have Python 3.8+ installed along with the required libraries. You can
set up your environment by installing standard data science and NLP
dependencies:

```bash
pip install numpy pandas scikit-learn
torch transformers matplotlib tqdm
```

### 2. Running Baselines

To establish initial benchmark performance, run the random baseline or the
Bag-of-Words Logistic Regression, ensuring file paths are corrected as
necessary:
```bash
# Run Random Baseline
python random_baseline.py

# Run Logistic Regression with Bag-of-Words
python LrwithBOW.py
```

### 3. Data Annotation

If you want to manually inspect or label new email contents, you can use either
the CLI script or the Graphical User Interface:

```bash
# Start the graphical annotation wizard
python annotate_gui.py

# Or use the command line annotation script
python annotate.py
```

### 4. Advanced Transformer Models

The model fine-tuning process for state-of-the-art transformers is documented
step-by-step inside the collaborative notebooks. Explore the individual team
member workflows to see how models were developed and trained:
* `phishing_detection_omar.ipynb`: Random Forest Classifier
* `phishing_detection_hamza.ipynb`: TF-IDF Logistic Regression + RoBERTa
Ensemble
* `phishing_detection_mahboob.ipynb`: ELECTRA fine-tune model
* `phishing_detection_viro.ipynb`: RoBERTa fine-tune model

### 5. Evaluation (Local)

To generate evaluation metrics and plot confusion matrices for your model
predictions against ground truth labels:

```bash
python evaluate2.py
```
### 6. Evaluation (Codabench)

The results obtained can be submitted to Codabench as a zip file containing the
appropriate CSV file in accordance with the Codabench page instructions.

---

## Results & Performance

The models are rigorously evaluated using standard classification metrics.
Results indicate that while traditional machine learning methods (Random Forest,
Logistic Regression) offer lightweight options, transformer-based architectures
dramatically reduce **False Negatives**, while maintaining a relatively low cost.

### Confusion Matrices

You can inspect the exact performance breakdown across
the different approaches:

* **Baseline (Random Forest)**: `Final Project TeX/Images/rfclf_cfm.png`
* **Fine-Tuned RoBERTa**: `Final Project TeX/Images/ft_roberta_base_cfm.png`
* **Fine-Tuned ELECTRA**: `Final Project TeX/Images/ft_electra_base_cfm.png`
* **Ensemble Architecture**: `Final Project TeX/Images/ensemble_cfm.png`

---

## Formal Report

A formal publication-grade report structured using the ACL
format details the methodology, dataset preprocessing, hyperparameters, and
detailed analysis.

The compiled document can be reviewed directly at: `Final Project TeX/main.pdf`

---

## Contributors

This repository reflects a collaborative group effort of the following
students, with equal contribution from all four members:

* **Hamza Abou Jaib**
* **Mohammad Mahdi Mahboob**
* **Omar Al-Asfar**
* **Virochaan Ravichandran**
