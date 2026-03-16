import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

train_df["text"] = train_df["subject"].fillna("") + " " + train_df["body"].fillna("")
test_df["text"] = test_df["subject"].fillna("") + " " + test_df["body"].fillna("")

X_train, y_train = train_df["text"], train_df["label"]
X_test = test_df["text"]

vectorizer = CountVectorizer(max_features=50)
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_bow, y_train)

y_pred = model.predict(X_test_bow)

pd.DataFrame({"label": y_pred}).to_csv("predictions.csv", index=False)

