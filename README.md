# Investment Dashboard

This Streamlit app provides an investment dashboard to track account values, investment amounts, and visualize account trends.

## Overview

The app is built using Python and Streamlit, with data stored in a SQLite database. It allows users to input account values and investment amounts, and then provides various metrics, visualizations, and raw data for analysis.

## Data Storage

The app connects to a SQLite database named 'Finance.db' and creates two tables: 'Data' for account values and 'Investment' for investment amounts. The tables are structured with date and amount columns to store the relevant data.

## Widgets and Metrics

The app includes a sidebar for data entry and displays the following metrics:
- Total Invested Amount
- Current Account Holding
- Current Profit/Loss

## Visualizations

The app provides the following visualizations:
- Account Trend Line Chart
- Account Trend Line Chart with Investment Amount
- Raw Data Table

## Dependencies

The app relies on the following Python libraries:
- streamlit
- datetime
- sqlite3
- pandas
- plotly.express

These dependencies can be installed using the following command:
```bash
pip install streamlit pandas plotly 
```

## How to Use

To use the app, follow these steps:
1. Run the provided Python code. Run the `main.py` file using Streamlit: ``` python3 -m streamlit run main.py ```
2. Input account values and investment amounts in the sidebar.
3. View the metrics and visualizations to analyze account trends and investment performance.




## Closing

This Streamlit app offers a convenient way to track and visualize investment data, making it easier to monitor account values and investment performance over time.

For any questions or feedback, please feel free to reach out.

