import streamlit as st
import pandas as pd
import time

# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Mimamori Heat Guard",
    page_icon="⌚",
    layout="wide"
)

st.title("MIMAMORI")
st.subheader("A Wearable Heat Guard for People with Dementia")

st.caption(
    "Prototype software simulation of a screenless wearable wristband "
    "that monitors heat-related risk factors and alerts the wearer and caregiver."
)

st.info(
    "This is a hackathon prototype. The heat-risk logic shown here is a "
    "rule-based simulation and has not been clinically validated."
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "wearer_responded" not in st.session_state:
    st.session_state.wearer_responded = False

if "caregiver_notified" not in st.session_state:
    st.session_state.caregiver_notified = False

if "simulate_timeout" not in st.session_state:
    st.session_state.simulate_timeout = False


# --------------------------------------------------
# SIDEBAR — SENSOR INPUTS
# --------------------------------------------------

st.sidebar.header("Sensor Simulation")

st.sidebar.caption(
    "These controls simulate readings collected by the Mimamori wristband."
)

air_temp = st.sidebar.slider(
    "Surrounding Air Temperature (°C)",
    min_value=20.0,
    max_value=45.0,
    value=29.0,
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
    max_value=150,
    value=78,
    step=1
)

skin_temp = st.sidebar.slider(
    "Skin Temperature (°C)",
    min_value=30.0,
    max_value=39.0,
    value=33.5,
    step=0.1
)

activity_level = st.sidebar.selectbox(
    "Activity Level",
    ["Normal", "Low", "Very Low"]
)

st.sidebar.divider()

auto_demo = st.sidebar.checkbox(
    "Run automatic heat-stress demo",
    value=False
)


# --------------------------------------------------
# PROTOTYPE RISK LOGIC
# --------------------------------------------------

def calculate_prototype_risk(
    air_temp,
    humidity,
    heart_rate,
    skin_temp,
    activity_level
):
    """
    Prototype rule-based indicator for demonstration only.
    This is NOT a clinically validated medical model.
    """

    score = 0

    # Surrounding air temperature
    if air_temp < 28:
        score += 5
    elif air_temp < 32:
        score += 12
    elif air_temp < 35:
        score += 20
    elif air_temp < 38:
        score += 30
    else:
        score += 40

    # Humidity
    if humidity < 50:
        score += 2
    elif humidity < 65:
        score += 6
    elif humidity < 80:
        score += 12
    else:
        score += 18

    # Heart rate
    if heart_rate < 90:
        score += 3
    elif heart_rate < 105:
        score += 8
    elif heart_rate < 120:
        score += 15
    else:
        score += 22

    # Skin temperature
    if skin_temp < 34.0:
        score += 3
    elif skin_temp < 35.0:
        score += 8
    elif skin_temp < 36.0:
        score += 15
    else:
        score += 22

    # Activity level
    if activity_level == "Normal":
        score += 2
    elif activity_level == "Low":
        score += 8
    else:
        score += 14

    return min(score, 100)


risk_score = calculate_prototype_risk(
    air_temp,
    humidity,
    heart_rate,
    skin_temp,
    activity_level
)


# --------------------------------------------------
# RISK LEVEL
# --------------------------------------------------

def get_risk_level(score):
    if score < 35:
        return "LOW"
    elif score < 65:
        return "MODERATE"
    else:
        return "HIGH"


risk_level = get_risk_level(risk_score)


# --------------------------------------------------
# ALERT SELECTION
# --------------------------------------------------

def get_alert_plan(level):
    if level == "LOW":
        return {
            "vibration": "OFF",
            "voice": "None",
            "caregiver": "No notification"
        }

    elif level == "MODERATE":
        return {
            "vibration": "Gentle vibration",
            "voice": "Please move somewhere cooler and drink water.",
            "caregiver": "Monitor only"
        }

    else:
        return {
            "vibration": "Strong repeated vibration",
            "voice": "Heat risk detected. Please move to a cool place now.",
            "caregiver": "Notify if high risk or no wearer response"
        }


alert_plan = get_alert_plan(risk_level)


# --------------------------------------------------
# SYSTEM ARCHITECTURE
# --------------------------------------------------

st.header("System Architecture")

st.markdown(
    """
**Sensors collect data**  
→ **ESP32 processes readings**  
→ **Prototype risk algorithm estimates heat-risk level**  
→ **LOW / MODERATE / HIGH identified**  
→ **Best alert is selected**  
→ **Wearer receives vibration + voice alert**  
→ **Wearer presses response button**  
→ **Caregiver is notified if risk is high or no response is received**
"""
)

# --------------------------------------------------
# CURRENT SENSOR DATA
# --------------------------------------------------

st.header("Live Sensor Data")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Air Temperature",
    f"{air_temp:.1f} °C"
)

c2.metric(
    "Humidity",
    f"{humidity}%"
)

c3.metric(
    "Heart Rate",
    f"{heart_rate} bpm"
)

c4.metric(
    "Skin Temperature",
    f"{skin_temp:.1f} °C"
)

c5.metric(
    "Activity",
    activity_level
)


# --------------------------------------------------
# ESP32 PROCESSING
# --------------------------------------------------

st.header("ESP32 Processing")

st.write(
    "The ESP32 would receive sensor readings and pass them to the "
    "prototype rule-based heat-risk algorithm."
)

st.code(
    f"""
Air temperature: {air_temp:.1f} °C
Humidity: {humidity} %
Heart rate: {heart_rate} bpm
Skin temperature: {skin_temp:.1f} °C
Activity level: {activity_level}

Prototype risk indicator: {risk_score} / 100
Risk level: {risk_level}
"""
)


# --------------------------------------------------
# RISK DISPLAY
# --------------------------------------------------

st.header("Prototype Heat-Risk Indicator")

r1, r2, r3 = st.columns(3)

with r1:
    st.metric(
        "Prototype Risk Indicator",
        f"{risk_score} / 100"
    )

with r2:
    st.metric(
        "Risk Level",
        risk_level
    )

with r3:
    if risk_level == "HIGH":
        status = "Escalation Active"
    elif risk_level == "MODERATE":
        status = "Wearer Alert"
    else:
        status = "Monitoring"

    st.metric(
        "System Status",
        status
    )

st.progress(risk_score / 100)


# --------------------------------------------------
# RISK MESSAGE
# --------------------------------------------------

if risk_level == "LOW":
    st.success(
        "LOW RISK — Conditions currently appear stable. "
        "Mimamori continues monitoring."
    )

elif risk_level == "MODERATE":
    st.warning(
        "MODERATE RISK — Mimamori alerts the wearer and recommends "
        "moving to a cooler location."
    )

else:
    st.error(
        "HIGH RISK — Mimamori activates a strong wearer alert and "
        "begins caregiver escalation logic."
    )


# --------------------------------------------------
# WATCH RESPONSE
# --------------------------------------------------

st.header("Screenless Wristband Response")

st.write(
    "The physical Mimamori wristband has no screen. "
    "It communicates through vibration and voice messages."
)

a1, a2, a3 = st.columns(3)

with a1:
    st.metric(
        "Vibration",
        alert_plan["vibration"]
    )

with a2:
    st.metric(
        "Voice Message",
        "ACTIVE" if alert_plan["voice"] != "None" else "OFF"
    )

with a3:
    st.metric(
        "Caregiver Status",
        alert_plan["caregiver"]
    )


if alert_plan["voice"] != "None":
    st.markdown("### Simulated Voice Message")
    st.info(
        f'🔊 "{alert_plan["voice"]}"'
    )


# --------------------------------------------------
# WEARER RESPONSE
# --------------------------------------------------

st.header("Wearer Response")

if risk_level == "LOW":

    st.info(
        "No response is required because the current risk level is LOW."
    )

    st.session_state.wearer_responded = False
    st.session_state.caregiver_notified = False
    st.session_state.simulate_timeout = False


else:

    st.write(
        "After receiving the alert, the wearer can press the physical "
        "response button on the wristband."
    )

    if st.button("Simulate Wearer Pressing Response Button"):

        st.session_state.wearer_responded = True
        st.session_state.caregiver_notified = False
        st.session_state.simulate_timeout = False


    if st.session_state.wearer_responded:

        st.success(
            "Response received. The wearer has acknowledged the alert."
        )


# --------------------------------------------------
# ESCALATION LOGIC
# --------------------------------------------------

st.header("Caregiver Escalation")

if risk_level == "LOW":

    st.info(
        "Caregiver notification not required."
    )


elif risk_level == "MODERATE":

    if st.session_state.wearer_responded:

        st.success(
            "Wearer acknowledged the alert. "
            "Caregiver escalation is not required at this stage."
        )

    else:

        st.warning(
            "Waiting for wearer response."
        )

        if st.button("Simulate Prolonged No Response"):

            st.session_state.simulate_timeout = True
            st.session_state.caregiver_notified = True


elif risk_level == "HIGH":

    st.warning(
        "High risk detected. Caregiver escalation is enabled."
    )

    if st.session_state.wearer_responded:

        st.session_state.caregiver_notified = True

        st.error(
            "HIGH RISK remains present. "
            "Caregiver notification is sent even though the wearer responded."
        )

    else:

        st.write(
            "The system waits for a wearer response."
        )

        if st.button("Simulate Prolonged No Response"):

            st.session_state.simulate_timeout = True
            st.session_state.caregiver_notified = True


# --------------------------------------------------
# CAREGIVER NOTIFICATION
# --------------------------------------------------

if st.session_state.caregiver_notified:

    st.error("CAREGIVER NOTIFICATION SENT")

    st.markdown(
        f"""
### Mimamori Caregiver Alert

**Wearer:** Demo User  
**Risk level:** {risk_level}  
**Prototype risk indicator:** {risk_score}/100

**Current readings**

- Air temperature: {air_temp:.1f} °C
- Humidity: {humidity}%
- Heart rate: {heart_rate} bpm
- Skin temperature: {skin_temp:.1f} °C
- Activity level: {activity_level}

**Recommended caregiver action**

- Contact the wearer
- Check their physical condition
- Encourage movement to a cooler environment
- Provide hydration if appropriate
- Seek medical assistance if symptoms suggest an emergency
"""
    )

    if st.button("Caregiver Acknowledges Alert"):

        st.success(
            "Caregiver acknowledgement recorded."
        )


# --------------------------------------------------
# AUTOMATIC DEMO
# --------------------------------------------------

st.header("Automatic Simulation")

st.write(
    "Use this for the hackathon video to demonstrate how Mimamori responds "
    "as environmental and physiological conditions worsen."
)

if auto_demo:

    placeholder = st.empty()

    simulation_rows = []

    for i in range(10):

        demo_air_temp = 28 + (i * 1.1)
        demo_humidity = min(55 + (i * 2), 90)
        demo_hr = 78 + (i * 4)
        demo_skin_temp = 33.2 + (i * 0.28)

        if i < 4:
            demo_activity = "Normal"
        elif i < 7:
            demo_activity = "Low"
        else:
            demo_activity = "Very Low"

        demo_risk = calculate_prototype_risk(
            demo_air_temp,
            demo_humidity,
            demo_hr,
            demo_skin_temp,
            demo_activity
        )

        demo_level = get_risk_level(demo_risk)

        simulation_rows.append(
            {
                "Step": i + 1,
                "Air Temperature": demo_air_temp,
                "Humidity": demo_humidity,
                "Heart Rate": demo_hr,
                "Skin Temperature": demo_skin_temp,
                "Activity": demo_activity,
                "Risk": demo_risk,
                "Level": demo_level
            }
        )

        with placeholder.container():

            st.subheader(
                f"Simulation Step {i + 1}"
            )

            d1, d2, d3 = st.columns(3)

            d1.metric(
                "Air Temperature",
                f"{demo_air_temp:.1f} °C"
            )

            d2.metric(
                "Heart Rate",
                f"{demo_hr} bpm"
            )

            d3.metric(
                "Prototype Risk",
                f"{demo_risk}/100"
            )

            st.progress(demo_risk / 100)

            if demo_level == "LOW":

                st.success(
                    "LOW — Monitoring continues."
                )

            elif demo_level == "MODERATE":

                st.warning(
                    "MODERATE — Gentle vibration and voice alert activated."
                )

            else:

                st.error(
                    "HIGH — Strong vibration activated. "
                    "Wearer response requested. "
                    "Caregiver escalation enabled."
                )

        time.sleep(0.6)

    simulation_df = pd.DataFrame(simulation_rows)

    st.subheader("Risk Progression")

    st.line_chart(
        simulation_df,
        x="Step",
        y="Risk"
    )


# --------------------------------------------------
# PHYSICAL PRODUCT SPECIFICATION
# --------------------------------------------------

with st.expander("Physical Wristband Design"):

    st.markdown(
        """
### Mimamori Wristband

**Type:**  
Screenless wearable wristband

**Band:**  
Medical-grade silicone  
- hypoallergenic
- waterproof
- sweat-resistant
- flexible

**Housing:**  
PC+ABS  
- lightweight
- impact-resistant

**Housing dimensions:**  
48 × 28 × 13 mm

**Strap width:**  
22 mm

**Target weight:**  
<35 g

### Sensor Placement

**Inward-facing sensors**
- Heart rate
- Skin temperature

**Outward-facing sensors**
- Surrounding air temperature
- Humidity

**Internal sensor**
- Accelerometer for activity level

### Outputs

- Vibration
- Voice messages
- Caregiver notifications

### Charging

Two gold-plated magnetic pogo-pin contacts are located on the underside.

The charging dock uses:
- spring-loaded pogo pins
- neodymium alignment magnets
- 5 V charging connection

**Target enclosure rating:** IP67
"""
    )


# --------------------------------------------------
# SOFTWARE EXPLANATION
# --------------------------------------------------

with st.expander("How This Software Prototype Matches Mimamori"):

    st.markdown(
        """
This app simulates the software logic of the Mimamori wearable system.

1. Sensor values are simulated.
2. The ESP32 processing stage is represented.
3. A prototype risk indicator is calculated.
4. The system identifies LOW, MODERATE, or HIGH risk.
5. The software selects an appropriate wearer alert.
6. The wearer can acknowledge the alert using a simulated response button.
7. A caregiver notification is generated when:
   - HIGH risk is detected, or
   - the wearer does not respond for a prolonged period.

The actual wristband is designed to be screenless. The Streamlit interface is
therefore a development and demonstration dashboard, not the interface the
wearer would see.
"""
    )
