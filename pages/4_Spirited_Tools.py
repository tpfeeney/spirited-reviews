import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def add_sidebar_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://raw.githubusercontent.com/tpfeeney/spirited-reviews/main/srlogo.png');
                background-repeat: no-repeat;
                background-position: 20px 20px;
                padding-top: 180px;
                background-size: 150px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_sidebar_logo()

# Raw data as a string
data = """
percent,20C,25C
40,0.93518,0.93148
41,0.93314,0.92940
42,0.93107,0.92729
43,0.92897,0.92516
44,0.92685,0.92301
45,0.92472,0.92085
46,0.92257,0.91868
47,0.92041,0.91649
48,0.91823,0.91429
49,0.91604,0.91208
50,0.91384,0.90985
51,0.91160,0.90760
52,0.90936,0.90534
53,0.90711,0.90307
54,0.90485,0.90079
55,0.90258,0.89850
56,0.90031,0.89621
57,0.89803,0.89392
58,0.89574,0.89162
59,0.89344,0.88931
60,0.89113,0.88699
61,0.88882,0.88466
62,0.88650,0.88233
63,0.88417,0.87998
64,0.88183,0.87763
65,0.87948,0.87527
66,0.87713,0.87291
67,0.87477,0.87054
68,0.87241,0.86817
69,0.87004,0.86579
70,0.86766,0.86340
71,0.86527,0.86100
72,0.86287,0.85859
73,0.86047,0.85618
74,0.85806,0.85376
75,0.85564,0.85134
76,0.85322,0.84891
77,0.85079,0.84647
78,0.84835,0.84403
79,0.84590,0.84158
80,0.84344,0.83911
"""

# Load into a DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data))

# Fit linear regression models
X = df[['percent']]
model_20C = LinearRegression().fit(X, df['20C'])
model_25C = LinearRegression().fit(X, df['25C'])

# Streamlit UI
st.title("Alcohol Density Predictor")

percent_input = st.number_input("Enter Alcohol Percent (40 - 80):", min_value=40.0, max_value=80.0, step=0.1)
volume_input = st.number_input("Enter Volume (in mL):", min_value=0.0, step=1.0)

# Predict on input
if percent_input and volume_input:
    pred_20C = model_20C.predict([[percent_input]])[0]
    pred_25C = model_25C.predict([[percent_input]])[0]
    
    mass_20C = pred_20C * volume_input
    mass_25C = pred_25C * volume_input

    st.write(f"### Predicted Density at 20°C: {pred_20C:.5f} g/mL")
    st.write(f"### Predicted Mass at 20°C: {mass_20C:.2f} g")

    st.write(f"### Predicted Density at 25°C: {pred_25C:.5f} g/mL")
    st.write(f"### Predicted Mass at 25°C: {mass_25C:.2f} g")
