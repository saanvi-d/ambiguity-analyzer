"""
Wraps the Gemini API call for the ambiguity analyzer.

Uses Google's current GenAI SDK and structured JSON output.
"""

import os
import yaml
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal


class AmbiguityFinding(BaseModel):
    sentence: str
    span: str
    type: Literal[
        "lexical",
        "syntactic",
        "referential",
        "pragmatic"
    ]

    interpretations: list[str]
    suggested_rewrite: str


class AmbiguityResponse(BaseModel):
    findings: list[AmbiguityFinding]


class AmbiguityClient:

    def __init__(self, config_path="config.yaml"):
        load_dotenv()

        # Load configuration
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. "
                "Copy .env.example to .env and add your key."
            )

        # Create Gemini client
        self.client = genai.Client(api_key=api_key)

        # Load prompt
        with open(
            self.config["prompt_path"],
            "r",
            encoding="utf-8"
        ) as f:
            self.prompt_template = f.read()

    def _build_prompt(self, text: str) -> str:
        """Insert the user's sentence into the prompt."""
        return self.prompt_template.replace(
            "{{INPUT_TEXT}}",
            text
        )

    def analyze(self, text: str) -> list:
        """
        Sends one sentence/message to Gemini and returns
        a list of ambiguity findings.
        """

        prompt = self._build_prompt(text)

        try:
            response = self.client.models.generate_content(
                model=self.config["model_name"],
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.config.get(
                        "temperature",
                        0.2
                    ),
                    max_output_tokens=self.config.get(
                        "max_output_tokens",
                        2048
                    ),
                    response_mime_type="application/json",
                    response_schema=AmbiguityResponse,
                ),
            )

            # Structured response from Gemini
            if response.parsed is not None:
                result = response.parsed

                return [
                    finding.model_dump()
                    for finding in result.findings
                ]

            print(
                "[llm_client] Model returned no parsed response."
            )
            return []

        except Exception as e:
            print(
                f"[llm_client] API call failed: {e}"
            )
            print(
                "[llm_client] The sentence could not be analyzed."
            )
            return None