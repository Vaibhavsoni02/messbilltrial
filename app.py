import streamlit as st
import pandas as pd
import base64
import datetime

# Define the expenses for the month
expenses = {
    "Electricity Bill": 31401,
    "Worker Salary": 37500,
    "Food Supplies": 113795,
    "Vegetables": 33118,
    "LPG Gas Cylinder": 23279,
    "Farewell & Fresher": 40054,
    "Other": 13279,
    "Feast": 3605
}

# Define the fixed and diet charges
fixed_charge = 1000
diet_charge = 70

# Function to calculate the total bill for a student
def calculate_bill(balance, meals):
    total_expenses = sum(expenses.values())
    total_students = len(student_list)
    per_student_expenses = total_expenses / total_students
    
    diet_charges = meals * diet_charge
    total_charges = fixed_charge + diet_charges + per_student_expenses
    
    if balance < total_charges:
        return "Insufficient Balance"
    
    return round(total_charges, 2)

# Define the Streamlit app
def app():
    st.title("Mess Bill Generator")
    
    # Create a sidebar for entering the month and year
    col1, col2 = st.beta_columns(2)
    with col1:
        month = st.selectbox("Select Month", list(range(1, 13)))
    with col2:
        year = st.number_input("Enter Year", value=datetime.date.today().year)
    
    # Create a file uploader for the student list
    st.header("Upload Student List")
    file = st.file_uploader("Choose CSV file with student list", type="csv")
    if file is not None:
        df = pd.read_csv(file)
        st.write(df)
    else:
        st.warning("Please upload a CSV file")
        return
        
    # Create sliders for the number of meals per day
    st.header("Enter Number of Meals per Day")
    breakfast_meals = st.slider("Breakfast", min_value=0, max_value=2, value=1, step=1)
    lunch_meals = st.slider("Lunch", min_value=0, max_value=2, value=2, step=1)
    dinner_meals = st.slider("Dinner", min_value=0, max_value=2, value=2, step=1)
    
    # Calculate the total meals per student
    total_meals = (breakfast_meals + lunch_meals + dinner_meals) * 30
    
    # Calculate the bill for each student
    df["Total Bill"] = df["Amount Balance"].apply(lambda x: calculate_bill(x, total_meals))
    st.write(df)
    
    # Create a button to download the bill as a CSV file
    if st.button("Download Bill"):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="mess_bill_{month}_{year}.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

--------------------------------------------------------------------------------------------------------------------------------------
# import streamlit as st
# import pandas as pd
# import base64

# # Define the expenses for the month as Streamlit slider widgets
# st.sidebar.title('Enter Expenses for the Month')
# electricity_bill = st.sidebar.slider('Electricity Bill', min_value=0, max_value=100000, value=31401)
# worker_salary = st.sidebar.slider('Worker Salary', min_value=0, max_value=100000, value=37500)
# food_supplies = st.sidebar.slider('Food Supplies', min_value=0, max_value=200000, value=113795)
# vegetables = st.sidebar.slider('Vegetables', min_value=0, max_value=50000, value=33118)
# lpg_gas_cylinder = st.sidebar.slider('LPG Gas Cylinder', min_value=0, max_value=50000, value=23279)
# farewell_fresher = st.sidebar.slider('Farewell & Fresher', min_value=0, max_value=100000, value=40054)
# other = st.sidebar.slider('Other', min_value=0, max_value=50000, value=13279)
# feast = st.sidebar.slider('Feast', min_value=0, max_value=10000, value=3605)

# # Define the expenses as a dictionary
# expenses = {
#     'Electricity Bill': electricity_bill,
#     'Worker Salary': worker_salary,
#     'Food Supplies': food_supplies,
#     'Vegetables': vegetables,
#     'LPG Gas Cylinder': lpg_gas_cylinder,
#     'Farewell & Fresher': farewell_fresher,
#     'Other': other,
#     'Feast': feast,
# }

# # Define the fixed charge per student and the diet charge per student
# num_students = 0
# for key, value in expenses.items():
#     if key != 'Food Supplies':
#         num_students += 1

# fixed_charge = expenses['Electricity Bill'] + expenses['Worker Salary']
# fixed_charge_per_student = fixed_charge / num_students
# diet_charge_per_student = expenses['Food Supplies'] / num_students

# # Define a function to calculate the total amount due for each student
# def calculate_total(row):
#     fixed = row['Fixed Charge']
#     diet = row['Diet Charge']
#     total = fixed + diet
#     if total > 0.1 * sum(expenses.values()):
#         return f'{total} *'
#     else:
#         return total

# # Define the Streamlit app
# st.title('College Hostel Mess Bill Generator')

# # Upload a CSV file containing a list of students and their account balances
# file = st.file_uploader('Upload CSV file')
# if file is not None:
#     df = pd.read_csv(file)

#     # Add columns for fixed charge, diet charge, and total amount due
#     df['Fixed Charge'] = fixed_charge_per_student
#     df['Diet Charge'] = diet_charge_per_student
#     df['Total Amount Due'] = df.apply(calculate_total, axis=1)

#     # Display the updated DataFrame
#     st.write(df)
    
#     # Allow the user to download the updated DataFrame as a CSV file
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="mess_bill.csv">Download CSV file</a>'
#     st.markdown(href, unsafe_allow_html=True)
