import json

import pytest

from rules.engine import Engine, Rule
from rules.guard_rules import build
from rules.scenarios import ROOT, play


@pytest.mark.parametrize("path", sorted((ROOT / "scenarios").glob("*.json")), ids=lambda p: p.stem)
def test_scenario(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    for record in play(data):
        assert record["ok"], record
        for guard in ("g1", "g2"):
            assert len([f for f in record["facts"] if f[:2] == ("state", guard)]) == 1
        for trace in record["trace"]:
            assert trace["added"] or trace["removed"]


def test_priority_rebuilt_after_each_firing():
    e = Engine()
    e.add(Rule("low", lambda f: ("ready",) in f and ("done",) not in f, lambda f: f.add(("done",)), 1))
    e.add(Rule("high", lambda f: ("ready",) not in f, lambda f: f.add(("ready",)), 10))
    assert e.run() == ["high", "low"]


def test_noop_not_logged():
    e = Engine([Rule("noop", lambda f: True, lambda f: None)])
    assert e.run() == []
    assert e.log == []


def test_limit_is_explicit_error():
    e = Engine([Rule("add", lambda f: True, lambda f: f.add(("a",)))])
    with pytest.raises(RuntimeError):
        e.run(max_cycles=1)


def test_rules_are_unique_and_repeat_run_is_stable():
    e = build()
    assert len(e.rules) == 25
    e.assert_fact("sees", "g1", "player")
    e.run()
    before = e.facts.copy()
    assert e.run() == []
    assert before == e.facts


def test_duplicate_names_rejected():
    e = Engine()
    r = Rule("x", lambda f: True, lambda f: None)
    e.add(r)
    with pytest.raises(ValueError):
        e.add(r)


def test_all_rule_schemas_are_demonstrated():
    exercised = set()
    for path in sorted((ROOT / "scenarios").glob("*.json")):
        for record in play(json.loads(path.read_text(encoding="utf-8-sig"))):
            exercised.update(name.removesuffix("_g1").removesuffix("_g2") for name in record["fired"])
    expected = {r.name.removesuffix("_g1").removesuffix("_g2") for r in build().rules}
    assert exercised == expected


def test_scenario_traces_are_deterministic():
    for path in sorted((ROOT / "scenarios").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        assert play(data) == play(data)
