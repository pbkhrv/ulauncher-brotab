"""
Extension event listeners
"""
import time
from brotab_ulauncher.wmctrl import iter_windows, activate_window_by_id
from ulauncher.api.client.EventListener import EventListener


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """
    def on_event(self, event, extension):
        """ Handles the event """
        keyword = event.get_keyword() or ""
        valid_keywords = ["cltab", "cl", "clt"]
        if keyword in valid_keywords:
            extension.mode = "killer"
        else:
            extension.mode = "activator"

        return extension.search_tabs(event)


def activate_window_with_title(title):
    for id, name in iter_windows():
        if title in name:
            activate_window_by_id(id)
            return
    print(f"No window found with title '{title}'")


class ItemEnterEventListener(EventListener):
    """ Listener that handles the click on an item """

    # pylint: disable=unused-argument,no-self-use
    def on_event(self, event, extension):
        """ Handles the event """
        data = event.get_data()
        if data["mode"] == "activator":
            extension.brotab_client.activate_tab(data["tab"])
            time.sleep(0.5)
            activate_window_with_title(data["name"])
        if data["mode"] == "killer":
            try:
                extension.brotab_client.close_tab(data["tab"])
            except Exception as error:
                extension.logger.error(error)

            extension.logger.info("Tab closed")
