from dataclasses import dataclass
from typing import List

@dataclass
class TechnicalDebtItem:
    id: int
    business_goal_alignment: float
    code_complexity: float
    age: float

def calculate_impact_score(item: TechnicalDebtItem) -> float:
    return item.business_goal_alignment

def calculate_risk_score(item: TechnicalDebtItem) -> float:
    return item.code_complexity * item.age

def prioritize_technical_debt(items: List[TechnicalDebtItem]) -> List[TechnicalDebtItem]:
    return sorted(items, key=lambda item: calculate_impact_score(item) / calculate_risk_score(item), reverse=True)
