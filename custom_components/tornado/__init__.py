# __init__.py
"""The AUX AC integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# Updated import name
from .aux_cloud import AuxCloudAPI
from .const import CONF_EMAIL, CONF_PASSWORD, CONF_REGION, DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

PLATFORMS: list[Platform] = [Platform.CLIMATE]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AUX AC from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})

    client = AuxCloudAPI(
        email=entry.data[CONF_EMAIL],
        password=entry.data[CONF_PASSWORD],
        region=entry.data[CONF_REGION],
        session=async_get_clientsession(hass),
    )

    try:
        await client.login()
    except Exception as err:
        await client.cleanup()
        _LOGGER.exception("Failed to connect to AUX AC")
        message = "Failed to connect to AUX AC"
        raise ConfigEntryNotReady(message) from err

    hass.data[DOMAIN][entry.entry_id]["client"] = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
        client = entry_data.get("client")

        if client:
            await client.cleanup()

        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
