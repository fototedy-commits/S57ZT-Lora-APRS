<div align="center">📡 LoRa APRS MQTT Monitor for Home Assistant</div>
<div align="center"> A custom Home Assistant integration for monitoring LoRa APRS stations via MQTT Supports temperature, humidity, battery, pressure, GPS position and more. </div>
🚀 Features

Receives LoRa APRS packets via MQTT

Automatically creates a device per callsign

Creates sensors for:

🌡 Temperature

💧 Humidity

🔋 Battery

🌬 Pressure

📍 GPS coordinates

Works with Ricardo CA2RXU LoRa APRS iGate/Digi firmware

Fully asynchronous, compliant with latest Home Assistant API

Supports translations (EN, SL)

Compatible with HACS

📦 Requirements

Home Assistant 2024.1+

MQTT broker (Mosquitto recommended)

LoRa APRS gateway sending MQTT packets (JSON format)

🛠 Installation (HACS)
Option 1: HACS Custom Repository

Open HACS → Integrations → ⋮ → Custom repositories

Add:

https://github.com/fototedy-commits/S57ZT-Lora-APRS


Category: Integration

Install LoRa APRS MQTT Monitor

Restart Home Assistant

🛠 Installation (Manual)

Download latest release ZIP:
👉 https://github.com/fototedy-commits/S57ZT-Lora-APRS/releases

Extract to:

custom_components/lora_aprs/


Restart Home Assistant.

⚙️ Configuration

Go to Settings → Devices & Services → Add Integration

Search for:
LoRa APRS MQTT Monitor

Enter your MQTT topic (default):

lora/#


Save → Integration will start receiving APRS packets.

🧪 Example MQTT Packet (JSON)
{
  "src": "S57ZT-7",
  "lat": 46.12345,
  "lon": 14.54321,
  "alt": 320,
  "temp": 12.4,
  "hum": 68,
  "batt": 87,
  "pressure": 1008,
  "time": "2025-01-04T12:43:10Z"
}

📊 Entities Created

For callsign S57ZT-7, Home Assistant will create:

S57ZT-7 Temperature
S57ZT-7 Humidity
S57ZT-7 Battery
S57ZT-7 Pressure
S57ZT-7 GPS


Under device:

APRS Station S57ZT-7
Model: iGate / Digi
Manufacturer: LoRa APRS

📁 Directory Structure
custom_components/lora_aprs/
├── __init__.py
├── manifest.json
├── config_flow.py
├── coordinator.py
├── sensor.py
├── services.yaml
├── icons/
└── translations/

🧰 Troubleshooting
Issue	Solution
No entities appear	Check MQTT topic; verify gateway publishes JSON
Only some sensors appear	Missing keys in MQTT payload
UI won’t load	Restart HA; check logs in Developer Tools
Integration won’t install	Ensure custom_components/lora_aprs/ exists and contains manifest.json
📮 Support & Issues

Please open issues here:
👉 https://github.com/fototedy-commits/S57ZT-Lora-APRS/issues

📜 License

MIT License
Copyright © S57ZT

🇸🇮 Slovenska različica (SL)
📡 LoRa APRS MQTT Monitor za Home Assistant

Integracija za spremljanje LoRa APRS postaj preko MQTT.
Samodejno ustvari naprave in senzorje za posamezne klicne znake.

✨ Funkcije

Sprejem APRS paketov preko MQTT

Avtomatsko dodajanje naprav in senzorjev

Podprti senzorji: temperatura, vlaga, baterija, tlak, GPS

Združljivo z Ricardo CA2RXU LoRa APRS iGate/digi firmware

Podpora za prevode (EN, SL)

Popolnoma kompatibilno s HACS

📦 Zahteve

Home Assistant 2024.1+

MQTT broker

LoRa APRS iGate z JSON MQTT paketom
