"""Formats ambiguity findings for readable console output."""


def print_report(text: str, findings: list):
    print("\n" + "=" * 60)
    print(f"INPUT: {text}")
    print("=" * 60)

    if not findings:
        print("No ambiguity detected.")
        return

    for i, finding in enumerate(findings, 1):
        print(f"\n[{i}] Span: \"{finding.get('span', '?')}\"")
        print(f"    Type: {finding.get('type', '?')}")
        print("    Possible readings:")
        for interp in finding.get("interpretations", []):
            print(f"      - {interp}")
        print(f"    Suggested rewrite: {finding.get('suggested_rewrite', '?')}")
