import json
from dataclasses import dataclass
from typing import List

@dataclass
class CIMetrics:
    coverage: float
    lint_score: float
    cyclomatic_complexity: float

@dataclass
class Standard:
    name: str
    coverage_threshold: float
    lint_score_threshold: float
    cyclomatic_complexity_threshold: float

def evaluate_quality_gates(ci_metrics: CIMetrics, standards: List[Standard]) -> dict:
    build_status = {"pass": True, "violated_standards": []}
    for standard in standards:
        if ci_metrics.coverage < standard.coverage_threshold:
            build_status["pass"] = False
            build_status["violated_standards"].append(standard.name)
        if ci_metrics.lint_score < standard.lint_score_threshold:
            build_status["pass"] = False
            build_status["violated_standards"].append(standard.name)
        if ci_metrics.cyclomatic_complexity > standard.cyclomatic_complexity_threshold:
            build_status["pass"] = False
            build_status["violated_standards"].append(standard.name)
    return build_status

def fetch_ci_metrics() -> CIMetrics:
    # Simulate fetching CI metrics from a CI provider
    return CIMetrics(coverage=0.8, lint_score=0.9, cyclomatic_complexity=10)

def get_standards() -> List[Standard]:
    # Simulate getting standards from a configuration file
    return [
        Standard("Standard 1", coverage_threshold=0.7, lint_score_threshold=0.8, cyclomatic_complexity_threshold=15),
        Standard("Standard 2", coverage_threshold=0.9, lint_score_threshold=0.95, cyclomatic_complexity_threshold=10)
    ]
