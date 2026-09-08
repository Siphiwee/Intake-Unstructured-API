import json
import requests


with open("evaluation/cases.json", "r", encoding="utf-8") as file:
    cases = json.load(file)


print(f"Loaded {len(cases)} evaluation cases.")
print()


passed_count = 0
failed_count = 0

category_results = {}


for case in cases:

    category = case["category"]

    if category not in category_results:
        category_results[category] = {
            "passed": 0,
            "failed": 0
        }

    response = requests.post(
        "http://127.0.0.1:8000/review",
        json={
            "request_text": case["request_text"]
        }
    )

    actual = response.json()["validation"]
    expected = case["expected"]

    status_match = actual["status"] == expected["status"]
    review_match = actual["review_required"] == expected["review_required"]
    missing_match = (
        actual["missing_information"]
        == expected["missing_information"]
    )
    invalid_match = (
        actual["invalid_information"]
        == expected["invalid_information"]
    )
    conflicting_match = (
        actual["conflicting_information"]
        == expected["conflicting_information"]
    )

    review_reasons_match = True

    if "review_reasons" in expected:
        actual_reasons = set(actual["review_reasons"])
        expected_reasons = set(expected["review_reasons"])

        review_reasons_match = (
            actual_reasons == expected_reasons
        )

    passed = (
        status_match
        and review_match
        and missing_match
        and invalid_match
        and conflicting_match
        and review_reasons_match
    )

    if passed:
        passed_count += 1
        category_results[category]["passed"] += 1
        print(f'{case["id"]}: PASS')

    else:
        failed_count += 1
        category_results[category]["failed"] += 1
        print(f'{case["id"]}: FAIL')
        print("Expected:", expected)
        print("Actual:", actual)


total_cases = len(cases)
accuracy = (passed_count / total_cases) * 100


print()
print(f"Passed: {passed_count}")
print(f"Failed: {failed_count}")
print(f"Total: {total_cases}")
print(f"Evaluation accuracy: {accuracy:.1f}%")


print()
print("Category Results")
print("----------------")


for category, results in category_results.items():

    category_total = results["passed"] + results["failed"]

    category_accuracy = (
        results["passed"] / category_total
    ) * 100

    print(
        f"{category}: "
        f"{results['passed']}/{category_total} passed "
        f"({category_accuracy:.1f}%)"
    )