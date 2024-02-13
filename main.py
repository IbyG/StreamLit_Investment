import streamlit as st
import datetime
import sqlite3
import pandas as pd

st.write(""" # Investment App  """)

date = st.date_input("Current Date", datetime.date.today(),format="DD/MM/YYYY")
amount = st.number_input("Insert Amount")
#submit_button = st.button('Submit', type="secondary")

# Connect to the SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('Finance.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Data (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date DATE,
                  amount DOUBLE)''')



# Insert data into the table
if st.button("Submit"):
    cursor.execute("INSERT INTO Data (date,amount) VALUES (?,?)", (date,amount))
    conn.commit() 

# Retrieve data from the table
#cursor.execute("SELECT * FROM Data")
#rows = cursor.fetchall()
#for row in rows:
#    print(row)

################################################################################
#Getting the latest Amount and showing it in a widget
latestAmount = "SELECT amount FROM Data ORDER BY date DESC LIMIT 1;"
df = pd.read_sql_query(latestAmount,conn)
latest_amount = df.iloc[0, 0]
#Getting the previous Amount
SeclatestAmount = "SELECT amount FROM Data ORDER BY date DESC LIMIT 1 OFFSET 1;" 
df = pd.read_sql_query(SeclatestAmount,conn)
Sec_Amount = df.iloc[0,0]

#difference between current and previous
difference = round(latest_amount - Sec_Amount, 2)

st.metric(label="Current Account Holding", value=latest_amount,delta=difference)
#st.metric(label="Previous Account Holding", value=Sec_Amount)
################################################################################
# Read data into a DataFrame
query = "SELECT strftime('%m-%Y', date) AS 'Month and Year', ROUND(AVG(amount), 2) AS 'Average Amount' FROM Data GROUP BY strftime('%m-%Y', date) ORDER BY date DESC;"
df = pd.read_sql_query(query, conn, parse_dates=['Month and Year'])

print(df)

# Display line chart using Streamlit
st.write("""#### Monthly Average""")
st.line_chart(df.set_index('Month and Year'))
#################################################################################
query = "SELECT strftime('%m-%Y', date) AS 'Month and Year', ROUND(AVG(amount), 2) AS 'Average Amount' FROM Data GROUP BY strftime('%m-%Y', date) ORDER BY date DESC;"
df = pd.read_sql_query(query, conn)
st.table(df)
#################################################################################


#Close the cursor and connection
cursor.close()
conn.close()


