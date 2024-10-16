from abc import ABC, abstractmethod

class User:
    def __init__(self, userName, password, dateOfBirth, balance):
        self.userName = userName
        self.password = password
        self.dateOfBirth = dateOfBirth
        self.balance = balance
        self.active = True
        self.failed_attempts = 0

class UserManager(ABC):
    def __init__(self):
        self.datadict = {
            "sample": User("sample", "123", "01012005", 10000.26)
        }

class AbstractLogin(ABC):
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def signup(self):
        pass

    @abstractmethod
    def newPassword(self, userName, isDefault=True):
        pass

class AbstractTransactions(ABC):
    @abstractmethod
    def withdrawal(self, userName):
        amount = int(input("Enter the amount to withdraw: "))
        if 0 < amount <= self.datadict[userName].balance:
            self.datadict[userName].balance = self.datadict[userName].balance - amount
            return amount
        else:
            print("Invalid amount or insufficient balance.")

    @abstractmethod
    def deposit(self, userName):
        amount = int(input("Enter the amount to deposit: "))
        if amount > 0:
            self.datadict[userName].balance = self.datadict[userName].balance + amount
            return amount
        else:
            print("Invalid amount")

    @abstractmethod
    def balanceEnquiry(self, userName):
        print(f"balance: {self.datadict[userName].balance}")

    @abstractmethod
    def showMenu(self, userName):
        pass

class Login(UserManager, AbstractLogin):
    def login(self):
        userName = input("Enter the username: ")
        if userName in self.datadict:
            user = self.datadict[userName]
            if not user.active:
                print("Account is deactivated due to multiple failed login attempts.")
                return None
            print(f"Hi {userName}!")
            password = input("Please enter the password: ")
            if password == user.password:
                user.failed_attempts = 0
                print(f"Hi {userName}! Password validated.")
                return userName
            else:
                user.failed_attempts += 1
                print("Wrong password!")
                if user.failed_attempts >= 3:
                    user.active = False
                    print("Account deactivated due to multiple failed login attempts.")
                    return None
                reset = input("Do you want to reset the password? (yes/no): ")
                if reset.lower() == "yes":
                    self.newPassword(userName, False)
                else:
                    return self.login()
        else:
            print("Username not found. Please sign up.")
            self.signup()

    def signup(self):
        userName = input("Please enter a username: ")
        if userName in self.datadict:
            print("Username already exists! Try again with a new username.")
            self.signup()
        else:
            dateOfBirth = int(input("Enter date of birth (DDMMYYYY): "))
            balance = float(input("Enter the amount to deposit (greater than 2000): "))
            if balance <= 2000:
                print("Deposit must be greater than 2000.")
                self.signup()
            else:
                self.datadict[userName] = User(userName, self.newPassword(userName), dateOfBirth, balance)
                print("Account created successfully!")
                return userName

    def newPassword(self, userName, isDefault=True):
        if isDefault:
            newPw = ""
            for i in range(len(userName)):
                temp = userName[i]
                for j in range(i + 1, len(userName)):
                    if userName[i] != userName[j] and userName[j] not in temp:
                        temp += userName[j]
                    else:
                        break
                if len(temp) > len(newPw):
                    newPw = temp
            return newPw
        else:
            dob = input("Please enter date of birth for validation (DDMMYYYY): ")
            if dob == self.datadict[userName].dateOfBirth:
                password = input("Enter a new password: ")
                self.datadict[userName].password = password
                self.datadict[userName].failed_attempts = 0
                self.datadict[userName].active = True
                print("Password reset done.")
            else:
                print("Date of birth validation failed!")

class Transactions(UserManager, AbstractTransactions):
    def withdrawal(self, userName):
        amount = float(input("Enter the amount to withdraw: "))
        if 0 < amount <= self.datadict[userName].balance:
            self.datadict[userName].balance -= amount
            return amount
        else:
            print("Invalid amount or insufficient balance.")

    def deposit(self, userName):
        amount = float(input("Enter the amount to deposit: "))
        if amount > 0:
            self.datadict[userName].balance += amount
            return amount
        else:
            print("Invalid amount")

    def balanceEnquiry(self, userName):
        print(f"balance: {self.datadict[userName].balance}")

    def showMenu(self, userName):
        while True:
            print("\nMenu:")
            print("1. Withdrawal")
            print("2. Deposit")
            print("3. Password Change")
            print("4. Balance Enquiry")
            print("5. Logout")
            choice = input("Choose an option: ")

            if choice == '1':
                amount = self.withdrawal(userName)
                if amount:
                    print(f"Withdrawal successful. \nAmount withdrawn: {amount}. \nNew balance: {self.datadict[userName].balance}")
            elif choice == '2':
                amount = self.deposit(userName)
                if amount:
                    print(f"Deposit successful. \nAmount deposited: {amount}. \nNew balance: {self.datadict[userName].balance}")
            elif choice == '3':
                login_manager.newPassword(userName, False)
            elif choice == '4':
                self.balanceEnquiry(userName)
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

login_manager = Login()
transaction_manager = Transactions()

user = login_manager.login()
if user:
    transaction_manager.showMenu(user)

for username, user_obj in login_manager.datadict.items():
    print(f"User: {username}, Active: {user_obj.active}, Balance: {user_obj.balance}")
