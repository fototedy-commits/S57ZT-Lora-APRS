"""LoRa APRS MQTT Monitor Integration."""

from __future__ import annotations

import json
import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import mqtt

from .coordinator import LoRaAPRSCoordinator

DOMAIN = "lora_aprs"
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the LoRa APRS integration."""
    hass.data.setdefault(DOMAIN, {})

    mqtt_topic = entry.data.get("mqtt_topic")

    coordinator = LoRaAPRSCoordinator(hass, mqtt_topic)
    hass.data[DOMAIN]["coordinator"] = coordinator

    # Subscribe to MQTT
    @callback
    def mqtt_message(topic: str, payload: str, qos: int):
        _LOGGER.debug("Received MQTT: %s %s", topic, payload)

        try:
            data = json.loads(payload)
        except Exception:
            _LOGGER.warning("Invalid JSON in message: %s", payload)
            return

        coordinator.handle_aprs_message(topic, data)

    await mqtt.async_subscribe(hass, mqtt_topic, mqtt_message)

    _LOGGER.info("LoRa APRS integration subscribed to: %s", mqtt_topic)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the integration."""
    hass.data.pop(DOMAIN, None)
    return True
