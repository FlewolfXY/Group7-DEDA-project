import pandas as pd
import os

# Load the CSV file while handling embedded null characters
try:
    with open("C:\\Users\ThinkPad\Desktop\digital pj\000.csv", 'r', encoding='utf-8', errors='replace') as file:
        df = pd.read_csv(file, sep=',', error_bad_lines=False, warn_bad_lines=True)
except ValueError:
    print("Failed to read the file. Please ensure it doesn't contain embedded null characters.")

# Ensure column names are stripped of any leading/trailing whitespace
df.columns = df.columns.str.strip()

# Check if the correct column for location exists ('City' and 'State Abbr' combined)
if 'City' in df.columns and 'State Abbr' in df.columns:
    # Drop rows where 'City' contains country-level data or is not specific
    df = df[~df['City'].str.contains('United States|Canada', case=False, na=False)]

    # Drop rows where 'State Abbr' is not valid (e.g., missing or non-standard values)
    valid_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    df = df[df['State Abbr'].isin(valid_states)]

    # Agglomerate the data by 'State Abbr' column, summing the 'Count'
    agglom_df = df.groupby('State Abbr', as_index=False)['Count'].sum()

    # Save the modified DataFrame to a new CSV file on the desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    output_file_path = os.path.join(desktop_path, 'agglomerated_job_posts.csv')
    agglom_df.to_csv(output_file_path, index=False)

    print(f"The agglomerated CSV file has been saved to: {output_file_path}")
else:
    print("The required columns ('City' and 'State Abbr') were not found in the CSV file.")