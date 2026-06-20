import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class QualityStandard:
    name: str
    description: str

@dataclass
class QualityMetric:
    standard: QualityStandard
    value: float
    timestamp: datetime

class QualityGuard:
    def __init__(self):
        self.standards = {}
        self.metrics = []

    def define_quality_standard(self, name, description):
        standard = QualityStandard(name, description)
        self.standards[name] = standard
        return standard

    def track_quality_metric(self, standard_name, value):
        if standard_name not in self.standards:
            raise ValueError("Quality standard not defined")
        standard = self.standards[standard_name]
        metric = QualityMetric(standard, value, datetime.now())
        self.metrics.append(metric)
        return metric

    def get_quality_trends(self):
        trends = {}
        for metric in self.metrics:
            standard_name = metric.standard.name
            if standard_name not in trends:
                trends[standard_name] = []
            trends[standard_name].append((metric.timestamp, metric.value))
        return trends

    def persist_quality_standards(self):
        return json.dumps({name: standard.__dict__ for name, standard in self.standards.items()})

    def load_quality_standards(self, data):
        self.standards = {}
        for name, standard_data in json.loads(data).items():
            standard = QualityStandard(**standard_data)
            self.standards[name] = standard
