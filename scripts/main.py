# =============================================================================
# DENTAL APPOINTMENT EDA PROJECT - INTERACTIVE MENU SYSTEM
# =============================================================================
# Run this file to access all project features through an interactive menu.
# Features: View Charts, Make Predictions, View Analysis, Run Full Pipeline
# =============================================================================

import os
import sys
import webbrowser
import pickle

# Get the scripts directory path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

# Add scripts directory to path
sys.path.insert(0, SCRIPTS_DIR)

# Import configuration
from config import Paths, Columns, ValidValues, DentistData

# Import pandas and numpy for data analysis
import pandas as pd
import numpy as np

# Import sklearn for predictions
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================

# Trained models (will be loaded/trained when needed)
trained_models = {
    'linear_regression': None,
    'logistic_regression': None,
    'decision_tree': None,
    'scaler_lin': None,
    'scaler_log': None,
    'label_encoders': None,
    'feature_columns': None
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_menu(title, options):
    """Print a formatted menu."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)
    for key, value in options.items():
        print(f"  {key}. {value}")
    print("=" * 60)


def get_choice(prompt, valid_choices):
    """Get user input with validation."""
    while True:
        choice = input(f"\n{prompt}: ").strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")


def press_enter():
    """Wait for user to press Enter."""
    input("\nPress ENTER to continue...")


# =============================================================================
# DATA LOADING
# =============================================================================

def load_data():
    """Load the cleaned dataset."""
    if not os.path.exists(Paths.CLEANED_CSV):
        print("\n❌ Cleaned data not found. Running data cleaning first...")
        run_full_pipeline()
    
    return pd.read_csv(Paths.CLEANED_CSV)


# =============================================================================
# TRAIN MODELS (for predictions)
# =============================================================================

def train_models_for_prediction():
    """Train models and store them for predictions."""
    global trained_models
    
    print("\n🔄 Training models for prediction...")
    
    df = load_data()
    
    # Prepare features
    ml_df = df.copy()
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
    
    # Feature columns
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
    y_class = (ml_df[Columns.NO_SHOW] == 'Yes').astype(int)
    y_reg = ml_df[Columns.WAITING_TIME]
    
    # Train Linear Regression
    scaler_lin = StandardScaler()
    X_scaled_lin = scaler_lin.fit_transform(X)
    lin_model = LinearRegression()
    lin_model.fit(X_scaled_lin, y_reg)
    
    # Train Logistic Regression
    scaler_log = StandardScaler()
    X_scaled_log = scaler_log.fit_transform(X)
    log_model = LogisticRegression(random_state=42, max_iter=1000)
    log_model.fit(X_scaled_log, y_class)
    
    # Train Decision Tree
    dt_model = DecisionTreeClassifier(random_state=42, max_depth=5)
    dt_model.fit(X, y_class)
    
    # Store models
    trained_models['linear_regression'] = lin_model
    trained_models['logistic_regression'] = log_model
    trained_models['decision_tree'] = dt_model
    trained_models['scaler_lin'] = scaler_lin
    trained_models['scaler_log'] = scaler_log
    trained_models['label_encoders'] = label_encoders
    trained_models['feature_columns'] = feature_columns
    
    print("✅ Models trained successfully!")


# =============================================================================
# MENU 1: VIEW CHARTS
# =============================================================================

def view_charts_menu():
    """Display menu to view charts (interactive matplotlib windows)."""
    import eda_analysis
    import ml_model
    
    while True:
        print_header("VIEW CHARTS")
        print("\nSelect a chart to view:\n")
        print("  1. Appointments per Dentist (Bar Chart)")
        print("  2. Appointment Status Distribution (Pie Chart)")
        print("  3. Daily Appointment Trend (Line Chart)")
        print("  4. Patient Age Distribution (Histogram)")
        print("  5. Busy Time Slots (Heatmap)")
        print("  0. Back to Main Menu")
        
        choice = get_choice("Enter choice", ['1', '2', '3', '4', '5', '0'])
        
        if choice == '0':
            return
        
        # Load data for chart generation
        df = eda_analysis.load_cleaned_data()
        if df is None:
            print("\n❌ No data found. Run the full pipeline first.")
            press_enter()
            continue
        
        if choice == '1':
            eda_analysis.plot_appointments_per_dentist(df)
        elif choice == '2':
            eda_analysis.plot_status_distribution(df)
        elif choice == '3':
            eda_analysis.plot_daily_trend(df)
        elif choice == '4':
            eda_analysis.plot_age_distribution(df)
        elif choice == '5':
            eda_analysis.plot_busy_time_slots(df)
        
        press_enter()


# =============================================================================
# MENU 2: MAKE PREDICTIONS
# =============================================================================

def prediction_menu():
    """Display menu for making predictions."""
    
    # Ensure models are trained
    if trained_models['linear_regression'] is None:
        train_models_for_prediction()
    
    while True:
        print_header("PREDICTION MENU")
        options = {
            '1': 'Predict Waiting Time (Linear Regression)',
            '2': 'Predict No-Show (Logistic Regression)',
            '3': 'Predict No-Show (Decision Tree)',
            '0': 'Back to Main Menu'
        }
        print_menu("SELECT PREDICTION TYPE", options)
        
        choice = get_choice("Enter choice", list(options.keys()))
        
        if choice == '0':
            return
        elif choice == '1':
            predict_waiting_time()
        elif choice == '2':
            predict_no_show('logistic')
        elif choice == '3':
            predict_no_show('decision_tree')


def get_prediction_input():
    """Get input values from user for prediction."""
    print("\n" + "-" * 40)
    print("Enter Patient/Appointment Details:")
    print("-" * 40)
    
    # Age
    while True:
        try:
            age = int(input("Patient Age (5-85): "))
            if 5 <= age <= 85:
                break
            print("Please enter age between 5 and 85.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Duration
    print("\nDuration options: 15, 30, 45, 60 minutes")
    while True:
        try:
            duration = int(input("Appointment Duration (minutes): "))
            if duration in [15, 30, 45, 60]:
                break
            print("Please enter 15, 30, 45, or 60.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Gender
    while True:
        gender = input("Patient Gender (M/F): ").upper().strip()
        if gender in ['M', 'F']:
            break
        print("Please enter M or F.")
    
    # Specialization
    print("\nSpecializations:")
    specs = ValidValues.SPECIALIZATIONS
    for i, spec in enumerate(specs, 1):
        print(f"  {i}. {spec}")
    while True:
        try:
            spec_idx = int(input("Select specialization (1-5): ")) - 1
            if 0 <= spec_idx < len(specs):
                specialization = specs[spec_idx]
                break
            print("Please enter 1-5.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Day
    print("\nDay of appointment:")
    days = ValidValues.DAYS_OF_WEEK
    for i, day in enumerate(days, 1):
        print(f"  {i}. {day}")
    while True:
        try:
            day_idx = int(input("Select day (1-7): ")) - 1
            if 0 <= day_idx < len(days):
                day = days[day_idx]
                break
            print("Please enter 1-7.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Time slot
    print("\nTime slots:")
    slots = ValidValues.TIME_SLOTS
    for i, slot in enumerate(slots, 1):
        print(f"  {i}. {slot}")
    while True:
        try:
            slot_idx = int(input(f"Select time slot (1-{len(slots)}): ")) - 1
            if 0 <= slot_idx < len(slots):
                time_slot = slots[slot_idx]
                break
            print(f"Please enter 1-{len(slots)}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Booking type
    while True:
        booking = input("Booking Type (Online/Walk-in): ").strip()
        if booking.lower() in ['online', 'walk-in', 'walkin']:
            booking = 'Online' if booking.lower() == 'online' else 'Walk-in'
            break
        print("Please enter Online or Walk-in.")
    
    return {
        'age': age,
        'duration': duration,
        'gender': gender,
        'specialization': specialization,
        'day': day,
        'time_slot': time_slot,
        'booking_type': booking
    }


def prepare_features_for_prediction(input_data):
    """Convert user input to model features."""
    le = trained_models['label_encoders']
    
    features = [
        input_data['age'],
        input_data['duration'],
        le[Columns.PATIENT_GENDER].transform([input_data['gender']])[0],
        le[Columns.SPECIALIZATION].transform([input_data['specialization']])[0],
        le[Columns.APPOINTMENT_DAY].transform([input_data['day']])[0],
        le[Columns.TIME_SLOT].transform([input_data['time_slot']])[0],
        le[Columns.BOOKING_TYPE].transform([input_data['booking_type']])[0]
    ]
    
    return np.array(features).reshape(1, -1)


def predict_waiting_time():
    """Predict waiting time using Linear Regression."""
    print_header("PREDICT WAITING TIME (Linear Regression)")
    
    input_data = get_prediction_input()
    features = prepare_features_for_prediction(input_data)
    
    # Scale and predict
    features_scaled = trained_models['scaler_lin'].transform(features)
    prediction = trained_models['linear_regression'].predict(features_scaled)[0]
    
    # Ensure non-negative
    prediction = max(0, prediction)
    
    print("\n" + "=" * 50)
    print("  PREDICTION RESULT")
    print("=" * 50)
    print(f"\n  📊 Model: Linear Regression")
    print(f"  🎯 Predicted Waiting Time: {prediction:.1f} minutes")
    print("\n  Input Summary:")
    print(f"    • Age: {input_data['age']}")
    print(f"    • Duration: {input_data['duration']} mins")
    print(f"    • Gender: {input_data['gender']}")
    print(f"    • Specialization: {input_data['specialization']}")
    print(f"    • Day: {input_data['day']}")
    print(f"    • Time Slot: {input_data['time_slot']}")
    print(f"    • Booking: {input_data['booking_type']}")
    print("=" * 50)
    
    press_enter()


def predict_no_show(model_type):
    """Predict no-show using classification model."""
    model_name = "Logistic Regression" if model_type == 'logistic' else "Decision Tree"
    print_header(f"PREDICT NO-SHOW ({model_name})")
    
    input_data = get_prediction_input()
    features = prepare_features_for_prediction(input_data)
    
    if model_type == 'logistic':
        features_scaled = trained_models['scaler_log'].transform(features)
        prediction = trained_models['logistic_regression'].predict(features_scaled)[0]
        probability = trained_models['logistic_regression'].predict_proba(features_scaled)[0]
    else:
        prediction = trained_models['decision_tree'].predict(features)[0]
        probability = trained_models['decision_tree'].predict_proba(features)[0]
    
    result = "YES (Patient may not show up)" if prediction == 1 else "NO (Patient will likely show up)"
    
    print("\n" + "=" * 50)
    print("  PREDICTION RESULT")
    print("=" * 50)
    print(f"\n  📊 Model: {model_name}")
    print(f"\n  🎯 Will Patient No-Show? {result}")
    print(f"\n  📈 Probability:")
    print(f"    • Will Show: {probability[0]*100:.1f}%")
    print(f"    • Won't Show: {probability[1]*100:.1f}%")
    print("\n  Input Summary:")
    print(f"    • Age: {input_data['age']}")
    print(f"    • Duration: {input_data['duration']} mins")
    print(f"    • Gender: {input_data['gender']}")
    print(f"    • Specialization: {input_data['specialization']}")
    print(f"    • Day: {input_data['day']}")
    print(f"    • Time Slot: {input_data['time_slot']}")
    print(f"    • Booking: {input_data['booking_type']}")
    print("=" * 50)
    
    press_enter()


# =============================================================================
# MENU 3: VIEW ANALYSIS
# =============================================================================

def analysis_menu():
    """Display menu for viewing analysis insights."""
    
    while True:
        print_header("VIEW ANALYSIS INSIGHTS")
        options = {
            '1': 'Dentist Workload Analysis',
            '2': 'Appointment Status Analysis',
            '3': 'Peak Time Analysis',
            '4': 'Patient Demographics Analysis',
            '5': 'No-Show Behavior Analysis',
            '6': 'Complete Data Summary',
            '0': 'Back to Main Menu'
        }
        print_menu("SELECT ANALYSIS", options)
        
        choice = get_choice("Enter choice", list(options.keys()))
        
        if choice == '0':
            return
        elif choice == '1':
            analyze_dentist_workload()
        elif choice == '2':
            analyze_appointment_status()
        elif choice == '3':
            analyze_peak_times()
        elif choice == '4':
            analyze_patient_demographics()
        elif choice == '5':
            analyze_no_show()
        elif choice == '6':
            show_complete_summary()
        
        press_enter()


def analyze_dentist_workload():
    """Show dentist workload analysis."""
    df = load_data()
    
    print_header("DENTIST WORKLOAD ANALYSIS")
    
    workload = df.groupby([Columns.DENTIST_ID, Columns.DENTIST_NAME]).size().reset_index(name='appointments')
    workload = workload.sort_values('appointments', ascending=False)
    
    print("\n📊 Appointments per Dentist:")
    print("-" * 50)
    for _, row in workload.iterrows():
        bar = "█" * (row['appointments'] // 3)
        print(f"  {row[Columns.DENTIST_NAME]}: {row['appointments']} {bar}")
    
    print("-" * 50)
    print(f"\n  📈 Summary:")
    print(f"    • Total Dentists: {len(workload)}")
    print(f"    • Busiest: {workload.iloc[0][Columns.DENTIST_NAME]} ({workload.iloc[0]['appointments']} appointments)")
    print(f"    • Least Busy: {workload.iloc[-1][Columns.DENTIST_NAME]} ({workload.iloc[-1]['appointments']} appointments)")
    print(f"    • Average Workload: {workload['appointments'].mean():.1f} appointments/dentist")


def analyze_appointment_status():
    """Show appointment status analysis."""
    df = load_data()
    
    print_header("APPOINTMENT STATUS ANALYSIS")
    
    status_counts = df[Columns.APPOINTMENT_STATUS].value_counts()
    total = len(df)
    
    print("\n📊 Status Distribution:")
    print("-" * 50)
    for status, count in status_counts.items():
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"  {status}: {count} ({pct:.1f}%) {bar}")
    
    print("-" * 50)
    print(f"\n  📈 Summary:")
    print(f"    • Total Appointments: {total}")
    print(f"    • Completion Rate: {status_counts.get('Completed', 0)/total*100:.1f}%")
    print(f"    • Cancellation Rate: {status_counts.get('Cancelled', 0)/total*100:.1f}%")


def analyze_peak_times():
    """Show peak time analysis."""
    df = load_data()
    
    print_header("PEAK TIME ANALYSIS")
    
    # By day
    day_counts = df[Columns.APPOINTMENT_DAY].value_counts()
    
    print("\n📊 Appointments by Day:")
    print("-" * 50)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in day_order:
        if day in day_counts.index:
            count = day_counts[day]
            bar = "█" * (count // 2)
            print(f"  {day:12}: {count:3} {bar}")
    
    # By time slot
    time_counts = df[Columns.TIME_SLOT].value_counts().head(5)
    
    print("\n📊 Top 5 Busiest Time Slots:")
    print("-" * 50)
    for slot, count in time_counts.items():
        bar = "█" * (count // 2)
        print(f"  {slot}: {count} {bar}")
    
    print("-" * 50)
    print(f"\n  📈 Summary:")
    print(f"    • Busiest Day: {day_counts.idxmax()} ({day_counts.max()} appointments)")
    print(f"    • Busiest Slot: {time_counts.idxmax()} ({time_counts.max()} appointments)")


def analyze_patient_demographics():
    """Show patient demographics analysis."""
    df = load_data()
    
    print_header("PATIENT DEMOGRAPHICS ANALYSIS")
    
    # Age statistics
    print("\n📊 Age Distribution:")
    print("-" * 50)
    print(f"  • Minimum Age: {df[Columns.PATIENT_AGE].min()} years")
    print(f"  • Maximum Age: {df[Columns.PATIENT_AGE].max()} years")
    print(f"  • Average Age: {df[Columns.PATIENT_AGE].mean():.1f} years")
    print(f"  • Median Age: {df[Columns.PATIENT_AGE].median():.0f} years")
    
    # Age groups
    bins = [0, 18, 35, 55, 100]
    labels = ['Children (0-17)', 'Young Adults (18-34)', 'Adults (35-54)', 'Seniors (55+)']
    df['age_group'] = pd.cut(df[Columns.PATIENT_AGE], bins=bins, labels=labels)
    age_groups = df['age_group'].value_counts().sort_index()
    
    print("\n📊 Age Groups:")
    print("-" * 50)
    for group, count in age_groups.items():
        pct = count / len(df) * 100
        bar = "█" * int(pct / 2)
        print(f"  {group}: {count} ({pct:.1f}%) {bar}")
    
    # Gender
    gender_counts = df[Columns.PATIENT_GENDER].value_counts()
    print("\n📊 Gender Distribution:")
    print("-" * 50)
    for gender, count in gender_counts.items():
        pct = count / len(df) * 100
        label = "Male" if gender == 'M' else "Female"
        print(f"  {label}: {count} ({pct:.1f}%)")


def analyze_no_show():
    """Show no-show behavior analysis."""
    df = load_data()
    
    print_header("NO-SHOW BEHAVIOR ANALYSIS")
    
    no_show_rate = (df[Columns.NO_SHOW] == 'Yes').mean() * 100
    
    print(f"\n📊 Overall No-Show Rate: {no_show_rate:.1f}%")
    print("-" * 50)
    
    # By booking type
    print("\n📊 No-Show Rate by Booking Type:")
    for booking in df[Columns.BOOKING_TYPE].unique():
        subset = df[df[Columns.BOOKING_TYPE] == booking]
        rate = (subset[Columns.NO_SHOW] == 'Yes').mean() * 100
        print(f"  • {booking}: {rate:.1f}%")
    
    # By day
    print("\n📊 No-Show Rate by Day:")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in day_order:
        subset = df[df[Columns.APPOINTMENT_DAY] == day]
        if len(subset) > 0:
            rate = (subset[Columns.NO_SHOW] == 'Yes').mean() * 100
            bar = "█" * int(rate)
            print(f"  {day:12}: {rate:5.1f}% {bar}")


def show_complete_summary():
    """Show complete data summary."""
    df = load_data()
    
    print_header("COMPLETE DATA SUMMARY")
    
    print("\n📊 Dataset Overview:")
    print("-" * 50)
    print(f"  • Total Records: {len(df)}")
    print(f"  • Total Columns: {len(df.columns)}")
    print(f"  • Date Range: {df[Columns.APPOINTMENT_DATE].min()} to {df[Columns.APPOINTMENT_DATE].max()}")
    
    print("\n📊 Quick Statistics:")
    print("-" * 50)
    print(f"  • Total Dentists: {df[Columns.DENTIST_ID].nunique()}")
    print(f"  • Total Patients: {df[Columns.PATIENT_ID].nunique()}")
    print(f"  • Completion Rate: {(df[Columns.APPOINTMENT_STATUS] == 'Completed').mean()*100:.1f}%")
    print(f"  • No-Show Rate: {(df[Columns.NO_SHOW] == 'Yes').mean()*100:.1f}%")
    print(f"  • Online Booking Rate: {(df[Columns.BOOKING_TYPE] == 'Online').mean()*100:.1f}%")
    print(f"  • Average Age: {df[Columns.PATIENT_AGE].mean():.1f} years")
    print(f"  • Average Duration: {df[Columns.APPOINTMENT_DURATION].mean():.1f} mins")
    print(f"  • Average Wait Time: {df[Columns.WAITING_TIME].mean():.1f} mins")


# =============================================================================
# MENU 4: RUN FULL PIPELINE
# =============================================================================

def run_full_pipeline():
    """Run the complete EDA pipeline."""
    print_header("RUNNING FULL PIPELINE")
    
    print("\nThis will run:")
    print("  1. Data Cleaning")
    print("  2. EDA Analysis (Generate Charts)")
    print("  3. ML Model Training")
    
    confirm = input("\nProceed? (y/n): ").lower().strip()
    if confirm != 'y':
        return
    
    # Import and run modules
    import data_cleaning
    import eda_analysis
    import ml_model
    
    print("\n" + "-" * 40)
    print("Step 1: Data Cleaning")
    print("-" * 40)
    data_cleaning.main()
    
    print("\n" + "-" * 40)
    print("Step 2: EDA Analysis")
    print("-" * 40)
    eda_analysis.main()
    
    print("\n" + "-" * 40)
    print("Step 3: ML Models")
    print("-" * 40)
    ml_model.main()
    
    print("\n" + "=" * 50)
    print("  🎉 FULL PIPELINE COMPLETED!")
    print("=" * 50)
    
    press_enter()


# =============================================================================
# MAIN MENU
# =============================================================================

def main_menu():
    """Display the main menu."""
    
    while True:
        print("\n")
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "  DENTAL APPOINTMENT ANALYSIS SYSTEM".center(58) + "║")
        print("║" + "  EDA & Machine Learning Project".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╠" + "═" * 58 + "╣")
        print("║" + " " * 58 + "║")
        print("║" + "  1. 📊 View Charts".ljust(58) + "║")
        print("║" + "  2. 🔮 Make Predictions".ljust(58) + "║")
        print("║" + "  3. 📈 View Analysis Insights".ljust(58) + "║")
        print("║" + "  4. ⚙️  Run Full Pipeline".ljust(58) + "║")
        print("║" + "  5. ❌ Exit".ljust(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "═" * 58 + "╝")
        
        choice = get_choice("Enter your choice (1-5)", ['1', '2', '3', '4', '5'])
        
        if choice == '1':
            view_charts_menu()
        elif choice == '2':
            prediction_menu()
        elif choice == '3':
            analysis_menu()
        elif choice == '4':
            run_full_pipeline()
        elif choice == '5':
            print("\n👋 Thank you for using Dental Appointment Analysis System!")
            print("   Goodbye!\n")
            break


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main_menu()
