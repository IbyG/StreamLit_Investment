import streamlit as st
import datetime
import sqlite3
import pandas as pd
import plotly.express as px

#st.set_page_config(layout="wide")



 # Connect to the SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('Finance.db')

 # Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    amount DOUBLE)''')

st.write(""" # Investment Dashboard  """)
col1, col2 =st.columns(2)
def form_section():
    with col1:
        date = st.date_input("Current Date", datetime.date.today(),format="DD/MM/YYYY")
    with col2:
        amount = st.number_input("Insert Amount")
    #submit_button = st.button('Submit', type="secondary")
    # Insert data into the table
    if st.button("Submit"):
        cursor.execute("INSERT INTO Data (date,amount) VALUES (?,?)", (date,amount))
        conn.commit() 

   
# Retrieve data from the table
#cursor.execute("SELECT * FROM Data")
#rows = cursor.fetchall()
#for row in rows:
#    print(row)

col1, col2 =st.columns(2)
def widget_section():
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
    with col1:
        st.metric(label="Current Account Holding", value=latest_amount,delta=difference)
        #st.metric(label="Previous Account Holding", value=Sec_Amount)


    #Current Invested amount
    Invested_Amount = 9700
    #Total Profit/Loss
    Prof_Loss = round(latest_amount - Invested_Amount,2)
    #Prof_Loss_Perc = round((Sec_Amount/Invested_Amount)*100,2)
    with col2:
        st.metric(label="Current Profit/Loss", value=Prof_Loss)




def streamlit_lineChart():
    # Read data into a DataFrame
    query = "SELECT strftime('%m-%Y', date) AS 'Month and Year', ROUND(AVG(amount), 2) AS 'Average Amount' FROM Data GROUP BY strftime('%m-%Y', date) ORDER BY date DESC;"
    df = pd.read_sql_query(query, conn, parse_dates=['Month and Year'])

    #print(df)

    # Display line chart using Streamlit
    st.write("""#### Account Trend""")
    st.line_chart(df.set_index('Month and Year'))



def plotly_LineChart():
    # Read data into a DataFrame
    query = "SELECT date as 'Date',amount as 'Amount' FROM Data ORDER BY date DESC;"
    df = pd.read_sql_query(query, conn, parse_dates=['Month and Year'])

    #print(df)

    # Display line chart using Streamlit
    #st.write("""#### Monthly Average""")
    #st.line_chart(df.set_index('Month and Year'))

    #plotly line chart
    fig = px.line(df, x="Date", y="Amount", title='Account Trend',markers=True)
    fig.update_layout(yaxis=dict(tickformat=".2f"))
    ##fig.show()
    st.plotly_chart(fig)

def Average_Amount_Table():
    st.write("# Average Acount Amount")
    query = "SELECT strftime('%m-%Y', date) AS 'Month and Year', ROUND(AVG(amount), 2) AS 'Average Amount' FROM Data GROUP BY strftime('%m-%Y', date) ORDER BY date DESC;"
    df = pd.read_sql_query(query, conn)
    st.table(df)




def sidebar():
    st.sidebar.write(""" # Entry Form   """)
    date = st.sidebar.date_input("Date", datetime.date.today(),format="DD/MM/YYYY")
    amount = st.sidebar.number_input("Amount")
    #submit_button = st.button('Submit', type="secondary")
    # Insert data into the table
    if st.sidebar.button("Submit"):
        cursor.execute("INSERT INTO Data (date,amount) VALUES (?,?)", (date,amount))
        conn.commit() 


def raw_table():
    query = "SELECT date AS 'Date',amount AS 'Amount',lag(amount, 1, 0) OVER (ORDER BY date DESC) - amount AS 'Difference' FROM Data ORDER BY date ASC;"
    df = pd.read_sql_query(query, conn)
  
    # Round the 'Amount' and 'Difference' columns to 2 decimal places
    #df['Amount'] = df['Amount'].round(2)
    #df['Difference'] = df['Difference'].round(2)
    # Format the 'Date' column to dd-mm-yyyy
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')
  
 
    def highlight_diff(val):
        color = 'green' if val >= 0 else 'red'
        return f'color: {color}'

    
    # Apply conditional formatting to the 'Difference' column
    df_styled = df.style.applymap(highlight_diff, subset=['Difference']).format({'Amount': '{:.2f}', 'Difference': '{:.2f}'})

    # Display the styled DataFrame
    #df_styled
    st.write(" # Raw Data")
    st.dataframe(df_styled,width=800)

#form_section()
sidebar()
widget_section()
#streamlit_lineChart()
plotly_LineChart()
#Average_Amount_Table()
raw_table()


#Close the cursor and connection
cursor.close()
conn.close()