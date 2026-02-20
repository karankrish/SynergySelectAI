import pandas as pd
import os
import numpy as np

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'Extended_Employee_Performance_and_Productivity_Data.csv')

def load_and_preprocess_data() -> pd.DataFrame:
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Data file not found at {DATA_FILE}")

    # Load dataset
    df = pd.read_csv(DATA_FILE)

    # Filter out resigned employees
    if 'Resigned' in df.columns: # Sometimes it's string 'True'/'False'
        df = df[df['Resigned'] == False]

    # Map Job_Title to Roles (Manager, Senior, Junior)
    role_mapping = {
        'Manager': 'Manager',
        'Consultant': 'Senior',
        'Engineer': 'Senior',
        'Specialist': 'Senior',
        'Developer': 'Junior',
        'Analyst': 'Junior',
        'Technician': 'Junior'
    }
    df['Role'] = df['Job_Title'].map(role_mapping).fillna('Junior')

    # Base calculations
    df['PCR_Raw'] = df['Performance_Score'] / df['Monthly_Salary']
    
    # Normalize PCR per Department
    # PCR = (x - min) / (max - min) but to avoid 0 we can do max scaling or min-max
    df['PCR'] = df.groupby('Department')['PCR_Raw'].transform(lambda x: (x - x.min()) / (x.max() - x.min() + 1e-9))
    
    # Velocity: Handle division by zero
    df['Velocity'] = df.apply(lambda row: row['Projects_Handled'] / row['Years_At_Company'] if row['Years_At_Company'] > 0 else row['Projects_Handled'], axis=1)
    
    # Reliability
    df['Reliability'] = 1 / (1 + df['Sick_Days'])
    
    # Capacity: Penalty for > 20 overtime hours
    def calc_capacity(row):
        base_cap = row['Work_Hours_Per_Week'] / 40.0
        ot_penalty = max(0, row['Overtime_Hours'] - 20) * 0.05
        return max(0, base_cap - ot_penalty)
    
    df['Capacity'] = df.apply(calc_capacity, axis=1)

    # CostEfficiencyRank within department (higher is better, meaning lower salary or higher PCR)
    # Let's rank by PCR for cost efficiency
    df['CostEfficiencyRank'] = df.groupby('Department')['PCR'].rank(pct=True)

    return df

# Initialize data on import so it stays in memory
employee_df = load_and_preprocess_data()
