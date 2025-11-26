"""Config flow for LoRa APRS MQTT Monitor."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

DOMAIN = "lora_aprs"
CONF_MQTT_TOPIC = "mqtt_topic"


class LoRaAPRSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LoRa APRS MQTT Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Start config flow."""
        if user_input is not None:
            # Prevent multiple instances of the integration
            await self.async_set_unique_id("lora_aprs_unique_instance")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="LoRa APRS MQTT Monitor",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_MQTT_TOPIC, default="lora/#"): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
