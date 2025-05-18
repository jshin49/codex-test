"""Client implementations for each LLM used by the orchestrator."""

from __future__ import annotations

import os
from typing import Iterable

import openai
import anthropic
import google.generativeai as genai
from googletrans import Translator


class TriClient:
    """Client for the Tri LLM including translation helpers."""

    def __init__(self) -> None:
        self.translator = Translator()

    def translate_to_english(self, korean_text: str) -> str:
        """Translate Korean text to English using Google Translate."""
        result = self.translator.translate(korean_text, src="ko", dest="en")
        return result.text

    def translate_to_korean(self, english_text: str) -> str:
        """Translate English text back to Korean using Google Translate."""
        result = self.translator.translate(english_text, src="en", dest="ko")
        return result.text

    def score_responses(self, prompt: str, responses: Iterable[str]) -> str:
        """Return the best response according to a simple heuristic."""
        return max(responses, key=len)


class GeminiClient:
    """Client for Google's Gemini model."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-pro") -> None:
        api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_response(self, prompt: str) -> str:
        result = self.model.generate_content(prompt)
        return result.text


class ChatGPTClient:
    """Client for OpenAI's ChatGPT models."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo") -> None:
        self.model = model
        openai.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY is not configured")

    def generate_response(self, prompt: str) -> str:
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content.strip()


class ClaudeClient:
    """Client for Anthropic's Claude models."""

    def __init__(self, api_key: str | None = None, model: str = "claude-3-opus-20240229") -> None:
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate_response(self, prompt: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
