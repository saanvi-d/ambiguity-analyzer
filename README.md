# NLP Ambiguity & Miscommunication Analyzer

An NLP-based application that detects linguistic ambiguity in text and uses a Large Language Model (LLM) to explain possible interpretations and suggest clearer rewrites.

The system accepts a paragraph and analyzes it for four types of ambiguity:

- Lexical ambiguity
- Syntactic ambiguity
- Referential ambiguity
- Pragmatic ambiguity

## Features

- Accepts complete paragraphs as input
- Uses paragraph context when analyzing ambiguity
- Identifies the sentence containing the ambiguity
- Extracts the ambiguous phrase
- Classifies the ambiguity type
- Provides multiple possible interpretations
- Generates a clearer rewrite
- Uses the Gemini API as the LLM component
- Returns structured JSON responses for reliable processing
- Provides an interactive command-line interface

## How It Works

```text
User enters a paragraph
          |
          v
   Paragraph analysis
          |
          v
      Gemini LLM
          |
          v
   Ambiguity detection
          |
     +----+----+----+
     |    |    |    |
     v    v    v    v
  Lexical Syntactic Referential Pragmatic
          |
          v
 Possible interpretations
          |
          v
   Suggested rewrite
          |
          v
       Output