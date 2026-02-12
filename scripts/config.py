# Dental Appointment EDA Project - Configuration File
# Single Source of Truth for all paths, columns, and settings
# All scripts must import from this file - no hardcoding allowed

import os

# Get the project root directory (parent of scripts folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

class Paths:
    """Centralized path management for the project."""
    
    # Data paths
    RAW_CSV = os.path.join(PROJECT_ROOT, "data", "dental_appointments_raw.csv")
    CLEANED_CSV = os.path.join(PROJECT_ROOT, "data", "dental_appointments_cleaned.csv")
    
    # Output paths
    GRAPHS_DIR = os.path.join(PROJECT_ROOT, "graphs")
    REPORT_DIR = os.path.join(PROJECT_ROOT, "report")
    
    # Graph files
    GRAPH_APPOINTMENTS_PER_DENTIST = os.path.join(GRAPHS_DIR, "appointments_per_dentist.png")
    GRAPH_STATUS_DISTRIBUTION = os.path.join(GRAPHS_DIR, "appointment_status_distribution.png")
    GRAPH_DAILY_TREND = os.path.join(GRAPHS_DIR, "daily_appointment_trend.png")
    GRAPH_AGE_DISTRIBUTION = os.path.join(GRAPHS_DIR, "patient_age_distribution.png")
    GRAPH_BUSY_TIME_SLOTS = os.path.join(GRAPHS_DIR, "busy_time_slots.png")


# =============================================================================
# COLUMN CONFIGURATION
# =============================================================================

class Columns:
    """Column names and metadata for the dental appointments dataset."""
    
    # Column names
    APPOINTMENT_ID = "appointment_id"
    PATIENT_ID = "patient_id"
    PATIENT_AGE = "patient_age"
    PATIENT_GENDER = "patient_gender"
    DENTIST_ID = "dentist_id"
    DENTIST_NAME = "dentist_name"
    SPECIALIZATION = "specialization"
    APPOINTMENT_DATE = "appointment_date"
    APPOINTMENT_DAY = "appointment_day"
    TIME_SLOT = "time_slot"
    APPOINTMENT_DURATION = "appointment_duration"
    APPOINTMENT_STATUS = "appointment_status"
    BOOKING_TYPE = "booking_type"
    WAITING_TIME = "waiting_time_minutes"
    NO_SHOW = "no_show"
    
    # All columns in order
    ALL_COLUMNS = [
        APPOINTMENT_ID, PATIENT_ID, PATIENT_AGE, PATIENT_GENDER,
        DENTIST_ID, DENTIST_NAME, SPECIALIZATION,
        APPOINTMENT_DATE, APPOINTMENT_DAY, TIME_SLOT, APPOINTMENT_DURATION,
        APPOINTMENT_STATUS, BOOKING_TYPE, WAITING_TIME, NO_SHOW
    ]
    
    # Column data types
    DTYPES = {
        APPOINTMENT_ID: str,
        PATIENT_ID: str,
        PATIENT_AGE: int,
        PATIENT_GENDER: str,
        DENTIST_ID: str,
        DENTIST_NAME: str,
        SPECIALIZATION: str,
        APPOINTMENT_DATE: str,  # Will be converted to datetime
        APPOINTMENT_DAY: str,
        TIME_SLOT: str,
        APPOINTMENT_DURATION: int,
        APPOINTMENT_STATUS: str,
        BOOKING_TYPE: str,
        WAITING_TIME: int,
        NO_SHOW: str
    }


# =============================================================================
# VALID VALUES FOR CATEGORICAL COLUMNS
# =============================================================================

class ValidValues:
    """Valid values for categorical columns."""
    
    GENDER = ["M", "F"]
    APPOINTMENT_STATUS = ["Pending", "Completed", "Cancelled"]
    BOOKING_TYPE = ["Online", "Walk-in"]
    NO_SHOW = ["Yes", "No"]
    SPECIALIZATIONS = [
        "General Dentistry",
        "Orthodontics",
        "Periodontics",
        "Endodontics",
        "Oral Surgery"
    ]
    DAYS_OF_WEEK = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]
    TIME_SLOTS = [
        "09:00-09:30", "09:30-10:00", "10:00-10:30", "10:30-11:00",
        "11:00-11:30", "11:30-12:00", "12:00-12:30",
        "14:00-14:30", "14:30-15:00", "15:00-15:30", "15:30-16:00",
        "16:00-16:30", "16:30-17:00", "17:00-17:30"
    ]
    DURATIONS = [15, 30, 45, 60]


# =============================================================================
# VALIDATION RANGES
# =============================================================================

class ValidationRanges:
    """Valid ranges for numerical columns."""
    
    AGE_MIN = 1
    AGE_MAX = 120
    DURATION_MIN = 5
    DURATION_MAX = 180
    WAITING_TIME_MIN = 0
    WAITING_TIME_MAX = 120


# =============================================================================
# DENTIST DATA
# =============================================================================

class DentistData:
    """Sample dentist data for the dataset."""
    
    DENTISTS = [
        {"id": "DEN001", "name": "Dr. Amit Sharma", "specialization": "General Dentistry"},
        {"id": "DEN002", "name": "Dr. Priya Patel", "specialization": "Orthodontics"},
        {"id": "DEN003", "name": "Dr. Rajesh Kumar", "specialization": "Periodontics"},
        {"id": "DEN004", "name": "Dr. Sneha Gupta", "specialization": "Endodontics"},
        {"id": "DEN005", "name": "Dr. Vikram Singh", "specialization": "Oral Surgery"},
    ]


# Test the configuration when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("Dental Appointment EDA - Configuration Test")
    print("=" * 60)
    print(f"\nProject Root: {PROJECT_ROOT}")
    print(f"\nRaw CSV Path: {Paths.RAW_CSV}")
    print(f"Cleaned CSV Path: {Paths.CLEANED_CSV}")
    print(f"Graphs Directory: {Paths.GRAPHS_DIR}")
    print(f"\nTotal Columns: {len(Columns.ALL_COLUMNS)}")
    print(f"Columns: {Columns.ALL_COLUMNS}")
    print(f"\nTotal Dentists: {len(DentistData.DENTISTS)}")
    print("\nConfiguration loaded successfully!")
