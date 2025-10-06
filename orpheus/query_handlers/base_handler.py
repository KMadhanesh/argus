# argus/orpheus/query_handlers/base_handler.py

from abc import ABC, abstractmethod

class BaseHandler(ABC):
    """
    Abstract Base Class for all query handlers in the Orpheus system.

    This class defines the standard interface that every handler must implement.
    By inheriting from this class, we ensure that Orpheus Core can interact
    with any handler in a consistent way, making the system modular and
    easily extensible.
    """

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """
        Determines if this handler is capable of processing the given query.

        Args:
            query (str): The user's input command.

        Returns:
            bool: True if the handler can process the query, False otherwise.
        """
        pass

    @abstractmethod
    def process(self, query: str) -> dict:
        """
        Processes the query and performs the corresponding action.

        This method contains the core logic of the handler. It should only be
        called if can_handle() returns True.

        Args:
            query (str): The user's input command.

        Returns:
            dict: A dictionary containing the result of the operation,
                  typically including a 'status' key ('success' or 'failed')
                  and a 'message' or other relevant data.
        """
        pass