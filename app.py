import streamlit as st
import mysql.connector
from mysql.connector import Error


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Database connection
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='scott'
)
cursor = mydb.cursor(buffered=True)  # Use buffered cursor to prevent unread result errors


def show_banking_options():
    st.subheader(f"Welcome, {st.session_state.username}")

    if st.session_state.logged_in:
        cursor.execute("SELECT balance FROM customer WHERE cname = %s", (st.session_state.username,))
        current_balance = cursor.fetchone()[0]
        st.info(f"Current Balance: Rs.{current_balance}")

        action = st.selectbox("Choose Action", ["Deposit", "Withdraw", "Balance Check"])

        if action == "Deposit":
            deposit_amount = st.number_input("Enter deposit amount", min_value=1)
            if st.button("Deposit"):
                try:
                    cursor.execute("UPDATE customer SET balance = balance + %s WHERE cname = %s",
                                   (deposit_amount, st.session_state.username))
                    mydb.commit()
                    st.success(f"Successfully deposited Rs.{deposit_amount}")
                    st.rerun()
                except Error as e:
                    st.error(f"An error occurred: {e}")
                    mydb.rollback()

        elif action == "Withdraw":
            withdraw_amount = st.number_input("Enter withdrawal amount", min_value=1)
            if st.button("Withdraw"):
                try:
                    if withdraw_amount > current_balance:
                        st.error("Insufficient balance!")
                    elif current_balance == 0:
                        st.error("Zero balance in account!")
                    else:
                        cursor.execute("UPDATE customer SET balance = balance - %s WHERE cname = %s",
                                       (withdraw_amount, st.session_state.username))
                        mydb.commit()
                        st.success(f"Successfully withdrawn Rs.{withdraw_amount}")
                        st.rerun()
                except Error as e:
                    st.error(f"An error occurred: {e}")
                    mydb.rollback()

        elif action == "Balance Check":
            if st.button("Refresh Balance"):
                cursor.execute("SELECT balance FROM customer WHERE cname = %s",
                               (st.session_state.username,))
                balance = cursor.fetchone()[0]
                st.info(f"Your current balance is: Rs.{balance}")


def main():
    st.title('My Bank Application :bank:')

    menu = st.sidebar.selectbox("OPTION", ["Home", "Sign Up", "Log In"])

    if menu == "Home":
        st.subheader("Welcome to the Bank Application")
        st.text("Please choose an option from the menu.")
        video_file = open(
            r"C:\Users\gowri\Downloads\vecteezy_2d-animation-of-a-bank-building-and-dollar-coins-depicting_50154283.mp4",
            "rb")
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
            if new_password != new_password_confirm:
                st.error("Passwords do not match.")
            elif len(phone_number) != 10 or not phone_number.isdigit():
                st.error("Invalid contact number.")
            elif len(aadhar) != 12 or not aadhar.isdigit():
                st.error("Invalid Aadhar number.")
            else:
                try:
                    query = """INSERT INTO customer 
                              (cname, password, balance, Age, Address, ph_no, occupation, aadhar_no, user_pin) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (new_username, new_password, 0, age, address, phone_number, occupation, aadhar, pin)
                    cursor.execute(query, values)
                    mydb.commit()
                    st.success("Account created successfully!")
                except Error as e:
                    st.error(f"An error occurred: {e}")
                    mydb.rollback()

    elif menu == "Log In":
        if not st.session_state.logged_in:
            st.subheader('Log In')
            username = st.text_input("Enter your username").upper()
            password = st.text_input("Enter your password", type="password")
            pin = st.text_input("Enter your PIN", type="password")

            if st.button("Log In"):
                cursor.execute('SELECT * FROM customer WHERE cname = %s AND password = %s AND user_pin = %s',
                               (username, password, pin))
                user = cursor.fetchone()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success('Log in successful')
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        else:
            show_banking_options()
            if st.sidebar.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.rerun()


if __name__ == "__main__":
    main()