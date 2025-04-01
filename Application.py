import streamlit as st
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='scott'
)
cursor = mydb.cursor()
class PasswordNotValidError(Exception):
    pass
class ZeroBalanceError(Exception):
    pass
class LackOfBalanceError(Exception):
    pass
def valid_password(password):
    numcount = 0
    spcount = 0
    lcount = 0
    ucount = 0
    if len(new_password) > 6:
        for i in new_password:
            if i.isalnum() == False:
                spcount += 1
            if i.isdigit():
                numcount += 1
            if i.islower():
                lcount += 1
            if i.isupper():
                ucount += 1
        if spcount >= 1 and numcount >= 1 and lcount >= 1 and ucount >= 1:
            pass
        else:
            raise PasswordNotValidError('password not valid')
    else:
        raise PasswordNotValidError('max 6 character password is required')

def user_data():
    cursor.execute('SELECT cname, password FROM customer')
    users = dict(cursor.fetchall())
    cursor.execute('SELECT cname, user_pin FROM customer')
    pins = dict(cursor.fetchall())
    return users, pins

st.title('My Bank Application :bank:')
menu = st.sidebar.selectbox("OPTION", ["Home", "Sign Up", "Log In"])
if menu == "Home":
    st.subheader("Welcome to the Bank Application")
    st.text("Please choose an option from the menu.")
    video_file = open(r"C:\Users\gowri\Downloads\vecteezy_2d-animation-of-a-bank-building-and-dollar-coins-depicting_50154283.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)


elif menu == "Sign Up":
    st.subheader("Sign Up")
    new_username = st.text_input("Enter your name").upper()
    new_password = st.text_input("Enter your password", type="password")
    new_password_confirm = st.text_input("Confirm your password", type="password")
    pin = st.text_input("Set a PIN (numeric only)", type="password")
    age = st.number_input("Enter your age", min_value=0)
    address = st.text_input("Enter your address")
    phone_number = st.text_input("Enter your contact number")
    occupation = st.text_input("Enter your occupation")
    aadhar = st.text_input("Enter your Aadhar Number")

    if st.button("Create Account"):
        try:
            valid_password(new_password)

            if new_password != new_password_confirm:
                st.error("Passwords do not match.")
            elif len(phone_number) != 10 or not phone_number.isdigit():
                st.error("Invalid contact number.")
            elif len(aadhar) != 12 or not aadhar.isdigit():
                st.error("Invalid Aadhar number.")
            else:
                query = """INSERT INTO customer 
                            (cname, password, balance, Age, Address, ph_no, occupation, aadhar_no, user_pin) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (new_username, new_password, 0, age, address, phone_number, occupation, aadhar, pin)
                cursor.execute(query, values)
                mydb.commit()
                st.success("Account created successfully!")
        except PasswordNotValidError as e:
            st.error(str(e))

elif menu == 'Log In':
    st.subheader('Log In')
    users, pins = user_data()
    username = st.text_input("Enter your username").upper()
    password = st.text_input("Enter your password", type="password")
    pin = st.text_input("Enter your PIN", type="password")

    if st.button("Log In"):
        if username in users and password == users[username]:
            if pin == str(pins[username]):
                st.success('log in successful')
                action = st.selectbox("Choose Action", ["Deposit", "Withdraw", "Balance Check"])

                if action == "Deposit":
                    amount = st.number_input("Enter deposit amount", min_value=1)
                    if st.button("Deposit"):
                        query = f"UPDATE customer SET balance = balance + %s WHERE cname = %s"
                        cursor.execute(query, (amount, username))
                        mydb.commit()
                        st.success(f"Successfully deposited Rs.{amount}.")

                elif action == "Withdraw":
                    amount = st.number_input("Enter withdrawal amount", min_value=1)
                    if st.button("Withdraw"):
                        cursor.execute("SELECT balance FROM customer WHERE cname = %s", (username,))
                        balance = cursor.fetchone()[0]

                        if balance == 0:
                            st.error("Zero balance in account.")
                        elif amount > balance:
                            st.error("Insufficient balance.")
                        else:
                            query = f"UPDATE customer SET balance = balance - %s WHERE cname = %s"
                            cursor.execute(query, (amount, username))
                            mydb.commit()
                            st.success(f"Successfully withdrawn Rs.{amount}.")

                elif action == "Balance Check":
                    cursor.execute(f"SELECT balance FROM customer WHERE cname = %s", (username,))
                    balance = cursor.fetchone()[0]
                    st.write(f"Your account balance is: Rs.{balance}")
                    st.write('hi')
            else:
                st.error("Invalid PIN.")
        else:
            st.error("Invalid username or password.")
