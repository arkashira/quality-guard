import json
from quality_guard import QualityGuard, QualityStandard, QualityMetric

def test_add_quality_standard():
    guard = QualityGuard()
    standard = QualityStandard("Standard 1", "Description 1")
    guard.add_quality_standard(standard)
    assert len(guard.get_quality_standards()) == 1
    assert guard.get_quality_standards()[0].name == "Standard 1"

def test_add_quality_metric():
    guard = QualityGuard()
    metric = QualityMetric("Metric 1", 90.0)
    guard.add_quality_metric(metric)
    assert len(guard.get_quality_metrics()) == 1
    assert guard.get_quality_metrics()[0].name == "Metric 1"

def test_visualize_quality_trends():
    guard = QualityGuard()
    metric1 = QualityMetric("Metric 1", 90.0)
    metric2 = QualityMetric("Metric 2", 80.0)
    guard.add_quality_metric(metric1)
    guard.add_quality_metric(metric2)
    trends = guard.visualize_quality_trends()
    assert "Metric 1: 90.0" in trends
    assert "Metric 2: 80.0" in trends

def test_persist_quality_standards():
    guard = QualityGuard()
    standard1 = QualityStandard("Standard 1", "Description 1")
    standard2 = QualityStandard("Standard 2", "Description 2")
    guard.add_quality_standard(standard1)
    guard.add_quality_standard(standard2)
    persisted = guard.persist_quality_standards()
    assert len(json.loads(persisted)) == 2
    assert json.loads(persisted)[0]["name"] == "Standard 1"

def test_empty_quality_guard():
    guard = QualityGuard()
    assert len(guard.get_quality_standards()) == 0
    assert len(guard.get_quality_metrics()) == 0
    assert guard.visualize_quality_trends() == ""
    assert guard.persist_quality_standards() == "[]"
