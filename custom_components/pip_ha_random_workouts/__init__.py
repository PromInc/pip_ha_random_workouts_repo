import logging
import random
import aiohttp
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_JSON_URLS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    # Store the URLs from the config flow
    urls = [url.strip() for url in entry.data[CONF_JSON_URLS].split(",") if url.strip()]
    
    async def pick_random_workout(call: ServiceCall):
        """The core service used by both Automations and Dashboard buttons."""
        target_entity = call.data.get("entity_id") # Optional TV entity
        session = async_get_clientsession(hass)

        try:
            # 1. Pick a random URL from your list
            list_url = random.choice(urls)
            async with session.get(list_url) as response:
                workouts = await response.json()
                workout = random.choice(workouts)
                
                title = workout.get("title", "Unknown Workout")
                video_url = workout.get("url")
                # Extract ID for the dashboard player (e.g., dQw4w9WgXcQ)
                video_id = video_url.split("v=")[-1] if "v=" in video_url else video_url.split("/")[-1]

                # 2. Update the Global Sensor (This updates the Dashboard)
                hass.bus.async_fire(f"{DOMAIN}_updated", {
                    "title": title,
                    "video_url": video_url,
                    "video_id": video_id
                })
                
                # 3. Automation Path: Send to TV if specified
                if target_entity:
                    await hass.services.async_call("media_player", "play_media", {
                        "entity_id": target_entity,
                        "media_content_id": video_url,
                        "media_content_type": "url"
                    })
        except Exception as e:
            _LOGGER.error("Failed to fetch workout: %s", e)

    hass.services.async_register(DOMAIN, "pick_random", pick_random_workout)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True