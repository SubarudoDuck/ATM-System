from sys import exit
import json

with open("data.json", "r") as d:
    customers = json.load(d)

usernames = []
for details in customers:
    usernames.append(details["name"])

def login():
    tries = 5
    initiateLogin(tries)

# find customer details linked to username to use later
def findCustomer(username):
    for details in customers:
        if username == details["name"]:
            found = details
            break
    return found

def updateAccount(customer):
    for details in customers:
        if details["name"] == customer["name"]:
            details = customer
            break
    with open("data.json", "w") as out:
        json.dump(customers, out, indent = 4)

# 
def initiateLogin(tries):
    while tries > 0:
        username = input("Enter Username: ")
        # first case: username doesnt exist / not found
        if username == "exit":
            exit()
        elif username not in usernames:
            print("Username not found, try again.\n")
            print(f"{tries - 1} tries left!")
            tries -= 1
            initiateLogin(tries)
        else:
            # second case: the account is locked => cant login
            customer = findCustomer(username)
            if customer["status"] == "locked":
                print("Account Locked! Please use a different account.")
                login()
            else:
                enterPassword(customer, tries)
                break
    if tries == 0:
        print("Suspending ATM. Call staff for assistance.")
        login()

def enterPassword(customer, tries):
    correctPassword = customer["password"]
    while tries > 0:
        inputPassword = input("Enter Password: ")
        if inputPassword != correctPassword:
            print(f"Incorrect Password! {tries - 1} tries left!")
            tries -= 1
        else:
            initiateWithdraw(customer)
    if tries == 0:
        print("Account Locked! Please use a different account.")
        customer["status"] = "locked"
        updateAccount(customer)
        print(customer)
        login()



def initiateWithdraw(customer):
    print(customer)
    choice = input("1 - Withdraw, 2 - Check Balance, 3 - Send Money to another account ")
    currentBalance = customer["money"]
    if choice == "1":
        withdraw(customer)
    elif choice == "2":
        print(f"You currently have {currentBalance} VND in your account.")
        initiateWithdraw(customer)
    elif choice == "3":
        tries = 5
        receiver = findReceiver(customer, tries)
        sendMoney(customer, receiver)
    else:
        print("Invalid Response. Try again.")
        initiateWithdraw(customer)

def withdraw(customer):
    withdrawInput = input("How much do you want to withdraw? ")
    if not withdrawInput.isnumeric():
        print("Invalid Response. Try again.")
        withdraw(customer)
    else:
        withdrawAmount = int(withdrawInput)
        if withdrawAmount > customer["money"]:
            print("You are too poor to withdraw that much.")
            withdraw(customer)
        else:
            customer["money"] -= withdrawAmount
            updateAccount(customer)
            rewithdraw(customer)

def rewithdraw(customer):
    response = input("Thank you for using the ATM\nWould you like to continue? 1 - Yes, 2 - No ")
    if response == "1":
        initiateWithdraw(customer)
    elif response == "2":
        login()
    else:
        print("Invalid Response. Try again.")
        rewithdraw(customer)

def findReceiver(customer, tries):
    while tries > 0:
        target = input("Which user do you want to send money to? ")
        if target in usernames:
            receiver = findCustomer(target)
            return receiver
        else:
            print(f"Unable to find user. {tries - 1} tries left.")
            tries -= 1
            findReceiver(customer, tries)
    if tries == 0:
        print("Suspicious activity detected. Locking account.")
        customer["status"] = "locked"
        updateAccount(customer)
        login()

def sendMoney(customer, receiver):
    sendInput = input("How much money do you want to send? ")
    if not sendInput.isnumeric():
        print("Invalid Response. Try again.")
        sendMoney(customer, receiver)
    else:
        sendAmount = int(sendInput)
        if sendAmount > customer["money"]:
            print("You are too poor to send that amount.")
            sendMoney(customer, receiver)
        else:
            customer["money"] -= sendAmount
            updateAccount(customer)
            receiver["money"] += sendAmount
            updateAccount(receiver)
            rewithdraw(customer)

login()
