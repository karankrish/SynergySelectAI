# SynergySelect AI – Intelligent Team-as-a-Service Engine
### Product Requirements Document (PRD)

---

## 1. Product Overview

| Field | Details |
|---|---|
| **Product Name** | SynergySelect AI |
| **Product Type** | AI-driven Team Optimization Engine |
| **Primary Users** | HR Leaders, Delivery Managers, PMOs, Department Heads |
| **Deployment** | Internal Enterprise Web App + API Layer |

### Vision
Enable organizations to automatically generate high-performing, cost-efficient, and diverse project teams in seconds using AI-driven optimization.

### Mission
Transform manual team formation into a data-driven, explainable, and scalable decision system.

---

## 2. Problem Statement

Team formation today is manual and biased, based on limited visibility, budget-inefficient, weak on diversity optimization, and poorly optimized for performance.

Managers struggle to balance budget constraints, performance expectations, burnout risks, seniority mix, and gender & education diversity.

**SynergySelect AI** solves this by creating an optimized team composition using algorithmic scoring and constrained optimization.

---

## 3. Target Users

| Persona | Needs | Pain Points |
|---|---|---|
| Delivery Manager | Fast team creation | Budget overshoot |
| HR Business Partner | Diversity compliance | Bias risk |
| PMO | Predictable execution | Unbalanced team mix |
| CTO / Director | Performance ROI | Lack of data-backed decisions |

---

## 4. MVP Scope

### User Inputs
- Department
- Team Size
- Total Budget

### System Output
- List of selected employees
- Seniority breakdown (1:2:3 ratio)
- Total cost
- KPI score breakdown
- Diversity metrics
- Explanation of selection logic

---

## 5. Success Metrics (KPIs)

### Business KPIs
- 30% reduction in manual team planning time
- 15% improvement in Performance-to-Cost Ratio
- 20% increase in diversity balance compliance
- 10% reduction in burnout-risk team formation

### Technical KPIs
- Team generation < 3 seconds
- Budget adherence ≥ 99%
- Selection explainability coverage: 100%

---

## 6. Functional Requirements

### 6.1 Data Inputs – Required Employee Fields

| Field | Type | Required |
|---|---|---|
| Employee_ID | String | Yes |
| Department | String | Yes |
| Job_Title | Enum (Manager / Senior / Junior) | Yes |
| Monthly_Salary | Float | Yes |
| Perf_Score | Float (1–5) | Yes |
| Projects_Handled | Integer | Yes |
| Years_At_Company | Float | Yes |
| Work_Hours_Per_Week | Integer | Yes |
| Overtime_Hours | Integer | Yes |
| Absence_Days | Integer | Yes |
| Training_Hours | Integer | Yes |
| Promotions | Integer | Yes |
| Gender | Enum | Yes |
| Education_Level | Enum | Yes |
| Resigned | Boolean | Yes |

---

## 7. Scoring Framework

### 7.1 Core Formula – Synergy Score

```
SynergyScore = w1(FinancialScore) + w2(ProductivityScore) + w3(ExperienceScore) + w4(DiversityScore)
```

---

### 7.2 Financial Efficiency

**Performance-to-Cost Ratio (PCR)**
```
PCR = PerfScore / MonthlySalary
```
*Normalized across department.*

**Financial Score**
```
FinancialScore = 0.7(PCR) + 0.3(CostEfficiencyRank)
```

---

### 7.3 Productivity & Reliability

**Historical Velocity**
```
Velocity = ProjectsHandled / YearsAtCompany
```

**Reliability Index**
```
Reliability = 1 / (1 + AbsenceDays)
```

**Capacity Score**
```
Capacity = f(WorkHours, Overtime)
```
> ⚠️ Overtime > 20 hrs/month reduces score (burnout penalty).

**Productivity Score**
```
ProductivityScore = 0.4(Velocity) + 0.3(Reliability) + 0.3(Capacity)
```

---

### 7.4 Experience & Growth

**Growth Score**
```
GrowthScore = 0.6(TrainingHoursNormalized) + 0.4(Promotions)
```
> ExperienceScore is weighted higher for juniors.

---

### 7.5 Diversity & Inclusion

**Gender Balance Contribution** — Rewards minority representation.

**Educational Breadth** — Score increases when team includes a mix of Bachelor, Master, and PhD holders.

> DiversityScore is adjusted during final team composition.

---

## 8. Algorithm Flow

### Step 1: Data Ingestion
- Load dataset
- Filter by: `Department = Input` and `Resigned = False`

### Step 2: Role Allocation

Using a **1:2:3 (Manager:Senior:Junior)** ratio:

| Team Size | Managers | Seniors | Juniors |
|---|---|---|---|
| 6 | 1 | 2 | 3 |
| 12 | 2 | 4 | 6 |
| Custom | Rounded proportionally | | |

### Step 3: Candidate Scoring
- Compute SynergyScore for all eligible employees
- Rank within Job_Title

### Step 4: Optimization Engine

**4.1 Constraint Optimization**

Constraints enforced:
- `Salary ≤ Budget`
- Role quota satisfied

**4.2 Greedy-Knapsack Hybrid**
1. Pick top Manager
2. Fill Senior slots by highest score
3. Fill Junior slots by highest PCR
4. Ensure budget feasibility
5. If budget overflow → replace lowest PCR candidate

### Step 5: Diversity Rebalancing
- If Gender ratio exceeds **70/30**:
  - Identify lowest scoring majority candidate
  - Swap with highest minority candidate within budget

### Step 6: Output Generation

```json
{
  "Team_List": ["..."],
  "Total_Cost": 54500,
  "Budget_Remaining": 4500,
  "Gender_Ratio": "60:40",
  "Education_Mix": ["Bachelor", "Master", "PhD"],
  "Avg_Performance": 4.3,
  "Synergy_Index": 87.4
}
```

---

## 9. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | < 3 sec response |
| Scalability | 50,000+ employees |
| Security | Role-based access control |
| Explainability | Score breakdown per employee |
| Auditability | Decision logs stored |

---

## 10. Architecture Overview

```
Frontend UI (React)
       ↓
API Layer (FastAPI)
       ↓
Scoring Engine
       ↓
Optimization Engine
       ↓
Database (Employee Data)
```

---

## 11. Explainability Layer

Each employee selection will surface:
- Synergy Score breakdown
- Reason selected
- Reason not selected (for rejected candidates)
- Budget impact

This ensures enterprise trust and compliance.

---

## 12. Risks & Mitigation

| Risk | Mitigation |
|---|---|
| Bias amplification | Fairness constraints |
| Salary inflation | Budget hard cap |
| Burnout | Overtime penalty in scoring |
| Gaming the system | 2% randomization factor |

---

## 13. Future Enhancements (Phase 2)

- Skill matching using NLP embeddings
- Personality compatibility modeling
- Graph-based collaboration scoring
- ML model replacing static weights
- Project type specialization
- Reinforcement learning feedback loop

---

## 14. Competitive Advantage

| Traditional Planning | SynergySelect AI |
|---|---|
| Manual | Automated |
| Biased | Data-driven |
| Slow | Instant |
| Cost unaware | Budget optimized |
| Low transparency | Fully explainable |

---

## 15. Implementation Roadmap

### Phase 1 – MVP *(6 Weeks)*
- Data ingestion
- Scoring model
- Greedy optimizer
- Basic UI

### Phase 2 – Advanced Optimization *(8 Weeks)*
- True knapsack solver
- Diversity constraint solver
- Simulation dashboard

### Phase 3 – Enterprise AI Layer
- ML-based dynamic weights
- Predictive project success model

---

## 16. Acceptance Criteria

- ✅ Team respects 1:2:3 seniority ratio
- ✅ Budget never exceeded
- ✅ Gender skew corrected
- ✅ Scores are reproducible
- ✅ API response under SLA (< 3 seconds)
