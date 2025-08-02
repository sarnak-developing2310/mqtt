# app.py
import streamlit as st
import paho.mqtt.client as mqtt
import threading
import queue
import time

# UI Configuration (must be first Streamlit command)
st.set_page_config(page_title="Drone Control", layout="centered")

# —————————————————————————————————————————————————————————————————————————————
# CONFIG
BROKER_HOST = "broker.emqx.io"
BROKER_PORT = 1883
TOPIC_COMMAND = "mavsdk/command"
TOPIC_STATUS = "mavsdk/status"
TOPIC_TELEMETRY = "mavsdk/telemetry"
# —————————————————————————————————————————————————————————————————————————————

# A thread-safe queue to hold incoming MQTT messages
@st.cache_resource
def get_mqtt_queue():
    return queue.Queue()

# Initialize (and start) the MQTT client exactly once
@st.cache_resource
def init_mqtt_client():
    q = get_mqtt_queue()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=f"streamlit_{int(time.time())}")
    # callbacks
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(TOPIC_STATUS)
            client.subscribe(TOPIC_TELEMETRY)
        else:
            q.put(("SYSTEM", f"Connection failed (rc={rc})"))
    def on_disconnect(client, userdata, rc):
        q.put(("SYSTEM", "Disconnected"))
    def on_message(client, userdata, msg):
        q.put((msg.topic, msg.payload.decode()))
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # start background network loop
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    return client

# Get or create session-state logs
if "logs" not in st.session_state:
    st.session_state.logs = []

# Pull any new messages off the queue into session_state.logs
mqtt_q = get_mqtt_queue()
while not mqtt_q.empty():
    topic, payload = mqtt_q.get()
    ts = time.strftime("%H:%M:%S", time.localtime())
    st.session_state.logs.append(f"[{ts}] {topic}: {payload}")

# UI
st.title("🚁 Drone Control")

# Connection status
client = init_mqtt_client()
conn_ok = client.is_connected()
st.markdown(f"**Connection:** {'🟢 Connected' if conn_ok else '🔴 Disconnected'}")

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🛬 Land"):
        if conn_ok:
            payload = {
                "action": "LAND",
                "timestamp": int(time.time() * 1000),
                "source": "streamlit_app",
                "mavsdk_command": "action.land()",
                "priority": "high"
            }
            client.publish(TOPIC_COMMAND, payload=str(payload))
            st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] SENT LAND")
        else:
            st.warning("Not connected — cannot send")

with col2:
    if st.button("⛔ Brake"):
        if conn_ok:
            payload = {
                "action": "BRAKE",
                "timestamp": int(time.time() * 1000),
                "source": "streamlit_app",
                "mavsdk_command": "action.hold()",
                "priority": "high"
            }
            client.publish(TOPIC_COMMAND, payload=str(payload))
            st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] SENT BRAKE")
        else:
            st.warning("Not connected — cannot send")

with col3:
    if st.button("🔄 Reconnect"):
        client.disconnect()
        time.sleep(1)
        client.reconnect()
        st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] Reconnecting...")

# Display logs
st.markdown("### Logs")
log_box = st.empty()
log_box.text("\n".join(st.session_state.logs[-20:]))  # show last 20

st.caption("Auto-refresh the page or press any button to pull in new messages.")
