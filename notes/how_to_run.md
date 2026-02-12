# Dental Appointment Project - Complete Setup Guide

This guide will help you install and run the project from scratch, even if you have no programming experience.

---

## Step 1: Install Python 3.10.0

1. Open your web browser and go to: https://www.python.org/downloads/release/python-3100/
2. Scroll down to **"Files"** section
3. Click on **"Windows installer (64-bit)"** to download
4. Open the downloaded file to start installation
5. **IMPORTANT:** Check the box that says **"Add Python to PATH"** at the bottom of the installer
6. Click **"Install Now"**
7. Wait for installation to complete, then click **"Close"**

---

## Step 2: Install VS Code

1. Go to: https://code.visualstudio.com/download
2. Click the **Windows** download button
3. Open the downloaded file and follow the installation steps
4. Open VS Code after installation

---

## Step 3: Open Project in VS Code

1. In VS Code, click **File** → **Open Folder**
2. Navigate to and select the `dental_appoinment_python_neha` folder
3. Click **Select Folder**

---

## Step 4: Open VS Code Terminal

1. In VS Code, click **Terminal** → **New Terminal** (or press `` Ctrl + ` ``)
2. A terminal panel will open at the bottom of VS Code

### Verify Python Installation

In the terminal, type:
```
python --version
```
You should see `Python 3.10.0`

---

## Step 5: Create Virtual Environment

In the VS Code terminal, type:

```
py -3.10 -m venv venv
```

This creates a separate space for the project's files.

---

## Step 6: Activate Virtual Environment

In the VS Code terminal, type:

```
venv\Scripts\activate
```

You should now see `(venv)` at the beginning of the line. This means the virtual environment is active.

---

## Step 7: Install Required Packages

In the VS Code terminal, type:

```
pip install -r requirements.txt
```

Wait for the installation to complete.

---

## Step 8: Run the Project

In the VS Code terminal, type:

```
python scripts/main.py
```

after opening the pthon idle 3.10 
open the main file 
then press the "F5"
---


done





## Step 9: Using the Application

After running the project, you'll see a menu with these options:

| Option | What It Does |
|--------|--------------|
| **1. View Charts** | Shows visual graphs like appointments per dentist, status distribution, age distribution |
| **2. Make Predictions** | Predicts waiting time or whether a patient will show up |
| **3. View Analysis** | Shows insights about dentist workload, peak times, patient demographics |
| **4. Run Full Pipeline** | Runs all data cleaning, analysis, and generates all charts at once |
| **5. Exit** | Closes the application |

### How to Navigate

- Type the **number** of your choice and press **Enter**
- Follow the on-screen instructions
- Press **Enter** to go back to the previous menu

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `'python' is not recognized` | Reinstall Python and make sure to check "Add Python to PATH" |
| `No module named 'pandas'` | Run `pip install -r requirements.txt` again |
| `(venv)` not showing | Run `venv\Scripts\activate` again |

---

## Quick Reference (After First Setup)

Once everything is installed, you only need these steps to run the project again:

1. Open the project folder in VS Code
2. Open terminal: **Terminal** → **New Terminal**
3. Activate virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Run the project:
   ```
   python scripts/main.py
   ```
