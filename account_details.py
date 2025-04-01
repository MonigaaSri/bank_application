username_password={'dinga':1234,'dingi':4567}
username_amount={'dinga':1000,'dingi':50}
username_pin={'dinga':1111,'dingi':0000}
def welcome(func):
    def inner():
        print('welcome')
        func()
    return inner
@welcome
def login():
    username = input('enter your name:')
    if username in username_password:
        password = int(input('enter the password:'))
        if username_password[username]==password:
            print('\t\t\t\t\t\t\t\t\t\t\t\t\tWELCOME TO HOME PAGE\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t-------------------\n')
            home(username)
        else:
            print('password is incorrect')
    else:
        print('username not exists')
def home(username):
    print('which of the services you want...\nfor deposit enter 1\nfor withdraw enter 2\nfor balance check enter 3\n')
    service=int(input('enter the option:'))
    if service==1:
        deposit(username)
    elif service==2:
        withdraw(username)
    elif service==3:
        balancecheck(username)
    else:
        print('invalid option')
def deposit(username):
    pin=int(input('enter your pin:'))
    if username_pin[username]==pin:
        print('pin is correct')
        amount = int(input('enter the amount:'))
        username_amount[username] += amount
        print('Amount credited')
        print(f'your new balance is{username_amount[username]}')
    else:
        print('pin is incorrect')

def withdraw(username):
    pin = int(input('enter your pin'))
    if username_pin[username]==pin:
        print('pin is correct')
        amount = int(input('enter the amount:'))
        if amount <= username_amount[username]:
            username_amount[username] -= amount
            print('Amount debited')
        else:
            print('enter the correct amount')
    else:
        print('pin is incorrect')

def balancecheck(username):
    pin = int(input('enter your pin'))
    if username_pin[username]==pin:
        print('pin is correct')
        print(f'The available balance in your account is {username_amount[username]}')
    else:
        print('pin is incorrect')
# prog
print('\t\t\t\t\t\t\t\t\t\t\t\t\tWELCOME TO OUR BANK\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t-------------------\n')
print('if account already exists enter y\nif you are a new user enter n')
option=input('please enter any option:')
if option=='y':
    login()
elif option=='n':
    print('to create account enter y\nto exit enter n')
    option = input('please enter any option:')
    if option == 'n':
        print('PLEASE EXIT')
    elif option=='y':
        new_username=input('enter your name:')
        new_password=int(input('enter the password:'))
        new_password2=int(input('re enter the password:'))
        n_pin=int(input('create the pin:'))
        if new_password==new_password2:
            username_password.setdefault(new_username,new_password)
            username_pin[new_username]=n_pin
            username_amount[new_username]=0

            print('welcome to your new account')
            login()
        else:
            print('recheck your password')
    else:
        print('invalid option')
else:
    print('invalid option')