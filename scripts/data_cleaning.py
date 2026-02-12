# =============================================================================
# DENTAL APPOINTMENT DATA CLEANING SCRIPT
# =============================================================================
# This script cleans the raw CSV data and generates a processed CSV
# Tasks: Handle missing values, remove duplicates, normalize values, validate ranges
# =============================================================================

import pandas as pd
import numpy as np
import os
import sys

# Add scripts folder to path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Paths, Columns, ValidValues, ValidationRanges

# =============================================================================
# DATA LOADING
# =============================================================================

def load_raw_data():
    """Load the raw CSV data."""
    print("=" * 60)
    print("DENTAL APPOINTMENT DATA CLEANING")
    print("=" * 60)
    
    if not os.path.exists(Paths.RAW_CSV):
        print(f"\n❌ Error: Raw CSV not found at {Paths.RAW_CSV}")
        print("Please ensure the raw data file exists.")
        return None
    
    print(f"\n📂 Loading data from: {Paths.RAW_CSV}")
    
    df = pd.read_csv(Paths.RAW_CSV, dtype=str)
    
    print(f"✓ Loaded {len(df)} records with {len(df.columns)} columns")
    
    return df


# =============================================================================
# DATA CLEANING FUNCTIONS
# =============================================================================

def handle_missing_values(df):
    """Handle missing values in the dataset."""
    print("\n" + "-" * 40)
    print("Step 1: Handling Missing Values")
    print("-" * 40)
    
    # Count missing values before
    missing_before = df.isnull().sum().sum() + (df == "").sum().sum()
    print(f"Missing values found: {missing_before}")
    
    # Replace empty strings with NaN for easier handling
    df = df.replace("", np.nan)
    
    # Handle patient_age - fill with median
    if df[Columns.PATIENT_AGE].isnull().any():
        df[Columns.PATIENT_AGE] = pd.to_numeric(df[Columns.PATIENT_AGE], errors='coerce')
        median_age = df[Columns.PATIENT_AGE].median()
        df[Columns.PATIENT_AGE] = df[Columns.PATIENT_AGE].fillna(median_age)
        print(f"  • Filled missing ages with median: {median_age:.0f}")
    
    # Handle patient_gender - fill with mode
    if df[Columns.PATIENT_GENDER].isnull().any():
        mode_gender = df[Columns.PATIENT_GENDER].mode()[0] if not df[Columns.PATIENT_GENDER].mode().empty else "M"
        df[Columns.PATIENT_GENDER] = df[Columns.PATIENT_GENDER].fillna(mode_gender)
        print(f"  • Filled missing genders with mode: {mode_gender}")
    
    # Handle appointment_duration - fill with mode
    if df[Columns.APPOINTMENT_DURATION].isnull().any():
        df[Columns.APPOINTMENT_DURATION] = pd.to_numeric(df[Columns.APPOINTMENT_DURATION], errors='coerce')
        mode_duration = df[Columns.APPOINTMENT_DURATION].mode()[0] if not df[Columns.APPOINTMENT_DURATION].mode().empty else 30
        df[Columns.APPOINTMENT_DURATION] = df[Columns.APPOINTMENT_DURATION].fillna(mode_duration)
        print(f"  • Filled missing durations with mode: {mode_duration:.0f} mins")
    
    # Handle booking_type - fill with mode
    if df[Columns.BOOKING_TYPE].isnull().any():
        mode_booking = df[Columns.BOOKING_TYPE].mode()[0] if not df[Columns.BOOKING_TYPE].mode().empty else "Online"
        df[Columns.BOOKING_TYPE] = df[Columns.BOOKING_TYPE].fillna(mode_booking)
        print(f"  • Filled missing booking types with mode: {mode_booking}")
    
    # Count missing values after
    missing_after = df.isnull().sum().sum()
    print(f"\n✓ Missing values after cleaning: {missing_after}")
    
    return df


def remove_duplicates(df):
    """Remove duplicate records based on patient and appointment details."""
    print("\n" + "-" * 40)
    print("Step 2: Removing Duplicates")
    print("-" * 40)
    
    records_before = len(df)
    
    # Check for exact duplicates (excluding appointment_id)
    duplicate_cols = [col for col in Columns.ALL_COLUMNS if col != Columns.APPOINTMENT_ID]
    df = df.drop_duplicates(subset=duplicate_cols, keep='first')
    
    records_after = len(df)
    removed = records_before - records_after
    
    print(f"  • Records before: {records_before}")
    print(f"  • Duplicates removed: {removed}")
    print(f"✓ Records after: {records_after}")
    
    return df


def normalize_categorical_values(df):
    """Normalize categorical values to standard formats."""
    print("\n" + "-" * 40)
    print("Step 3: Normalizing Categorical Values")
    print("-" * 40)
    
    changes = 0
    
    # Normalize gender values
    gender_mapping = {
        'm': 'M', 'male': 'M', 'MALE': 'M', 'Male': 'M',
        'f': 'F', 'female': 'F', 'FEMALE': 'F', 'Female': 'F'
    }
    
    original_genders = df[Columns.PATIENT_GENDER].copy()
    df[Columns.PATIENT_GENDER] = df[Columns.PATIENT_GENDER].replace(gender_mapping)
    gender_changes = (original_genders != df[Columns.PATIENT_GENDER]).sum()
    changes += gender_changes
    print(f"  • Gender values normalized: {gender_changes}")
    
    # Normalize appointment status
    status_mapping = {
        'pending': 'Pending', 'PENDING': 'Pending',
        'completed': 'Completed', 'COMPLETED': 'Completed',
        'cancelled': 'Cancelled', 'CANCELLED': 'Cancelled', 'canceled': 'Cancelled'
    }
    
    df[Columns.APPOINTMENT_STATUS] = df[Columns.APPOINTMENT_STATUS].replace(status_mapping)
    
    # Normalize booking type
    booking_mapping = {
        'online': 'Online', 'ONLINE': 'Online',
        'walk-in': 'Walk-in', 'walkin': 'Walk-in', 'Walk-In': 'Walk-in', 'WALK-IN': 'Walk-in'
    }
    
    df[Columns.BOOKING_TYPE] = df[Columns.BOOKING_TYPE].replace(booking_mapping)
    
    # Normalize no_show
    noshow_mapping = {
        'yes': 'Yes', 'YES': 'Yes', 'y': 'Yes', 'Y': 'Yes', '1': 'Yes', 'true': 'Yes',
        'no': 'No', 'NO': 'No', 'n': 'No', 'N': 'No', '0': 'No', 'false': 'No'
    }
    
    df[Columns.NO_SHOW] = df[Columns.NO_SHOW].replace(noshow_mapping)
    
    print(f"✓ Total normalizations applied: {changes}")
    
    return df


def validate_numerical_ranges(df):
    """Validate and fix numerical values within acceptable ranges."""
    print("\n" + "-" * 40)
    print("Step 4: Validating Numerical Ranges")
    print("-" * 40)
    
    # Convert to numeric
    df[Columns.PATIENT_AGE] = pd.to_numeric(df[Columns.PATIENT_AGE], errors='coerce')
    df[Columns.APPOINTMENT_DURATION] = pd.to_numeric(df[Columns.APPOINTMENT_DURATION], errors='coerce')
    df[Columns.WAITING_TIME] = pd.to_numeric(df[Columns.WAITING_TIME], errors='coerce')
    
    # Validate age (1-120)
    invalid_ages = ((df[Columns.PATIENT_AGE] < ValidationRanges.AGE_MIN) | 
                    (df[Columns.PATIENT_AGE] > ValidationRanges.AGE_MAX)).sum()
    df[Columns.PATIENT_AGE] = df[Columns.PATIENT_AGE].clip(
        ValidationRanges.AGE_MIN, ValidationRanges.AGE_MAX
    )
    print(f"  • Age values corrected: {invalid_ages}")
    
    # Validate duration (5-180 minutes)
    invalid_durations = ((df[Columns.APPOINTMENT_DURATION] < ValidationRanges.DURATION_MIN) | 
                         (df[Columns.APPOINTMENT_DURATION] > ValidationRanges.DURATION_MAX)).sum()
    df[Columns.APPOINTMENT_DURATION] = df[Columns.APPOINTMENT_DURATION].clip(
        ValidationRanges.DURATION_MIN, ValidationRanges.DURATION_MAX
    )
    print(f"  • Duration values corrected: {invalid_durations}")
    
    # Validate waiting time (0-120 minutes)
    invalid_waiting = ((df[Columns.WAITING_TIME] < ValidationRanges.WAITING_TIME_MIN) | 
                       (df[Columns.WAITING_TIME] > ValidationRanges.WAITING_TIME_MAX)).sum()
    df[Columns.WAITING_TIME] = df[Columns.WAITING_TIME].clip(
        ValidationRanges.WAITING_TIME_MIN, ValidationRanges.WAITING_TIME_MAX
    )
    print(f"  • Waiting time values corrected: {invalid_waiting}")
    
    # Convert back to int
    df[Columns.PATIENT_AGE] = df[Columns.PATIENT_AGE].astype(int)
    df[Columns.APPOINTMENT_DURATION] = df[Columns.APPOINTMENT_DURATION].astype(int)
    df[Columns.WAITING_TIME] = df[Columns.WAITING_TIME].astype(int)
    
    print("✓ All numerical ranges validated")
    
    return df


def convert_data_types(df):
    """Ensure proper data types for all columns."""
    print("\n" + "-" * 40)
    print("Step 5: Converting Data Types")
    print("-" * 40)
    
    # Convert date column to datetime
    df[Columns.APPOINTMENT_DATE] = pd.to_datetime(df[Columns.APPOINTMENT_DATE], errors='coerce')
    
    # Convert back to string in standard format
    df[Columns.APPOINTMENT_DATE] = df[Columns.APPOINTMENT_DATE].dt.strftime('%Y-%m-%d')
    
    print("✓ Date column converted to standard format (YYYY-MM-DD)")
    
    return df


# =============================================================================
# SAVE CLEANED DATA
# =============================================================================

def save_cleaned_data(df):
    """Save the cleaned data to CSV."""
    print("\n" + "-" * 40)
    print("Saving Cleaned Data")
    print("-" * 40)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(Paths.CLEANED_CSV), exist_ok=True)
    
    # Save to CSV
    df.to_csv(Paths.CLEANED_CSV, index=False)
    
    print(f"✓ Cleaned data saved to: {Paths.CLEANED_CSV}")
    print(f"✓ Total records: {len(df)}")


# =============================================================================
# DATA SUMMARY
# =============================================================================

def show_cleaning_summary(df_original, df_cleaned):
    """Display a summary of the cleaning process."""
    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)
    
    print(f"\nRecords: {len(df_original)} → {len(df_cleaned)} " +
          f"({len(df_original) - len(df_cleaned)} removed)")
    
    print("\nCleaned Data Statistics:")
    print(f"  • Gender Distribution: {df_cleaned[Columns.PATIENT_GENDER].value_counts().to_dict()}")
    print(f"  • Status Distribution: {df_cleaned[Columns.APPOINTMENT_STATUS].value_counts().to_dict()}")
    print(f"  • Booking Types: {df_cleaned[Columns.BOOKING_TYPE].value_counts().to_dict()}")
    print(f"  • No-Show Rate: {(df_cleaned[Columns.NO_SHOW] == 'Yes').mean()*100:.1f}%")
    print(f"  • Average Age: {df_cleaned[Columns.PATIENT_AGE].mean():.1f} years")
    print(f"  • Average Duration: {df_cleaned[Columns.APPOINTMENT_DURATION].mean():.1f} minutes")
    
    print("\n" + "=" * 60)
    print("Data cleaning completed successfully!")
    print("=" * 60)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    
    # Load raw data
    df = load_raw_data()
    if df is None:
        return
    
    # Store original for comparison
    df_original = df.copy()
    
    # Apply cleaning steps
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = normalize_categorical_values(df)
    df = validate_numerical_ranges(df)
    df = convert_data_types(df)
    
    # Save cleaned data
    save_cleaned_data(df)
    
    # Show summary
    show_cleaning_summary(df_original, df)
    
    return df


if __name__ == "__main__":
    cleaned_df = main()
