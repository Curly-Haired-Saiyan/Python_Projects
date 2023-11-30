import pandas as pd
import yfinance as yf
import datetime as dt
import tkinter as tk
from tkinter import messagebox, filedialog

def GetStockData(symbol, start_date, end_date, save_path):
    data = yf.download(symbol, start=start_date, end=end_date)
    file_path = f"{save_path}/{symbol}.csv"
    data.to_csv(file_path)
    print(f"Data for {symbol} is saved at {file_path}.")
    return data.head(10)
    
def SaveStockData(symbols, start_date, end_date, save_path):
    stock_data_display.delete(1.0, tk.END)
    for symbol in symbols:
        data = GetStockData(symbol, start_date, end_date, save_path)
        stock_data_display.insert(tk.END, f"Data for {symbol}: \n")
        stock_data_display.insert(tk.END, data.to_string(index=False) + "\n\n")
        
def RetrieveInput():
    symbol_input = symbol_entry.get()
    symbols = [symbol.strip() for symbol in symbol_input.split(",")]
    
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    
    try:
        start_date = dt.datetime.strptime(start_date, "%m/%d/%Y")
        end_date = dt.datetime.strptime(end_date, "%m/%d/%Y")
        if start_date > end_date:
            messagebox.showerror("Error", "End date mut be after start date")
        else:
            save_path =  filedialog.askdirectory()
            if save_path:
                SaveStockData(symbols, start_date, end_date, save_path)
                messagebox.showinfo("Success", "Stock data downloaded succesfully.")
            else:
                messagebox.showwarning("Warning", "No Directory selected. Please select a directory")
    except ValueError:
        messagebox.showerror("Error", "Please enter dates n MM/DD/YYYY format.")

if __name__ == "__main__":
    # GUI window
    root = tk.Tk()
    root.title("Stock Data Downloader")

    # Symbol input field
    symbol_label = tk.Label(root, text="Enter Stock symbol(s) seperated by a comma")
    symbol_label.pack()
    symbol_entry = tk.Entry(root)
    symbol_entry.pack()

    # Date range selection
    start_date_label = tk.Label(root, text="Start date (MM/DD/YYYY):")
    start_date_label.pack()
    start_date_var = tk.StringVar()
    start_date_entry = tk.Entry(root, textvariable=start_date_var)
    start_date_entry.pack()

    end_date_label = tk.Label(root, text="End Date (MM/DD/YYYY):")
    end_date_label.pack()
    end_date_var = tk.StringVar()
    end_date_entry = tk.Entry(root, textvariable=end_date_var)
    end_date_entry.pack()

    # Button to trigger data retrieval
    retrieve_button = tk.Button(root, text="Download Stock Data", command=RetrieveInput)
    retrieve_button.pack()
    
    # display area for stock data
    stock_data_label = tk.Label(root, text="Stock Data Preview")
    stock_data_label.pack()
    stock_data_display = tk.Text(root, height=15, width = 60)
    stock_data_display.pack()

    root.mainloop()