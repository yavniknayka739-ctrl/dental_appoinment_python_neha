# =============================================================================
# DENTAL APPOINTMENT EDA PROJECT - AUTO-RUN SCRIPT
# =============================================================================
# This script automatically runs all analysis steps without user interaction.
# Outputs: Data Cleaning -> EDA Charts -> Analysis Insights -> ML Model
# =============================================================================

import os
import sys

# Get the scripts directory path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

# Add scripts directory to path
sys.path.insert(0, SCRIPTS_DIR)

# Import configuration
from config import Paths, Columns

# Import pandas and numpy for data analysis
import pandas as pd
import numpy as np


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_separator():
    """Print a visual separator."""
    print("\n" + "-" * 60)


def load_data():
    """Load the cleaned dataset."""
    if not os.path.exists(Paths.CLEANED_CSV):
        print("\nError: Cleaned data not found. Running data cleaning first...")
        import data_cleaning
        data_cleaning.main()
    
    return pd.read_csv(Paths.CLEANED_CSV)


# =============================================================================
# STEP 1: DATA CLEANING
# =============================================================================

def run_data_cleaning():
    """Execute data cleaning step."""
    print_header("STEP 1: DATA CLEANING")
    
    import data_cleaning
    data_cleaning.main()
    
    print("\nData cleaning completed!")


# =============================================================================
# STEP 2: EDA CHARTS GENERATION
# =============================================================================

def run_eda_charts():
    """Generate all EDA charts automatically."""
    print_header("STEP 2: EDA CHARTS GENERATION")
    
    import eda_analysis
    
    # Load data
    df = eda_analysis.load_cleaned_data()
    if df is None:
        print("\nError: Failed to load data for EDA charts.")
        return
    
    print(f"\nLoaded {len(df)} records from cleaned dataset")
    
    # Generate all charts
    charts = [
        ("Appointments per Dentist (Bar Chart)", eda_analysis.plot_appointments_per_dentist),
        ("Appointment Status Distribution (Pie Chart)", eda_analysis.plot_status_distribution),
        ("Daily Appointment Trend (Line Chart)", eda_analysis.plot_daily_trend),
        ("Patient Age Distribution (Histogram)", eda_analysis.plot_age_distribution),
        ("Busy Time Slots (Heatmap)", eda_analysis.plot_busy_time_slots)
    ]
    
    for chart_name, chart_function in charts:
        print(f"\nGenerating: {chart_name}")
        chart_function(df)
    
    print("\nAll EDA charts generated successfully!")


# =============================================================================
# STEP 3: ANALYSIS INSIGHTS (4 MOST RELEVANT SECTIONS)
# =============================================================================

def run_analysis_insights():
    """Print the 4 most business-relevant analysis insights."""
    print_header("STEP 3: ANALYSIS INSIGHTS")
    
    df = load_data()
    
    # 1. Dentist Workload Analysis
    print_separator()
    print("DENTIST WORKLOAD ANALYSIS")
    print_separator()
    
    workload = df.groupby([Columns.DENTIST_ID, Columns.DENTIST_NAME]).size().reset_index(name='appointments')
    workload = workload.sort_values('appointments', ascending=False)
    
    print("\nAppointments per Dentist:")
    for _, row in workload.iterrows():
        bar = "█" * (row['appointments'] // 3)
        print(f"  {row[Columns.DENTIST_NAME]}: {row['appointments']} {bar}")
    
    print(f"\n  Summary:")
    print(f"    - Total Dentists: {len(workload)}")
    print(f"    - Busiest: {workload.iloc[0][Columns.DENTIST_NAME]} ({workload.iloc[0]['appointments']} appointments)")
    print(f"    - Least Busy: {workload.iloc[-1][Columns.DENTIST_NAME]} ({workload.iloc[-1]['appointments']} appointments)")
    print(f"    - Average Workload: {workload['appointments'].mean():.1f} appointments/dentist")
    
    # 2. Appointment Status Analysis
    print_separator()
    print("APPOINTMENT STATUS ANALYSIS")
    print_separator()
    
    status_counts = df[Columns.APPOINTMENT_STATUS].value_counts()
    total = len(df)
    
    print("\nStatus Distribution:")
    for status, count in status_counts.items():
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"  {status}: {count} ({pct:.1f}%) {bar}")
    
    print(f"\n  Summary:")
    print(f"    - Total Appointments: {total}")
    print(f"    - Completion Rate: {status_counts.get('Completed', 0)/total*100:.1f}%")
    print(f"    - Cancellation Rate: {status_counts.get('Cancelled', 0)/total*100:.1f}%")
    
    # 3. Peak Time Analysis
    print_separator()
    print("PEAK TIME ANALYSIS")
    print_separator()
    
    day_counts = df[Columns.APPOINTMENT_DAY].value_counts()
    
    print("\nAppointments by Day:")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in day_order:
        if day in day_counts.index:
            count = day_counts[day]
            bar = "█" * (count // 2)
            print(f"  {day:12}: {count:3} {bar}")
    
    time_counts = df[Columns.TIME_SLOT].value_counts().head(5)
    
    print("\nTop 5 Busiest Time Slots:")
    for slot, count in time_counts.items():
        bar = "█" * (count // 2)
        print(f"  {slot}: {count} {bar}")
    
    print(f"\n  Summary:")
    print(f"    - Busiest Day: {day_counts.idxmax()} ({day_counts.max()} appointments)")
    print(f"    - Busiest Slot: {time_counts.idxmax()} ({time_counts.max()} appointments)")
    
    # 4. No-Show Behavior Analysis
    print_separator()
    print("NO-SHOW BEHAVIOR ANALYSIS")
    print_separator()
    
    no_show_rate = (df[Columns.NO_SHOW] == 'Yes').mean() * 100
    
    print(f"\nOverall No-Show Rate: {no_show_rate:.1f}%")
    
    print("\nNo-Show Rate by Booking Type:")
    for booking in df[Columns.BOOKING_TYPE].unique():
        subset = df[df[Columns.BOOKING_TYPE] == booking]
        rate = (subset[Columns.NO_SHOW] == 'Yes').mean() * 100
        print(f"  - {booking}: {rate:.1f}%")
    
    print("\nNo-Show Rate by Day:")
    for day in day_order:
        subset = df[df[Columns.APPOINTMENT_DAY] == day]
        if len(subset) > 0:
            rate = (subset[Columns.NO_SHOW] == 'Yes').mean() * 100
            bar = "█" * int(rate)
            print(f"  {day:12}: {rate:5.1f}% {bar}")
    
    print("\nAll analysis insights generated!")


# =============================================================================
# STEP 4: MACHINE LEARNING - DECISION TREE FOR NO-SHOW PREDICTION
# =============================================================================

def run_ml_model():
    """Train and evaluate the Decision Tree model."""
    print_header("STEP 4: MACHINE LEARNING - NO-SHOW PREDICTION")
    
    print("\nTraining Decision Tree model for no-show prediction...")
    
    import ml_model
    model = ml_model.main()
    
    print("\nMachine learning model trained and evaluated!")
    
    return model


# =============================================================================
# STEP 5: SAMPLE PREDICTION DEMONSTRATION
# =============================================================================

def run_sample_prediction():
    """Demonstrate a sample prediction using the trained model."""
    print_header("STEP 5: SAMPLE NO-SHOW PREDICTION")
    
    print("\nPreparing sample prediction...")
    
    # Load the trained model
    import ml_model
    
    # Load data for encoding
    df = load_data()
    
    # Prepare features
    X, y, feature_columns, label_encoders = ml_model.prepare_features(df)
    
    # Train model (quick retrain for demo)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier(random_state=42, max_depth=5, min_samples_split=10)
    model.fit(X_train, y_train)
    
    # Create sample patient data
    print("\nSample Patient Profile:")
    print("  - Age: 45 years")
    print("  - Gender: Female")
    print("  - Specialization: Orthodontics")
    print("  - Day: Monday")
    print("  - Time Slot: 10:00-11:00")
    print("  - Booking Type: Online")
    print("  - Duration: 30 minutes")
    
    # Encode sample data
    sample_data = {
        Columns.PATIENT_AGE: 45,
        Columns.APPOINTMENT_DURATION: 30,
        Columns.PATIENT_GENDER: 'F',
        Columns.SPECIALIZATION: 'Orthodontics',
        Columns.APPOINTMENT_DAY: 'Monday',
        Columns.TIME_SLOT: '10:00-11:00',
        Columns.BOOKING_TYPE: 'Online'
    }
    
    # Encode categorical variables
    sample_encoded = []
    sample_encoded.append(sample_data[Columns.PATIENT_AGE])
    sample_encoded.append(sample_data[Columns.APPOINTMENT_DURATION])
    
    for col in [Columns.PATIENT_GENDER, Columns.SPECIALIZATION, Columns.APPOINTMENT_DAY, 
                Columns.TIME_SLOT, Columns.BOOKING_TYPE]:
        try:
            encoded_value = label_encoders[col].transform([sample_data[col]])[0]
            sample_encoded.append(encoded_value)
        except:
            # If value not in training data, use 0
            sample_encoded.append(0)
    
    # Make prediction
    prediction = model.predict([sample_encoded])[0]
    probability = model.predict_proba([sample_encoded])[0]
    
    # Display results
    print("\nPrediction Results:")
    print(f"\n  Model: Decision Tree Classifier")
    print(f"\n  Will Patient No-Show? {'YES' if prediction == 1 else 'NO'}")
    
    if prediction == 1:
        print(f"  Confidence: {probability[1]*100:.1f}%")
        print("\n  Recommendation:")
        print("    - Send reminder SMS/email 24 hours before appointment")
        print("    - Consider calling patient to confirm attendance")
        print("    - Have backup patient on waitlist")
    else:
        print(f"  Confidence: {probability[0]*100:.1f}%")
        print("\n  Recommendation:")
        print("    - Standard appointment confirmation")
        print("    - Patient likely to attend as scheduled")
    
    print("\nSample prediction completed!")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to execute all steps sequentially."""
    
    # Print welcome banner
    print("\n" + "=" * 60)
    print("         DENTAL APPOINTMENT ANALYSIS")
    print("           EDA & Machine Learning Project")
    print("                AUTO-RUN MODE")
    print("=" * 60)
    
    print("\nStarting automated analysis pipeline...\n")
    
    # Execute all steps
    run_data_cleaning()
    run_eda_charts()
    run_analysis_insights()
    run_ml_model()
    run_sample_prediction()
    
    # Print completion summary
    print_header("ANALYSIS PIPELINE COMPLETED SUCCESSFULLY!")
    
    print("\n  Summary of Generated Outputs:")
    print("    - Cleaned data saved")
    print("    - EDA charts generated (graphs/ folder)")
    print("    - Analysis insights printed")
    print("    - ML model trained and evaluated")
    print("    - Sample prediction demonstrated")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
