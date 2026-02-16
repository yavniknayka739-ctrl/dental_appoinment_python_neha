# Dental Appointment Analysis - Project Flow

## Overview

This project analyzes dental appointment data using **Exploratory Data Analysis (EDA)** and **Machine Learning** to predict patient no-shows. The entire process runs automatically in 5 sequential steps.

---

## Project Flow Diagram

```
Raw Data (CSV)
    ↓
[STEP 1] Data Cleaning
    ↓
Cleaned Data (CSV)
    ↓
[STEP 2] EDA Charts Generation (5 Charts)
    ↓
[STEP 3] Analysis Insights (4 Sections)
    ↓
[STEP 4] Machine Learning Model Training
    ↓
[STEP 5] Sample Prediction Demo
    ↓
Complete Analysis with Interactive Charts
```

---

## Step-by-Step Flow

### STEP 1: Data Cleaning

**What Happens:**
- Loads raw appointment data from CSV file
- Cleans and prepares data for analysis

**Technical Process:**
1. **Handle Missing Values**
   - Fills missing ages with median age
   - Fills missing genders with most common gender
   - Fills missing durations with most common duration

2. **Remove Duplicates**
   - Identifies duplicate appointment records
   - Keeps only the first occurrence

3. **Normalize Values**
   - Standardizes gender values (M/F)
   - Standardizes status values (Completed/Pending/Cancelled)
   - Standardizes booking types (Online/Walk-in)

4. **Validate Ranges**
   - Ensures ages are between 1-120 years
   - Ensures durations are between 5-180 minutes
   - Ensures waiting times are between 0-120 minutes

5. **Convert Data Types**
   - Converts dates to standard format (YYYY-MM-DD)
   - Converts numbers to proper integer types

**Output:**
- Cleaned CSV file saved to `data/cleaned_dental_appointments.csv`
- Summary statistics printed to console

---

### STEP 2: EDA Charts Generation

**What Happens:**
- Creates 5 visualizations to understand the data
- Each chart opens in an interactive window
- All charts are also saved as PNG files

**Charts Created:**

1. **Appointments per Dentist (Bar Chart)**
   - Shows workload distribution across dentists
   - Helps identify busy vs. less busy dentists
   - **Interactive**: Hover to see exact appointment counts

2. **Appointment Status Distribution (Pie Chart)**
   - Shows percentage of Completed/Pending/Cancelled appointments
   - Helps track operational efficiency
   - **Interactive**: Hover to see percentages and counts

3. **Daily Appointment Trend (Line Chart)**
   - Shows appointment volume over time
   - Includes 7-day moving average trend line
   - **Interactive**: Zoom to focus on specific date ranges

4. **Patient Age Distribution (Histogram)**
   - Shows age distribution of patients
   - Displays mean and median age lines
   - **Interactive**: Hover to see patient counts per age group

5. **Busy Time Slots (Heatmap)**
   - Shows appointment density by day and time slot
   - Helps optimize scheduling
   - **Interactive**: Hover to see exact appointment counts

**Technical Details:**
- Uses `matplotlib` for visualization
- Charts open in non-blocking mode (`plt.show(block=False)`)
- Script continues running while charts stay open
- All charts saved to `graphs/` folder

**Output:**
- 5 interactive matplotlib windows
- 5 PNG files in `graphs/` folder

---

### STEP 3: Analysis Insights

**What Happens:**
- Analyzes the cleaned data
- Prints 4 key business insights to console

**Analysis Sections:**

1. **Dentist Workload Analysis**
   - Lists appointments per dentist with visual bars
   - Identifies busiest and least busy dentists
   - Calculates average workload
   - **Business Value**: Optimize staff allocation

2. **Appointment Status Analysis**
   - Shows distribution of appointment statuses
   - Calculates completion and cancellation rates
   - **Business Value**: Track operational efficiency

3. **Peak Time Analysis**
   - Shows appointments by day of week
   - Lists top 5 busiest time slots
   - Identifies peak day and time
   - **Business Value**: Optimize scheduling and staffing

4. **No-Show Behavior Analysis**
   - Calculates overall no-show rate
   - Breaks down no-show rate by booking type
   - Shows no-show rate by day of week
   - **Business Value**: Reduce revenue loss from no-shows

**Technical Details:**
- Uses `pandas` for data aggregation
- Calculates percentages, averages, and distributions
- Prints formatted tables with visual bars

**Output:**
- Formatted analysis printed to console
- Key metrics and insights displayed

---

### STEP 4: Machine Learning Model Training

**What Happens:**
- Trains a Decision Tree model to predict no-shows
- Evaluates model performance
- Generates 2 visualization charts

**Technical Process:**

1. **Data Preparation**
   - Loads cleaned data
   - Encodes categorical variables (gender, day, time slot, etc.)
   - Splits data into features (X) and target (y)
   - Creates training set (80%) and test set (20%)

2. **Model Training**
   - Trains Decision Tree Classifier
   - Uses parameters: `max_depth=5`, `min_samples_split=10`
   - Learns patterns that predict no-shows

3. **Model Evaluation**
   - Tests model on unseen data
   - Calculates performance metrics:
     - **Accuracy**: Overall correctness
     - **Precision**: How many predicted no-shows were correct
     - **Recall**: How many actual no-shows were caught
     - **F1-Score**: Balance between precision and recall

4. **Feature Importance Analysis**
   - Identifies which factors most influence no-shows
   - Ranks features by importance

**Charts Created:**

1. **Confusion Matrix**
   - Shows correct vs. incorrect predictions
   - 2x2 grid: Show/No-Show (Actual vs. Predicted)
   - **Interactive**: Hover to see prediction counts

2. **Feature Importance**
   - Bar chart showing which factors drive no-shows
   - Sorted by importance (most to least)
   - **Interactive**: Hover to see exact importance values

**Technical Details:**
- Uses `scikit-learn` library
- Decision Tree algorithm (supervised learning)
- Classification task (binary: Yes/No)

**Output:**
- Trained model
- Performance metrics printed to console
- 2 interactive matplotlib windows
- 2 PNG files in `graphs/` folder

---

### STEP 5: Sample Prediction Demo

**What Happens:**
- Demonstrates how to use the trained model
- Makes a prediction for a sample patient
- Shows business recommendations

**Sample Patient Profile:**
- Age: 45 years
- Gender: Female
- Specialization: Orthodontics
- Day: Monday
- Time Slot: 10:00-11:00
- Booking Type: Online
- Duration: 30 minutes

**Prediction Process:**
1. Encodes patient data (converts text to numbers)
2. Feeds data into trained model
3. Model predicts: Will patient show up or not?
4. Calculates confidence level (probability)

**Output:**
- Prediction result (YES/NO for no-show)
- Confidence percentage
- Business recommendations based on prediction

**Example Output:**
```
Will Patient No-Show? NO
Confidence: 87.3%

Recommendation:
  - Standard appointment confirmation
  - Patient likely to attend as scheduled
```

---

## Data Flow Summary

```
Raw CSV File (1000+ records)
    ↓
Data Cleaning (handle missing, duplicates, validation)
    ↓
Cleaned CSV File (clean, validated records)
    ↓
EDA Analysis (5 charts + 4 insights)
    ↓
Feature Engineering (encode categories, split data)
    ↓
ML Model Training (Decision Tree)
    ↓
Model Evaluation (metrics + visualizations)
    ↓
Prediction Demo (sample patient)
    ↓
Complete Analysis Ready for Use
```

---

## Technical Stack

**Programming Language:** Python 3.x

**Core Libraries:**
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical operations
- `matplotlib` - Data visualization
- `scikit-learn` - Machine learning

**Key Files:**
- `scripts/main.py` - Main orchestration script
- `scripts/data_cleaning.py` - Data cleaning logic
- `scripts/eda_analysis.py` - Chart generation
- `scripts/ml_model.py` - Machine learning model
- `scripts/config.py` - Configuration settings

---

## How to Run

```powershell
# Navigate to project folder
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha

# Activate virtual environment
.\venv\Scripts\activate

# Run the project
python scripts/main.py
```

**What You'll See:**
1. Console output showing progress through each step
2. 5 EDA chart windows opening (interactive)
3. Analysis insights printed to console
4. 2 ML chart windows opening (interactive)
5. Sample prediction results
6. Completion message

**Total Time:** ~30-60 seconds (depending on data size)

---

## Output Files

**Generated Files:**
- `data/cleaned_dental_appointments.csv` - Cleaned data
- `graphs/appointments_per_dentist.png` - Bar chart
- `graphs/appointment_status_distribution.png` - Pie chart
- `graphs/daily_appointment_trend.png` - Line chart
- `graphs/patient_age_distribution.png` - Histogram
- `graphs/busy_time_slots.png` - Heatmap
- `graphs/decision_tree_confusion_matrix.png` - ML evaluation
- `graphs/decision_tree_feature_importance.png` - ML insights

**Interactive Windows:**
- 7 total matplotlib windows (5 EDA + 2 ML)
- All support zoom, pan, hover, and save
- Remain open after script completes

---

## Key Features

1. **Fully Automated** - No user input required
2. **Interactive Visualizations** - All charts open in GUI windows
3. **Non-Blocking Execution** - Script runs continuously
4. **Professional Output** - Clean, formatted console output
5. **Business Insights** - 4 focused analysis sections
6. **Predictive Model** - Decision Tree for no-show prediction
7. **Complete Documentation** - All outputs saved to files

---

## Business Value

**For Dental Clinics:**
- Understand appointment patterns
- Identify peak times for better staffing
- Predict no-shows to reduce revenue loss
- Optimize dentist workload distribution
- Improve scheduling efficiency

**For Academic Projects:**
- Demonstrates full data science pipeline
- Shows EDA best practices
- Implements supervised machine learning
- Includes proper data cleaning
- Professional visualization and reporting
