# Week 5 — Telco Customer Churn Analysis

## Overview
This week I moved from SQL fundamentals into a full end-to-end analytics project: a customer churn analysis on a telco dataset of 7,043 customers. The goal was to practice the complete analyst workflow — not just writing queries, but taking a business question all the way through to a report, a presentation, and shareable content.

## What I did
I followed a structured 5-step process:

1. **Defined the problem** — which customer segments, contract terms, and services are most associated with churn, and what can the business do about it.
2. **Explored the data** — checked shape, types, and missing values in pandas; confirmed a clean dataset (0 nulls across all 21 columns) after fixing `TotalCharges`, which was stored as text.
3. **Found key drivers** — computed churn rate (not just raw counts) across every categorical column using pandas `groupby`, then rebuilt the same breakdowns as DAX measures in Power BI (`DIVIDE(churned, total)`).
4. **Turned findings into insights** — translated the numbers into plain-English "so what" statements a non-technical manager could act on.
5. **Made recommendations** — 5 concrete, prioritized actions tied directly to the findings.

## Deliverables produced
- **Report** (Word doc, 3 pages): Intro → Problem → Dataset → Analysis Process → Findings → Insights → Recommendations → Conclusion
- **Presentation** (8 slides): condensed, visual-first version with native Power BI-style charts, built for a stakeholder audience
- **LinkedIn post + X thread**: public-facing summary of the findings, tagged with #AnalystLabAfrica

## Key findings
- Overall churn rate: 27% (1,869 of 7,043 customers)
- Contract type is the single biggest driver — month-to-month customers churn at 43% vs. 3% for two-year contracts (a 14x gap)
- Churn is concentrated in the first 12 months of tenure (48% churn) and drops sharply after that
- Fiber optic customers churn more than DSL customers, despite fiber being the premium product
- Electronic check payers churn nearly 3x more than customers on automatic payment methods
- $2.86M of $16.06M total revenue is tied to customers who have already churned (~18%)

## Tools used
Python (pandas) for cleaning and exploration, Power BI (DAX measures, custom theme/color palette) for the dashboard, and Word/PowerPoint for the written and visual deliverables.

## What I learned
- Churn *rate* (a DAX/groupby ratio) tells a completely different story than raw churn *counts* — this was the most important technical lesson of the week.
- Going from "chart" to "insight" to "recommendation" is a distinct skill from the analysis itself — a manager doesn't want the chart, they want the sentence the chart implies.
- Cross-tabulating two variables (e.g. Contract × PaymentMethod) surfaced a compounded high-risk segment that no single-variable chart would have shown.

## Next steps
Apply this same 5-step workflow to a new dataset, and start incorporating SQL window functions from Week 3 into the "find key drivers" step instead of relying solely on pandas/DAX.