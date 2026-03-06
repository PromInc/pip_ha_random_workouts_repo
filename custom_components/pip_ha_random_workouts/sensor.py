from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([RandomWorkoutSensor(hass)], True)

class RandomWorkoutSensor(SensorEntity):
    def __init__(self, hass):
        self.hass = hass
        self._attr_name = "PIP HA Random Workout"
        self._attr_unique_id = f"{DOMAIN}_current_workout"
        self._state = "Ready"
        self._attributes = {}

        # Listen for updates from the service call
        hass.bus.async_listen(f"{DOMAIN}_updated", self._update_handler)

    def _update_handler(self, event):
        self._state = event.data.get("title")
        self._attributes = {
            "video_url": event.data.get("video_url"),
            "video_id": event.data.get("video_id")
        }
        self.async_write_ha_state()

    @property
    def state(self): return self._state

    @property
    def extra_state_attributes(self): return self._attributes