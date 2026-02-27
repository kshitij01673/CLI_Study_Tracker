from datetime import datetime   # Used to get today's date
import csv                      # Used to read/write CSV files
import os                       # Used for clearing screen and file checking
from error_logging import error_logging  # Your decorator for error handling

# ---------------------------------------------
# Define a single filename for ALL study data
# ---------------------------------------------
filename = "study_data.csv"

# ---------------------------------------------
# This function checks if the CSV file exists.
# If it does not exist, it creates the file
# and writes the header row.
# ---------------------------------------------
@error_logging
def check_csv():
    if not os.path.exists(filename):   # Check if file does NOT exist
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            # Write header row (column names)
            writer.writerow(["Date", "Subject", "Hours"])
    return True


# ---------------------------------------------
# Function to log study time
# ---------------------------------------------
@error_logging
def log_sub():
    date = datetime.now().strftime("%d-%m-%Y")  # Get today's date
    
    sub = input("Enter the subject: ")
    hrs = input("Enter the hours in format (hrs:mins) : ")

    # Split hours and minutes using colon
    hrs = hrs.split(":")
    
    # Convert into total hours (decimal format)
    hr = float(hrs[0]) + float(hrs[1]) / 60
    
    # Round to 2 decimal places
    hr = round(hr, 2)

    # Capitalize subject properly
    sub1 = sub.title()

    # Open file in append mode to ADD new row
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, sub1, hr])

    print(f"\nStudy time for {sub1} logged successfully for {hr} hours on {date}\n")


# ---------------------------------------------
# View total study hours for TODAY only
# ---------------------------------------------
@error_logging
def view_total_hrs_today():
    os.system("cls")  # Clear screen (Windows)
    
    today = datetime.now().strftime("%d-%m-%Y")
    total_hrs = {}   # Dictionary to store subject-wise totals

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Check only rows matching today's date
            if row["Date"] == today:
                subject = row["Subject"]
                hours = float(row["Hours"])

                # Add hours to dictionary
                total_hrs[subject] = total_hrs.get(subject, 0) + hours

    print(f"\nStudy summary for {today}\n")

    for subject, hrs in total_hrs.items():
        print(f"{subject}: {hrs} hours")

    print(f"\nTotal: {sum(total_hrs.values())} hours\n")


# ---------------------------------------------
# View total study hours for ANY specific date
# ---------------------------------------------
@error_logging
def view_total_hrs_date():
    os.system("cls")
    
    date1 = input("Enter the date (dd-mm-yyyy): ")

    total_hrs = {}

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Match given date
            if row["Date"] == date1:
                subject = row["Subject"]
                hours = float(row["Hours"])
                total_hrs[subject] = total_hrs.get(subject, 0) + hours

    print(f"\nStudy summary for {date1}\n")

    for subject, hrs in total_hrs.items():
        print(f"{subject}: {hrs} hours")

    print(f"\nTotal: {sum(total_hrs.values())} hours\n")


# ---------------------------------------------
# Main menu function
# ---------------------------------------------
@error_logging
def main():
    check_csv()  # Ensure file exists

    choice = input(
        "Enter your choice:\n"
        "1. Log study time\n"
        "2. View total study time today\n"
        "3. View total hours for a specific date\n"
        "4. Exit\n"
        "<--: "
    )

    if choice == "1":
        log_sub()
    elif choice == "2":
        view_total_hrs_today()
    elif choice == "3":
        view_total_hrs_date()
    elif choice == "4":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice")


# ---------------------------------------------
# Program starts here
# ---------------------------------------------
if __name__ == "__main__":
    while True:
        main()
        input("\nPress Enter to continue...")
        os.system("cls")