import streamlit as st
import datetime
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

#st.set_page_config(layout="wide")



 # Connect to the SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('Finance.db')

 # Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the Data table
cursor.execute('''CREATE TABLE IF NOT EXISTS Data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    amount DOUBLE)''')

#Create the Investment Tabel
cursor.execute('''CREATE TABLE IF NOT EXISTS Investment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    InvestedAmount DOUBLE)''')

st.write(""" # Investment Dashboard  """)

col1, col2,col3 =st.columns(3)
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
    


    #Current Invested amount
    Invested_Amount_que = "SELECT sum(InvestedAmount) as InvestedAmount FROM Investment;"
    df = pd.read_sql_query(Invested_Amount_que,conn)
    Invested_Amount = df.iloc[0,0]
    #print(Invested_Amount)
    #Total Profit/Loss
    Prof_Loss = round(latest_amount - Invested_Amount,2)
    #Prof_Loss_Perc = round((Sec_Amount/Invested_Amount)*100,2)
    with col1:
        st.metric(label="Total Invested Amount", value="$ " + str(Invested_Amount))
    with col2:
        st.metric(label="Current Account Holding", value="$ "+str(latest_amount),delta="$ "+str(difference))
    with col3:
        st.metric(label="Current Profit/Loss", value="$ "+ str(Prof_Loss))



    



def streamlit_lineChart():
    # Read data into a DataFrame
    query = "SELECT strftime('%m-%Y', date) AS 'Month and Year', ROUND(AVG(amount), 2) AS 'Average Amount' FROM Data GROUP BY strftime('%m-%Y', date) ORDER BY date DESC;"
    df = pd.read_sql_query(query, conn, parse_dates=['Month and Year'])

    #print(df)

    # Display line chart using Streamlit
    st.write("""#### Account Trend""")
    st.line_chart(df.set_index('Month and Year'))



def plotly_LineChart():
    Account_query = "SELECT date as 'Date',amount as 'Amount' FROM Data ORDER BY date DESC;"
    inv_query = "Select date as 'Date', InvestedAmount as 'Invested Amount' FROM Investment ORDER BY date DESC;"
    # Read data into a DataFrame
    df = pd.read_sql_query(Account_query, conn, parse_dates=['Month and Year'])
    #print(df)
    inv_df = pd.read_sql_query(inv_query,conn,parse_dates=['Month and Year'])
    #pritn(inv_df)

    # Display line chart using Streamlit
    #st.write("""#### Monthly Average""")
    #st.line_chart(df.set_index('Month and Year'))

    #plotly line chart
    fig = px.line(df, x="Date", y="Amount", title='Account Trend',markers=True)
    # Add line chart for the second DataFrame (inv_df) to the same figure
    fig.add_scatter(x=inv_df['Date'], y=inv_df['Invested Amount'], mode='lines+markers', name='Invested Amount')
    # Update layout to 2 decimal places
    fig.update_layout(yaxis=dict(tickformat="$,.2f"))
    #fig.px.line(inv_df)
    ##fig.show()
    st.plotly_chart(fig)



def plotly_BarChart():
    # Execute SQL queries to get data
    Account_query = "SELECT amount FROM Data ORDER BY date DESC LIMIT 1;"
    inv_query = "SELECT SUM(InvestedAmount) as 'Invested Amount' FROM Investment;"

    df = pd.read_sql_query(Account_query, conn)
    inv_df = pd.read_sql_query(inv_query, conn)

    # Get the total amount and invested amount
    total_amount = df.iloc[0, 0]
    invested_amount = inv_df.iloc[0]['Invested Amount']

    colour = "darkred"
    if(total_amount > invested_amount):
        colour = "darkgreen"
    # Create the Plotly bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[ 'Total Invested Amount','Total Account Amount'],
        y=[invested_amount, total_amount ],
        text=[f'${invested_amount:,.2f}',f'${total_amount:,.2f}'],
        textposition='auto',
        marker_color=['darkblue', colour]
    ))

    fig.update_layout(
        title='Account and Invested Amount',
        yaxis_title='Amount',
        showlegend=False
    )

    st.plotly_chart(fig)


def Average_Amount_Table():
    st.write("# Average Acount Amount")
    query = "SELECT strftime('%m-%Y', date) AS 'Month and Year', ROUND(AVG(amount), 2) AS 'Average Amount' FROM Data GROUP BY strftime('%m-%Y', date) ORDER BY date DESC;"
    df = pd.read_sql_query(query, conn)
    st.table(df)




def sidebar():
    #st.sidebar.write(""" # Account Value Form   """)
    st.sidebar.write(""" # Data Entry Form  """)
    date = st.sidebar.date_input("Date", datetime.date.today(),format="DD/MM/YYYY")
    amount = st.sidebar.number_input("Current Account Value",help="The Account value that you see in vanguard")
    #submit_button = st.button('Submit', type="secondary")
    # Insert data into the table
    
    #st.sidebar.write(""" # Investment Value Form   """)
    inv_amount = st.sidebar.number_input("Invested amount",help="What ever the amount you have invested on that date example $500 on 01/01/2024")
    #submit_button = st.button('Submit', type="secondary")
    # Insert data into the table
    if st.sidebar.button("Submit"):
        if(amount != 0):   
            cursor.execute("INSERT INTO Data (date,amount) VALUES (?,?)", (date,amount))
            conn.commit() 
            st.sidebar.success("Inserted the Acount Value Data")
        if(inv_amount != 0):
            cursor.execute("INSERT INTO Investment (date,InvestedAmount) VALUES (?,?)", (date,inv_amount))
            conn.commit() 
            st.sidebar.success("Inserted the Investment Amount Data")
            #We  add the investment amount the total account amount now if the current account value field is empty
            if(amount == 0):
                latestAmount = "SELECT amount FROM Data ORDER BY date DESC LIMIT 1;"
                df = pd.read_sql_query(latestAmount,conn)
                latest_amount = df.iloc[0, 0]+ inv_amount
                #latest_amount = latest_amount + inv_amount
                cursor.execute("INSERT INTO Data (date,amount) VALUES (?,?)", (date,latest_amount))
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
    st.write(" #### Raw Data")
    st.dataframe(df_styled,width=800,hide_index=True)

sidebar()
widget_section()
#streamlit_lineChart()
plotly_LineChart()
plotly_BarChart()
#Average_Amount_Table()
raw_table()


#Close the cursor and connection
cursor.close()
conn.close()