import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mimamori",
    page_icon="⌚",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "caregiver_message" not in st.session_state:
    st.session_state.caregiver_message = (
        "Everything looks okay. I am checking on you."
    )

if "patient_reply" not in st.session_state:
    st.session_state.patient_reply = ""

if "caregiver_alert_acknowledged" not in st.session_state:
    st.session_state.caregiver_alert_acknowledged = False


# =========================================================
# HEAT INDEX CALCULATION
# =========================================================

def calculate_heat_index(temp_c, humidity):
    """
    Approximate NOAA/NWS Heat Index using the Rothfusz regression.

    The Heat Index estimates how hot conditions feel when relative
    humidity is considered together with air temperature.

    This is environmental heat-risk information and is NOT a
    dementia-specific medical diagnosis.
    """

    temp_f = (temp_c * 9 / 5) + 32
    rh = humidity

    # Heat Index is primarily relevant in hot conditions.
    # Below 80°F, use air temperature as a simple approximation.
    if temp_f < 80:
        return temp_c

    heat_index_f = (
        -42.379
        + (2.04901523 * temp_f)
        + (10.14333127 * rh)
        - (0.22475541 * temp_f * rh)
        - (0.00683783 * temp_f ** 2)
        - (0.05481717 * rh ** 2)
        + (0.00122874 * temp_f ** 2 * rh)
        + (0.00085282 * temp_f * rh ** 2)
        - (0.00000199 * temp_f ** 2 * rh ** 2)
    )

    heat_index_c = (heat_index_f - 32) * 5 / 9

    return heat_index_c


# =========================================================
# SIMPLIFIED PROTOTYPE RISK CLASSIFICATION
# =========================================================

def determine_risk(heat_index_c):
    """
    Simplified prototype classification based on traditional
    NWS Heat Index risk categories.

    LOW:
        Heat Index below approximately 32°C / 90°F

    MODERATE:
        Approximately 32–39°C / 90–103°F

    HIGH:
        Approximately 39°C / 103°F or above

    This prototype combines NWS categories into three simpler
    levels for caregiver readability.
    """

    if heat_index_c < 32:
        return "LOW"

    elif heat_index_c < 39:
        return "MODERATE"

    else:
        return "HIGH"


# =========================================================
# SIDEBAR — SIMULATION CONTROLS
# =========================================================

st.sidebar.title("Simulation Controls")

st.sidebar.caption(
    "Hackathon prototype: adjust these values to simulate "
    "sensor readings from the Mimamori wristband."
)

st.sidebar.markdown("### Environmental Sensors")

air_temperature = st.sidebar.slider(
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


st.sidebar.markdown("### Wearer Sensors")

heart_rate = st.sidebar.slider(
    "Heart Rate (bpm)",
    min_value=50,
    max_value=150,
    value=78,
    step=1
)

skin_temperature = st.sidebar.slider(
    "Skin Temperature (°C)",
    min_value=30.0,
    max_value=39.0,
    value=33.5,
    step=0.1
)

activity = st.sidebar.selectbox(
    "Activity Level",
    [
        "Normal",
        "Low",
        "Very Low"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "The controls are for prototype demonstration and would "
    "normally be replaced by live sensor readings from the ESP32."
)


# =========================================================
# CALCULATE CURRENT ENVIRONMENTAL RISK
# =========================================================

heat_index = calculate_heat_index(
    air_temperature,
    humidity
)

risk = determine_risk(heat_index)


# =========================================================
# HEADER
# =========================================================

st.title("MIMAMORI")

st.caption(
    "A Wearable Heat Guard for People with Dementia"
)


# =========================================================
# TABS
# =========================================================

caregiver_tab, wearer_tab = st.tabs(
    [
        "Caregiver View",
        "Wearer View"
    ]
)


# =========================================================
# CAREGIVER VIEW
# =========================================================

with caregiver_tab:

    st.header("Current Status")

    # -----------------------------------------------------
    # Overall status
    # -----------------------------------------------------

    if risk == "LOW":

        st.success(
            "LOW HEAT RISK — Current environmental conditions "
            "do not indicate elevated heat risk."
        )

    elif risk == "MODERATE":

        st.warning(
            "MODERATE HEAT RISK — Heat conditions are becoming "
            "concerning. Mimamori is alerting the wearer."
        )

    else:

        st.error(
            "HIGH HEAT RISK — Potentially dangerous heat conditions "
            "detected. Please check on the wearer."
        )


    # =====================================================
    # LIVE SENSOR DATA
    # =====================================================

    st.header("Live Sensor Data")

    st.caption(
        "Current readings simulated from the Mimamori wristband."
    )

    sensor1, sensor2, sensor3 = st.columns(3)

    with sensor1:

        st.metric(
            "Heart Rate",
            f"{heart_rate} bpm"
        )

    with sensor2:

        st.metric(
            "Skin Temperature",
            f"{skin_temperature:.1f} °C"
        )

    with sensor3:

        st.metric(
            "Activity Level",
            activity
        )


    sensor4, sensor5, sensor6 = st.columns(3)

    with sensor4:

        st.metric(
            "Air Temperature",
            f"{air_temperature:.1f} °C"
        )

    with sensor5:

        st.metric(
            "Humidity",
            f"{humidity}%"
        )

    with sensor6:

        st.metric(
            "Estimated Heat Index",
            f"{heat_index:.1f} °C"
        )


    # =====================================================
    # HEAT-RISK INDICATOR
    # =====================================================

    st.header("Heat-Risk Indicator")

    risk_col, explanation_col = st.columns(
        [1, 2]
    )

    with risk_col:

        if risk == "LOW":

            st.success("### LOW")

        elif risk == "MODERATE":

            st.warning("### MODERATE")

        else:

            st.error("### HIGH")


    with explanation_col:

        if risk == "LOW":

            st.write(
                "**What this means:** Current environmental heat "
                "conditions are relatively low risk. Mimamori "
                "continues monitoring."
            )

        elif risk == "MODERATE":

            st.write(
                "**What this means:** Heat exposure is increasing. "
                "Mimamori alerts the wearer to move somewhere cooler."
            )

        else:

            st.write(
                "**What this means:** Environmental conditions may "
                "increase the risk of heat illness. Mimamori alerts "
                "the wearer and notifies the caregiver."
            )


    st.caption(
        "The environmental classification is based on Heat Index. "
        "This is not a medical diagnosis."
    )


    # =====================================================
    # SCREENLESS WRISTBAND RESPONSE
    # =====================================================

    st.header("Screenless Wristband Response")

    response1, response2, response3 = st.columns(3)


    if risk == "LOW":

        with response1:
            st.metric(
                "Vibration",
                "OFF"
            )

        with response2:
            st.metric(
                "Voice Alert",
                "OFF"
            )

        with response3:
            st.metric(
                "Caregiver Alert",
                "OFF"
            )

        st.info(
            "The wristband continues passive monitoring."
        )


    elif risk == "MODERATE":

        with response1:
            st.metric(
                "Vibration",
                "ACTIVE"
            )

        with response2:
            st.metric(
                "Voice Alert",
                "ACTIVE"
            )

        with response3:
            st.metric(
                "Caregiver Alert",
                "STANDBY"
            )

        st.warning(
            'Wristband voice message: '
            '"It is getting hot. Please move somewhere cooler."'
        )


    else:

        with response1:
            st.metric(
                "Vibration",
                "STRONG"
            )

        with response2:
            st.metric(
                "Voice Alert",
                "ACTIVE"
            )

        with response3:
            st.metric(
                "Caregiver Alert",
                "ACTIVE"
            )

        st.error(
            'Wristband voice message: '
            '"It is too hot. Please move to a cool place now."'
        )


    # =====================================================
    # WEARER REPLY
    # =====================================================

    if st.session_state.patient_reply:

        st.header("Latest Wearer Response")

        if st.session_state.patient_reply == "I am OK":

            st.success(
                "Wearer replied: I'M OK"
            )

        elif st.session_state.patient_reply == "I need help":

            st.error(
                "Wearer replied: I NEED HELP"
            )


    # =====================================================
    # CAREGIVER MESSAGE
    # =====================================================

    st.header("Message the Wearer")

    st.caption(
        "Send a short, simple message to the wearer's companion app."
    )

    new_message = st.text_input(
        "Message",
        value=st.session_state.caregiver_message,
        placeholder="Example: Please go inside and drink some water."
    )

    if st.button(
        "Send Message",
        type="primary"
    ):

        st.session_state.caregiver_message = new_message

        st.success(
            "Message sent to wearer."
        )


    # =====================================================
    # HIGH-RISK CAREGIVER ALERT
    # =====================================================

    if risk == "HIGH":

        st.divider()

        st.error("CAREGIVER ATTENTION REQUIRED")

        st.markdown(
            f"""
### Mimamori Alert

**Heat-risk level:** HIGH

**Current environmental conditions**
- Air temperature: **{air_temperature:.1f} °C**
- Humidity: **{humidity}%**
- Estimated Heat Index: **{heat_index:.1f} °C**

**Wearer information**
- Heart rate: **{heart_rate} bpm**
- Skin temperature: **{skin_temperature:.1f} °C**
- Activity: **{activity}**

Please check on the wearer and determine whether assistance is needed.
"""
        )

        if st.button(
            "I have checked on the wearer"
        ):

            st.session_state.caregiver_alert_acknowledged = True

        if st.session_state.caregiver_alert_acknowledged:

            st.success(
                "Caregiver acknowledgement recorded."
            )


# =========================================================
# WEARER VIEW
# =========================================================

with wearer_tab:

    # Larger, simpler layout
    st.title("Mimamori")

    st.markdown(
        "## How are you?"
    )


    # =====================================================
    # SIMPLE SAFETY MESSAGE
    # =====================================================

    if risk == "LOW":

        st.success(
            """
### YOU ARE OK

Everything looks okay.

You can continue what you are doing.
"""
        )

    elif risk == "MODERATE":

        st.warning(
            """
### IT IS GETTING HOT

Please move somewhere cooler.

Rest and drink some water.
"""
        )

    else:

        st.error(
            """
### IT IS TOO HOT

Please stop what you are doing.

Move to a cool place now.
"""
        )


    # =====================================================
    # ACTIVITY
    # =====================================================

    st.markdown(
        "## Your Activity"
    )

    if activity == "Normal":

        st.info(
            """
### Moving normally
"""
        )

    elif activity == "Low":

        st.warning(
            """
### Moving less than usual

Please take care and rest if you need to.
"""
        )

    else:

        st.error(
            """
### Very little movement

Please check that you are feeling okay.
"""
        )


    # =====================================================
    # CAREGIVER MESSAGE
    # =====================================================

    st.markdown(
        "## Message From Your Caregiver"
    )

    st.info(
        f"""
### {st.session_state.caregiver_message}
"""
    )


    # =====================================================
    # SIMPLE RESPONSE BUTTONS
    # =====================================================

    st.markdown(
        "## Tell Your Caregiver"
    )

    button1, button2 = st.columns(2)


    with button1:

        if st.button(
            "I'M OK",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.patient_reply = "I am OK"

            st.success(
                "Your caregiver knows you are OK."
            )


    with button2:

        if st.button(
            "I NEED HELP",
            use_container_width=True
        ):

            st.session_state.patient_reply = "I need help"

            st.error(
                "Your caregiver has been notified."
            )


    # No sensor numbers here intentionally
    st.caption(
        "Mimamori keeps detailed sensor information in the caregiver "
        "view so this screen stays simple and easy to understand."
    )


# =========================================================
# PROTOTYPE INFORMATION
# =========================================================

st.divider()

with st.expander("About this prototype"):

    st.markdown(
        """
**Mimamori** is a prototype screenless wearable designed to monitor
heat-related risk factors for people with dementia.

### Sensors represented in this simulation

**Inward-facing**
- Heart rate
- Skin temperature

**Outward-facing**
- Surrounding air temperature
- Humidity

**Internal**
- Accelerometer for activity level

### Wristband outputs

- Vibration
- Voice messages
- Caregiver notifications

### Current prototype risk calculation

The environmental component uses the **Heat Index**, which combines
air temperature and relative humidity.

Heart rate, skin temperature, and activity are currently shown as
supporting sensor information. They are **not currently used as
clinically validated dementia-specific danger thresholds**.

Future development would require clinical testing and validation before
Mimamori could be used to make medical decisions.
"""
    )


st.caption(
    "Hackathon prototype — not a medical device or diagnostic system."
)
