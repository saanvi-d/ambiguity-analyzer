"""
Interactive interface for the NLP Ambiguity Analyzer.
"""

from llm_client import AmbiguityClient


def main():
    client = AmbiguityClient()

    print("=" * 60)
    print("NLP AMBIGUITY ANALYZER")
    print("=" * 60)
    print("Enter a paragraph to analyze.")
    print("Type 'quit' to exit.")
    print()

    while True:

        text = input("Enter paragraph: ").strip()

        if text.lower() == "quit":
            print("Exiting...")
            break

        if not text:
            print("Please enter some text.")
            continue

        print("\nAnalyzing...\n")

        findings = client.analyze(text)

        if findings is None:
            print("Analysis failed. Please try again.")
            continue

        if not findings:
            print("No ambiguity detected.")
            continue

        print(f"Found {len(findings)} ambiguity finding(s):\n")

        for i, finding in enumerate(findings, start=1):

            print(f"Ambiguity {i}")
            print("-" * 40)

            print("Sentence:")
            print(finding.get("sentence", "N/A"))

            print("\nAmbiguous span:")
            print(finding.get("span", "N/A"))

            print("\nType:")
            print(finding.get("type", "N/A"))

            print("\nPossible interpretations:")

            for interpretation in finding.get(
                "interpretations", []
            ):
                print(f"- {interpretation}")

            print("\nSuggested rewrite:")
            print(finding.get("suggested_rewrite", "N/A"))

            print()


if __name__ == "__main__":
    main()