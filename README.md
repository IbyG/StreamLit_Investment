# Investment App

This is a Streamlit web application for managing investments. Users can input their investment amounts and view various metrics and visualizations.

## Features

- **Current Date:** Users can select the current date for their investment input.
- **Insert Amount:** Users can input their investment amount.
- **Submit Button:** Users can submit their investment data.

The application stores investment data in a SQLite database named `Finance.db`. It creates a table named `Data` to store investment records with columns for `id`, `date`, and `amount`.

### Metrics

The application displays the following metrics:

- **Current Account Holding:** Shows the latest investment amount and the difference from the previous investment.

### Visualisations

- **Monthly Average:** Displays a line chart showing the monthly average investment amount over time.

## Getting Started

To run the application locally:

1. Clone this repository to your local machine.
2. Run the `main.py` file using Streamlit: ``` python3 -m streamlit run main.py ```

## Dependencies

- Streamlit
- SQLite
- Pandas
- Datetime

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
