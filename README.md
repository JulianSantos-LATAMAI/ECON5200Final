# ECON 5200: Consulting Report — Final Project
## Do Commercial Airbnb Operators Extract More Housing from San Francisco's Rental Market?
## Julián Santos Vasquez
**Northeastern University | Spring 2026**

---

## Overview

This project estimates the causal effect of professional/commercial host status on short-term rental (STR) occupancy in San Francisco using a Double Machine Learning (DML) identification strategy with Gradient Boosting nuisance models.

Data comes from Inside Airbnb's San Francisco scrape (December 2025), which provides listing-level data on occupancy, host characteristics, property type, and neighborhood for 7,535 active listings. Occupancy is measured as estimated days booked in the past year (0–255).

---

## Causal Question

Does operating multiple Airbnb listings (professional/commercial host status) cause higher short-term rental occupancy — i.e., more housing removed from San Francisco's long-term rental market?

---

## Identification Strategy

**Method:** Double Machine Learning (DML) — Chernozhukov et al. (2018)

- **Treatment:** `is_professional_host` — 1 if host operates more than 1 listing on the platform
- **Outcome:** `estimated_occupancy_l365d` — estimated days occupied in the past year
- **Nuisance models:** Gradient Boosting (primary), Random Forest (robustness check)
- **Standard errors:** HC3 robust sandwich estimator
- **Cross-fitting:** 5-fold

**Controls / confounders (W):**
* Room type (entire home vs. private/shared room)
* Accommodates (number of guests)
* Minimum nights
* Number of reviews
* Availability (days listed per year)
* Superhost status
* Instant book enabled
* Neighborhood fixed effects (37 SF neighborhoods)

**Key assumption:** Conditional independence — after controlling for observed listing characteristics and neighborhood, whether a host operates multiple listings is independent of unobserved determinants of occupancy.

---

## Data

* **Source:** Inside Airbnb — San Francisco
* **URL:** https://insideairbnb.com/get-the-data/
* **Scrape date:** December 2025
* **N:** 7,535 listings across 37 neighborhoods
* **Outcome:** `estimated_occupancy_l365d` — days occupied in past year
* **Treatment:** `is_professional_host` — binary (>1 listing on platform)

---

## Results

| Model | Estimate | 95% CI |
|---|---|---|
| Naive OLS | −39.5 days/year | [−44.1, −34.9] |
| DML (GBM nuisance) | −13.5 days/year | [−17.3, −9.6] |
| DML Robust (RF nuisance) | −13.1 days/year | [−17.2, −9.0] |

The naive estimate is heavily confounded — professional hosts concentrate in hotel-heavy tourist corridors with mechanically lower occupancy. After partialling out confounders with DML, the causal estimate shrinks to −13.5 days/year (p < 0.001), stable across both nuisance model specifications. This suggests enforcement focus should shift toward entire-home amateur listings, which drive higher sustained occupancy.

---

## Repository Structure

```
econ5200-final/
├── 5200_final_sf_airbnb.ipynb   # Main analysis notebook
├── listings.csv.gz               # Raw data (Inside Airbnb SF, Dec 2025)
├── app.py                        # Streamlit dashboard
├── requirements.txt              # Python dependencies
└── README.md
```

---

## How to Reproduce

```bash
git clone https://github.com/yourusername/econ5200-final
cd econ5200-final
pip install -r requirements.txt
jupyter notebook 5200_final_sf_airbnb.ipynb
```

---

## Deliverables

* Checkpoint notebook + proposal
* Streamlit dashboard (deployed) 
* Executive Summary  
* Technical Report 
* Threats to Identification 
* AI Methodology Appendix 

---

## Tools & Libraries

* Python 3.13
* pandas, numpy, matplotlib, seaborn
* scikit-learn (DML nuisance models, cross-validation)
* scipy (HC3 robust standard errors)
* streamlit, plotly (dashboard)

---

## AI Methodology

This project uses AI-augmented methodology documented via the P.R.I.M.E. framework (Prompt → Response → Iterate → Modify → Evaluate). All AI interactions are documented in the AI Methodology Appendix included in the final submission. All outputs were verified by the author.

---

*ECON 5200 — Causal Machine Learning & Applied Analytics — Northeastern University — Spring 2026*
