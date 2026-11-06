print("Welcome to ChalanCheck")

print("************ChalanCheck Menu*********** ")
while True:
    print("1. Display Project Information")
    print("2. Display Sample questions.")
    print("3. Check Traffic Rule")
    print("0. Exit ")

    choice =input("\nEnter Your Choice : ")

    if choice == "1":
        print("ChalanCheck is an AI-powered Traffic Challan Assistant.\n\n")
    elif choice =="2":
        print("1. What is the Motor Vehicles Act?")
        print("2. What is section 184?")
        print("3. What is the penalty for speeding?\n\n")
    elif choice =="3":
        print("1. Keep left: Drive on the left side of the road and overtake only from the right")
        print("2. Obey signals: Stop completely at red lights and follow all posted speed limits")
        print("3. No phones: Using mobile phones while driving is strictly prohibited.\n\n")
    elif choice == "0": 
        print("Thank You for using ChalanCheck\n\n")
        break
    else: 
        print("Invalid Choice")
    
