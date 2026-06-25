from technical_debt import TechnicalDebtItem, calculate_impact_score, calculate_risk_score, prioritize_technical_debt

def test_calculate_impact_score():
    item = TechnicalDebtItem(1, 0.8, 0.5, 2.0)
    assert calculate_impact_score(item) == 0.8

def test_calculate_risk_score():
    item = TechnicalDebtItem(1, 0.8, 0.5, 2.0)
    assert calculate_risk_score(item) == 1.0

def test_prioritize_technical_debt():
    items = [
        TechnicalDebtItem(1, 0.8, 0.5, 2.0),
        TechnicalDebtItem(2, 0.9, 0.6, 1.5),
        TechnicalDebtItem(3, 0.7, 0.4, 2.5),
    ]
    prioritized_items = prioritize_technical_debt(items)
    assert prioritized_items[0].id == 2
    assert prioritized_items[1].id == 1
    assert prioritized_items[2].id == 3

def test_prioritize_technical_debt_empty_list():
    items = []
    prioritized_items = prioritize_technical_debt(items)
    assert prioritized_items == []

def test_prioritize_technical_debt_single_item():
    items = [TechnicalDebtItem(1, 0.8, 0.5, 2.0)]
    prioritized_items = prioritize_technical_debt(items)
    assert prioritized_items == items
