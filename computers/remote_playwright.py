from playwright.sync_api import Browser, Page
from .base_playwright import BasePlaywrightComputer

class RemotePlaywrightComputer(BasePlaywrightComputer):
    """Connects to a remote Playwright instance."""

    def __init__(self, remote_url: str, headless: bool = True):
        super().__init__()
        self.remote_url = remote_url
        self.headless = headless

    def _get_browser_and_page(self) -> tuple[Browser, Page]:
        connection_url = self.remote_url
        
        browser = self._playwright.chromium.connect_over_cdp(connection_url)
        context = browser.new_context()
        
        # Add event listeners for page creation and closure
        context.on("page", self._handle_new_page)
        
        page = context.new_page()
        page.set_viewport_size({"width": self.dimensions[0], "height": self.dimensions[1]})
        page.on("close", self._handle_page_close)

        page.goto("https://bing.com")
        
        return browser, page
        
    def _handle_new_page(self, page: Page):
        """Handle the creation of a new page."""
        print("New page created")
        self._page = page
        page.on("close", self._handle_page_close)
        
    def _handle_page_close(self, page: Page):
        """Handle the closure of a page."""
        print("Page closed")
        if self._page == page:
            if self._browser.contexts[0].pages:
                self._page = self._browser.contexts[0].pages[-1]
            else:
                print("Warning: All pages have been closed.")
                self._page = None
