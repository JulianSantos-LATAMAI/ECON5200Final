import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SF Airbnb Causal Dashboard", layout="wide")
st.title("SF Airbnb: Causal Effect of Professional Host Status on STR Occupancy")
st.markdown("**ECON 5200 Final Project** — Double Machine Learning estimates")

# Sidebar
st.sidebar.header("What-If Scenarios")
multiplier = st.sidebar.slider("Treatment intensity multiplier", 0.5, 3.0, 1.0, 0.1)
alpha = st.sidebar.slider("Significance level (α)", 0.01, 0.10, 0.05, 0.01)

# Base estimates from DML
BASE_ATE = -13.458
BASE_SE  = 1.975

z = {0.01: 2.576, 0.05: 1.960, 0.10: 1.645}.get(alpha, 1.960)
adj_ate  = BASE_ATE * multiplier
adj_se   = BASE_SE  * multiplier
ci_lower = adj_ate - z * adj_se
ci_upper = adj_ate + z * adj_se

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Causal ATE (days/year)", f"{adj_ate:.2f}")
col2.metric(f"{(1-alpha)*100:.0f}% CI Lower", f"{ci_lower:.2f}")
col3.metric(f"{(1-alpha)*100:.0f}% CI Upper", f"{ci_upper:.2f}")
col4.metric("Std Error", f"{adj_se:.3f}")

st.markdown(f"> **Interpretation:** With a treatment intensity multiplier of {multiplier:.1f}x, "
            f"professional host status is estimated to change occupancy by **{adj_ate:.1f} days/year** "
            f"({(1-alpha)*100:.0f}% CI: [{ci_lower:.1f}, {ci_upper:.1f}]).")

# Sensitivity chart
multipliers = np.arange(0.5, 3.1, 0.1)
ates = BASE_ATE * multipliers
ses  = BASE_SE  * multipliers

fig = go.Figure()
fig.add_trace(go.Scatter(x=multipliers, y=ates + z*ses, mode="lines",
                          line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=multipliers, y=ates - z*ses, mode="lines",
                          line=dict(width=0), fill="tonexty",
                          fillcolor="rgba(26,35,126,0.2)", name=f"{(1-alpha)*100:.0f}% CI"))
fig.add_trace(go.Scatter(x=multipliers, y=ates, mode="lines",
                          line=dict(color="#1a237e", width=2), name="ATE"))
fig.add_vline(x=multiplier, line_dash="dash", line_color="red",
              annotation_text=f"Current: {multiplier:.1f}x")
fig.update_layout(title="Sensitivity: ATE vs Treatment Intensity Multiplier",
                  xaxis_title="Multiplier", yaxis_title="Estimated Effect (days/year)",
                  template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Naive vs DML comparison
st.subheader("Naive vs. Causal Estimates")
fig2 = go.Figure()
labels = ["Naive OLS", "DML (GBM)", "DML Robust (RF)"]
ates_all = [-39.511, -13.458, -13.102]
cis_all  = [(-44.092, -34.930), (-17.328, -9.587), (-17.193, -9.010)]
colors   = ["#c62828", "#1a237e", "#1565c0"]
for i, (lbl, ate, ci, col) in enumerate(zip(labels, ates_all, cis_all, colors)):
    fig2.add_trace(go.Scatter(
        x=[lbl], y=[ate],
        error_y=dict(type="data", symmetric=False,
                     array=[ci[1]-ate], arrayminus=[ate-ci[0]], visible=True),
        mode="markers", marker=dict(size=14, color=col), name=lbl
    ))
fig2.add_hline(y=0, line_dash="dash", line_color="gray")
fig2.update_layout(title="Naive vs. Causal Effect Estimates with 95% CIs",
                   yaxis_title="Effect on Occupancy (days/year)",
                   template="plotly_white", showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# Counterfactual
st.subheader("Counterfactual: What if commercial host prevalence doubled?")
cf_ate = BASE_ATE * 2.0
cf_ci  = (cf_ate - z*BASE_SE*2, cf_ate + z*BASE_SE*2)
n_listings = 7535
fte_units = abs(cf_ate) * n_listings / 365
st.write(
    f"If commercial host share doubled across SF's {n_listings:,} listings, "
    f"the estimated per-listing effect would be **{cf_ate:.1f} days/year** "
    f"({(1-alpha)*100:.0f}% CI: [{cf_ci[0]:.1f}, {cf_ci[1]:.1f}]). "
    f"This implies approximately **{fte_units:.0f} fewer full-time equivalent "
    f"rental units** available to long-term tenants."
)

st.markdown("---")
st.markdown("*Data: Inside Airbnb SF (Dec 2025). Method: Double ML with GBM nuisance models, HC3 robust SEs. N = 7,535.*")
