# Data Strategy

## 1. Categories

Define 4–6 IT categories:

- Network Issue
- Access / Permissions
- Deployment Failure
- Monitoring / Alert
- Database Issue
- Infrastructure Issue

## 2. Urgency Levels

- Low
- Medium
- High

## 3. Dataset Strategy

Hybrid approach:

- Start from small realistic examples
- Expand synthetically via LLM if needed
- Balance classes if required

Target size: 1000 records

Each record should include:

{
  "ticket_text": "...",
  "category": "...",
  "urgency": "..."
}

## 4. Preprocessing Rules

- Lowercase
- Remove special characters
- Remove extra spaces
- Optional stopword removal