import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = r'C:\Users\Lenovo\Desktop\gsearch_jobs.xlsx'
df = pd.read_excel(file_path)

# Convert the 'date_time' column to datetime format
df['posting_time'] = pd.to_datetime(df['date_time'], errors='coerce')

# Filter out rows with missing posting time
df = df.dropna(subset=['posting_time'])

# Filter the data to include only postings from 2022 onwards
df = df[df['posting_time'] >= '2022-01-01']

# Extract month and year from the posting time
df['month_year'] = df['posting_time'].dt.to_period('M')

# Ensure 'work_from_home' is numeric (converting from strings if needed)
df['work_from_home'] = pd.to_numeric(df['work_from_home'], errors='coerce').fillna(0)

# Group by month and calculate the percentage of work-from-home jobs
monthly_data = df.groupby('month_year').agg(
    total_jobs=('work_from_home', 'size'),
    work_from_home_jobs=('work_from_home', 'sum')
)

# Calculate the percentage
monthly_data['work_from_home_percentage'] = (monthly_data['work_from_home_jobs'] / monthly_data['total_jobs']) * 100

# Plot the percentage of work-from-home jobs by month
plt.figure(figsize=(10, 6))
monthly_data['work_from_home_percentage'].plot(kind='line', marker='o', color='b')
plt.title('Percentage of Jobs Allowing Work from Home by Month (2022 Onwards)')
plt.xlabel('Month')
plt.ylabel('Percentage of Work from Home Jobs (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
