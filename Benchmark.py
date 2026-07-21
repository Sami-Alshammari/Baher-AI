import requests
import json

# 1. Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
BASE_MODEL = "deepseek-coder"
MY_MODEL = "my-deepseek"
MODELS_TO_TEST = [BASE_MODEL, MY_MODEL]

# 2. Evaluation Dataset with Flexible Concept Synonym Groups
benchmark_dataset = [
    {
        "feature": "Bugs (Debugging)",
        "prompt": (
            "### Instruction:\nYou are a debugging specialist. Inspect the provided Python code for logical or runtime errors.\n\n"
            "### Input:\n```python\ndef clean_inactive_users(user_db):\n    for user_id, profile in user_db.items():\n        if not profile['is_active']:\n            del user_db[user_id]\n    return user_db\n```\n\n### Response:\n"
        ),
        "concepts": [
            ["runtimeerror", "runtime error", "exception", "error"],
            ["iteration", "looping", "iterating", "during loop"],
            ["keys", "copy", "list", "snapshot"],
            ["size changed", "changed size", "modifying", "modified"]
        ]
    },
    {
        "feature": "Optimize (Performance)",
        "prompt": (
            "### Instruction:\nYou are a high-performance Python engineer. Optimize the provided Python code strictly for speed.\n\n"
            "### Input:\n```python\ndef find_target_pairs(numbers, target):\n    pairs = []\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if numbers[i] + numbers[j] == target:\n                pairs.append((numbers[i], numbers[j]))\n    return pairs\n```\n\n### Response:\n"
        ),
        "concepts": [
            ["o(n)", "linear time", "linear"],
            ["hash", "hashmap", "hashing", "set"],
            ["dict", "dictionary", "lookup"],
            ["complexity", "performance", "efficient", "faster"]
        ]
    },
    {
        "feature": "Review (Clean Code)",
        "prompt": (
            "### Instruction:\nYou are a senior code auditor. Perform a rigorous code review checking for PEP 8 and anti-patterns.\n\n"
            "### Input:\n```python\nGlobal_Config_Cache = [10, 20, 30]\ndef Process_Data_Function(DataInput, output_list=[]):\n    for X in DataInput:\n        if X in Global_Config_Cache:\n            output_list.append(X * 1.15)\n    return output_list\n```\n\n### Response:\n"
        ),
        "concepts": [
            ["pep 8", "pep8", "style guide"],
            ["mutable", "mutable default", "changes across calls"],
            ["default", "argument", "parameter"],
            ["snake_case", "lowercase", "underscore", "naming convention"]
        ]
    },
    {
        "feature": "Explain (Architecture)",
        "prompt": (
            "### Instruction:\nYou are an expert Python software architect. Explain the core logic of the provided code.\n\n"
            "### Input:\n```python\nimport time\nfrom functools import wraps\ndef retry_request(retries=3, delay=1):\n    def decorator(func):\n        @wraps(func)\n        def wrapper(*args, **kwargs):\n            return func(*args, **kwargs)\n        return wrapper\n    return decorator\n```\n\n### Response:\n"
        ),
        "concepts": [
            ["decorator", "decorators", "decorates"],
            ["wrapper", "inner function", "wrap"],
            ["wraps", "functools", "preserve"],
            ["metadata", "docstring", "name", "attributes"]
        ]
    }
]

def evaluate_model(model_name):
    print(f"\n[*] Evaluating model: {model_name}...")
    feature_scores = {}
    total_score = 0
    
    for case in benchmark_dataset:
        payload = {
            "model": model_name,
            "prompt": case["prompt"],
            "stream": False
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            if response.status_code != 200:
                print(f" [!] Connection failed for {model_name} (Status {response.status_code})")
                feature_scores[case["feature"]] = 0
                continue
                
            response_text = response.json().get("response", "").lower()
            
            hit_count = 0
            total_concepts = len(case["concepts"])
            
            for concept_group in case["concepts"]:
                if any(synonym in response_text for synonym in concept_group):
                    hit_count += 1
            
            score = (hit_count / total_concepts) * 100
            feature_scores[case["feature"]] = score
            total_score += score
            print(f"   -> {case['feature']}: {score:.1f}%")
            
        except Exception as e:
            print(f" [!] Error communicating with Ollama: {e}")
            feature_scores[case["feature"]] = 0
            
    final_avg = total_score / len(benchmark_dataset)
    return feature_scores, final_avg

def main():
    print("=======================================================")
    print("       STARTING COMPARATIVE QUALITY BENCHMARK")
    print("=======================================================")
    
    results = {}
    for model in MODELS_TO_TEST:
        scores, avg = evaluate_model(model)
        results[model] = {"features": scores, "average": avg}
        
    print("\n\n=======================================================")
    print("               FINAL COMPARISON REPORT                 ")
    print("=======================================================")
    print(f"{'Feature / Task':<25} | {BASE_MODEL:<18} | {MY_MODEL:<18}")
    print("-" * 68)
    
    for case in benchmark_dataset:
        feature = case["feature"]
        base_score = f"{results[BASE_MODEL]['features'].get(feature, 0):.1f}%"
        my_score = f"{results[MY_MODEL]['features'].get(feature, 0):.1f}%"
        print(f"{feature:<25} | {base_score:<18} | {my_score:<18}")
        
    print("-" * 68)
    base_avg = results[BASE_MODEL]['average']
    my_avg = results[MY_MODEL]['average']
    print(f"{'GLOBAL QUALITY SCORE':<25} | {base_avg:.2f}%{' ' * 11} | {my_avg:.2f}%")
    print("=======================================================")
    
    diff = my_avg - base_avg
    if diff > 0:
        print(f" 🏆 RESULTS: '{MY_MODEL}' outperforms the base model by +{diff:.2f}%")
    elif diff < 0:
        print(f" 🏆 RESULTS: '{BASE_MODEL}' maintains higher baseline keyword retention by {abs(diff):.2f}%")
    else:
        print(" 🤝 RESULTS: Statistical tie. Both models scored equally on key concepts.")
    print("=======================================================")

if __name__ == "__main__":
    main()