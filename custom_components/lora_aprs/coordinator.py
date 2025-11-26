async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the LoRa APRS integration."""
    hass.data.setdefault(DOMAIN, {})

    mqtt_topic = entry.data.get("mqtt_topic")

    coordinator = LoRaAPRSCoordinator(hass, mqtt_topic)
    hass.data[DOMAIN]["coordinator"] = coordinator

    # Load sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Subscribe to MQTT
    @callback
    def mqtt_message(topic: str, payload: str, qos: int):
        _LOGGER.debug("Received MQTT: %s %s", topic, payload)

        try:
            data = json.loads(payload)
        except Exception:
            _LOGGER.warning("Invalid JSON: %s", payload)
            return

        coordinator.handle_aprs_message(topic, data)

    await mqtt.async_subscribe(hass, mqtt_topic, mqtt_message)

    return True
