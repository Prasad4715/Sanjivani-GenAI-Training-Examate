print("Welcome to ChalanCheck")

print("************ChalanCheck Menu*********** ")
while True:
    print("1. Display Project Information")
    print("2. Display Sample questions.")
    print("3. Check Traffic Rule")
    print("0. Exit ")

    choice =input("\nEnter Your Choice : ").strip()

    if choice == "1":
        print("ChalanCheck is an AI-powered Traffic Challan Assistant.\n\n")
    elif choice =="2":
        print("1. What is the Motor Vehicles Act?")
        print("2. What is section 184?")
        print("3. What is the penalty for speeding?\n\n")
    elif choice == "3":
        print("\n--- Traffic Rule Checker ---")
        section = input("Enter Motor Vehicles Act section: ").strip()

        if section == "184":
            print("Section 184: Dangerous driving.")
        elif section == "185":
            print("Section 185: Driving under the influence of alcohol or drugs.")
        elif section == "194D":
            print("Section 194D: Driving without wearing a helmet.")
        else:
            print("Section not available in this basic demonstration.")
    elif choice == "0": 
        print("Thank You for using ChalanCheck\n\n")
        break
    else: 
        print("Invalid Choice")
    
