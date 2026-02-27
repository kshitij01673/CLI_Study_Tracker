from datetime import datetime
import csv
import os
from error_logging import error_logging

@error_logging
def check_csv():
    if not os.path.exists("study_data.csv"):
        os.system("cls")
        print("Data file not found\n")
        with open("study_data.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Subject", "Hours"])
            print("Data file created successfully\n")
            input("\nPress Enter to continue...")
            os.system("cls")
    return True

@error_logging
def log_sub():
    sub = input("Enter the subject: ")
    hrs = input("Enter the hours in format (hrs:mins) : ")
    hrs = hrs.split(":")
    hr = float(hrs[0])+ float(hrs[1])/60
    hr = round(hr,2)
    sub1 = sub.title()
    date = datetime.now().strftime("%d-%m-%Y")
    with open("study_data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([date, sub1, hr])
    print(f"Study time for {sub1} logged successfully for {hr} hours on {date}\n")

@error_logging
def view_total_hrs():
    os.system("cls")
    # Create an empty dictionary to store total hours per subject.
    # Example structure later:
    # {
    #   "Math": 5.5,
    #   "Physics": 3.0
    # }
    total_hrs = {}

    # Open the CSV file in read mode.
    # "with" ensures the file automatically closes after use.
    with open("study_data.csv", mode="r") as file:
        
        # Create a DictReader object.
        # This reads each row as a dictionary instead of a list.
        # Column names become dictionary keys.
        # Example row:
        # {"date": "2026-02-27", "subject": "Math", "hours": "2"}
        reader = csv.DictReader(file)

        # Loop through each row in the CSV file.
        for row in reader:
            
            # Extract subject from current row.
            # Since DictReader uses column headers,
            # we refer to the column by name.
            subject = row["Subject"]

            # Extract hours and convert from string to float.
            # CSV stores everything as text, so conversion is necessary.
            hours = float(row["Hours"])

            # Add hours to dictionary.
            # If subject already exists → add to existing total.
            # If subject does not exist → start it at 0.
            # .get(subject, 0) returns:
            #   existing value if present
            #   otherwise 0
            total_hrs[subject] = total_hrs.get(subject, 0) + hours

    # After processing all rows,
    # loop through dictionary to print results.
    for subject, hrs in total_hrs.items():
        print(f"{subject}: {hrs} hours")

@error_logging
def main():
    check_csv()
    choice = input("Enter your choice: \n1. Log study time\n2. View total study time\n3. Exit\n <--: ")
    if choice == "1":
        log_sub()
    elif choice == "2":
        view_total_hrs()
    elif choice == "3":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    
    while True:
        main()
        input("\nPress Enter to continue...")
        os.system("cls") 