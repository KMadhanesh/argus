# argus/orpheus/query_handlers/git_handler.py

import subprocess
from .base_handler import BaseHandler
from ..services import gemini_client
from ..models.response import HandlerResponse

class GitHandler(BaseHandler):
    """
    Handles interactions with local Git repositories.

    Its primary function is to analyze staged code changes and use the Gemini
    API to suggest a professional, well-formatted commit message, acting as
    an intelligent development partner.
    """

    def can_handle(self, query: str) -> bool:
        """
        Determines if this handler can process the query.

        Listens for the specific keyword "commit msg" to provide a commit
        message suggestion.
        """
        query = query.lower()
        return "commit msg" in query

    def _get_staged_diff(self):
        """
        Executes the 'git diff --staged' command to capture all changes
        that are ready to be committed.
        """
        try:
            # The 'subprocess.run' command executes shell commands from Python.
            result = subprocess.run(
                ['git', 'diff', '--staged'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            # If stdout is empty, it means no files were added with 'git add'.
            if not result.stdout:
                return None, "There are no changes staged. Use 'git add <file>' first."
            return result.stdout, None
        except subprocess.CalledProcessError as e:
            # This handles errors if 'git diff' itself fails.
            return None, f"Error executing git diff: {e.stderr}"
        except FileNotFoundError:
            # This handles the case where Git is not installed or not in the system's PATH.
            return None, "Command 'git' not found. This handler must be run inside a Git repository."

    def _build_prompt(self, diff_text: str) -> str:
        """
        Constructs a detailed, rule-based prompt for the Gemini API to ensure
        it generates a high-quality, conventional commit message.
        """
        return f"""
        As Orpheus, an expert software engineering assistant, your task is to generate a precise and complete commit message based on the provided 'git diff'.

        RULES:
        1.  Strictly follow the "Conventional Commits" standard.
        2.  The final output must be only the commit message itself.
        3.  The message must have the following structure:
            <type>(<scope>): <subject>
            <blank line>
            [optional body: explain the 'why' and 'how' of the change in more detail.]
            <blank line>
            [optional footer: for referencing issues, e.g., 'Closes #123'.]
        4.  The subject line must be in lowercase and not end with a period.
        5.  The message must focus on the *intent* of the change.

        Based on the following diff, generate the complete commit message:
        ---
        {diff_text}
        ---
        """

    def process(self, query: str) -> HandlerResponse:
        """
        Orchestrates the process of getting a commit suggestion:
        1. Gets the staged diff.
        2. Builds the prompt.
        3. Queries the AI.
        4. Formats the final response.
        """
        print("Git Handler activated.")
        
        diff_text, error = self._get_staged_diff()
        if error:
            return HandlerResponse(status="failed", display_message=error)

        print("🎶 Building prompt and querying the AI...")
        full_prompt = self._build_prompt(diff_text)
        # The handler delegates the API call to the centralized client.
        suggestion, error = gemini_client.query(full_prompt)

        if error:
            return HandlerResponse(status="failed", display_message=error)
        
        display_message = (
            "\n🎶 AI-Generated Commit Suggestion:\n\n"
            "--------------------------------------\n"
            f"{suggestion}\n"
            "--------------------------------------\n"
        )
        
        return HandlerResponse(
            status="success",
            display_message=display_message
        )