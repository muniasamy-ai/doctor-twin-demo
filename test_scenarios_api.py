import json
import sys
from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    client = TestClient(app)
    
    with open('data/scenarios.json', 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
        
    total = len(scenarios)
    passed = 0
    failed = []
    
    print(f"Testing {total} scenarios...")
    
    for i, scenario in enumerate(scenarios):
        expected_id = scenario['scenario_id']
        triggers = scenario.get('triggers', [])
        
        if not triggers:
            continue
            
        test_trigger = triggers[0]
        
        try:
            response = client.post(
                "/api/v1/check",
                json={"question": test_trigger}
            )
            
            if response.status_code == 200:
                data = response.json()
                # `data` should contain `scenario_id` based on actual retrieval logic
                actual_id = data.get('scenario_id')
                
                if actual_id == expected_id:
                    passed += 1
                else:
                    failed.append({
                        "id": expected_id,
                        "trigger": test_trigger,
                        "reason": f"Expected ID '{expected_id}', got '{actual_id}'."
                    })
            else:
                failed.append({
                    "id": expected_id,
                    "trigger": test_trigger,
                    "reason": f"HTTP Error {response.status_code}: {response.text}"
                })
        except Exception as e:
            failed.append({
                "id": expected_id,
                "trigger": test_trigger,
                "reason": f"Exception occurred: {str(e)}"
            })
            
    report_content = [
        "# Scenario Test Report",
        "",
        f"**Total Scenarios Tested:** {total}",
        f"**Passed:** {passed} / {total}",
        f"**Failed:** {len(failed)}",
        f"**Success Rate:** {((passed / total) * 100 if total > 0 else 0):.2f}%",
        ""
    ]
    
    if failed:
        report_content.extend(["## Failed Scenarios", ""])
        for fail in failed:
            report_content.extend([
                f"- **Scenario ID**: `{fail['id']}`",
                f"  - **Input:** `{fail['trigger']}`",
                f"  - **Reason:** {fail['reason']}",
                ""
            ])
            
    with open('scenario_test_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))
        
    print(f"Completed! Passed: {passed}/{total}. Failed: {len(failed)}.")
    if len(failed) > 0:
        print("See scenario_test_report.md for details of failed tests.")

if __name__ == "__main__":
    run_tests()
