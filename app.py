import streamlit as st
import pandas as pd
import base64

# Set up expenses dictionary
expenses = {
    'Electricity Bill': 31401,
    'Worker Salary': 37500,
    'Food Supplies': 113795,
    'Vegetables': 33118,
    'LPG Gas Cylinder': 23279,
    'Farewell & Fresher': 40054,
    'Other': 13279,
    'Feast': 3605
}

def calculate_bill(expenses, students_df, month, year, diet_charge=1500, fixed_charge=500):
    total_expenses = sum(expenses.values())
    total_students = students_df.shape[0]
    total_meals = total_students * 2 * 30  # 2 meals per day per student for 30 days
    total_bill = total_expenses / total_meals + diet_charge + fixed_charge
    bill_per_student = total_bill / total_students

    # Create a new DataFrame with the calculated bill per student
    bill_df = pd.DataFrame({'Serial Number': students_df['Serial Number'], 
                            'Student Name': students_df['Student Name'], 
                            'Amount Balance': students_df['Amount Balance'], 
                            f'{month} {year} Bill': bill_per_student})
    return bill_df

# Set page title
st.set_page_config(page_title='Mess Bill Calculator')

# Define page layout
col1, col2 = st.columns(2)

# Add page title
col1.title('Mess Bill Calculator')

# Add file uploader
csv_file = col1.file_uploader('Upload CSV', type=['csv'])

# Add month and year input
month = col1.text_input('Enter month (e.g. January)')
year = col1.text_input('Enter year (e.g. 2022)')

# Add expenses slider for each expense
with col1.expander('Expenses'):
    for expense, amount in expenses.items():
        expenses[expense] = col1.slider(expense, 0, 100000, amount)

# Add diet charge and fixed charge inputs
diet_charge = col1.number_input('Enter diet charge', value=1500)
fixed_charge = col1.number_input('Enter fixed charge', value=500)

# Add button to calculate bill
if col1.button('Calculate Bill'):
    if csv_file is not None:
        # Read CSV file
        students_df = pd.read_csv(csv_file)

        # Calculate bill and show it
        bill_df = calculate_bill(expenses, students_df, month, year, diet_charge, fixed_charge)
        col2.dataframe(bill_df)

        # Download link
        csv = bill_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{month}_{year}_Bill.csv">Download CSV</a>'
        col2.markdown(href, unsafe_allow_html=True)
    else:
        col2.warning('Please upload a CSV file.')
