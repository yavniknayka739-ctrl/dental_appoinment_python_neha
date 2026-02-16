# =============================================================================
# DENTAL APPOINTMENT EDA ANALYSIS SCRIPT
# =============================================================================
# This script performs Exploratory Data Analysis on cleaned dental appointment data
# Generates 5 PNG visualizations for academic evaluation
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

# Set matplotlib style for professional-looking graphs
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Color palette for consistent styling
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#C73E1D',
    'neutral': '#3B1F2B',
    'palette': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#6B4C4C']
}


# =============================================================================
# DATA LOADING
# =============================================================================

def load_cleaned_data():
    """Load the cleaned CSV data."""
    print("=" * 60)
    print("DENTAL APPOINTMENT EDA ANALYSIS")
    print("=" * 60)
    
    if not os.path.exists(Paths.CLEANED_CSV):
        print(f"\nError: Error: Cleaned CSV not found at {Paths.CLEANED_CSV}")
        print("Please run data_cleaning.py first.")
        return None
    
    print(f"\n Loading data from: {Paths.CLEANED_CSV}")
    
    df = pd.read_csv(Paths.CLEANED_CSV)
    
    # Convert date column
    df[Columns.APPOINTMENT_DATE] = pd.to_datetime(df[Columns.APPOINTMENT_DATE])
    
    print(f" Loaded {len(df)} records")
    
    return df


# =============================================================================
# VISUALIZATION 1: Appointments per Dentist (Bar Chart)
# =============================================================================

def plot_appointments_per_dentist(df):
    """Create a bar chart showing appointments per dentist."""
    print("\n Creating: Appointments per Dentist (Bar Chart)")
    
    # Count appointments per dentist
    dentist_counts = df.groupby([Columns.DENTIST_ID, Columns.DENTIST_NAME]).size().reset_index(name='count')
    dentist_counts = dentist_counts.sort_values('count', ascending=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create horizontal bar chart
    bars = ax.barh(dentist_counts[Columns.DENTIST_NAME], dentist_counts['count'], 
                   color=COLORS['palette'][:len(dentist_counts)], edgecolor='white', linewidth=1)
    
    # Add value labels on bars
    for bar, count in zip(bars, dentist_counts['count']):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontweight='bold')
    
    # Styling
    ax.set_xlabel('Number of Appointments')
    ax.set_ylabel('Dentist')
    ax.set_title('Appointments per Dentist', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Save
    os.makedirs(Paths.GRAPHS_DIR, exist_ok=True)
    plt.savefig(Paths.GRAPH_APPOINTMENTS_PER_DENTIST, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {Paths.GRAPH_APPOINTMENTS_PER_DENTIST}")
    
    return dentist_counts


# =============================================================================
# VISUALIZATION 2: Appointment Status Distribution (Pie Chart)
# =============================================================================

def plot_status_distribution(df):
    """Create a pie chart showing appointment status distribution."""
    print("\n Creating: Appointment Status Distribution (Pie Chart)")
    
    # Count status distribution
    status_counts = df[Columns.APPOINTMENT_STATUS].value_counts()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Colors for each status
    status_colors = {
        'Completed': '#28a745',
        'Pending': '#ffc107',
        'Cancelled': '#dc3545'
    }
    colors = [status_colors.get(status, '#6c757d') for status in status_counts.index]
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.02] * len(status_counts),
        shadow=True,
        startangle=90
    )
    
    # Style the text
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    ax.set_title('Appointment Status Distribution', fontsize=16, fontweight='bold', pad=20)
    
    # Add legend with counts
    legend_labels = [f'{status}: {count}' for status, count in status_counts.items()]
    ax.legend(wedges, legend_labels, title="Status", loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    
    # Save
    plt.savefig(Paths.GRAPH_STATUS_DISTRIBUTION, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {Paths.GRAPH_STATUS_DISTRIBUTION}")
    
    return status_counts


# =============================================================================
# VISUALIZATION 3: Daily Appointment Trend (Line Chart)
# =============================================================================

def plot_daily_trend(df):
    """Create a line chart showing daily appointment trends."""
    print("\n Creating: Daily Appointment Trend (Line Chart)")
    
    # Group by date
    daily_counts = df.groupby(Columns.APPOINTMENT_DATE).size().reset_index(name='count')
    daily_counts = daily_counts.sort_values(Columns.APPOINTMENT_DATE)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot line chart
    ax.plot(daily_counts[Columns.APPOINTMENT_DATE], daily_counts['count'], 
            color=COLORS['primary'], linewidth=2, marker='o', markersize=4, alpha=0.7)
    
    # Add trend line (moving average)
    window = min(7, len(daily_counts))
    if window > 1:
        daily_counts['trend'] = daily_counts['count'].rolling(window=window, center=True).mean()
        ax.plot(daily_counts[Columns.APPOINTMENT_DATE], daily_counts['trend'],
                color=COLORS['secondary'], linewidth=2.5, linestyle='--', label='7-day Moving Average')
    
    # Fill area under the curve
    ax.fill_between(daily_counts[Columns.APPOINTMENT_DATE], daily_counts['count'], 
                    alpha=0.3, color=COLORS['primary'])
    
    # Styling
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Appointments')
    ax.set_title('Daily Appointment Trend', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    ax.legend()
    plt.tight_layout()
    
    # Save
    plt.savefig(Paths.GRAPH_DAILY_TREND, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {Paths.GRAPH_DAILY_TREND}")
    
    return daily_counts


# =============================================================================
# VISUALIZATION 4: Patient Age Distribution (Histogram)
# =============================================================================

def plot_age_distribution(df):
    """Create a histogram showing patient age distribution."""
    print("\n Creating: Patient Age Distribution (Histogram)")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(df[Columns.PATIENT_AGE], bins=15, 
                                color=COLORS['primary'], edgecolor='white', 
                                linewidth=1.5, alpha=0.8)
    
    # Color gradient for bins
    for i, (patch, bin_val) in enumerate(zip(patches, bins)):
        color_intensity = i / len(patches)
        patch.set_facecolor(plt.cm.Blues(0.3 + 0.6 * color_intensity))
    
    # Add statistics
    mean_age = df[Columns.PATIENT_AGE].mean()
    median_age = df[Columns.PATIENT_AGE].median()
    
    ax.axvline(mean_age, color=COLORS['secondary'], linestyle='--', linewidth=2, 
               label=f'Mean: {mean_age:.1f}')
    ax.axvline(median_age, color=COLORS['accent'], linestyle=':', linewidth=2,
               label=f'Median: {median_age:.1f}')
    
    # Styling
    ax.set_xlabel('Patient Age (years)')
    ax.set_ylabel('Number of Patients')
    ax.set_title('Patient Age Distribution', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()
    
    plt.tight_layout()
    
    # Save
    plt.savefig(Paths.GRAPH_AGE_DISTRIBUTION, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {Paths.GRAPH_AGE_DISTRIBUTION}")
    
    return df[Columns.PATIENT_AGE].describe()


# =============================================================================
# VISUALIZATION 5: Busy Time Slots (Heatmap)
# =============================================================================

def plot_busy_time_slots(df):
    """Create a heatmap showing busy time slots by day of week."""
    print("\n Creating: Busy Time Slots (Heatmap)")
    
    # Create pivot table: days vs time slots
    heatmap_data = pd.crosstab(df[Columns.APPOINTMENT_DAY], df[Columns.TIME_SLOT])
    
    # Reorder days of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_order = [d for d in day_order if d in heatmap_data.index]
    heatmap_data = heatmap_data.reindex(day_order)
    
    # Sort time slots
    time_slots = sorted(heatmap_data.columns.tolist())
    heatmap_data = heatmap_data[time_slots]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Create heatmap
    im = ax.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto')
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.set_ylabel('Number of Appointments', rotation=-90, va="bottom", fontsize=11)
    
    # Set ticks
    ax.set_xticks(np.arange(len(time_slots)))
    ax.set_yticks(np.arange(len(day_order)))
    ax.set_xticklabels(time_slots, rotation=45, ha='right')
    ax.set_yticklabels(day_order)
    
    # Add text annotations
    for i in range(len(day_order)):
        for j in range(len(time_slots)):
            value = heatmap_data.values[i, j]
            text_color = 'white' if value > heatmap_data.values.max() / 2 else 'black'
            ax.text(j, i, str(value), ha='center', va='center', 
                   color=text_color, fontsize=9, fontweight='bold')
    
    # Styling
    ax.set_xlabel('Time Slot')
    ax.set_ylabel('Day of Week')
    ax.set_title('Busy Time Slots by Day of Week', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # Save
    plt.savefig(Paths.GRAPH_BUSY_TIME_SLOTS, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show(block=False)  # Non-blocking interactive display
    plt.pause(0.1)  # Give GUI time to render
    
    print(f"   Saved: {Paths.GRAPH_BUSY_TIME_SLOTS}")
    
    return heatmap_data


# =============================================================================
# ANALYSIS INSIGHTS
# =============================================================================

def generate_insights(df, dentist_counts, status_counts, daily_counts, age_stats, heatmap_data):
    """Generate and print analysis insights."""
    print("\n" + "=" * 60)
    print("ANALYSIS INSIGHTS")
    print("=" * 60)
    
    # Dentist workload
    print("\n Dentist Workload Insights:")
    busiest_dentist = dentist_counts.iloc[-1]
    print(f"  - Busiest Dentist: {busiest_dentist[Columns.DENTIST_NAME]} ({busiest_dentist['count']} appointments)")
    
    # Appointment status
    print("\n Appointment Status Insights:")
    completed_rate = (status_counts.get('Completed', 0) / status_counts.sum()) * 100
    cancelled_rate = (status_counts.get('Cancelled', 0) / status_counts.sum()) * 100
    print(f"  - Completion Rate: {completed_rate:.1f}%")
    print(f"  - Cancellation Rate: {cancelled_rate:.1f}%")
    
    # Peak booking days
    print("\n Peak Booking Insights:")
    day_counts = df[Columns.APPOINTMENT_DAY].value_counts()
    peak_day = day_counts.idxmax()
    print(f"  - Busiest Day: {peak_day} ({day_counts.max()} appointments)")
    
    # Peak time slots
    time_counts = df[Columns.TIME_SLOT].value_counts()
    peak_time = time_counts.idxmax()
    print(f"  - Busiest Time Slot: {peak_time} ({time_counts.max()} appointments)")
    
    # No-show analysis
    print("\n No-Show Behavior Analysis:")
    no_show_rate = (df[Columns.NO_SHOW] == 'Yes').mean() * 100
    print(f"  - Overall No-Show Rate: {no_show_rate:.1f}%")
    
    # No-show by booking type
    no_show_by_booking = df.groupby(Columns.BOOKING_TYPE)[Columns.NO_SHOW].apply(
        lambda x: (x == 'Yes').mean() * 100
    )
    for booking_type, rate in no_show_by_booking.items():
        print(f"  - No-Show Rate ({booking_type}): {rate:.1f}%")
    
    # Patient demographics
    print("\n Patient Demographics:")
    print(f"  - Average Age: {df[Columns.PATIENT_AGE].mean():.1f} years")
    print(f"  - Age Range: {df[Columns.PATIENT_AGE].min()} - {df[Columns.PATIENT_AGE].max()} years")
    gender_dist = df[Columns.PATIENT_GENDER].value_counts(normalize=True) * 100
    for gender, pct in gender_dist.items():
        print(f"  - {gender}: {pct:.1f}%")
    
    print("\n" + "=" * 60)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    
    # Load data
    df = load_cleaned_data()
    if df is None:
        return
    
    # Generate all visualizations
    dentist_counts = plot_appointments_per_dentist(df)
    status_counts = plot_status_distribution(df)
    daily_counts = plot_daily_trend(df)
    age_stats = plot_age_distribution(df)
    heatmap_data = plot_busy_time_slots(df)
    
    # Generate insights
    generate_insights(df, dentist_counts, status_counts, daily_counts, age_stats, heatmap_data)
    
    print("\n All visualizations generated successfully!")
    print(f" Graphs saved to: {Paths.GRAPHS_DIR}")
    
    return df


if __name__ == "__main__":
    df = main()
