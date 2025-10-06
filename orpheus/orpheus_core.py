# argus/orpheus/orpheus_core.py

"""
This module contains the OrpheusCore class, the central nervous system for the
Orpheus command-line application. It is responsible for initializing the system,
dynamically loading all command handlers, routing user queries to the
appropriate handler, and managing the interactive session.
"""

import os
import importlib
import inspect
from typing import List

from .query_handlers.base_handler import BaseHandler
from .query_handlers.chat_handler import ChatHandler
from .models.response import HandlerResponse


class OrpheusCore:
    """
    The brain of the Orpheus system.

    It orchestrates user requests by dynamically loading and routing them
    to the appropriate specialized handler, making the system modular and
    extensible.
    """

    def __init__(self):
        """
        Initializes the Core by discovering and loading all available handlers
        from the 'query_handlers' directory.
        """
        print("Initializing Orpheus Core...")
        self.handlers: List[BaseHandler] = self._load_handlers()
        print(f"✅ Orpheus Core ready with {len(self.handlers)} loaded handlers.")

    def _load_handlers(self) -> List[BaseHandler]:
        """
        Dynamically discover, import, and instantiate all handler classes.

        This method scans the 'query_handlers' directory for Python files,
        imports them as modules, inspects them to find subclasses of
        BaseHandler, and creates an instance of each. This "plug-and-play"
        mechanism allows for easy addition of new capabilities to Orpheus
        by just adding a new handler file.

        Returns:
            A list of instantiated handler objects, with ChatHandler
            guaranteed to be the last element.
        """
        loaded_handlers = []
        handler_directory = os.path.join(os.path.dirname(__file__), "query_handlers")
        
        print("Scanning for handlers...")
        for filename in os.listdir(handler_directory):
            # Process only Python files, excluding special files like __init__.py
            # or the base class file itself.
            if filename.endswith(".py") and not filename.startswith("__") and "base_handler" not in filename:
                # Construct the full module path required for dynamic import
                # (e.g., 'argus.orpheus.query_handlers.git_handler').
                module_path = f"orpheus.query_handlers.{filename[:-3]}"
                # module = importlib.import_module(module_path, package=__package__)
                
                try:
                    # Programmatically import the module using its path.
                    module = importlib.import_module(module_path)
                    
                    # Inspect the imported module to find any class that is a
                    # subclass of our BaseHandler contract.
                    for _, member_class in inspect.getmembers(module, inspect.isclass):
                        if issubclass(member_class, BaseHandler) and member_class is not BaseHandler:
                            # An instance of the discovered handler is created and added.
                            loaded_handlers.append(member_class())
                            print(f"   -> Handler loaded: {member_class.__name__}")

                except ImportError as e:
                    print(f"⚠️  Could not load handler from {filename}: {e}")

        # Sort handlers alphabetically by class name for predictable behavior.
        loaded_handlers.sort(key=lambda h: h.__class__.__name__)

        # It is critical to move the ChatHandler to the end of the list.
        # As the fallback handler, it must only be tried after all specialized
        # handlers have declined to process the query.
        for i, handler in enumerate(loaded_handlers):
            if isinstance(handler, ChatHandler):
                chat_handler_instance = loaded_handlers.pop(i)
                loaded_handlers.append(chat_handler_instance)
                print("   -> Fallback handler (ChatHandler) moved to the end of the chain.")
                break
        
        return loaded_handlers

    def route_query(self, query: str) -> HandlerResponse:
        """
        Route the user's query to the first available handler that can process it.

        It iterates through the loaded handlers in their established order.
        The first handler to return True from its can_handle() method gets
        to process the query and its response is returned.

        Args:
            query: The user input string.

        Returns:
            A HandlerResponse object from the selected handler, or a
            "not_handled" response if no suitable handler is found.
        """
        print(f"\n▶ Processing command: '{query}'")
        for handler in self.handlers:
            if handler.can_handle(query):
                # Delegate processing to the appropriate handler.
                return handler.process(query)
        
        # If the loop completes, no handler could process the query.
        # We return a consistent HandlerResponse to signal this.
        return HandlerResponse(
            status="not_handled",
            display_message="Sorry, Architect. I don't have a handler for this task."
        )

    def display_response(self, response: HandlerResponse):
        """
        Provide a consistent, user-friendly display for any response.

        This decouples the presentation logic from the handlers' processing
        logic. It interprets the status of the HandlerResponse object and
        prints an appropriately formatted message to the console.

        Args:
            response: The HandlerResponse object returned by route_query.
        """
        if response.status == "success":
            print(f"✅ {response.display_message}")
        elif response.status == "failed":
            print(f"❌ Execution failed: {response.display_message}")
        elif response.status == "not_handled":
            print(f"❔ {response.display_message}")
        else:
            # A catch-all for any unexpected status types.
            print(f"⚠️  Unknown response: {response}")

    def start_interactive_session(self):
        """
        Start the main application loop (the command-line interface).

        This method creates a persistent session where the user can repeatedly
        enter commands. It handles user input, routing, and response display
        until the user decides to exit.
        """
        print("\n--- Interactive Session with Orpheus Started ---")
        print("Type 'exit' or 'quit' to end the session.")
        
        while True:
            try:
                # The input prompt for the user.
                query = input("\nArchitect> ")
                if query.lower() in ["exit", "quit"]:
                    print("Ending session. See you next time, Architect.")
                    break
                
                # Ignore empty input and re-prompt.
                if not query.strip():
                    continue

                # The core workflow: route query and display response.
                response = self.route_query(query)
                self.display_response(response)

            except KeyboardInterrupt:
                # Ensure a graceful exit if the user presses Ctrl+C.
                print("\nSession interrupted by user. Shutting down.")
                break
            except Exception as e:
                # Top-level exception handler to prevent the app from crashing.
                print(f"\nAn unexpected error occurred in the Core: {e}")

def main():
    """
    The main entry point for the Orpheus application.
    This function creates an instance of the Core and starts the session.
    """
    orpheus = OrpheusCore()
    orpheus.start_interactive_session()


# This standard Python construct ensures that main() is called only when
# the script is executed directly (e.g., `python -m argus.orpheus.orpheus_core`).
if __name__ == "__main__":
    main()