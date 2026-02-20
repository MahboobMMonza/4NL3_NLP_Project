import pandas as pd
import sys

# Raw agreement and Cohen's Kappa
def calculate_agreement(df):
    # Filter for rows where both team members annotated
    overlap = df[df['annotation1'].notna() & df['annotation2'].notna()].copy()
    
    if len(overlap) < 2:
        print("\n[!] Not enough double-annotated data (need at least 2 rows).")
        return

    # Convert to numeric for math
    y1 = pd.to_numeric(overlap['annotation1']).astype(int)
    y2 = pd.to_numeric(overlap['annotation2']).astype(int)
    
    total = len(y1)
    # 1. Observed Agreement (Po)
    po = (y1 == y2).sum() / total
    
    # 2. Expected Agreement (Pe) - Probability of agreeing by chance
    p1_phish = (y1 == 1).sum() / total
    p2_phish = (y2 == 1).sum() / total
    pe = (p1_phish * p2_phish) + ((1 - p1_phish) * (1 - p2_phish))
    
    # 3. Kappa Calculation
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0

    print("\n" + "═"*40)
    print(f"{'TEAM AGREEMENT (COHEN KAPPA)':^40}")
    print("═"*40)
    print(f"Overlap Samples:  {total}")
    print(f"Raw Agreement:    {po*100:.2f}%")
    print(f"Cohen's Kappa:    {kappa:.3f}")
    print("-" * 40)
    print("Interpretation: 0.6-0.8 Good, >0.8 Excellent")
    print("═"*40 + "\n")

    
def annotate_data(file_path, start_idx=0, end_idx=None):
    df = pd.read_csv(file_path)
    
    # Ensure annotation columns exist
    for col in ['annotation1', 'annotation2']:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = df[col].astype("Int64")

    # Set the limit for annotation
    limit = min(end_idx, len(df)) if end_idx is not None else len(df)

    print(f"Annotating indices {start_idx} to {limit-1}. Press 'q' to quit.")
    
    for i in range(start_idx, limit):
        # Skip if already fully annotated by two people
        if pd.notna(df.at[i, 'annotation1']) and pd.notna(df.at[i, 'annotation2']):
            continue
            
        print("\n" + "═"*68)
        print(f"INDEX: {i} / {len(df)-1}")
        print(f"FROM:  {str(df.at[i, 'sender'])}")
        print(f"TO:    {str(df.at[i, 'receiver'])}")
        print(f"DATE:  {str(df.at[i, 'date'])}")
        print(f"SUBJECT:  {str(df.at[i, 'subject'])}")
        print("═"*68)
        print("BODY:")
        print(f"{df.at[i, 'body']}")
        print("═"*68)
        
        # Decide which slot to fill, fill annotation1 first, then annotation2
        target_col = 'annotation1' if pd.isna(df.at[i, 'annotation1']) else 'annotation2'
        
        if target_col == 'annotation2':
            print(f"*** DOUBLE ANNOTATION MODE ***")
        
        prompt = "Label (0=Legit, 1=Phish, q=Quit): "
        label = input(prompt).strip().lower()
        
        if label == 'q':
            break
        elif label in ['0', '1']:
            df.at[i, target_col] = int(label)
            # Save progress
            df.to_csv(file_path, index=False)
        else:
            print("Invalid input. Use 0, 1, or q.")
            
    print("\nProgress saved to CSV. Closing interface.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python annotate.py your_data.csv [start_index]  <- To Annotate")
        print("  python annotate.py your_data.csv --stats        <- To Check Agreement")
        sys.exit(1)

    file = sys.argv[1]
    
    if "--stats" in sys.argv:
        try:
            df = pd.read_csv(file)
            calculate_agreement(df)
        except FileNotFoundError:
            print("Error: File not found.")
    else:
        try:
            start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            # Check for end index
            end = int(sys.argv[3]) if len(sys.argv) > 3 else None
            annotate_data(file, start, end)
        except FileNotFoundError:
            print("Error: File not found.")
        except ValueError:
            print("Error: Start index must be a number.")