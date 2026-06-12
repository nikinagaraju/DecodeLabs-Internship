"""
DecodeLabs - Project 2: Data Classification Using AI
Algorithm: K-Nearest Neighbors on the Iris Dataset
Pipeline: Load → Scale → Split → Train → Evaluate
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix, classification_report,
    f1_score, accuracy_score
)

# ─────────────────────────────────────────────
# STEP 1 — LOAD & UNDERSTAND THE DATASET
# ─────────────────────────────────────────────
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target, name="species")
class_names = iris.target_names  # ['setosa', 'versicolor', 'virginica']

print("=" * 55)
print("  DecodeLabs | Project 2: Data Classification Using AI")
print("=" * 55)
print(f"\n📦 Dataset: Iris Benchmark")
print(f"   Samples   : {X.shape[0]}")
print(f"   Features  : {X.shape[1]}  →  {list(iris.feature_names)}")
print(f"   Classes   : {len(class_names)}  →  {list(class_names)}")
print(f"\n{X.describe().round(2)}")

# ─────────────────────────────────────────────
# STEP 2 — FEATURE SCALING (StandardScaler)
# ─────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("\n✅ Feature scaling applied  (mean=0, variance=1)")

# ─────────────────────────────────────────────
# STEP 3 — TRAIN / TEST SPLIT  (80 / 20)
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, shuffle=True
)
print(f"\n✅ Train-Test Split")
print(f"   Training samples : {len(X_train)}  (80%)")
print(f"   Testing  samples : {len(X_test)}   (20%)")

# ─────────────────────────────────────────────
# STEP 4 — FIND OPTIMAL K (Elbow Method)
# ─────────────────────────────────────────────
error_rates = []
k_range = range(1, 31)
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    preds = knn.predict(X_test)
    error_rates.append(1 - accuracy_score(y_test, preds))

optimal_k = int(np.argmin(error_rates)) + 1
print(f"\n✅ Optimal K found : K = {optimal_k}  (elbow method)")

# ─────────────────────────────────────────────
# STEP 5 — TRAIN THE MODEL
# ─────────────────────────────────────────────
model = KNeighborsClassifier(n_neighbors=optimal_k)
model.fit(X_train, y_train)
print(f"\n✅ KNN model trained with K = {optimal_k}")

# ─────────────────────────────────────────────
# STEP 6 — PREDICT & EVALUATE
# ─────────────────────────────────────────────
y_pred = model.predict(X_test)

acc    = accuracy_score(y_test, y_pred)
f1     = f1_score(y_test, y_pred, average="weighted")
cm     = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=class_names)

print("\n" + "=" * 55)
print("  MODEL RESULTS")
print("=" * 55)
print(f"  Accuracy  : {acc*100:.2f}%")
print(f"  F1 Score  : {f1:.4f}  (weighted)")
print(f"\n{report}")

# ─────────────────────────────────────────────
# STEP 7 — VISUALISE (4-panel figure)
# ─────────────────────────────────────────────
fig = plt.figure(figsize=(18, 13), facecolor="#F0F4F8")
fig.suptitle(
    "DecodeLabs  |  Project 2: Data Classification Using AI\nIris Dataset — KNN Classifier",
    fontsize=17, fontweight="bold", color="#1a2a4a", y=0.98
)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.35)

BLUE   = "#1a3a6b"
ORANGE = "#e85d04"
PALETTE = ["#1a3a6b", "#e85d04", "#2dc653"]

# ── Panel 1: Elbow curve ──────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(k_range, error_rates, color=BLUE, lw=2.5, marker="o",
         markersize=5, markerfacecolor="white", markeredgecolor=BLUE)
ax1.axvline(optimal_k, color=ORANGE, lw=2, linestyle="--", label=f"Optimal K = {optimal_k}")
ax1.scatter([optimal_k], [error_rates[optimal_k-1]],
            s=160, color=ORANGE, zorder=5)
ax1.set_title("Tuning the Engine: Choosing K", fontweight="bold", color=BLUE)
ax1.set_xlabel("K Value", color="#333")
ax1.set_ylabel("Error Rate", color="#333")
ax1.legend(fontsize=10)
ax1.set_facecolor("#fafbfc")
ax1.grid(True, alpha=0.3)

# ── Panel 2: Confusion Matrix ─────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names,
            ax=ax2, linewidths=0.5, annot_kws={"size": 14, "weight": "bold"},
            cbar=False)
ax2.set_title("Confusion Matrix", fontweight="bold", color=BLUE)
ax2.set_xlabel("Predicted Label", color="#333")
ax2.set_ylabel("True Label", color="#333")
ax2.tick_params(axis="x", rotation=20)

# ── Panel 3: F1 per class bar chart ──────────────────────
ax3 = fig.add_subplot(gs[1, 0])
per_class_f1 = f1_score(y_test, y_pred, average=None)
bars = ax3.bar(class_names, per_class_f1, color=PALETTE, edgecolor="white",
               linewidth=1.2, width=0.55)
for bar, val in zip(bars, per_class_f1):
    ax3.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.02,
             f"{val:.2f}", ha="center", va="bottom",
             fontsize=12, fontweight="bold", color="#1a2a4a")
ax3.set_title("F1 Score per Class", fontweight="bold", color=BLUE)
ax3.set_ylabel("F1 Score", color="#333")
ax3.set_ylim(0, 1.15)
ax3.set_facecolor("#fafbfc")
ax3.grid(axis="y", alpha=0.3)

# ── Panel 4: Decision scatter (petal features) ────────────
ax4 = fig.add_subplot(gs[1, 1])
# Use original (unscaled) petal length vs petal width for readability
X_arr = np.array(X)
for cls_idx, (cls_name, col) in enumerate(zip(class_names, PALETTE)):
    mask = (y == cls_idx)
    ax4.scatter(X_arr[mask, 2], X_arr[mask, 3],
                label=cls_name, color=col, alpha=0.75,
                edgecolors="white", linewidths=0.5, s=70)
ax4.set_title("Feature Space: Petal Length vs Width", fontweight="bold", color=BLUE)
ax4.set_xlabel("Petal Length (cm)", color="#333")
ax4.set_ylabel("Petal Width (cm)", color="#333")
ax4.legend(title="Species", fontsize=9)
ax4.set_facecolor("#fafbfc")
ax4.grid(True, alpha=0.3)

# ── Score banner at bottom ────────────────────────────────
fig.text(0.5, 0.01,
         f"Accuracy: {acc*100:.2f}%   |   Weighted F1 Score: {f1:.4f}   |   K = {optimal_k}   |   Train/Test: 80/20",
         ha="center", fontsize=12, color="white",
         bbox=dict(boxstyle="round,pad=0.4", facecolor=BLUE, alpha=0.85))

plt.savefig("project2_iris_knn_results.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("\n📊 Visualisation saved.")