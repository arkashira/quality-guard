import json
from dataclasses import dataclass
from typing import List

@dataclass
class QualityStandard:
    name: str
    description: str
    checks: List[str]

class QualityGuard:
    def __init__(self, standards: List[QualityStandard]):
        self.standards = standards

    def enforce(self, codebase: str) -> bool:
        for standard in self.standards:
            for check in standard.checks:
                if check not in codebase:
                    return False
        return True

    def configure(self, standards: List[QualityStandard]):
        self.standards = standards

    def integrate(self, pipeline: str) -> str:
        return f"{pipeline} with quality guard"
