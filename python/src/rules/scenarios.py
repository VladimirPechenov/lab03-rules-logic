"""Единый исполнитель сценариев для тестов, журналов, сцены и демонстрационного видео."""

import argparse
import json
from pathlib import Path

from .guard_rules import build, replace, value

ROOT = Path(__file__).resolve().parents[3]

# Восприятие и события действуют один такт. Позиции, свет, память и состояния сохраняются.
TRANSIENT = {"sees", "hidden", "hears", "door_opened", "power_failed"}


def play(data):
    """Выполнить шаги сценария и сохранить вход, цепочку вывода, итог и проверки."""
    engine = build()
    records = []
    time = 0
    for index, step in enumerate(data.get("steps", [data])):
        # dt изменяет модельное время; скорость воспроизведения видео на него не влияет.
        time += step.get("dt", 0)
        engine.facts.difference_update({f for f in engine.facts if f[0] in TRANSIENT | {"time"}})
        engine.assert_fact("time", time)
        for fact in step.get("remove", []):
            engine.retract(*fact)
        # Свойства с одним значением заменяем, прочие факты добавляем в множество.
        for fact in step.get("facts", []):
            if fact[0] in ("at", "state", "since"):
                replace(engine.facts, *fact)
            else:
                engine.assert_fact(*fact)
        # Входной снимок и новые записи журнала позволяют объяснить решение пошагово.
        before = sorted(engine.facts)
        log_start = len(engine.log)
        fired = engine.run()
        states = {g: value(engine.facts, "state", g) for g in ("g1", "g2")}
        # Проверяем состояния, обязательные факты и отсутствие запрещённых фактов.
        checks = [states[g] == state for g, state in step["expect"].items()]
        checks += [tuple(f) in engine.facts for f in step.get("expect_facts", [])]
        checks += [tuple(f) not in engine.facts for f in step.get("absent_facts", [])]
        records.append(
            {
                "step": index + 1,
                "time": time,
                "caption": step.get("caption", data["name"]),
                "input": before,
                "fired": fired,
                "trace": engine.log[log_start:],
                "facts": sorted(engine.facts),
                "states": states,
                "expected": step["expect"],
                "ok": all(checks),
            }
        )
    return records


def run_all(output=ROOT / "results"):
    """Проверить все JSON-сценарии и записать текстовые журналы и структурированные трассы."""
    output.mkdir(parents=True, exist_ok=True)
    summary = []
    for path in sorted((ROOT / "scenarios").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        records = play(data)
        payload = {"id": path.stem, "name": data["name"], "records": records}
        (output / f"{path.stem}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        lines = [data["name"]]
        for rec in records:
            lines += [f"\nШАГ {rec['step']} t={rec['time']}s: {rec['caption']}", f"ВХОД: {rec['input']}"]
            for trace in rec["trace"]:
                lines += [
                    f"ПРАВИЛО {trace['rule']} приоритет={trace['priority']}",
                    f"  + {trace['added']}",
                    f"  - {trace['removed']}",
                    f"  ФАКТЫ {trace['facts']}",
                ]
            lines += [f"РЕЗУЛЬТАТ: {rec['states']} ОЖИДАЛОСЬ: {rec['expected']} {'OK' if rec['ok'] else 'ОШИБКА'}"]
        (output / f"{path.stem}.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
        summary.append(
            {
                "id": path.stem,
                "name": data["name"],
                "steps": len(records),
                "firings": sum(len(r["fired"]) for r in records),
                "ok": all(r["ok"] for r in records),
            }
        )
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Проверка сценариев логической модели стражников")
    parser.add_argument("--output", type=Path, default=ROOT / "results", help="Папка для журналов и сводки результатов")
    args = parser.parse_args()
    summary = run_all(args.output)
    for row in summary:
        print(f"{row['id']}: {'OK' if row['ok'] else 'FAIL'} ({row['steps']} шагов, {row['firings']} срабатываний)")
    if not all(row["ok"] for row in summary):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
