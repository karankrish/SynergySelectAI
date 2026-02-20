# SynergySelect AI

An intelligent Team-as-a-Service (TaaS) engine that dynamically builds high-performing, cost-optimized project teams from a pool of candidates by evaluating real-world KPI metrics.

The application leverages a scoring heuristic and greedy Knapsack optimization algorithms to balance experience requirements, strict budgets, and maximum workforce synergy without exceeding the client's cost constraints.

## Tech Stack

**Backend**
*   **Python 3.x**: Core scripting and data algorithms
*   **FastAPI**: High-performance REST API routing
*   **Pandas**: In-memory data manipulation and CSV ingestion
*   **Uvicorn**: ASGI server for running FastAPI

**Frontend**
*   **React (Vite ⚡)**: Lightning-fast development server and UI framework
*   **Lucide React**: Modern iconography
*   **Recharts**: SVG-based charting library for visualizing synergy and seniority data
*   **Vanilla CSS**: Premium dark-mode glassmorphism aesthetic styling without bulky CSS frameworks

## Core Concepts & Algorithms

### 1. Data Ingestion & Preprocessing
The backend parses the `Extended_Employee_Performance_and_Productivity_Data.csv` dataset into a structured Pandas DataFrame.
As data is ingested, candidates are assigned specific Roles based on their abstract titles:
*   **Manager**: `Manager`, `Director`
*   **Senior**: `Specialist`, `Analyst`
*   **Junior**: `Technician`, `Associate`

### 2. Synergy Scoring Engine
The application converts multidimensional candidate data into a unified, comparable score out of 100.
Metrics evaluated include:
*   **Financial Constraint (PCR)**: Performance-to-Cost Ratio (Performance divided by Salary)
*   **Productivity Metrics**: Delivery Speed, Overtime usage (penalized), CSAT (Customer Satisfaction)
*   **Experience Cap**: Juniors are weighted favorably to ensure pipeline growth, whereas Seniors are scored on strict deliverability.

### 3. Optimizer (Greedy Knapsack variant)
When a user requests a team of size $N$ for department $D$ with budget $B$:
1.  **Role Enforcement**: The app enforces a strict `1:2:3` ratio constraint (Managers : Seniors : Juniors) to ensure leadership coverage without top-heavy expenditures.
2.  **Initial Pool**: The algorithm selects the "best absolute" candidates in a vacuum that satisfy the role ratio, acting as the initial optimal, but likely over-budget, team.
3.  **Knapsack Budget Reduction**: If the initial optimal team sits above the allowed $B$ budget limit:
    *   The algorithm iterates over the currently selected team members, sorting them by their PCR (Performance-to-cost ratio).
    *   It identifies the candidate contributing the minimum relative value to the team (lowest PCR).
    *   It queries the unselected candidate pool for a structurally cheaper replacement that fulfills the same restricted Role bucket.
    *   The highest-synergy candidate out of the cheaper options is swapped in.
    *   This down-stepping recursively repeats until the overall team salary fits within the absolute budgetary limits, minimizing quality degradation while satisfying the financial constraint.

## Running Locally

### 1. Backend Server
Navigate to the root directory and start the Python environment:
```bash
# Optional: source your venv
source venv/bin/activate

# Install requirements if not present
pip install fastapi uvicorn pandas

# Run the backend locally
uvicorn backend.main:app --port 8000 --reload
```
The API will be available at `http://127.0.0.1:8000/api/v1/team/generate`

### 2. Frontend Development Server
Open a new terminal session, navigate to the `frontend` directory, and run the Vite server:
```bash
cd frontend

# Install Node modules if not present
npm install

# Start the dev server
npm run dev
```
The User Interface can be accessed locally via your browser (usually `http://localhost:5173`).

---

## API Structure

Requests to generate a team must be `POST` calls to `/api/v1/team/generate` containing the payload constraints:
```json
{
  "department": "Engineering",
  "team_size": 12,
  "total_budget": 100000.0
}
```

The server returns a structured schema indicating specific candidates chosen, their individual explainability reasoning, and overarching metrics for the dashboard to render (Avg Performance, Synergy Index, Remaining Budget, Education Mix).
