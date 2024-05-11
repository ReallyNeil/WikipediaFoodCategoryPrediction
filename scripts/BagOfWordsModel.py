from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer

#Basic Skeleton for bag of words from chatgpt.
# Example data with multiple labels per article
data = [
    ("Health benefits of running and jogging", ["Health", "Fitness"]),
    ("Investment strategies for 2023", ["Finance", "Economy"]),
    ("The latest trends in machine learning", ["Technology", "AI"]),
    ("How to save money and manage finances", ["Finance", "Lifestyle"]),
    ("Tips for healthy eating", ["Health", "Diet"]),
    ("Advancements in deep learning", ["Technology", "AI"]),
]

articles, labels = zip(*data)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(articles)

# Use MultiLabelBinarizer to convert labels to a binary form
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a OneVsRestClassifier using Logistic Regression
model = OneVsRestClassifier(LogisticRegression())
model.fit(X_train, y_train)

# Predict the categories of the test articles
predictions = model.predict(X_test)

from sklearn.metrics import f1_score

# Calculate F1 Score with 'micro' method
f1_micro = f1_score(y_test, predictions, average='micro')

print(f"F1 Score (Micro): {f1_micro:.2f}")