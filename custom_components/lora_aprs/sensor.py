"""Improved dynamic APRS sensors for LoRa APRS MQTT Monitor."""

from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    TEMP_CELSIUS,
    PERCENTAGE,
    PRESSURE_HPA,
)

from . import DOMAIN
from .coordinator import LoRaAPRSCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up APRS sensors."""

    coordinator: LoRaAPRSCoordinator = hass.data[DOMAIN]["coordinator"]
    entities = {}

    @callback
    def handle_update(event):
        callsign = event.data["callsign"]
        data = coordinator.stations.get(callsign)

        if not data:
            return

        if callsign not in entities:
            sensors = [
                APRSTemperatureSensor(callsign, data),
                APRSHumiditySensor(callsign, data),
                APRSBatterySensor(callsign, data),
                APRSPressureSensor(callsign, data),
                APRSGPSSensor(callsign, data),
            ]
            entities[callsign] = sensors
            async_add_entities(sensors)
        else:
            for sensor in entities[callsign]:
                sensor.update_from_aprs(data)
                sensor.async_write_ha_state()

    hass.bus.async_listen("lora_aprs_updated", handle_update)


# ------------------------------------------------------------------
# BASE SENSOR CLASS
# ------------------------------------------------------------------

class APRSSensorBase(SensorEntity):
    """Base class for APRS sensors."""

    device_class = None
    state_class = "measurement"

    def __init__(self, callsign: str, data: dict):
        self.callsign = callsign
        self._data = data
        self._attr_name = f"{callsign} {self.sensor_type.title()}"
        self._attr_unique_id = f"lora_aprs_{callsign}_{self.sensor_type}".lower()

    def update_from_aprs(self, data: dict):
        self._data = data

    @property
    def device_info(self):
        """Group sensors under the APRS station device."""
        return {
            "identifiers": {(DOMAIN, self.callsign)},
            "name": f"APRS Station {self.callsign}",
            "manufacturer": "LoRa APRS",
            "model": "iGate / Digi",
        }


# ------------------------------------------------------------------
# INDIVIDUAL SENSORS
# ------------------------------------------------------------------

class APRSTemperatureSensor(APRSSensorBase):
    sensor_type = "temperature"
    device_class = "temperature"
    native_unit_of_measurement = TEMP_CELSIUS

    @property
    def native_value(self):
        return self._data.get("temp")


class APRSHumiditySensor(APRSSensorBase):
    sensor_type = "humidity"
    device_class = "humidity"
    native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self):
        return self._data.get("hum")


class APRSBatterySensor(APRSSensorBase):
    sensor_type = "battery"
    device_class = "battery"
    native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self):
        return self._data.get("batt")


class APRSPressureSensor(APRSSensorBase):
    sensor_type = "pressure"
    device_class = "pressure"
    native_unit_of_measurement = PRESSURE_HPA

    @property
    def native_value(self):
        return self._data.get("pressure")


class APRSGPSSensor(APRSSensorBase):
    sensor_type = "gps"
    device_class = "location"

    @property
    def native_value(self):
        if "lat" in self._data and "lon" in self._data:
            return f"{self._data['lat']},{self._data['lon']}"
        return None
