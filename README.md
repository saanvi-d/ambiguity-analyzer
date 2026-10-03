# NLP Ambiguity & Miscommunication Analyzer

An NLP-based application that detects linguistic ambiguity in text and uses a Large Language Model (LLM) to explain possible interpretations and suggest clearer rewrites.

The system analyzes user-provided sentences for four types of linguistic ambiguity:

- Lexical ambiguity
- Syntactic ambiguity
- Referential ambiguity
- Pragmatic ambiguity

## Features

- Accepts a sentence or short text as input
- Detects genuine linguistic ambiguity
- Identifies the ambiguous phrase
- Classifies the ambiguity type
- Provides multiple possible interpretations
- Generates a clearer rewrite
- Uses the Gemini API as the LLM component
- Returns structured JSON responses for reliable processing
- Provides an interactive command-line interface
- Includes a test dataset and evaluation script

## How It Works

```text
User enters a sentence
        |
        v
Prompt construction
        |
        v
Gemini LLM
        |
        v
Ambiguity detection
        |
        +-------------------------------+
        |        |          |            |
        v        v          v            v
     Lexical  Syntactic  Referential  Pragmatic
        |        |          |            |
        +--------+----------+------------+
                         |
                         v
              Possible interpretations
                         |
                         v
                  Suggested rewrite
                         |
                         v
                       Output