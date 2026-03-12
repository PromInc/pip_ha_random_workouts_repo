import logging
import random

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_JSON_URLS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry):
    _LOGGER.debug("Setting up PIP HA Random Workouts entry %s", entry.entry_id)

    # Forward to sensor platform and wait for it
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    async def pick_random_workout(call: ServiceCall):
        category_target = call.data.get("category", "").strip().lower()
        media_player = call.data.get("entity_id")

        raw_urls = entry.data.get(CONF_JSON_URLS, "")
        url_map = {}
        for line in raw_urls.split("\n"):
            if "|" in line:
                name, url = line.split("|", 1)
                url_map[name.strip().lower()] = url.strip()

        target_url = url_map.get(category_target)
        if not target_url:
            _LOGGER.error("Category %s not found in config", category_target)
            return

        session = async_get_clientsession(hass)
        async with session.get(target_url) as response:
            workouts = await response.json()
        workout = random.choice(workouts)

        hass.bus.async_fire(
            f"{DOMAIN}_update_{category_target}",
            {
                "title": workout.get("title"),
                "video_url": workout.get("url"),
                "video_id": workout.get("url").split("v=")[-1]
                if "v=" in workout.get("url")
                else "",
            },
        )

        if media_player:
            await hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": media_player,
                    "media_content_id": workout.get("url"),
                    "media_content_type": "url",
                },
            )

    hass.services.async_register(DOMAIN, "pick_random", pick_random_workout)

    # IMPORTANT: must return a bool
    return True
