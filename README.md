# MQTT Drone Control Dashboard

A real-time drone control dashboard built with Streamlit and MQTT for sending commands and monitoring telemetry data.

## Features

- 🚁 **Real-time Drone Control**: Send LAND and BRAKE commands via MQTT
- 🔄 **Auto-reconnection**: Reconnect to MQTT broker with a single click
- 📊 **Live Telemetry**: Monitor incoming status and telemetry data
- 📝 **Live Logs**: View real-time command history and system messages
- 🌐 **Web Interface**: Easy-to-use browser-based control panel

## Screenshots

The dashboard provides an intuitive interface with:
- Connection status indicator (🟢 Connected / 🔴 Disconnected)
- Control buttons for Land, Brake, and Reconnect operations
- Real-time logs showing the last 20 messages
- Auto-refresh capability

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/mqtt-drone-control.git
cd mqtt-drone-control
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run mqtt_1.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the control buttons to:
   - **🛬 Land**: Send landing command to drone
   - **⛔ Brake**: Send brake/hold command to drone
   - **🔄 Reconnect**: Reconnect to MQTT broker

## Configuration

The app connects to the public MQTT broker `broker.emqx.io` by default. You can modify the broker settings in the configuration section:

```python
BROKER_HOST = "broker.emqx.io"
BROKER_PORT = 1883
TOPIC_COMMAND = "mavsdk/command"
TOPIC_STATUS = "mavsdk/status"
TOPIC_TELEMETRY = "mavsdk/telemetry"
```

## MQTT Topics

- **Commands**: `mavsdk/command` - Outgoing drone commands
- **Status**: `mavsdk/status` - Incoming status updates
- **Telemetry**: `mavsdk/telemetry` - Incoming telemetry data

## Command Format

Commands are sent as JSON strings with the following structure:
```json
{
    "action": "LAND",
    "timestamp": 1691234567890,
    "source": "streamlit_app",
    "mavsdk_command": "action.land()",
    "priority": "high"
}
```

## Requirements

- Python 3.7+
- Streamlit
- paho-mqtt

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
