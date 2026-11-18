"""Прямой логический вывод: приоритеты, защита от повторов и журнал изменений.

Факты описывают мир, а правила преобразуют их по принципу «если — то».
Движок не зависит от стражников, сценариев и графического интерфейса.
"""

from dataclasses import dataclass, field
from typing import Callable

# Факт — кортеж, например ("state", "g1", "patrol"). Множество исключает дубликаты.
Fact = tuple


@dataclass
class Rule:
    """Продукция: имя, условие применимости, действие над фактами и приоритет."""

    name: str
    condition: Callable[[set[Fact]], bool]
    action: Callable[[set[Fact]], None]
    priority: int = 0


@dataclass
class Engine:
    """Хранит базу фактов и правил; log объясняет каждое изменение мира."""

    rules: list[Rule] = field(default_factory=list)
    facts: set[Fact] = field(default_factory=set)
    log: list[dict] = field(default_factory=list)

    def add(self, rule: Rule) -> None:
        """Зарегистрировать правило; уникальное имя нужно для журнала и защиты от повторов."""
        if any(r.name == rule.name for r in self.rules):
            raise ValueError(f"Повторяющееся имя правила: {rule.name}")
        self.rules.append(rule)

    def assert_fact(self, *fact) -> None:
        """Добавить факт в рабочую память."""
        self.facts.add(tuple(fact))

    def retract(self, *fact) -> None:
        """Удалить факт; отсутствие такого факта не считается ошибкой."""
        self.facts.discard(tuple(fact))

    def run(self, max_cycles: int = 100) -> list[str]:
        """Выполнить один такт вывода и вернуть имена сработавших правил.

        После каждого изменения заново проверить условия в порядке приоритета.
        В пределах вызова каждый экземпляр правила применяется не более одного раза.
        """
        fired = []
        # Защита от повторов действует только в этом такте, а не на всё время игры.
        considered = set()
        # Больший приоритет раньше; при равенстве — имя по алфавиту.
        ordered = sorted(self.rules, key=lambda r: (-r.priority, r.name))
        for _ in range(max_cycles):
            for rule in ordered:
                if rule.name in considered or not rule.condition(self.facts):
                    continue
                # Снимок до действия позволяет вычислить добавленные и удалённые факты.
                before = self.facts.copy()
                rule.action(self.facts)
                considered.add(rule.name)
                # Действия без изменений не считаются продуктивными срабатываниями.
                if self.facts == before:
                    continue
                fired.append(rule.name)
                self.log.append(
                    {
                        "rule": rule.name,
                        "priority": rule.priority,
                        "added": sorted(self.facts - before),
                        "removed": sorted(before - self.facts),
                        "facts": sorted(self.facts),
                    }
                )
                # Вернуться к началу списка: действие могло разрешить более важное правило.
                break
            else:
                # Ни одно оставшееся правило не изменило базу — вывод завершён.
                return fired
        raise RuntimeError("Превышен лимит циклов вывода; проверьте базу правил")
