import json
from dataclasses import dataclass
from typing import List

@dataclass
class QualityStandard:
    name: str
    description: str

@dataclass
class QualityMetric:
    name: str
    value: float

class QualityGuard:
    def __init__(self):
        self.quality_standards = []
        self.quality_metrics = []

    def add_quality_standard(self, standard: QualityStandard):
        self.quality_standards.append(standard)

    def add_quality_metric(self, metric: QualityMetric):
        self.quality_metrics.append(metric)

    def get_quality_standards(self) -> List[QualityStandard]:
        return self.quality_standards

    def get_quality_metrics(self) -> List[QualityMetric]:
        return self.quality_metrics

    def visualize_quality_trends(self) -> str:
        trends = []
        for metric in self.quality_metrics:
            trends.append(f"{metric.name}: {metric.value}")
        return "\n".join(trends)

    def persist_quality_standards(self) -> str:
        standards = [standard.__dict__ for standard in self.quality_standards]
        return json.dumps(standards)
