# =============================================================================
# DENTAL APPOINTMENT ML MODEL SCRIPT
# =============================================================================
# This script trains a Decision Tree model for no-show prediction.
# This is the most business-relevant prediction for dental clinics.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import sys

# Add scripts folder to path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Paths, Columns

# Machine Learning imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix

# Set random seed for reproducibility
np.random.seed(42)

# Matplotlib settings
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12


# =============================================================================
# DATA LOADING AND PREPROCESSING
# =============================================================================

def load_and_preprocess_data():
    """Load cleaned data and prepare it for ML."""
    print("=" * 60)
    print("MACHINE LEARNING: NO-SHOW PREDICTION")
    print("=" * 60)
    
    if not os.path.exists(Paths.CLEANED_CSV):
        print(f"\nError: Error: Cleaned CSV not found at {Paths.CLEANED_CSV}")
        print("Please run data_cleaning.py first.")
        return None
    
    print(f"\n Loading data from: {Paths.CLEANED_CSV}")
    
    df = pd.read_csv(Paths.CLEANED_CSV)
    print(f" Loaded {len(df)} records")
    
    return df


def prepare_features(df):
    """Prepare features for machine learning."""
    print("\n" + "-" * 40)
    print("Preparing Features")
    print("-" * 40)
    
    # Create a copy for ML
    ml_df = df.copy()
    
    # Encode categorical variables
    label_encoders = {}
    categorical_cols = [
        Columns.PATIENT_GENDER,
        Columns.SPECIALIZATION,
        Columns.APPOINTMENT_DAY,
        Columns.TIME_SLOT,
        Columns.BOOKING_TYPE
    ]
    
    for col in categorical_cols:
        le = LabelEncoder()
        ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
        label_encoders[col] = le
        print(f"  - Encoded: {col}")
    
    # Prepare classification target (no_show)
    ml_df['target_classification'] = (ml_df[Columns.NO_SHOW] == 'Yes').astype(int)
    
    # Select features for model
    feature_columns = [
        Columns.PATIENT_AGE,
        Columns.APPOINTMENT_DURATION,
        Columns.PATIENT_GENDER + '_encoded',
        Columns.SPECIALIZATION + '_encoded',
        Columns.APPOINTMENT_DAY + '_encoded',
        Columns.TIME_SLOT + '_encoded',
        Columns.BOOKING_TYPE + '_encoded'
    ]
    
    X = ml_df[feature_columns]
    y = ml_df['target_classification']
    
    print(f"\n Features prepared: {len(feature_columns)} features")
    print(f" Target: no_show (Yes={y.sum()}, No={len(y)-y.sum()})")
    
    return X, y, feature_columns, label_encoders


# =============================================================================
# DECISION TREE MODEL
# =============================================================================

def train_decision_tree(X_train, X_test, y_train, y_test, feature_columns):
    """Train and evaluate Decision Tree model for no-show classification."""
    print("\n" + "=" * 60)
    print("DECISION TREE CLASSIFIER")
    print("=" * 60)
    print("Purpose: Predict appointment no-shows (Yes/No)")
    print("Business Value: Helps reduce revenue loss and improve scheduling")
    print("-" * 40)
    
    # Train model
    model = DecisionTreeClassifier(random_state=42, max_depth=5, min_samples_split=10)
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"\n   Model Performance:")
    print(f"  - Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  - Precision: {precision:.4f}")
    print(f"  - Recall:    {recall:.4f}")
    print(f"  - F1-Score:  {f1:.4f}")
    
    # Feature importance
    print("\n   Feature Importance (What Drives No-Shows):")
    importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for _, row in importance.head(5).iterrows():
        print(f"    - {row['feature']}: {row['importance']:.4f}")
    
    return model, importance, {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}, y_pred


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_confusion_matrix(y_test, y_pred):
    """Plot confusion matrix for Decision Tree."""
    cm = confusion_matrix(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(cm, cmap='Blues')
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    
    # Labels
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Show (0)', 'No-Show (1)'])
    ax.set_yticklabels(['Show (0)', 'No-Show (1)'])
    
    # Add text annotations
    for i in range(2):
        for j in range(2):
            text_color = 'white' if cm[i, j] > cm.max() / 2 else 'black'
            ax.text(j, i, str(cm[i, j]), ha='center', va='center', 
                   color=text_color, fontsize=16, fontweight='bold')
    
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title('Decision Tree - Confusion Matrix - Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(Paths.GRAPHS_DIR, 'decision_tree_confusion_matrix.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {filepath}")


def plot_feature_importance(importance):
    """Plot feature importance bar chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort and plot
    importance_sorted = importance.sort_values('importance', ascending=True)
    
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(importance_sorted)))
    
    bars = ax.barh(importance_sorted['feature'], importance_sorted['importance'], 
                   color=colors, edgecolor='white')
    
    ax.set_xlabel('Importance')
    ax.set_ylabel('Feature')
    ax.set_title('Decision Tree - Feature Importance - Bar Chart', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(Paths.GRAPHS_DIR, 'decision_tree_feature_importance.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {filepath}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    
    # Load data
    df = load_and_preprocess_data()
    if df is None:
        return
    
    # Prepare features
    X, y, feature_columns, label_encoders = prepare_features(df)
    
    # Split data for classification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n Train set: {len(X_train)} samples")
    print(f" Test set: {len(X_test)} samples")
    
    # Train Decision Tree
    model, importance, metrics, y_pred = train_decision_tree(
        X_train, X_test, y_train, y_test, feature_columns
    )
    
    # Generate Visualizations
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    print("\n Decision Tree Visualizations:")
    plot_confusion_matrix(y_test, y_pred)
    plot_feature_importance(importance)
    
    # Final Summary
    print("\n" + "=" * 60)
    print("ML MODEL SUMMARY")
    print("=" * 60)
    
    print("\n┌─────────────────────────────────────────────────────────┐")
    print("│         DECISION TREE - NO-SHOW PREDICTION              │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│                                                         │")
    print("│  Algorithm: Decision Tree Classifier                   │")
    print(f"│  Target: No-Show (Yes/No)                               │")
    print(f"│  Accuracy: {metrics['accuracy']*100:.2f}%                                      │")
    print(f"│  Precision: {metrics['precision']:.4f}                                  │")
    print(f"│  Recall: {metrics['recall']:.4f}                                     │")
    print(f"│  F1-Score: {metrics['f1']:.4f}                                    │")
    print("│                                                         │")
    print("│  Business Impact:                                       │")
    print("│  - Predicts which patients may not show up              │")
    print("│  - Helps optimize scheduling and reduce revenue loss    │")
    print("│  - Enables proactive reminder campaigns                 │")
    print("│                                                         │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n ML model training completed!")
    print(f" Visualizations saved to: {Paths.GRAPHS_DIR}")
    
    return model


if __name__ == "__main__":
    model = main()
