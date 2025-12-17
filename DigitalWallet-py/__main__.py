# Dafny program DigitalWallet.dfy compiled into Python
import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny

def print_menu():
    print("\n" + "=" * 40)
    print("      Digital Wallet CLI Menu")
    print("=" * 40)
    print("1: New Account")
    print("2: Authenticate (Check Attempts)")
    print("3: Get Balance")
    print("4: Transfer Funds")
    print("5: Add Interest to All Accounts")
    print("0: Quit")
    print("-" * 40)

def run_cli():
    # Instantiate the Digital Wallet
    wallet = module_.DigitalWallet()
    wallet.ctor__() # Call the constructor method

    # --- Setup Demo Accounts ---
    try:
        wallet.NewAccount(101, 5000, 1234)
        wallet.NewAccount(102, 2500, 4321)
        print("Initialization complete. Accounts 101 (PIN 1234) and 102 (PIN 4321) created.")
    except Exception as e:
        print(f"Initial setup failed: {e}. Check if module_ is correctly imported.")
        return

    while True:
        print_menu()
        choice = input("Enter your choice (0-5): ")

        try:
            if choice == '0':
                print("Exiting Digital Wallet CLI. Goodbye!")
                break
            
            elif choice == '1': # New Account
                print("\n--- New Account ---")
                userId = int(input("Enter new User ID: "))
                initialBalance = int(input("Enter initial Balance (e.g., 5000 for $50.00): "))
                pin = int(input("Enter new PIN (4 digits recommended): "))
                if not wallet.Balances.get(userId):
                    wallet.NewAccount(userId, initialBalance, pin)
                    print(f"Success: Account {userId} created with balance {initialBalance}.")
                else:
                    print(f"Failure: Account ID {userId} already exists.")

            elif choice == '2': # Authenticate (Check Attempts)
                print("\n--- Authenticate ---")
                userId = int(input("Enter User ID: "))
                pin = int(input("Enter PIN: "))
                
                if userId not in wallet.PINs:
                    print(f"Failure: User ID {userId} does not exist.")
                    continue
                    
                if wallet.AccountIsLocked(userId):
                    print(f"Account Locked: Account {userId} is currently locked due to too many failed attempts.")
                elif wallet.Authenticate(userId, pin):
                    print(f"Success: Authentication for ID {userId} successful.")
                else:
                    attempts = wallet.WrongAttempts.get(userId, 0)
                    remaining = wallet.MaxWrongAttempts - attempts
                    print(f"Failure: Authentication failed. Wrong Attempts: {attempts}. Attempts remaining: {remaining}.")

            elif choice == '3': # Get Balance
                print("\n--- Get Balance ---")
                userId = int(input("Enter User ID: "))
                pin = int(input("Enter PIN: "))

                if userId not in wallet.PINs:
                    print(f"Failure: User ID {userId} does not exist.")
                    continue

                if wallet.AccountIsLocked(userId):
                    print(f"Account Locked: Cannot access balance. Account {userId} is locked.")
                elif wallet.Authenticate(userId, pin):
                    balance = wallet.GetBalance(userId, pin)
                    print(f"Success: Account {userId} balance is {balance}.")
                else:
                    print(f"Failure: Authentication failed for ID {userId}. Cannot view balance.")

            elif choice == '4': # Transfer Funds
                print("\n--- Transfer Funds ---")
                sourceId = int(input("Enter Source User ID: "))
                sourcePin = int(input("Enter Source PIN: "))
                destinationId = int(input("Enter Destination User ID: "))
                amount = int(input("Enter Amount to Transfer: "))
                
                # Check IDs exist
                if sourceId not in wallet.PINs or destinationId not in wallet.PINs:
                    print("Failure: Source or Destination ID not found.")
                    continue

                # Authentication and Locked Check
                if wallet.AccountIsLocked(sourceId):
                    print(f"Account Locked: Source account {sourceId} is locked.")
                elif wallet.Authenticate(sourceId, sourcePin):
                    # Balance Check (Implied logic for fixed-point integer arithmetic)
                    if wallet.Balances[sourceId] >= amount:
                        wallet.Transfer(sourceId, sourcePin, destinationId, amount)
                        print(f"Success: Transferred {amount} from {sourceId} to {destinationId}.")
                    else:
                        print("Failure: Insufficient funds in source account.")
                else:
                    print("Failure: Source authentication failed.")

            elif choice == '5': # Add Interest
                print("\n--- Add Interest ---")
                ratePercentage = int(input("Enter Annual Interest Rate (%) (e.g., 5): "))
                wallet.AddInterest(ratePercentage)
                print(f"Success: Applied {ratePercentage}% interest to all accounts. Note: Balances may be updated.")
            
            else:
                print("Invalid choice. Please enter a number between 0 and 5.")

        except ValueError:
            print("Error: Please ensure all inputs are valid integers.")
        except Exception as e:
            # Catch errors like key not found if an ID is entered that wasn't checked above
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_cli()