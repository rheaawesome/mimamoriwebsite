import streamlit as st

st.set_page_config(
    page_title="Mimamori Care",
    page_icon="⌚",
    layout="wide"
)

# =========================================================
# HEAT INDEX
# NOAA / NWS Rothfusz regression
# =========================================================

def calculate_heat_index(temp_c, humidity):
    """
    Approximate NOAA/NWS Heat Index.

    The Rothfusz regression is principally applicable to warm,
    humid conditions. For cooler conditions we return air temperature.

    This is environmental heat-risk information, NOT a clinical
    diagnosis or dementia-specific medical threshold.
    """

    temp_f = temp_c * 9 / 5 + 32
    rh = humidity

    if temp_f < 80:
        return temp_c

    hi = (
        -42.379
        + 2.04901523 * temp_f
        + 10.14333127 * rh
        - 0.22475541 * temp_f * rh
        - 0.00683783 * temp_f ** 2
        - 0.05481717 * rh ** 2
        + 0.00122874 * temp_f ** 2 * rh
        + 0.00085282 * temp_f * rh ** 2
        - 0.00000199 * temp_f ** 2 * rh ** 2
    )

    return (hi - 32) * 5 / 9


def determine_risk(heat_index_c):
    """
    Simplified prototype grouping derived from traditional
    NWS Heat Index risk categories.

    LOW: below ~32°C / 90°F
    MODERATE: ~32–39°C / 90–103°F
    HIGH: >= ~39°C / 103°F

    The original NWS system contains more categories.
    Mimamori simplifies them to LOW / MODERATE / HIGH
    for this prototype.
    """

    if heat_index_c < 32:
        return "LOW"

    elif heat_index_c < 39:
        return "MODERATE"

    else:
        return "HIGH"


# =========================================================
# SESSION STATE
# =========================================================

if "wearer_response" not in st.session_state:
    st.session_state.wearer_response = False

if "caregiver_alert" not in st.session_state:
    st.session_state.caregiver_alert = False


# =========================================================
# SIDEBAR — DEVELOPER / DEMO CONTROLS
# =========================================================

st.sidebar.title("Simulation Controls")

st.sidebar.caption(
    "For prototype demonstration only. "
    "These controls simulate data coming from the Mimamori wristband."
)

air_temperature = st.sidebar.slider(
    "Surrounding Air Temperature (°C)",
    20.0,
    45.0,
    29.0,
    0.5
)

humidity = st.sidebar.slider(
    "Humidity (%)",
    20,
    100,
    55
)

heart_rate = st.sidebar.slider(
    "Heart Rate (bpm)",
    50,
    150,
    78
)

skin_temperature = st.sidebar.slider(
    "Skin Temperature (°C)",
    30.0,
    39.0,
    33.5,
    0.1
)

activity = st.sidebar.selectbox(
    "Activity Level",
    [
        "Normal",
        "Low",
        "Very Low"
    ]
)


# =========================================================
# CALCULATIONS
# =========================================================

heat_index = calculate_heat_index(
    air_temperature,
    humidity
)

risk = determine_risk(heat_index)


# =========================================================
# CAREGIVER DASHBOARD
# =========================================================

st.title("Mimamori Care")

st.caption(
    "Live safety monitoring for the Mimamori screenless wristband"
)

# ---------------------------------------------------------
# Current status
# ---------------------------------------------------------

if risk == "LOW":

    st.success(
        "● LOW HEAT RISK — Current environmental conditions "
        "do not indicate elevated heat risk."
    )

elif risk == "MODERATE":

    st.warning(
        "● MODERATE HEAT RISK — Heat conditions are becoming "
        "concerning. Mimamori is alerting the wearer."
    )

else:

    st.error(
        "● HIGH HEAT RISK — Potentially dangerous heat conditions "
        "detected. Check the wearer."
    )


# =========================================================
# 1. LIVE SENSOR DATA
# =========================================================

st.header("Live Sensor Data")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Heart Rate",
        f"{heart_rate} bpm"
    )

    st.caption("Measured by inward-facing sensor")

with col2:

    st.metric(
        "Skin Temperature",
        f"{skin_temperature:.1f} °C"
    )

    st.caption("Measured at the wrist")

with col3:

    st.metric(
        "Activity",
        activity
    )

    st.caption("Measured by accelerometer")


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Air Temperature",
        f"{air_temperature:.1f} °C"
    )

with col5:

    st.metric(
        "Humidity",
        f"{humidity}%"
    )

with col6:

    st.metric(
        "Estimated Heat Index",
        f"{heat_index:.1f} °C"
    )


# =========================================================
# 2. PROTOTYPE HEAT-RISK INDICATOR
# =========================================================

st.header("Heat-Risk Indicator")

risk_col, explanation_col = st.columns([1, 2])

with risk_col:

    if risk == "LOW":

        st.metric(
            "Current Risk",
            "LOW"
        )

    elif risk == "MODERATE":

        st.metric(
            "Current Risk",
            "MODERATE"
        )

    else:

        st.metric(
            "Current Risk",
            "HIGH"
        )


with explanation_col:

    if risk == "LOW":

        st.write(
            "**What this means:** Mimamori continues monitoring. "
            "No wearer intervention is currently required."
        )

    elif risk == "MODERATE":

        st.write(
            "**What this means:** Environmental heat exposure is increasing. "
            "Mimamori prompts the wearer to move somewhere cooler."
        )

    else:

        st.write(
            "**What this means:** Environmental conditions may increase "
            "the risk of heat illness. Mimamori alerts the wearer and "
            "escalates monitoring to the caregiver."
        )


st.caption(
    "Prototype classification based primarily on environmental Heat Index. "
    "This is not a medical diagnosis."
)


# =========================================================
# 3. SCREENLESS WRISTBAND RESPONSE
# =========================================================

st.header("Wristband Response")

if risk == "LOW":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Vibration",
        "OFF"
    )

    col2.metric(
        "Voice Alert",
        "OFF"
    )

    col3.metric(
        "Caregiver Alert",
        "OFF"
    )

    st.info(
        "Mimamori continues passive monitoring."
    )


elif risk == "MODERATE":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Vibration",
        "ACTIVE"
    )

    col2.metric(
        "Voice Alert",
        "ACTIVE"
    )

    col3.metric(
        "Caregiver Alert",
        "Standby"
    )

    st.warning(
        '🔊 Wristband voice message: '
        '"It is getting hot. Please move somewhere cooler."'
    )


    if st.button(
        "Simulate wearer pressing response button",
        type="primary"
    ):

        st.session_state.wearer_response = True


    if st.session_state.wearer_response:

        st.success(
            "Wearer response received. Mimamori continues monitoring."
        )

    else:

        st.write(
            "Waiting for wearer acknowledgement."
        )

        if st.button(
            "Simulate prolonged no response"
        ):

            st.session_state.caregiver_alert = True


elif risk == "HIGH":

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Vibration",
        "STRONG"
    )

    col2.metric(
        "Voice Alert",
        "ACTIVE"
    )

    col3.metric(
        "Caregiver Alert",
        "ACTIVE"
    )

    st.error(
        '🔊 Wristband voice message: '
        '"Heat risk detected. Please move to a cool place now."'
    )

    st.session_state.caregiver_alert = True


# =========================================================
# CAREGIVER ALERT
# =========================================================

if st.session_state.caregiver_alert:

    st.divider()

    st.error("CAREGIVER ATTENTION REQUIRED")

    st.subheader("Mimamori Alert")

    st.write(
        f"""
**Current heat-risk level:** {risk}

**Air temperature:** {air_temperature:.1f} °C  
**Humidity:** {humidity}%  
**Estimated Heat Index:** {heat_index:.1f} °C  
**Heart rate:** {heart_rate} bpm  
**Skin temperature:** {skin_temperature:.1f} °C  
**Activity:** {activity}
"""
    )

    st.markdown(
        """
**Suggested next steps**

Check on the wearer and determine whether they need assistance
moving to a cooler environment. If the wearer shows symptoms of
heat illness, follow appropriate emergency medical guidance.
"""
    )

    if st.button(
        "I have checked on the wearer"
    ):

        st.session_state.caregiver_alert = False
        st.session_state.wearer_response = False

        st.success(
            "Caregiver acknowledgement recorded."
        )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "Mimamori prototype. Environmental heat-risk classification is "
    "based on the NOAA/NWS Heat Index concept. Heart rate, skin "
    "temperature and activity readings are currently displayed as "
    "supporting sensor information and are not used as clinically "
    "validated diagnostic thresholds."
)
