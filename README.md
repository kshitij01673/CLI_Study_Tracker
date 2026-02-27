# Study Tracker CLI

A simple command-line Study Tracker built with Python.  
It allows you to log study hours and view total hours per subject.

---

## Features

- Automatically creates `study_data.csv` if it does not exist  
- Log study time in `hrs:mins` format (example: `2:30`)  
- Converts time into decimal hours (rounded to 2 decimal places)  
- View total study hours per subject  
- Runs continuously in a menu loop  

---

## How It Works

### 1. Log Study Time

- Enter subject name  
- Enter time in `hrs:mins` format  
- Time is converted to decimal hours  
- Entry is saved with today's date  

Example stored format:

```
Date,Subject,Hours
27-02-2026,Math,2.5
```

---

### 2. View Total Study Hours

- Reads the CSV file  
- Calculates total hours per subject  
- Displays results in the terminal  

Example output:

```
Math: 5.5 hours
Physics: 3.0 hours
```

---

## How to Run

```bash
python main.py
```

---

## Concepts Used

- datetime module  
- csv module  
- file handling  
- dictionaries  
- decorators  
- CLI menu loop  

---

A beginner-friendly Python project for practicing file handling and data aggregation.
