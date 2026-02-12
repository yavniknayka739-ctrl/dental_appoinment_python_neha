# =============================================================================
# DENTAL APPOINTMENT ML MODEL SCRIPT (OPTIONAL)
# =============================================================================
# This script trains machine learning models for:
# 1. REGRESSION: Linear Regression - Predict waiting time (continuous)
# 2. CLASSIFICATION: Logistic Regression - Predict no-show (Yes/No)
# 3. CLASSIFICATION: Decision Tree - Predict no-show with feature importance
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

from config import Paths, Columns, ValidValues

# Machine Learning imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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
    print("DENTAL APPOINTMENT ML MODEL")
    print("=" * 60)
    
    if not os.path.exists(Paths.CLEANED_CSV):
        print(f"\n❌ Error: Cleaned CSV not found at {Paths.CLEANED_CSV}")
        print("Please run data_cleaning.py first.")
        return None
    
    print(f"\n📂 Loading data from: {Paths.CLEANED_CSV}")
    
    df = pd.read_csv(Paths.CLEANED_CSV)
    print(f"✓ Loaded {len(df)} records")
    
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
        Columns.APPOINTMENT_STATUS,
        Columns.BOOKING_TYPE
    ]
    
    for col in categorical_cols:
        le = LabelEncoder()
        ml_df[col + '_encoded'] = le.fit_transform(ml_df[col].astype(str))
        label_encoders[col] = le
        print(f"  • Encoded: {col}")
    
    # Prepare classification target (no_show)
    ml_df['target_classification'] = (ml_df[Columns.NO_SHOW] == 'Yes').astype(int)
    
    # Prepare regression target (waiting_time)
    ml_df['target_regression'] = ml_df[Columns.WAITING_TIME]
    
    # Select features for model (excluding targets)
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
    y_classification = ml_df['target_classification']
    y_regression = ml_df['target_regression']
    
    print(f"\n✓ Features prepared: {len(feature_columns)} features")
    print(f"✓ Classification Target: no_show (Yes={y_classification.sum()}, No={len(y_classification)-y_classification.sum()})")
    print(f"✓ Regression Target: waiting_time (Mean={y_regression.mean():.1f} mins)")
    
    return X, y_classification, y_regression, feature_columns, label_encoders


# =============================================================================
# MODEL 1: LINEAR REGRESSION (Prediction - Continuous)
# =============================================================================

def train_linear_regression(X_train, X_test, y_train, y_test, feature_columns):
    """Train and evaluate Linear Regression model for waiting time prediction."""
    print("\n" + "=" * 60)
    print("MODEL 1: LINEAR REGRESSION (Regression/Prediction)")
    print("=" * 60)
    print("Purpose: Predict waiting time (continuous value in minutes)")
    print("-" * 40)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate using regression metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n  📊 Regression Model Performance:")
    print(f"  • Mean Squared Error (MSE):      {mse:.4f}")
    print(f"  • Root Mean Squared Error (RMSE): {rmse:.4f} minutes")
    print(f"  • Mean Absolute Error (MAE):      {mae:.4f} minutes")
    print(f"  • R² Score:                       {r2:.4f} ({r2*100:.2f}%)")
    
    # Feature coefficients
    print(f"\n  📋 Feature Coefficients (Impact on Waiting Time):")
    coefficients = pd.DataFrame({
        'feature': feature_columns,
        'coefficient': model.coef_
    }).sort_values('coefficient', key=abs, ascending=False)
    
    for _, row in coefficients.head(5).iterrows():
        direction = "↑" if row['coefficient'] > 0 else "↓"
        print(f"    • {row['feature']}: {row['coefficient']:.4f} {direction}")
    
    metrics = {'mse': mse, 'rmse': rmse, 'mae': mae, 'r2': r2}
    
    return model, scaler, metrics, coefficients, y_pred


# =============================================================================
# MODEL 2: LOGISTIC REGRESSION (Classification)
# =============================================================================

def train_logistic_regression(X_train, X_test, y_train, y_test):
    """Train and evaluate Logistic Regression model for no-show classification."""
    print("\n" + "=" * 60)
    print("MODEL 2: LOGISTIC REGRESSION (Classification)")
    print("=" * 60)
    print("Purpose: Classify appointments as No-Show (Yes/No)")
    print("-" * 40)
    
    # Scale features for logistic regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Evaluate using classification metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"\n  📊 Classification Model Performance:")
    print(f"  • Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  • Precision: {precision:.4f}")
    print(f"  • Recall:    {recall:.4f}")
    print(f"  • F1-Score:  {f1:.4f}")
    
    return model, scaler, {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}, y_pred


# =============================================================================
# MODEL 3: DECISION TREE (Classification)
# =============================================================================

def train_decision_tree(X_train, X_test, y_train, y_test, feature_columns):
    """Train and evaluate Decision Tree model for no-show classification."""
    print("\n" + "=" * 60)
    print("MODEL 3: DECISION TREE (Classification)")
    print("=" * 60)
    print("Purpose: Classify appointments as No-Show with interpretable rules")
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
    
    print(f"\n  📊 Classification Model Performance:")
    print(f"  • Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  • Precision: {precision:.4f}")
    print(f"  • Recall:    {recall:.4f}")
    print(f"  • F1-Score:  {f1:.4f}")
    
    # Feature importance
    print("\n  📋 Feature Importance:")
    importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for _, row in importance.head(5).iterrows():
        print(f"    • {row['feature']}: {row['importance']:.4f}")
    
    return model, importance, {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}, y_pred


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_linear_regression_results(y_test, y_pred, metrics):
    """Plot Linear Regression actual vs predicted values."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Actual vs Predicted Scatter
    ax1 = axes[0]
    ax1.scatter(y_test, y_pred, alpha=0.6, color='#2E86AB', edgecolors='white')
    
    # Perfect prediction line
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
    
    ax1.set_xlabel('Actual Waiting Time (minutes)')
    ax1.set_ylabel('Predicted Waiting Time (minutes)')
    ax1.set_title('Linear Regression: Actual vs Predicted', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Plot 2: Residual Distribution
    ax2 = axes[1]
    residuals = y_test - y_pred
    ax2.hist(residuals, bins=20, color='#A23B72', edgecolor='white', alpha=0.8)
    ax2.axvline(0, color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel('Residual (Actual - Predicted)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Residual Distribution', fontsize=14, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Add metrics text
    textstr = f'RMSE: {metrics["rmse"]:.2f} min\nMAE: {metrics["mae"]:.2f} min\nR²: {metrics["r2"]:.4f}'
    ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(Paths.GRAPHS_DIR, 'linear_regression_results.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()
    
    print(f"  ✓ Saved: {filepath}")


def plot_confusion_matrix(y_test, y_pred, model_name):
    """Plot confusion matrix for a classification model."""
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
    ax.set_title(f'{model_name} - Confusion Matrix', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Save
    filename = f"{model_name.lower().replace(' ', '_')}_confusion_matrix.png"
    filepath = os.path.join(Paths.GRAPHS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()
    
    print(f"  ✓ Saved: {filepath}")


def plot_feature_importance(importance, model_name):
    """Plot feature importance bar chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort and plot
    importance_sorted = importance.sort_values('importance', ascending=True)
    
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(importance_sorted)))
    
    bars = ax.barh(importance_sorted['feature'], importance_sorted['importance'], 
                   color=colors, edgecolor='white')
    
    ax.set_xlabel('Importance')
    ax.set_ylabel('Feature')
    ax.set_title(f'{model_name} - Feature Importance', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Save
    filename = f"{model_name.lower().replace(' ', '_')}_feature_importance.png"
    filepath = os.path.join(Paths.GRAPHS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()
    
    print(f"  ✓ Saved: {filepath}")


def plot_model_comparison(lr_metrics, dt_metrics):
    """Plot comparison of classification model performances."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    x = np.arange(len(metrics))
    width = 0.35
    
    lr_values = [lr_metrics[m] for m in metrics]
    dt_values = [dt_metrics[m] for m in metrics]
    
    bars1 = ax.bar(x - width/2, lr_values, width, label='Logistic Regression', color='#2E86AB')
    bars2 = ax.bar(x + width/2, dt_values, width, label='Decision Tree', color='#A23B72')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_ylabel('Score')
    ax.set_title('Classification Model Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['Accuracy', 'Precision', 'Recall', 'F1-Score'])
    ax.legend()
    ax.set_ylim(0, 1.1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(Paths.GRAPHS_DIR, 'model_comparison.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()
    
    print(f"  ✓ Saved: {filepath}")


def plot_algorithm_summary():
    """Create a summary visualization of all algorithms used."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Data for the summary
    algorithms = ['Linear\nRegression', 'Logistic\nRegression', 'Decision\nTree']
    types = ['Regression\n(Prediction)', 'Classification', 'Classification']
    targets = ['Waiting Time\n(Continuous)', 'No-Show\n(Yes/No)', 'No-Show\n(Yes/No)']
    colors = ['#F18F01', '#2E86AB', '#A23B72']
    
    # Create grouped bar-like visualization
    x = np.arange(len(algorithms))
    
    for i, (algo, typ, target, color) in enumerate(zip(algorithms, types, targets, colors)):
        ax.bar(i, 1, width=0.6, color=color, edgecolor='white', linewidth=2)
        ax.text(i, 0.5, algo, ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        ax.text(i, 1.1, typ, ha='center', va='bottom', fontsize=10, color=color, fontweight='bold')
        ax.text(i, -0.1, target, ha='center', va='top', fontsize=9, color='gray')
    
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.4, 1.5)
    ax.set_title('Machine Learning Algorithms Used in This Project', fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    
    # Save
    filepath = os.path.join(Paths.GRAPHS_DIR, 'algorithm_summary.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()
    
    print(f"  ✓ Saved: {filepath}")


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
    X, y_class, y_reg, feature_columns, label_encoders = prepare_features(df)
    
    # ==========================================================================
    # PART 1: LINEAR REGRESSION (Prediction of continuous value)
    # ==========================================================================
    print("\n" + "=" * 60)
    print("PART 1: REGRESSION (Predicting Continuous Values)")
    print("=" * 60)
    
    # Split data for regression
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )
    
    print(f"\n✓ Train set: {len(X_train_reg)} samples")
    print(f"✓ Test set: {len(X_test_reg)} samples")
    
    # Train Linear Regression
    lin_model, lin_scaler, lin_metrics, coefficients, y_pred_lin = train_linear_regression(
        X_train_reg, X_test_reg, y_train_reg, y_test_reg, feature_columns
    )
    
    # ==========================================================================
    # PART 2: CLASSIFICATION (Predicting Categories)
    # ==========================================================================
    print("\n" + "=" * 60)
    print("PART 2: CLASSIFICATION (Predicting Categories)")
    print("=" * 60)
    
    # Split data for classification
    X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(
        X, y_class, test_size=0.2, random_state=42, stratify=y_class
    )
    
    print(f"\n✓ Train set: {len(X_train_cls)} samples")
    print(f"✓ Test set: {len(X_test_cls)} samples")
    
    # Train Logistic Regression
    log_model, log_scaler, log_metrics, y_pred_log = train_logistic_regression(
        X_train_cls, X_test_cls, y_train_cls, y_test_cls
    )
    
    # Train Decision Tree
    dt_model, importance, dt_metrics, y_pred_dt = train_decision_tree(
        X_train_cls, X_test_cls, y_train_cls, y_test_cls, feature_columns
    )
    
    # ==========================================================================
    # GENERATE VISUALIZATIONS
    # ==========================================================================
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    # Linear Regression plots
    print("\n📊 Linear Regression Visualizations:")
    plot_linear_regression_results(y_test_reg, y_pred_lin, lin_metrics)
    
    # Classification plots
    print("\n📊 Classification Visualizations:")
    plot_confusion_matrix(y_test_cls, y_pred_log, 'Logistic Regression')
    plot_confusion_matrix(y_test_cls, y_pred_dt, 'Decision Tree')
    plot_feature_importance(importance, 'Decision Tree')
    plot_model_comparison(log_metrics, dt_metrics)
    
    # Algorithm summary
    print("\n📊 Algorithm Summary:")
    plot_algorithm_summary()
    
    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================
    print("\n" + "=" * 60)
    print("ML MODEL SUMMARY")
    print("=" * 60)
    
    print("\n┌─────────────────────────────────────────────────────────┐")
    print("│              SUPERVISED LEARNING ALGORITHMS              │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│                                                         │")
    print("│  1. LINEAR REGRESSION (Regression/Prediction)           │")
    print(f"│     → Target: Waiting Time (continuous)                 │")
    print(f"│     → R² Score: {lin_metrics['r2']:.4f}                              │")
    print(f"│     → RMSE: {lin_metrics['rmse']:.2f} minutes                           │")
    print("│                                                         │")
    print("│  2. LOGISTIC REGRESSION (Classification)                │")
    print(f"│     → Target: No-Show (Yes/No)                          │")
    print(f"│     → Accuracy: {log_metrics['accuracy']*100:.2f}%                             │")
    print("│                                                         │")
    print("│  3. DECISION TREE (Classification)                      │")
    print(f"│     → Target: No-Show (Yes/No)                          │")
    print(f"│     → Accuracy: {dt_metrics['accuracy']*100:.2f}%                             │")
    print("│                                                         │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n✅ ML model training completed!")
    print(f"📁 Visualizations saved to: {Paths.GRAPHS_DIR}")
    
    return lin_model, log_model, dt_model


if __name__ == "__main__":
    models = main()
