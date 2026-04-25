# ECON 5200 Final Project: SF Airbnb Causal Analysis

## Research Question
Does professional/commercial host status (operating >1 Airbnb listing) *cause* higher short-term rental occupancy in San Francisco — i.e., more housing removed from the long-term rental market?

## Method
Double Machine Learning (DML) — Chernozhukov et al. (2018)  
- Nuisance models: Gradient Boosting (primary) + Random Forest (robustness)  
- Standard errors: HC3 robust sandwich estimator  
- Cross-fitting: 5-fold

## Key Result
Professional host status **causes −13.5 occupancy days/year** (95% CI: [−17.3, −9.6], p < 0.001)  
Naive OLS: −39.5 days — overstated by ~26 days due to confounding

## Data
Inside Airbnb — San Francisco (December 2025 scrape)  
N = 7,535 listings across 37 neighborhoods

## Files
- `5200_final_sf_airbnb.ipynb` — Full analysis notebook
- `app.py` — Streamlit dashboard
- `listings.csv` — Source data (download from insideairbnb.com)
- `requirements.txt` — Python dependencies

## Reproduce
```bash
pip install -r requirements.txt
jupyter notebook 5200_final_sf_airbnb.ipynb
streamlit run app.py
```
