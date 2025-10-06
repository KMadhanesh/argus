# argus/orpheus/query_handlers/system_handler.py

import os
import platform
from .base_handler import BaseHandler
from ..models.response import HandlerResponse

class SystemHandler(BaseHandler):
    """
    Handles system-level commands that interact with the operating system,
    such as clearing the terminal screen.
    """

    def can_handle(self, query: str) -> bool:
        """
        Checks if the query is a command to clear the screen.
        to make the handler more user-friendly.
        """
        query = query.lower()
        # Listens for common clear-screen commands on both Windows ('cls') and Unix ('clear').
        return query in ["cls"]

    def _clear_screen(self) -> str:
        """
        Clears the terminal screen in a cross-platform way by executing
        the appropriate system command.
        """
        # Determines the correct command based on the operating system.
        command = 'cls' if platform.system() == "Windows" else 'clear'
        os.system(command)
        return "Terminal screen has been cleared."

    def process(self, query: str) -> HandlerResponse:
        """

        Processes the system command by calling the clear screen function.
        """
        message = self._clear_screen()
        
        # The primary action is visual (clearing the screen), but we return
        # a success message for consistency with the Orpheus architecture.
        return HandlerResponse(
            status="success",
            display_message=f"🎶 {message}"
        )