treamlit_code = """
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SF Airbnb Causal Dashboard", layout="wide")
st.title("SF Airbnb: Causal Effect of Professional Host Status on STR Occupancy")
st.markdown("**ECON 5200 Final Project** — Double Machine Learning estimates")

# Sidebar
st.sidebar.header("What-If Scenarios")
multiplier = st.sidebar.slider("Treatment intensity multiplier", 0.5, 3.0, 1.0, 0.1)
pro_threshold = st.sidebar.slider("Professional host threshold (# listings)", 1, 5, 2, 1)
alpha = st.sidebar.slider("Significance level (α)", 0.01, 0.10, 0.05, 0.01)

# Base estimates
BASE_ATE = -13.458
BASE_SE  = 1.975

z = {0.01: 2.576, 0.05: 1.960, 0.10: 1.645}.get(alpha, 1.960)
adj_ate  = BASE_ATE * multiplier
adj_se   = BASE_SE  * multiplier
ci_lower = adj_ate - z * adj_se
ci_upper = adj_ate + z * adj_se

# Metrics
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

# Counterfactual
st.subheader("Counterfactual: What if we doubled commercial host prevalence?")
cf_ate = BASE_ATE * 2.0
cf_ci  = (cf_ate - z*BASE_SE*2, cf_ate + z*BASE_SE*2)
st.write(f"If the commercial host share doubled in SF, the estimated aggregate effect "
         f"would be **{cf_ate:.1f} days/year per listing** ({(1-alpha)*100:.0f}% CI: [{cf_ci[0]:.1f}, {cf_ci[1]:.1f}]). "
         f"Applied to SF's ~7,500 Airbnb listings, this implies approximately "
         f"**{abs(cf_ate)*7500/365:.0f} fewer full-time equivalent rental units** available to long-term tenants.")
"""

# Write to app.py
with open("app.py", "w") as f:
    f.write(streamlit_code.strip())
print("app.py written. Deploy to Streamlit Community Cloud.")
