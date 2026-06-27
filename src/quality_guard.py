import argparse
import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Metric:
    name: str
    threshold: int
    value: int

def load_quality_model(path: str) -> Dict[str, int]:
    with open(path, 'r') as f:
        return json.load(f)

def evaluate_codebase(quality_model: Dict[str, int]) -> List[Metric]:
    metrics = []
    # Simulate static analysis
    metrics.append(Metric('lint', quality_model['lint'], 5))
    metrics.append(Metric('cyclomatic_complexity', quality_model['cyclomatic_complexity'], 10))
    return metrics

def check_thresholds(metrics: List[Metric]) -> bool:
    for metric in metrics:
        if metric.value > metric.threshold:
            return False
    return True

def print_report(metrics: List[Metric], json_output: bool) -> None:
    if json_output:
        print(json.dumps([{'name': m.name, 'threshold': m.threshold, 'value': m.value} for m in metrics]))
    else:
        for metric in metrics:
            print(f"{metric.name}: {metric.value} (threshold: {metric.threshold})")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    quality_model = load_quality_model('quality-guard.json')
    metrics = evaluate_codebase(quality_model)
    if not check_thresholds(metrics):
        print_report(metrics, args.json)
        exit(1)

if __name__ == '__main__':
    main()
