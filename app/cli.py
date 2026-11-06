
from app.records import load_records, search, count_by, get_by_id


def main():

    while True:

        print("\n========== CHALANCHECK ==========")
        print("1. Display all traffic rules")
        print("2. Search by keyword")
        print("3. Count records by category")
        print("4. Find by section number")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        # Display all records
        if choice == "1":

            records = load_records()

            for record in records:
                print("\nSection:", record["section"])
                print("Offence:", record["offence"])
                print("First Fine:", record["max_fine_first"])
                print("Repeat Fine:", record["max_fine_repeat"])
                print("Additional Action:", record["other_action"])

        # Search by keyword
        elif choice == "2":

            keyword = input("Enter keyword: ").strip()
            results = search(keyword)

            if results:
                for record in results:
                    print("\nSection:", record["section"])
                    print("Offence:", record["offence"])
                    print("First Fine:", record["max_fine_first"])
            else:
                print("No matching records found.")

        # Count records by category
        elif choice == "3":

            counts = count_by("category")

            print("\n--- Category Summary ---")

            for category, total in counts.items():
                print(category, ":", total)

        # Find record by section number
        elif choice == "4":

            section = input("Enter section number: ").strip()
            record = get_by_id(section)

            if record:
                print("\nSection:", record["section"])
                print("Offence:", record["offence"])
                print("First Fine:", record["max_fine_first"])
                print("Repeat Fine:", record["max_fine_repeat"])
                print("Additional Action:", record["other_action"])
            else:
                print("Section not found.")

        # Exit
        elif choice == "0":

            print("Thank you for using ChalanCheck!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
