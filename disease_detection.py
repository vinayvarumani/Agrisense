from utils.disease_preprocess import load_and_preprocess_data

(X_train, X_test, y_train, y_test), label_map = load_and_preprocess_data()

print("Train set size:", X_train.shape)
print("Test set size:", X_test.shape)
print("Class label mapping:", label_map)
