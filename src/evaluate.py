"""
Runs the ambiguity analyzer on the test dataset
and reports evaluation results.
"""

import json
import time
import yaml

from llm_client import AmbiguityClient


def load_test_data(config_path="config.yaml"):
    """Load test sentences from the configured JSON file."""

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    with open(config["test_data_path"], "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate():
    """Run the analyzer on every test sentence."""

    test_data = load_test_data()
    client = AmbiguityClient()

    total = len(test_data)

    # Evaluation metrics
    detection_correct = 0
    type_correct = 0
    ambiguous_cases = 0
    api_errors = 0

    # Error analysis
    detection_errors = []
    type_errors = []

    print("=" * 60)
    print("AMBIGUITY ANALYZER - EVALUATION")
    print("=" * 60)

    for item in test_data:

        text = item["text"]
        expected_ambiguous = item["expected_ambiguous"]
        expected_type = item["expected_type"]

        print("\n" + "-" * 60)
        print("INPUT:", text)

        findings = client.analyze(text)

        # Wait between requests to reduce rate-limit problems
        time.sleep(7)

        # --------------------------------------------------
        # API error
        # --------------------------------------------------

        if findings is None:
            api_errors += 1

            print("Expected ambiguity:", expected_ambiguous)
            print("Predicted ambiguity: API ERROR")
            print("Result: NOT EVALUATED")

            continue

        # --------------------------------------------------
        # Ambiguity detection
        # --------------------------------------------------

        predicted_ambiguous = len(findings) > 0

        if predicted_ambiguous == expected_ambiguous:
            detection_correct += 1
            detection_result = "CORRECT"
        else:
            detection_result = "INCORRECT"

            detection_errors.append({
                "id": item["id"],
                "text": text,
                "expected": expected_ambiguous,
                "predicted": predicted_ambiguous
            })

        print("Expected ambiguity:", expected_ambiguous)
        print("Predicted ambiguity:", predicted_ambiguous)
        print("Detection result:", detection_result)

        # --------------------------------------------------
        # Ambiguity type classification
        # --------------------------------------------------

        if expected_ambiguous:

            ambiguous_cases += 1

            predicted_types = {
                finding.get("type")
                for finding in findings
                if finding.get("type")
            }

            print("Expected type:", expected_type)
            print("Predicted type(s):", predicted_types)

            if expected_type in predicted_types:
                type_correct += 1
                print("Type result: CORRECT")
            else:
                print("Type result: INCORRECT")

                type_errors.append({
                    "id": item["id"],
                    "text": text,
                    "expected": expected_type,
                    "predicted": list(predicted_types)
                })

        else:
            print("Expected type: None")

    # ------------------------------------------------------
    # Calculate metrics
    # ------------------------------------------------------

    evaluated_cases = total - api_errors

    if evaluated_cases > 0:
        detection_accuracy = (
            detection_correct / evaluated_cases
        ) * 100
    else:
        detection_accuracy = 0

    if ambiguous_cases > 0:
        type_accuracy = (
            type_correct / ambiguous_cases
        ) * 100
    else:
        type_accuracy = 0

    # ------------------------------------------------------
    # Evaluation summary
    # ------------------------------------------------------

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Total test cases           : {total}")
    print(f"API failures              : {api_errors}")
    print(f"Evaluated cases            : {evaluated_cases}")

    print("\nAmbiguity Detection")
    print(f"Correct detections         : {detection_correct}")
    print(f"Detection accuracy         : {detection_accuracy:.2f}%")

    print("\nAmbiguity Type Classification")
    print(f"Ambiguous cases            : {ambiguous_cases}")
    print(f"Correct type predictions   : {type_correct}")
    print(f"Type accuracy              : {type_accuracy:.2f}%")

    # ------------------------------------------------------
    # Error analysis
    # ------------------------------------------------------

    print("\n" + "=" * 60)
    print("ERROR ANALYSIS")
    print("=" * 60)

    if detection_errors:
        print("\nAmbiguity Detection Errors:")

        for error in detection_errors:
            print(f"\nID: {error['id']}")
            print(f"Text: {error['text']}")
            print(f"Expected: {error['expected']}")
            print(f"Predicted: {error['predicted']}")
    else:
        print("\nNo ambiguity detection errors.")

    if type_errors:
        print("\nAmbiguity Type Errors:")

        for error in type_errors:
            print(f"\nID: {error['id']}")
            print(f"Text: {error['text']}")
            print(f"Expected type: {error['expected']}")
            print(f"Predicted type(s): {error['predicted']}")
    else:
        print("\nNo ambiguity type errors.")

    print("=" * 60)


if __name__ == "__main__":
    evaluate()