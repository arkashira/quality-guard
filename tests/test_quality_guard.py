from quality_guard import load_quality_model, evaluate_codebase, check_thresholds, print_report, Metric
import json
from io import StringIO
import sys

def test_load_quality_model():
    quality_model = {'lint': 10, 'cyclomatic_complexity': 20}
    with open('quality-guard.json', 'w') as f:
        json.dump(quality_model, f)
    loaded_model = load_quality_model('quality-guard.json')
    assert loaded_model == quality_model

def test_evaluate_codebase():
    quality_model = {'lint': 10, 'cyclomatic_complexity': 20}
    metrics = evaluate_codebase(quality_model)
    assert len(metrics) == 2
    assert metrics[0].name == 'lint'
    assert metrics[1].name == 'cyclomatic_complexity'

def test_check_thresholds():
    metrics = [Metric('lint', 10, 5), Metric('cyclomatic_complexity', 20, 25)]
    assert not check_thresholds(metrics)
    metrics = [Metric('lint', 10, 5), Metric('cyclomatic_complexity', 20, 15)]
    assert check_thresholds(metrics)

def test_print_report(capsys):
    metrics = [Metric('lint', 10, 5), Metric('cyclomatic_complexity', 20, 25)]
    print_report(metrics, False)
    captured = capsys.readouterr()
    assert "lint: 5 (threshold: 10)" in captured.out
    assert "cyclomatic_complexity: 25 (threshold: 20)" in captured.out
    print_report(metrics, True)
    captured = capsys.readouterr()
    assert '{"name": "lint", "threshold": 10, "value": 5}' in captured.out
    assert '{"name": "cyclomatic_complexity", "threshold": 20, "value": 25}' in captured.out

def test_main():
    quality_model = {'lint': 10, 'cyclomatic_complexity': 20}
    with open('quality-guard.json', 'w') as f:
        json.dump(quality_model, f)
    sys.argv = ['quality_guard.py']
    try:
        from quality_guard import main
        main()
    except SystemExit as e:
        assert e.code == 0
    sys.argv = ['quality_guard.py', '--json']
    try:
        from quality_guard import main
        main()
    except SystemExit as e:
        assert e.code == 0
