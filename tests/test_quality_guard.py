from quality_guard import CIMetrics, Standard, evaluate_quality_gates, fetch_ci_metrics, get_standards

def test_evaluate_quality_gates_pass():
    ci_metrics = CIMetrics(coverage=0.8, lint_score=0.9, cyclomatic_complexity=10)
    standards = [
        Standard("Standard 1", coverage_threshold=0.7, lint_score_threshold=0.8, cyclomatic_complexity_threshold=15),
        Standard("Standard 2", coverage_threshold=0.6, lint_score_threshold=0.7, cyclomatic_complexity_threshold=20)
    ]
    build_status = evaluate_quality_gates(ci_metrics, standards)
    assert build_status["pass"] == True
    assert build_status["violated_standards"] == []

def test_evaluate_quality_gates_fail():
    ci_metrics = CIMetrics(coverage=0.6, lint_score=0.7, cyclomatic_complexity=20)
    standards = [
        Standard("Standard 1", coverage_threshold=0.7, lint_score_threshold=0.8, cyclomatic_complexity_threshold=15),
        Standard("Standard 2", coverage_threshold=0.8, lint_score_threshold=0.9, cyclomatic_complexity_threshold=10)
    ]
    build_status = evaluate_quality_gates(ci_metrics, standards)
    assert build_status["pass"] == False
    assert len(build_status["violated_standards"]) > 0

def test_fetch_ci_metrics():
    ci_metrics = fetch_ci_metrics()
    assert ci_metrics.coverage == 0.8
    assert ci_metrics.lint_score == 0.9
    assert ci_metrics.cyclomatic_complexity == 10

def test_get_standards():
    standards = get_standards()
    assert len(standards) == 2
    assert standards[0].name == "Standard 1"
    assert standards[1].name == "Standard 2"
