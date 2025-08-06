#!/usr/bin/env python3

import asyncio
import json
import time
import statistics
from typing import List, Dict, Any
import httpx

ACCURACY_TEST_CASES = [
    {
        "text": "I goes to the store yesterday. She have a apple.",
        "expected_errors": [
            {"wrong": "I goes", "corrected": "I went", "error_type": "verb tense"},
            {"wrong": "She have", "corrected": "She has", "error_type": "subject-verb agreement"},
            {"wrong": "a apple", "corrected": "an apple", "error_type": "article usage"}
        ]
    },
    {
        "text": "The cat are sleeping. They was happy.",
        "expected_errors": [
            {"wrong": "The cat are", "corrected": "The cat is", "error_type": "subject-verb agreement"},
            {"wrong": "They was", "corrected": "They were", "error_type": "subject-verb agreement"}
        ]
    },
    {
        "text": "He don't like it. We was going home.",
        "expected_errors": [
            {"wrong": "He don't", "corrected": "He doesn't", "error_type": "subject-verb agreement"},
            {"wrong": "We was", "corrected": "We were", "error_type": "subject-verb agreement"}
        ]
    }
]

PERFORMANCE_TEST_TEXTS = [
    "This is a simple test sentence.",
    "I goes to the store yesterday. She have a apple. The cat are sleeping. They was happy. He don't like it.",
    "This is a longer text with multiple sentences. Each sentence should be checked for grammar errors. The system should identify issues like subject-verb agreement, verb tense, and article usage. We was going to the store when we seen the cat."
]

async def evaluate_accuracy():
    print("🎯 ACCURACY EVALUATION")
    print("=" * 50)
    
    total_cases = len(ACCURACY_TEST_CASES)
    correct_detections = 0
    false_positives = 0
    false_negatives = 0
    
    for i, test_case in enumerate(ACCURACY_TEST_CASES, 1):
        print(f"\n📝 Test Case {i}: {test_case['text']}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/check",
                    json={"text": test_case['text']},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    detected_errors = result.get('issues', [])
                    
                    detected = set()
                    for error in detected_errors:
                        detected.add((error['wrong'], error['corrected'], error['error_type']))
                    
                    expected = set()
                    for error in test_case['expected_errors']:
                        expected.add((error['wrong'], error['corrected'], error['error_type']))
                    
                    correct = len(detected.intersection(expected))
                    false_pos = len(detected - expected)
                    false_neg = len(expected - detected)
                    
                    correct_detections += correct
                    false_positives += false_pos
                    false_negatives += false_neg
                    
                    print(f"  ✅ Correct detections: {correct}")
                    print(f"  ❌ False positives: {false_pos}")
                    print(f"  ❌ False negatives: {false_neg}")
                    
                    if detected:
                        print("  📋 Detected errors:")
                        for error in detected_errors:
                            print(f"    - '{error['wrong']}' → '{error['corrected']}' ({error['error_type']})")
                    else:
                        print("  📋 No errors detected")
                        
                else:
                    print(f"  ❌ API error: {response.status_code}")
                    
        except Exception as e:
            print(f"  ❌ Test failed: {e}")
    
    total_expected = sum(len(case['expected_errors']) for case in ACCURACY_TEST_CASES)
    precision = correct_detections / (correct_detections + false_positives) if (correct_detections + false_positives) > 0 else 0
    recall = correct_detections / total_expected if total_expected > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\n📊 ACCURACY METRICS:")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall: {recall:.3f}")
    print(f"  F1-Score: {f1_score:.3f}")
    print(f"  Total Correct: {correct_detections}/{total_expected}")

async def evaluate_performance():
    print("\n⚡ PERFORMANCE EVALUATION")
    print("=" * 50)
    
    response_times = []
    success_count = 0
    total_tests = len(PERFORMANCE_TEST_TEXTS) * 3
    
    for i, text in enumerate(PERFORMANCE_TEST_TEXTS, 1):
        print(f"\n📝 Performance Test {i}: {len(text)} characters")
        
        for run in range(3):
            try:
                start_time = time.time()
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "http://localhost:8000/check",
                        json={"text": text},
                        timeout=60
                    )
                
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                if response.status_code == 200:
                    success_count += 1
                    result = response.json()
                    issues_count = len(result.get('issues', []))
                    print(f"  Run {run + 1}: {response_time:.2f}s, {issues_count} issues")
                else:
                    print(f"  Run {run + 1}: Failed ({response.status_code})")
                    
            except Exception as e:
                print(f"  Run {run + 1}: Error - {e}")
    
    if response_times:
        print(f"\n📊 PERFORMANCE METRICS:")
        print(f"  Average Response Time: {statistics.mean(response_times):.2f}s")
        print(f"  Median Response Time: {statistics.median(response_times):.2f}s")
        print(f"  Min Response Time: {min(response_times):.2f}s")
        print(f"  Max Response Time: {max(response_times):.2f}s")
        print(f"  Success Rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")

async def evaluate_reliability():
    print("\n🛡️ RELIABILITY EVALUATION")
    print("=" * 50)
    
    reliability_tests = [
        {"text": "", "expected_status": 400, "description": "Empty text"},
        {"text": "a" * 6000, "expected_status": 400, "description": "Text too long"},
        {"text": "This is a normal sentence.", "expected_status": 200, "description": "Normal text"},
        {"text": "I goes to store.", "expected_status": 200, "description": "Text with errors"},
    ]
    
    passed_tests = 0
    total_tests = len(reliability_tests)
    
    for test in reliability_tests:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/check",
                    json={"text": test["text"]},
                    timeout=60
                )
                
                if response.status_code == test["expected_status"]:
                    print(f"  ✅ {test['description']}: PASS")
                    passed_tests += 1
                else:
                    print(f"  ❌ {test['description']}: FAIL (got {response.status_code}, expected {test['expected_status']})")
                    
        except Exception as e:
            print(f"  ❌ {test['description']}: ERROR - {e}")
    
    print(f"\n📊 RELIABILITY SCORE: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")

async def evaluate_api_endpoints():
    print("\n🌐 API ENDPOINT EVALUATION")
    print("=" * 50)
    
    endpoints = [
        {"url": "http://localhost:8000/", "method": "GET", "name": "Root endpoint"},
        {"url": "http://localhost:8000/health", "method": "GET", "name": "Health check"},
        {"url": "http://localhost:8000/docs", "method": "GET", "name": "API documentation"},
    ]
    
    working_endpoints = 0
    
    for endpoint in endpoints:
        try:
            async with httpx.AsyncClient() as client:
                if endpoint["method"] == "GET":
                    response = await client.get(endpoint["url"], timeout=10)
                else:
                    response = await client.post(endpoint["url"], timeout=10)
                
                if response.status_code == 200:
                    print(f"  ✅ {endpoint['name']}: Working")
                    working_endpoints += 1
                else:
                    print(f"  ❌ {endpoint['name']}: Failed ({response.status_code})")
                    
        except Exception as e:
            print(f"  ❌ {endpoint['name']}: Error - {e}")
    
    print(f"\n📊 API ENDPOINTS: {working_endpoints}/{len(endpoints)} working")

async def generate_evaluation_report():
    print("📋 GRAMMAR CHECK API EVALUATION REPORT")
    print("=" * 60)
    print("Date: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Model: gemma3:1b")
    print("Framework: FastAPI")
    print("=" * 60)
    
    await evaluate_accuracy()
    await evaluate_performance()
    await evaluate_reliability()
    await evaluate_api_endpoints()
    
    print("\n" + "=" * 60)
    print("📋 EVALUATION SUMMARY")
    print("=" * 60)
    print("✅ Accuracy: Grammar error detection capability")
    print("✅ Performance: Response time and throughput")
    print("✅ Reliability: Error handling and edge cases")
    print("✅ API: Endpoint functionality and documentation")
    print("\n🎯 This evaluation framework provides comprehensive")
    print("   assessment of the grammar checking system.")

if __name__ == "__main__":
    asyncio.run(generate_evaluation_report()) 