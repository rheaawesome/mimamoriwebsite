
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Mimamori Heat Risk Monitor",
    page_icon="⌚",
    layout="wide"
)

st.title("MIMAMORI")
st.caption("Wearable heat-risk monitoring system for people with dementia")

# -----------------------------
# Sidebar: simulated sensor data
# -----------------------------

st.sidebar.header("Simulation Controls")

temperature = st.sidebar.slider(
    "Outdoor Temperature (°C)",
    min_value=20.0,
    max_value=45.0,
    value=30.0,
    step=0.5
)

humidity = st.sidebar.slider(
    "Humidity (%)",
    min_value=20,
    max_value=100,
    value=55,
    step=1
)

heart_rate = st.sidebar.slider(
    "Heart Rate (bpm)",
    min_value=50,
    max_value=160,
    value=78,
    step=1
)

skin_temp = st.sidebar.slider(
    "Skin Temperature (°C)",
    min_value=30.0,
    max_value=40.0,
    value=33.5,
    step=0.1
)

gsr = st.sidebar.slider(
    "Skin Conductance / GSR",
    min_value=0.0,
    max_value=10.0,
    value=3.0,
    step=0.1
)

movement_level = st.sidebar.selectbox(
    "Movement Level",
    ["Normal", "Low", "Very Low"]
)

st.sidebar.divider()

auto_simulate = st.sidebar.checkbox(
    "Run automatic heat simulation",
    value=False
)

# -----------------------------
# Heat risk calculation
# -----------------------------

def calculate_risk(temp, humidity, hr, skin_temp, gsr, movement):
    risk = 0

    # Environmental temperature
    if temp <= 28:
        risk += 5
    elif temp <= 32:
        risk += 12
    elif temp <= 35:
        risk += 20
    elif temp <= 38:
        risk += 28
    else:
        risk += 35

    # Humidity
    if humidity > 80:
        risk += 15
    elif humidity > 65:
        risk += 10
    elif humidity > 50:
        risk += 5

    # Heart rate
    if hr > 120:
        risk += 20
    elif hr > 100:
        risk += 14
    elif hr > 90:
        risk += 8

    # Skin temperature
    if skin_temp > 36.0:
        risk += 18
    elif skin_temp > 35.0:
        risk += 12
    elif skin_temp > 34.0:
        risk += 6

    # GSR
    if gsr > 8:
        risk += 12
    elif gsr > 6:
        risk += 8
    elif gsr > 4:
        risk += 4

    # Movement
    if movement == "Very Low":
        risk += 12
    elif movement == "Low":
        risk += 6

    return min(int(risk), 100)


risk_score = calculate_risk(
    temperature,
    humidity,
    heart_rate,
    skin_temp,
    gsr,
    movement_level
)

# -----------------------------
# Risk level
# -----------------------------

def get_risk_level(score):
    if score < 35:
        return "SAFE"
    elif score < 65:
        return "WARNING"
    else:
        return "HIGH RISK"


risk_level = get_risk_level(risk_score)

# -----------------------------
# Main dashboard
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Heat Risk Score",
        f"{risk_score} / 100"
    )

with col2:
    st.metric(
        "Risk Level",
        risk_level
    )

with col3:
    alert_status = "Triggered" if risk_score >= 65 else "Not Triggered"
    st.metric(
        "Caregiver Alert",
        alert_status
    )

st.progress(risk_score / 100)

# -----------------------------
# Alert message
# -----------------------------

if risk_level == "SAFE":
    st.success(
        "Current conditions appear stable. Continue monitoring."
    )

elif risk_level == "WARNING":
    st.warning(
        "Heat risk is increasing. Consider moving the wearer to a cooler environment."
    )

else:
    st.error(
        "HIGH HEAT RISK DETECTED. Mimamori would trigger vibration, visual alerts, "
        "and notify the caregiver."
    )

# -----------------------------
# Sensor display
# -----------------------------

st.subheader("Live Sensor Data")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Outdoor Temp", f"{temperature:.1f} °C")
c2.metric("Humidity", f"{humidity}%")
c3.metric("Heart Rate", f"{heart_rate} bpm")
c4.metric("Skin Temp", f"{skin_temp:.1f} °C")
c5.metric("GSR", f"{gsr:.1f}")

st.write(f"**Movement Level:** {movement_level}")

# -----------------------------
# Watch response
# -----------------------------

st.subheader("Mimamori Watch Response")

if risk_score < 35:
    st.write("Watch status: Normal")
    st.write("Vibration: OFF")
    st.write("LED Alert: OFF")
    st.write("Caregiver notification: OFF")

elif risk_score < 65:
    st.write("Watch status: Warning")
    st.write("Vibration: LIGHT")
    st.write("LED Alert: YELLOW")
    st.write("Caregiver notification: Monitoring")

else:
    st.write("Watch status: Emergency Alert")
    st.write("Vibration: STRONG")
    st.write("LED Alert: RED")
    st.write("Caregiver notification: SENT")

# -----------------------------
# Risk history chart
# -----------------------------

st.subheader("Example Risk Progression")

history = pd.DataFrame({
    "Time": [
        "12:00",
        "12:05",
        "12:10",
        "12:15",
        "12:20",
        "12:25"
    ],
    "Risk Score": [
        max(risk_score - 45, 5),
        max(risk_score - 35, 10),
        max(risk_score - 25, 15),
        max(risk_score - 15, 20),
        max(risk_score - 7, 25),
        risk_score
    ]
})

st.line_chart(
    history,
    x="Time",
    y="Risk Score"
)

# -----------------------------
# Caregiver panel
# -----------------------------

st.subheader("Caregiver Dashboard")

if risk_score >= 65:

    st.error("Emergency notification")

    st.write(
        """
        **Wearer:** Akira Tanaka  
        **Status:** High heat risk detected  
        **Current risk score:** {}
        
        Recommended actions:
        - Contact the wearer
        - Encourage hydration
        - Move to a cooler location
        - Check physical condition
        """.format(risk_score)
    )

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Call Wearer"):
            st.info("Demo: caregiver call initiated.")

    with col_b:
        if st.button("Acknowledge Alert"):
            st.success("Alert acknowledged.")

else:
    st.info(
        "No emergency notification currently active."
    )

# -----------------------------
# Automatic demo simulation
# -----------------------------

if auto_simulate:

    st.subheader("Automatic Heat Exposure Simulation")

    placeholder = st.empty()

    simulation_data = []

    for i in range(12):

        simulated_temp = 28 + i * 0.9
        simulated_humidity = min(55 + i * 2, 90)
        simulated_hr = 78 + i * 3
        simulated_skin = 33.2 + i * 0.2
        simulated_gsr = 3 + i * 0.35

        simulated_risk = calculate_risk(
            simulated_temp,
            simulated_humidity,
            simulated_hr,
            simulated_skin,
            simulated_gsr,
            "Low" if i > 5 else "Normal"
        )

        simulation_data.append({
            "Temperature": simulated_temp,
            "Humidity": simulated_humidity,
            "Heart Rate": simulated_hr,
            "Skin Temperature": simulated_skin,
            "Risk": simulated_risk
        })

        with placeholder.container():

            st.metric(
                "Simulated Temperature",
                f"{simulated_temp:.1f} °C"
            )

            st.metric(
                "Simulated Heart Rate",
                f"{simulated_hr} bpm"
            )

            st.metric(
                "Simulated Risk Score",
                f"{simulated_risk} / 100"
            )

            st.progress(simulated_risk / 100)

            if simulated_risk >= 65:
                st.error(
                    "MIMAMORI ALERT: High heat risk detected. "
                    "Caregiver notification triggered."
                )
            elif simulated_risk >= 35:
                st.warning(
                    "Risk increasing."
                )
            else:
                st.success(
                    "Condition stable."
                )

        time.sleep(0.4)

    st.line_chart(
        pd.DataFrame(simulation_data)["Risk"]
    )

# -----------------------------
# Explanation
# -----------------------------

with st.expander("How this prototype works"):

    st.write(
        """
        This prototype simulates data that could be collected by the
        Mimamori wearable.

        The system combines environmental and physiological signals,
        including:

        - outdoor temperature
        - humidity
        - heart rate
        - skin temperature
        - skin conductance
        - movement

        These values are passed into a prototype heat-risk scoring
        algorithm.

        When the estimated risk passes a threshold, the simulated watch
        activates alerts and sends a notification to the caregiver.

        This is a hackathon prototype and is not a clinically validated
        medical device.
        """
    )
