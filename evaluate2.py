import pandas as pd
from sklearn.metrics import f1_score
import os

# 1. Define paths where Codabench will place the files
# Standard Codabench path mapping:
submission_path = "submission.csv"  # Where the participant's file lands
ground_truth_path = "test_with_labels.csv" # Where your hidden file lives

def evaluate():
    # Load data
    submission = pd.read_csv(submission_path)
    truth = pd.read_csv(ground_truth_path)

    # 2. Safety Check: Ensure the user submitted the right number of rows
    if len(submission) != len(truth):
        raise ValueError(f"Submission has {len(submission)} rows, expected {len(truth)}")

    # 3. Calculate F1-Score
    # We assume both CSVs have a column named 'label'
    score = f1_score(truth['label'], submission['label'], average='binary')

    # 4. Save result to scores.txt (Codabench looks for this file)
    with open('/output/scores.txt', 'w') as f:
        f.write(f"f1_score:{score}")

if __name__ == "__main__":
    evaluate()
