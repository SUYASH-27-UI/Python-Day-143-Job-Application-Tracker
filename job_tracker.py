
import csv
import os

FILE_NAME = "applications.csv"
FIELDS = ["ID", "Company", "Role", "Date", "Status"]


def load_applications():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_applications(applications):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(applications)


def add_application():
    applications = load_applications()

    try:
        app_id = int(input("Enter application ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    if any(app["ID"] == str(app_id) for app in applications):
        print("Application ID already exists.")
        return

    company = input("Enter company name: ").strip()
    role = input("Enter job role: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    from datetime import datetime
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    if not company or not role:
        print("Company and role cannot be empty.")
        return

    applications.append({
        "ID": str(app_id),
        "Company": company,
        "Role": role,
        "Date": date,
        "Status": "Applied"
    })

    save_applications(applications)
    print("Application added successfully!")


def view_applications():
    applications = load_applications()

    if not applications:
        print("No applications found.")
        return

    print("\n===== JOB APPLICATIONS =====")

    for app in applications:
        print(
            f'ID: {app["ID"]} | {app["Company"]} | '
            f'{app["Role"]} | {app["Date"]} | {app["Status"]}'
        )


def update_status():
    applications = load_applications()
    app_id = input("Enter application ID: ").strip()

    for app in applications:
        if app["ID"] == app_id:
            print("1. Applied")
            print("2. Interview")
            print("3. Selected")
            print("4. Rejected")

            choice = input("Choose new status: ").strip()

            statuses = {
                "1": "Applied",
                "2": "Interview",
                "3": "Selected",
                "4": "Rejected"
            }

            if choice not in statuses:
                print("Invalid status.")
                return

            app["Status"] = statuses[choice]
            save_applications(applications)
            print("Status updated successfully!")
            return

    print("Application not found.")


def search_company():
    applications = load_applications()
    name = input("Enter company name to search: ").strip().lower()

    found = False

    for app in applications:
        if name in app["Company"].lower():
            print(app)
            found = True

    if not found:
        print("No matching company found.")


def show_summary():
    applications = load_applications()
    summary = {
        "Applied": 0,
        "Interview": 0,
        "Selected": 0,
        "Rejected": 0
    }

    for app in applications:
        if app["Status"] in summary:
            summary[app["Status"]] += 1

    print("\n===== APPLICATION SUMMARY =====")

    for status, count in summary.items():
        print(f"{status}: {count}")

    print("Total applications:", len(applications))


def main():
    while True:
        print("\n===== JOB APPLICATION TRACKER =====")
        print("1. Add Application")
        print("2. View Applications")
        print("3. Update Status")
        print("4. Search Company")
        print("5. Show Summary")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_status()
        elif choice == "4":
            search_company()
        elif choice == "5":
            show_summary()
        elif choice == "6":
            print("Tracker closed.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
