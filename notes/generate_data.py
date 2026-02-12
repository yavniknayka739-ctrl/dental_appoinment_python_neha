# =============================================================================
# DENTAL APPOINTMENT DATA GENERATOR
# =============================================================================
# PRIVATE SCRIPT - DO NOT INCLUDE IN SUBMISSION
# This script generates realistic synthetic dental appointment data
# Run once to create the raw CSV, then keep this file hidden
# =============================================================================

import csv
import random
from datetime import datetime, timedelta
import os
import sys

# Add scripts folder to path for config import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from config import Paths, Columns, ValidValues, DentistData

# =============================================================================
# CONFIGURATION
# =============================================================================

NUM_RECORDS = 200  # Number of appointment records to generate
DATE_RANGE_DAYS = 180  # Generate dates for last 6 months

# Probability settings for realistic data
NO_SHOW_RATE = 0.15  # 15% no-show rate
CANCELLED_RATE = 0.10  # 10% cancellation rate
ONLINE_BOOKING_RATE = 0.65  # 65% online bookings

# Intentional "dirty" data rates (for cleaning script to fix)
MISSING_VALUE_RATE = 0.03  # 3% missing values
DUPLICATE_RATE = 0.02  # 2% duplicate records
INCONSISTENT_GENDER_RATE = 0.05  # 5% inconsistent gender formats


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_patient_id(index):
    """Generate a patient ID."""
    return f"PAT{str(index).zfill(4)}"


def generate_appointment_id(index):
    """Generate an appointment ID."""
    return f"APT{str(index).zfill(4)}"


def generate_age():
    """Generate realistic patient age (skewed toward adults)."""
    # Weighted distribution: fewer children, more adults
    age_groups = [
        (5, 17, 0.15),    # Children: 15%
        (18, 35, 0.30),   # Young adults: 30%
        (36, 55, 0.35),   # Middle-aged: 35%
        (56, 85, 0.20),   # Seniors: 20%
    ]
    
    rand = random.random()
    cumulative = 0
    for min_age, max_age, probability in age_groups:
        cumulative += probability
        if rand <= cumulative:
            return random.randint(min_age, max_age)
    return random.randint(25, 45)


def generate_gender(dirty=False):
    """Generate gender with optional inconsistent formatting."""
    gender = random.choice(["M", "F"])
    
    if dirty and random.random() < INCONSISTENT_GENDER_RATE:
        # Introduce variations for cleaning script to handle
        variations = {
            "M": ["M", "m", "Male", "male", "MALE"],
            "F": ["F", "f", "Female", "female", "FEMALE"]
        }
        return random.choice(variations[gender])
    
    return gender


def generate_date():
    """Generate a random date within the last 6 months."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DATE_RANGE_DAYS)
    
    random_days = random.randint(0, DATE_RANGE_DAYS)
    random_date = start_date + timedelta(days=random_days)
    
    return random_date


def generate_time_slot():
    """Generate time slot with realistic distribution (busier mid-morning)."""
    # Weight mid-morning and late afternoon slots higher
    weights = [3, 4, 5, 5, 4, 3, 2, 3, 4, 5, 5, 4, 3, 2]
    
    return random.choices(ValidValues.TIME_SLOTS, weights=weights, k=1)[0]


def generate_appointment_status(no_show):
    """Generate appointment status based on no-show."""
    if no_show == "Yes":
        return "Cancelled"  # No-shows are recorded as cancelled
    
    rand = random.random()
    if rand < CANCELLED_RATE:
        return "Cancelled"
    elif rand < 0.3:  # 20% pending (recent appointments)
        return "Pending"
    else:
        return "Completed"


def generate_waiting_time(status):
    """Generate waiting time based on appointment status."""
    if status in ["Cancelled", "Pending"]:
        return 0
    
    # Realistic waiting time distribution
    if random.random() < 0.6:
        return random.randint(0, 10)  # 60% wait 0-10 mins
    elif random.random() < 0.85:
        return random.randint(11, 25)  # 25% wait 11-25 mins
    else:
        return random.randint(26, 45)  # 15% wait 26-45 mins


def maybe_null(value):
    """Randomly return None to simulate missing data."""
    if random.random() < MISSING_VALUE_RATE:
        return ""
    return value


# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_dental_data():
    """Generate the complete dental appointments dataset."""
    
    print("=" * 60)
    print("Dental Appointment Data Generator")
    print("=" * 60)
    print(f"\nGenerating {NUM_RECORDS} appointment records...")
    
    data = []
    patient_pool = list(range(1, NUM_RECORDS // 2))  # Reuse some patients
    
    for i in range(1, NUM_RECORDS + 1):
        # Generate base data
        appointment_id = generate_appointment_id(i)
        patient_id = generate_patient_id(random.choice(patient_pool))
        age = generate_age()
        gender = generate_gender(dirty=True)
        
        # Select dentist
        dentist = random.choice(DentistData.DENTISTS)
        dentist_id = dentist["id"]
        dentist_name = dentist["name"]
        specialization = dentist["specialization"]
        
        # Generate appointment details
        appointment_date = generate_date()
        appointment_day = appointment_date.strftime("%A")
        date_str = appointment_date.strftime("%Y-%m-%d")
        
        time_slot = generate_time_slot()
        duration = random.choice(ValidValues.DURATIONS)
        
        # Booking and status
        booking_type = "Online" if random.random() < ONLINE_BOOKING_RATE else "Walk-in"
        no_show = "Yes" if random.random() < NO_SHOW_RATE else "No"
        status = generate_appointment_status(no_show)
        waiting_time = generate_waiting_time(status)
        
        # Create record with some intentional missing values
        record = {
            Columns.APPOINTMENT_ID: appointment_id,
            Columns.PATIENT_ID: patient_id,
            Columns.PATIENT_AGE: maybe_null(age),
            Columns.PATIENT_GENDER: maybe_null(gender),
            Columns.DENTIST_ID: dentist_id,
            Columns.DENTIST_NAME: dentist_name,
            Columns.SPECIALIZATION: specialization,
            Columns.APPOINTMENT_DATE: date_str,
            Columns.APPOINTMENT_DAY: appointment_day,
            Columns.TIME_SLOT: time_slot,
            Columns.APPOINTMENT_DURATION: maybe_null(duration),
            Columns.APPOINTMENT_STATUS: status,
            Columns.BOOKING_TYPE: maybe_null(booking_type),
            Columns.WAITING_TIME: waiting_time,
            Columns.NO_SHOW: no_show
        }
        
        data.append(record)
        
        # Add occasional duplicates (for cleaning script to remove)
        if random.random() < DUPLICATE_RATE and i > 10:
            duplicate = record.copy()
            duplicate[Columns.APPOINTMENT_ID] = generate_appointment_id(i + 1000)
            data.append(duplicate)
    
    # Shuffle to mix duplicates naturally
    random.shuffle(data)
    
    return data


def save_to_csv(data):
    """Save the generated data to CSV."""
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(Paths.RAW_CSV), exist_ok=True)
    
    with open(Paths.RAW_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Columns.ALL_COLUMNS)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n✓ Data saved to: {Paths.RAW_CSV}")
    print(f"✓ Total records: {len(data)}")


def show_data_summary(data):
    """Display a summary of the generated data."""
    
    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)
    
    # Count statistics
    total = len(data)
    completed = sum(1 for r in data if r[Columns.APPOINTMENT_STATUS] == "Completed")
    cancelled = sum(1 for r in data if r[Columns.APPOINTMENT_STATUS] == "Cancelled")
    pending = sum(1 for r in data if r[Columns.APPOINTMENT_STATUS] == "Pending")
    no_shows = sum(1 for r in data if r[Columns.NO_SHOW] == "Yes")
    online = sum(1 for r in data if r[Columns.BOOKING_TYPE] == "Online")
    
    # Missing values count
    missing_age = sum(1 for r in data if r[Columns.PATIENT_AGE] == "")
    missing_gender = sum(1 for r in data if r[Columns.PATIENT_GENDER] == "")
    
    print(f"\nTotal Records: {total}")
    print(f"\nAppointment Status:")
    print(f"  - Completed: {completed} ({completed/total*100:.1f}%)")
    print(f"  - Cancelled: {cancelled} ({cancelled/total*100:.1f}%)")
    print(f"  - Pending: {pending} ({pending/total*100:.1f}%)")
    print(f"\nNo-Shows: {no_shows} ({no_shows/total*100:.1f}%)")
    print(f"Online Bookings: {online} ({online/total*100:.1f}%)")
    print(f"\nIntentional Missing Values (for cleaning):")
    print(f"  - Missing Age: {missing_age}")
    print(f"  - Missing Gender: {missing_gender}")
    
    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Set random seed for reproducibility (optional - remove for truly random data)
    # random.seed(42)
    
    # Generate data
    data = generate_dental_data()
    
    # Save to CSV
    save_to_csv(data)
    
    # Show summary
    show_data_summary(data)
