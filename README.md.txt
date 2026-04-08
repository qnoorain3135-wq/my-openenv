# Budget Tracker OpenEnv

A real-world OpenEnv environment simulating monthly budget management.

## Environment Description
An AI agent manages a 1000-unit monthly budget over 30 days by allocating 
spending across food, transport, savings, and entertainment.

## Action Space
- `allocate_food` — spend on food
- `allocate_transport` — spend on transport  
- `allocate_savings` — move money to savings
- `allocate_entertainment` — spend on entertainment
- `skip` — do nothing this step

## Observation Space
| Field | Type | Description |
|-------|------|-------------|
| remaining_budget | float | Budget left |
| food_spent | float | Total food spending |
| transport_spent | float | Total transport spending |
| savings | float | Total saved |
| entertainment_spent | float | Entertainment spending |
| day | int | Current day (1-30) |
| month_target_savings | float | Target savings amount |

## Tasks
| ID | Difficulty | Goal |
|----|-----------|------|
| easy | Easy | Save ≥ 10% of budget |
| medium | Medium | Save ≥ 20%, food < 30% |
| hard | Hard | Save ≥ 30%, food < 25%, entertainment < 10% |

## Setup
```bash
pip install -r requirements.txt
export API_BASE_URL="your-api-endpoint"
export MODEL_NAME="your-model"
export HF_TOKEN="your-hf-token"
python inference.py
```

## Reward
Scores range from 0.0–1.0 based on savings ratio, food discipline, and remaining budget.