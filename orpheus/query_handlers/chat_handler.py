# argus/orpheus/query_handlers/chat_handler.py

from .base_handler import BaseHandler
from ..services import gemini_client
from ..models.response import HandlerResponse

class ChatHandler(BaseHandler):
    """
    A default handler to answer general questions using the Gemini API.

    This handler is designed to be the "fallback" in the Orpheus system.
    If no other specialized handler can process a query, this one will,
    allowing Orpheus to have general conversational abilities.
    """

    def can_handle(self, query: str) -> bool:
        """
        Determines if this handler can process the query.

        Returns True for any query, as it's the default catch-all handler.
        It must be placed last in the handler list within OrpheusCore.
        """
        return True
    
    def _build_personality_prompt(self, query: str) -> str:
        """
        Constructs the full prompt by injecting the Orpheus persona
        before the user's query. This ensures the AI responds in character.
        """
        # This multi-line string defines the persona for Orpheus. It provides
        # the AI with context about its role, capabilities, and tone, ensuring
        # consistent and in-character responses.
        persona = (
            "You are Orpheus, a wise and articulate AI assistant to a user you refer to as 'the Architect'.\n"
            "You currently operate through a Command-Line Interface (CLI).\n"
            "Your purpose is to be a foundational part of the Architect's 'Argus' ecosystem, acting as an intelligent development partner.\n"
            "Your core intelligence is powered by Google's Gemini model, which you access securely via an API key.\n"
            "Your current capabilities are provided by your 'handlers':\n"
            "- GitHandler: To analyze code changes and suggest professional commit messages.\n"
            "- SystemHandler: To execute simple system commands, like clearing the terminal screen.\n"
            "- ChatHandler (this is you): To answer general questions and provide information.\n"
            "Your tone is knowledgeable, precise, and slightly philosophical, often using musical metaphors. You are a partner in creation.\n"
            "Now, answer the Architect's following query:\n\n"
            f"Architect: \"{query}\""
        )
        return persona

    def process(self, query: str) -> HandlerResponse:
        """
        Processes the general question by building the persona prompt
        and fetching the response from the Gemini API.
        """
        print("Chat Handler activated.")

        # 1. Construct the full prompt including the persona.
        full_prompt = self._build_personality_prompt(query)
        
        # 2. Delegate the API call to the centralized client.
        answer, error = gemini_client.query(full_prompt)

        if error:
            return HandlerResponse(status="failed", display_message=error)
        
        # 3. Format the successful response for display by the Core.
        return HandlerResponse(
            status="success",
            display_message=f"\n🎶 Orpheus:\n{answer}\n"
        )