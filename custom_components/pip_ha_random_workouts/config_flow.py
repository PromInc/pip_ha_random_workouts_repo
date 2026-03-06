import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_JSON_URLS

class PIPHARandomWorkoutsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PIP HA Random Workouts."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters their JSON URLs."""
        errors = {}

        if user_input is not None:
            # You could add validation logic here to check if the URLs are reachable
            return self.async_create_entry(
                title="PIP Random Workouts", 
                data=user_input
            )

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_JSON_URLS): str,
            }),
            description_placeholders={
                "instructions": "Enter your JSON URLs separated by commas."
            },
            errors=errors,
        )