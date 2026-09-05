# Mimamori – Wearable Heat Guard for People with Dementia

Mimamori is a hackathon prototype designed to help protect people with dementia from heat-related risks.

The concept combines a screenless wearable with a caregiver/wearer web interface. The wearable monitors environmental and physiological information, while the website demonstrates how that information could be communicated simply to both users.

## Website Prototype

This Streamlit website simulates the Mimamori system from two perspectives:

### Caregiver View
Caregivers can see:
- Live simulated sensor readings
- Environmental heat-risk level
- Wristband alert status
- Messages and responses from the wearer

### Wearer View
The wearer interface is intentionally simplified for older adults and people experiencing cognitive decline.

Instead of displaying detailed sensor data, it focuses on:
- A simple current safety status
- Activity information
- Clear instructions
- Messages from the caregiver
- "I'm OK" and "I need help" response buttons

## Simulated Sensor Data

The prototype represents data that could be collected by the Mimamori wristband:

- Air temperature
- Humidity
- Heart rate
- Skin temperature
- Activity level

The sidebar controls allow these readings to be changed manually for demonstration purposes.

## Heat-Risk Calculation

The environmental component of the prototype is based on the **NOAA/National Weather Service Heat Index**, which combines air temperature and relative humidity.

The website simplifies environmental heat risk into **LOW, MODERATE, and HIGH** categories for easier communication.

Heart rate, skin temperature, and activity are currently displayed as supporting information. They are not treated as clinically validated dementia-specific danger thresholds.

## Technology

- **Python**
- **Streamlit**
- **GitHub**
- NOAA/NWS Heat Index concept

The wider Mimamori prototype also uses:
- Fusion 360 for wearable design
- Unity for component visualization
- Wokwi and Arduino C++ for electronics simulation

## Running the Website

Install Streamlit:

```bash
pip install streamlit
