import pandas as pd
from typing import List, Dict

def run_optimizer(department: str, team_size: int, total_budget: float) -> Dict:
    from .data_loader import employee_df
    from .scoring import compute_synergy_scores

    # Step 1: Filter & Score
    df = employee_df[employee_df['Department'] == department]
    if df.empty:
        raise ValueError(f"No employees found for department: {department}")
        
    df = compute_synergy_scores(df)

    # Step 2: Role Allocation (1:2:3 ratio)
    mgr_count = max(1, round(team_size * (1/6)))
    sen_count = max(1, round(team_size * (2/6)))
    jun_count = team_size - mgr_count - sen_count

    # Check capacity
    mgr_df = df[df['Role'] == 'Manager'].sort_values('SynergyScore', ascending=False)
    sen_df = df[df['Role'] == 'Senior'].sort_values('SynergyScore', ascending=False)
    jun_df = df[df['Role'] == 'Junior'].sort_values('PCR', ascending=False)  # PRD specifies filling Junior slots by PCR

    if len(mgr_df) < mgr_count or len(sen_df) < sen_count or len(jun_df) < jun_count:
        raise ValueError(f"Not enough employees in {department} to fulfill {mgr_count} Managers, {sen_count} Seniors, {jun_count} Juniors.")

    # Convert to lists of dicts for easier manipulation
    managers = mgr_df.to_dict('records')
    seniors = sen_df.to_dict('records')
    juniors = jun_df.to_dict('records')

    # Initial Selection
    selected = managers[:mgr_count] + seniors[:sen_count] + juniors[:jun_count]
    
    # Store availability
    avail_mgr = managers[mgr_count:]
    avail_sen = seniors[sen_count:]
    avail_jun = juniors[jun_count:]
    available = {'Manager': avail_mgr, 'Senior': avail_sen, 'Junior': avail_jun}

    def current_cost(team):
        return sum(e['Monthly_Salary'] for e in team)

    # Step 4: Budget Constraints (Greedy-Knapsack Swap)
    while current_cost(selected) > total_budget:
        # Find candidate to swap out: the one with lowest PCR
        # Sort current team by PCR ascending
        selected.sort(key=lambda x: x['PCR'])
        
        swapped = False
        for candidate in selected:
            role = candidate['Role']
            cand_salary = candidate['Monthly_Salary']
            # Find cheaper available candidate for the same role
            cheaper_options = [c for c in available[role] if c['Monthly_Salary'] < cand_salary]
            if cheaper_options:
                # Pick the one with the best SynergyScore among cheaper options to drop minimal quality
                best_cheaper = max(cheaper_options, key=lambda x: x['SynergyScore'])
                selected.remove(candidate)
                selected.append(best_cheaper)
                available[role].remove(best_cheaper)
                available[role].append(candidate)
                swapped = True
                break
                
        if not swapped:
            # Cannot reduce cost further within role constraints
            raise ValueError(f"Unable to form a team within the budget of {total_budget}. Minimum required cost is {current_cost(selected)}.")

    # Step 5: Diversity Rebalancing
    def check_diversity(team):
        genders = [e['Gender'] for e in team]
        total = len(genders)
        if total == 0: return False, None, None
        counts = {g: genders.count(g) for g in set(genders)}
        for g, count in counts.items():
            if count / total > 0.70:
                return True, g, count/total # Needs rebalance, majority gender
        return False, None, None

    needs_rebalance, majority_gender, _ = check_diversity(selected)
    while needs_rebalance:
        # Sort majority members in team by SynergyScore ascending (lowest first)
        majority_members = sorted([e for e in selected if e['Gender'] == majority_gender], key=lambda x: x['SynergyScore'])
        
        swapped = False
        for cand in majority_members:
            role = cand['Role']
            # Find minority candidates in available pool for same role
            minority_options = [c for c in available[role] if c['Gender'] != majority_gender]
            # Ensure budget stringency
            budget_slack = total_budget - current_cost(selected)
            valid_options = [c for c in minority_options if c['Monthly_Salary'] - cand['Monthly_Salary'] <= budget_slack]
            
            if valid_options:
                best_minority = max(valid_options, key=lambda x: x['SynergyScore'])
                selected.remove(cand)
                selected.append(best_minority)
                available[role].remove(best_minority)
                available[role].append(cand)
                swapped = True
                break
                
        if not swapped:
            break # Can't rebalance further
        needs_rebalance, majority_gender, _ = check_diversity(selected)

    # Prepare Output
    total_team_cost = current_cost(selected)
    
    genders = [e['Gender'] for e in selected]
    counts = {g: genders.count(g) for g in set(genders)}
    gender_ratios = {g: round(c / len(genders) * 100, 1) for g, c in counts.items()}
    
    educations = list(set([e['Education_Level'] for e in selected]))
    
    avg_performance = sum(e['Performance_Score'] for e in selected) / len(selected)
    synergy_index = sum(e['SynergyScore'] for e in selected) * 100  # Scaling up to 100 base if it was small, wait let's just do sum or avg. Let's do (avg_synergy * 100)
    avg_score = sum(e['SynergyScore'] for e in selected) / len(selected)
    synergy_index = min(100.0, avg_score * 100) # Ensure it looks like an index out of 100
    
    team_list = []
    for e in selected:
        team_list.append({
            "Employee_ID": e['Employee_ID'],
            "Role": e['Role'],
            "Job_Title": e['Job_Title'],
            "Salary": e['Monthly_Salary'],
            "SynergyScore": round(e['SynergyScore'] * 100, 2),
            "Explainability": f"Selected for {e['Role']} role. High synergy index based on performance vs cost and alignment."
        })

    return {
        "Team_List": sum(1 for e in selected),  # We'll just return lengths or full object
        "Candidates": team_list,
        "Total_Cost": total_team_cost,
        "Budget_Remaining": total_budget - total_team_cost,
        "Gender_Ratio": gender_ratios,
        "Education_Mix": educations,
        "Avg_Performance": round(avg_performance, 2),
        "Synergy_Index": round(synergy_index, 2)
    }

def generate_team(department: str, team_size: int, total_budget: float) -> Dict:
    return run_optimizer(department, team_size, total_budget)
