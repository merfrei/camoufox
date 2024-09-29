from typing import Any, Dict, List, Optional, Union

from browserforge.fingerprints import Fingerprint, Screen
from playwright.async_api import Browser, Playwright, PlaywrightContextManager

from .addons import DefaultAddons
from .utils import ListOrString, get_launch_options


class AsyncCamoufox(PlaywrightContextManager):
    """
    Wrapper around playwright.async_api.PlaywrightContextManager that automatically
    launches a browser and closes it when the context manager is exited.
    """

    def __init__(self, **launch_options):
        super().__init__()
        self.launch_options = launch_options
        self.browser: Optional[Browser] = None

    async def __aenter__(self) -> Browser:
        _playwright = await super().__aenter__()
        self.browser = await AsyncNewBrowser(_playwright, **self.launch_options)
        return self.browser

    async def __aexit__(self, *args: Any):
        if self.browser:
            await self.browser.close()
        await super().__aexit__(*args)


async def AsyncNewBrowser(
    playwright: Playwright,
    *,
    config: Optional[Dict[str, Any]] = None,
    os: Optional[ListOrString] = None,
    block_images: Optional[bool] = None,
    block_webrtc: Optional[bool] = None,
    allow_webgl: Optional[bool] = None,
    geoip: Optional[Union[str, bool]] = None,
    locale: Optional[str] = None,
    addons: Optional[List[str]] = None,
    fonts: Optional[List[str]] = None,
    exclude_addons: Optional[List[DefaultAddons]] = None,
    fingerprint: Optional[Fingerprint] = None,
    screen: Optional[Screen] = None,
    executable_path: Optional[str] = None,
    firefox_user_prefs: Optional[Dict[str, Any]] = None,
    proxy: Optional[Dict[str, str]] = None,
    ff_version: Optional[int] = None,
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, Union[str, float, bool]]] = None,
    **launch_options: Dict[str, Any]
) -> Browser:
    """
    Launches a new browser instance for Camoufox.
    Accepts all Playwright Firefox launch options, along with the following:

    Parameters:
        config (Optional[Dict[str, Any]]):
            Camoufox properties to use. (read https://github.com/daijro/camoufox/blob/main/README.md)
        os (Optional[ListOrString]):
            Operating system to use for the fingerprint generation.
            Can be "windows", "macos", or "linux", or a list of these to choose from randomly.
            Default: ["windows", "macos", "linux"]
        block_images (Optional[bool]):
            Whether to block all images.
        block_webrtc (Optional[bool]):
            Whether to block WebRTC entirely.
        allow_webgl (Optional[bool]):
            Whether to allow WebGL. To prevent leaks, only use this for special cases.
        geoip (Optional[Union[str, bool]]):
            Calculate longitude, latitude, timezone, country, & locale based on the IP address.
            Pass the target IP address to use, or `True` to find the IP address automatically.
        locale (Optional[str]):
            Locale to use in Camoufox.
        addons (Optional[List[str]]):
            List of Firefox addons to use.
        fonts (Optional[List[str]]):
            Fonts to load into Camoufox (in addition to the default fonts for the target `os`).
            Takes a list of font family names that are installed on the system.
        exclude_addons (Optional[List[DefaultAddons]]):
            Default addons to exclude. Passed as a list of camoufox.DefaultAddons enums.
        fingerprint (Optional[Fingerprint]):
            Use a custom BrowserForge fingerprint. Note: Not all values will be implemented.
            If not provided, a random fingerprint will be generated based on the provided os & user_agent.
        screen (Optional[Screen]):
            NOT YET IMPLEMENTED: Constrains the screen dimensions of the generated fingerprint.
            Takes a browserforge.fingerprints.Screen instance.
        executable_path (Optional[str]):
            Custom Camoufox browser executable path.
        firefox_user_prefs (Optional[Dict[str, Any]]):
            Firefox user preferences to set.
        proxy (Optional[Dict[str, str]]):
            Proxy to use for the browser.
            Note: If geoip is True, a request will be sent through this proxy to find the target IP.
        ff_version (Optional[int]):
            Firefox version to use. Defaults to the current Camoufox version.
            To prevent leaks, only use this for special cases.
        args (Optional[List[str]]):
            Arguments to pass to the browser.
        env (Optional[Dict[str, Union[str, float, bool]]]):
            Environment variables to set.
        **launch_options (Dict[str, Any]):
            Additional Firefox launch options.
    """
    data = locals()
    data.pop('playwright')

    opt = get_launch_options(**data)
    return await playwright.firefox.launch(**opt)
