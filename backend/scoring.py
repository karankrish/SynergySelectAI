import pandas as pd
import numpy as np

def compute_synergy_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes the SynergyScore for a filtered dataframe of eligible employees.
    """
    df = df.copy()
    
    # -- 7.2 Financial Efficiency --
    # FinancialScore = 0.7(PCR) + 0.3(CostEfficiencyRank)
    df['FinancialScore'] = 0.7 * df['PCR'] + 0.3 * df['CostEfficiencyRank']
    
    # -- 7.3 Productivity & Reliability --
    # ProductivityScore = 0.4(Velocity_Norm) + 0.3(Reliability) + 0.3(Capacity)
    # We should normalize velocity to 0-1 to blend well
    v_min, v_max = df['Velocity'].min(), df['Velocity'].max()
    if v_max > v_min:
        df['Velocity_Norm'] = (df['Velocity'] - v_min) / (v_max - v_min)
    else:
        df['Velocity_Norm'] = 1.0

    df['ProductivityScore'] = 0.4 * df['Velocity_Norm'] + 0.3 * df['Reliability'] + 0.3 * df['Capacity']

    # -- 7.4 Experience & Growth --
    # GrowthScore = 0.6(TrainingHoursNormalized) + 0.4(Promotions_Norm)
    t_min, t_max = df['Training_Hours'].min(), df['Training_Hours'].max()
    df['Training_Norm'] = (df['Training_Hours'] - t_min) / (t_max - t_min + 1e-9)

    p_min, p_max = df['Promotions'].min(), df['Promotions'].max()
    df['Promotions_Norm'] = (df['Promotions'] - p_min) / (p_max - p_min + 1e-9)

    df['GrowthScore'] = 0.6 * df['Training_Norm'] + 0.4 * df['Promotions_Norm']

    # ExperienceScore is weighted higher for juniors? 
    # Let's assign an ExperienceScore based on GrowthScore.
    def adjust_exp(row):
        if row['Role'] == 'Junior':
            return row['GrowthScore'] * 1.5  # Boost junior growth
        return row['GrowthScore']
    df['ExperienceScore'] = df.apply(adjust_exp, axis=1)

    # -- 7.5 Diversity & Inclusion --
    # Baseline diversity score is neutral and rebalanced later.
    df['DiversityScore'] = 0.5 

    # Overall SynergyScore
    # We can use static weights. w1=0.4, w2=0.3, w3=0.2, w4=0.1
    df['SynergyScore'] = (
        0.4 * df['FinancialScore'] +
        0.3 * df['ProductivityScore'] +
        0.2 * df['ExperienceScore'] +
        0.1 * df['DiversityScore']
    )
    
    return df
