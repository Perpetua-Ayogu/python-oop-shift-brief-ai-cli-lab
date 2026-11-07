if __package__:
    from .ai_client import OllamaChatClient
    from .brief_builder import HandoffBriefBuilder
else:
    from ai_client import OllamaChatClient
    from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """
        Initialize the CLI application.

        Requirements:
        - Store the injected AI client.
        - Use the provided brief builder when one is passed in.
        - Create a HandoffBriefBuilder when one is not passed in.
        - Set self.running to True.
        """
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """
        Print a welcome message and command guidance.

        Requirements:
        - Mention that this is a shift handoff brief CLI.
        - Include the available commands.
        """
        print("Shift Handoff Brief CLI")
        print(self.command_help())

    def command_help(self):
        """
        Return command guidance as a string.

        Required commands:
        - brief <shift notes>
        - revise <feedback>
        - history
        - reset
        - help
        - exit
        - quit
        """
        return (
            "brief <shift notes> - Create a brief\n"
            "revise <feedback> - Revise the previous brief\n"
            "history - Show conversation message count\n"
            "reset - Clear history\nhelp - Show commands\nexit or quit - Stop"
        )

    def handle_command(self, raw_input):
        """
        Route a user command.

        Requirements:
        - Return a readable input error for blank input.
        - Commands should be case-insensitive.
        - Extra spaces around commands should not break the app.
        - brief <shift notes> should call the brief builder's create_brief().
        - revise <feedback> should call the brief builder's revise_brief().
        - history should return the current message count.
        - reset should clear conversation history.
        - help should return command guidance.
        - exit and quit should stop the application.
        - Unknown commands should return a readable input error.
        - ValueError should become a readable Input Error.
        - RuntimeError should become a readable Service Error.
        """
        if not isinstance(raw_input, str) or not raw_input.strip():
            return "Input Error: Enter a command."
        parts = raw_input.strip().split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""
        try:
            if command == "brief":
                if not payload:
                    raise ValueError("Shift notes cannot be empty.")
                return self.brief_builder.create_brief(self.ai_client, payload)
            if command == "revise":
                if not payload:
                    raise ValueError("Revision feedback cannot be empty.")
                return self.brief_builder.revise_brief(self.ai_client, payload)
            if command == "history":
                return f"Conversation messages: {self.ai_client.message_count()}"
            if command == "reset":
                self.ai_client.reset()
                return "Conversation history reset."
            if command == "help":
                return self.command_help()
            if command in ("exit", "quit"):
                self.running = False
                return "Goodbye!"
            return "Input Error: Unknown command. Type help for commands."
        except ValueError as error:
            return f"Input Error: {error}"
        except RuntimeError as error:
            return f"Service Error: {error}"

    def run(self):
        """
        Run the CLI input loop.

        Requirements:
        - Display the welcome message before the loop starts.
        - Continue while self.running is True.
        - Read user input.
        - Pass user input to handle_command().
        - Print returned messages.
        - Stop cleanly if EOFError occurs.
        """
        self.display_welcome()
        while self.running:
            try:
                command = input("> ")
            except (EOFError, KeyboardInterrupt):
                self.running = False
                print("Goodbye!")
                break
            print(self.handle_command(command))


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()
