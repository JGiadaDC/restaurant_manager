# Expense & Income Management App

A web application built with **Streamlit**, designed to help users manage and track their expenses and incomes. Users can input their data, view their expenses and incomes, and visualize charts to track financial performance.

## Features

- **Add Expenses**: Record various types of expenses with details such as date, category, supplier, and amount.
- **Add Incomes**: Log incomes through cash and POS transactions.
- **View Data**: View and filter expenses and incomes by date range and supplier.
- **Charts**: Visualize financial performance with charts such as pie charts for expenses by category and line charts for daily profits.

## Requirements

Make sure you have the following libraries installed:

- Python 3.x
- Streamlit
- Pandas
- Openpyxl
- Plotly

You can install them using pip:

```bash
pip install streamlit pandas openpyxl plotly
```

## restaurant_manager/ │ ├── app.py # Main application file ├── database_fornitori.xlsx # Excel file where data is saved ├── requirements.txt # List of dependencies ├── .git/ # Git version control directory └── venv/ # Virtual environment directory

## How to Use

1. **Run the app**:

   ```bash
   streamlit run app.py

2. **Add Expenses**: Select the "Ingresar Gasto" option to input expense data.

3. **Add Incomes**: Use the "Ingresar Ingreso" section to log income data.

4. **View Data**: View your logged expenses and incomes, filtered by date and supplier.

5. **Charts**: Check the "Análisis & Gráficos" section to view charts and track financial trends.

## Data Storage

Data is saved in an Excel file (`database_fornitori.xlsx`). The app loads and saves expenses and incomes to this file.

## Troubleshooting

- **KeyError: "There is no item named '[Content_Types].xml' in the archive"**:  
  This error occurs if the Excel file is corrupted. Try re-saving the file in Excel, or ensure the file is a valid `.xlsx` format.

- **File Not Found**:  
  Ensure the `database_fornitori.xlsx` file is in the correct directory or re-create it as necessary.


## Author
This project was developed by Giada De . You can contact me at giada.decarlo@gmail.com

