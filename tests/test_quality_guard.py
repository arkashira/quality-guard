from quality_guard import QualityGuard, QualityStandard, QualityMetric
import pytest
from datetime import datetime

def test_define_quality_standard():
    guard = QualityGuard()
    standard = guard.define_quality_standard("Test Standard", "This is a test standard")
    assert isinstance(standard, QualityStandard)
    assert standard.name == "Test Standard"
    assert standard.description == "This is a test standard"

def test_track_quality_metric():
    guard = QualityGuard()
    standard = guard.define_quality_standard("Test Standard", "This is a test standard")
    metric = guard.track_quality_metric("Test Standard", 0.5)
    assert isinstance(metric, QualityMetric)
    assert metric.standard == standard
    assert metric.value == 0.5
    assert isinstance(metric.timestamp, datetime)

def test_track_quality_metric_with_undefined_standard():
    guard = QualityGuard()
    with pytest.raises(ValueError):
        guard.track_quality_metric("Test Standard", 0.5)

def test_get_quality_trends():
    guard = QualityGuard()
    standard = guard.define_quality_standard("Test Standard", "This is a test standard")
    guard.track_quality_metric("Test Standard", 0.5)
    guard.track_quality_metric("Test Standard", 0.6)
    trends = guard.get_quality_trends()
    assert "Test Standard" in trends
    assert len(trends["Test Standard"]) == 2

def test_persist_quality_standards():
    guard = QualityGuard()
    standard = guard.define_quality_standard("Test Standard", "This is a test standard")
    data = guard.persist_quality_standards()
    loaded_guard = QualityGuard()
    loaded_guard.load_quality_standards(data)
    assert "Test Standard" in loaded_guard.standards
    assert loaded_guard.standards["Test Standard"].name == "Test Standard"
    assert loaded_guard.standards["Test Standard"].description == "This is a test standard"
