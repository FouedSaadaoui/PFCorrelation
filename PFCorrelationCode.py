import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np

# Try Google Colab import, if it fails, assume a local environment
try:
    from google.colab import files
    colab_env = True
except ImportError:
    colab_env = False

# File upload handling
if colab_env:
    print("Upload your file:")
    uploaded = files.upload()
    filename = list(uploaded.keys())[0]  # Get uploaded file name
else:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Hide main window
    filename = filedialog.askopenfilename(title="Select your data file", 
                                          filetypes=[("CSV files", "*.csv"),
                                                     ("Excel files", "*.xls;*.xlsx")])
    if not filename:
        sys.exit("No file selected. Exiting...")

# Determine file type and read data
if filename.endswith('.csv'):
    df = pd.read_csv(filename, na_values=['#N/A', 'NA', 'NaN', '?', ''], index_col=0)  # First column as index
elif filename.endswith(('.xls', '.xlsx')):
    df = pd.read_excel(filename, na_values=['#N/A', 'NA', 'NaN', '?', ''], index_col=0)
else:
    sys.exit("Unsupported file format. Please upload a CSV or Excel file.")

# Drop 'Dates' column if it exists
if 'Dates' in df.columns:
    df = df.drop(columns=['Dates'])

# Convert all columns (except index) to numeric
df = df.apply(pd.to_numeric, errors='coerce')

# Handle missing values (choose one method)
df = df.fillna(0)  # Replace NaN with 0
# df = df.fillna(df.mean())  # Uncomment to replace NaN with column mean
# df = df.dropna()  # Uncomment to remove rows with NaN

# Convert prices to returns (if the data contains prices)
# Calculate percentage returns and drop NaN values
df = df.pct_change().dropna()  
# Alternatively, use log returns:
# df = np.log(df / df.shift(1)).dropna() 

# Compute correlation matrix
corr_matrix = df.corr()

# Plot heatmap 
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=False, cmap='spring', linewidths=0.5)  # Set annot=False
plt.title('Correlation Matrix Heatmap')
plt.show()

# Display correlation matrix as a table
display(corr_matrix)  # Display the DataFrame
