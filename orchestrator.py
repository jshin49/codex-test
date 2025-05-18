"""Simple orchestrator that routes prompts through multiple LLMs."""

from __future__ import annotations

import os

from llm_clients import TriClient, GeminiClient, ChatGPTClient, ClaudeClient


class Orchestrator:
    """Main orchestrator that delegates prompts to each LLM."""

    def __init__(self) -> None:
        self.tri = TriClient()
        self.gemini = GeminiClient(api_key=os.environ.get("GEMINI_API_KEY"))
        self.chatgpt = ChatGPTClient(api_key=os.environ.get("OPENAI_API_KEY"))
        self.claude = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def chat(self, user_input: str) -> str:
        """Process user input in Korean and return a Korean response."""
        english_prompt = self.tri.translate_to_english(user_input)
        responses = [
            self.gemini.generate_response(english_prompt),
            self.chatgpt.generate_response(english_prompt),
            self.claude.generate_response(english_prompt),
        ]
        best_response = self.tri.score_responses(english_prompt, responses)
        return self.tri.translate_to_korean(best_response)


def main() -> None:
    orchestrator = Orchestrator()
    try:
        while True:
            user_input = input("User (Korean): ")
            if not user_input:
                break
            reply = orchestrator.chat(user_input)
            print(f"AI: {reply}")
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
