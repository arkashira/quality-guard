from quality_guard import QualityGuard, QualityStandard

def test_enforce_pass():
    standards = [QualityStandard("standard1", "description1", ["check1", "check2"])]
    guard = QualityGuard(standards)
    codebase = "check1 check2"
    assert guard.enforce(codebase) == True

def test_enforce_fail():
    standards = [QualityStandard("standard1", "description1", ["check1", "check2"])]
    guard = QualityGuard(standards)
    codebase = "check1"
    assert guard.enforce(codebase) == False

def test_configure():
    standards = [QualityStandard("standard1", "description1", ["check1", "check2"])]
    guard = QualityGuard([])
    guard.configure(standards)
    assert guard.standards == standards

def test_integrate():
    standards = [QualityStandard("standard1", "description1", ["check1", "check2"])]
    guard = QualityGuard(standards)
    pipeline = "pipeline"
    assert guard.integrate(pipeline) == f"{pipeline} with quality guard"
