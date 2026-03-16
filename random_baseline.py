import pandas as pd
import numpy as np

test = pd.read_csv("test.csv")

pred = np.random.randint(0, 2, size=len(test))

df = pd.DataFrame(pred, columns=["label"])
df.to_csv("submission.csv", index=False)

print("Predictions Complete")