import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.metrics import classification_report

# Set paths
data_dir = "artifacts/disease"

# Load preprocessed data
train_images = np.load(os.path.join(data_dir, "train_images.npy"))
train_labels = np.load(os.path.join(data_dir, "train_labels.npy"))
val_images = np.load(os.path.join(data_dir, "test_images.npy"))
val_labels = np.load(os.path.join(data_dir, "test_labels.npy"))

# Squeeze if needed
train_labels = np.squeeze(train_labels)
val_labels = np.squeeze(val_labels)

print("train_labels shape after squeeze:", train_labels.shape)
print("val_labels shape after squeeze:", val_labels.shape)

# Use raw labels (already multi-label binary)
num_classes = train_labels.shape[1]
train_labels_cat = train_labels
val_labels_cat = val_labels

# Model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=train_images.shape[1:]),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='sigmoid')  # ⬅ multi-label output
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',   # ⬅ correct loss for multi-label
              metrics=['accuracy'])

# Train the model
history = model.fit(train_images, train_labels_cat,
                    validation_data=(val_images, val_labels_cat),
                    epochs=10,
                    batch_size=32)

# Evaluate
pred_probs = model.predict(val_images)
pred_labels = (pred_probs > 0.5).astype(int)  # ⬅ multi-label thresholding

print(classification_report(val_labels, pred_labels))

# Save model
model.save(os.path.join(data_dir, "plant_disease_model.h5"))
print("✅ Model saved to:", os.path.join(data_dir, "plant_disease_model.h5"))
