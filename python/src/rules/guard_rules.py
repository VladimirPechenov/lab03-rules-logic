"""База из 13 типов правил для стелс-сцены. Модельное время задаётся в секундах.

Для каждого стражника создаются 12 правил; сброс тревоги — один на всех.
Состояния: patrol — патруль, investigate — проверка, chase — погоня, search — поиск.
"""

from .engine import Engine, Rule


def has(facts, *pat):
    """Проверить наличие конкретного факта в базе."""
    return tuple(pat) in facts


def value(facts, pred, entity, default=None):
    """Получить значение факта вида (предикат, объект, значение) или значение по умолчанию."""
    return next((f[2] for f in facts if f[:2] == (pred, entity)), default)


def now(facts):
    """Получить текущее модельное время из факта time."""
    return next((f[1] for f in facts if f[0] == "time"), 0)


def replace(facts, pred, entity, val):
    """Заменить значение свойства объекта, удалив прежние значения."""
    facts.difference_update({f for f in facts if f[:2] == (pred, entity)})
    facts.add((pred, entity, val))


def set_state(facts, guard, new):
    """Изменить состояние и запомнить время входа в него для расчёта таймера."""
    replace(facts, "state", guard, new)
    replace(facts, "since", guard, now(facts))


def co_located(facts, guard):
    """Проверить, находятся ли стражник и игрок в одной известной зоне."""
    zone = value(facts, "at", guard)
    return zone is not None and zone == value(facts, "at", "player")


def age(facts, guard):
    """Вычислить, сколько секунд стражник находится в текущем состоянии."""
    return now(facts) - value(facts, "since", guard, now(facts))


def build(guards=("g1", "g2")) -> Engine:
    e = Engine()
    e.assert_fact("time", 0)
    for g in guards:
        e.assert_fact("state", g, "patrol")
        e.assert_fact("since", g, 0)

        # g=g фиксирует текущего стражника: замыкания G1 и G2 должны быть независимыми.
        def add(name, priority, condition, action, g=g):
            e.add(Rule(f"{name}_{g}", lambda f: condition(f, g), lambda f: action(f, g), priority))

        # Темнота: совместная зона без света даёт hidden. Факты восприятия очищаются каждый такт.
        add(
            "dark_zone",
            100,
            lambda f, g: co_located(f, g) and not has(f, "light_on", value(f, "at", g)),
            lambda f, g: f.add(("hidden", g, "player")),
        )
        # Зрение в этой модели зависит только от совпадения зоны и включённого света.
        add(
            "light_visible",
            95,
            lambda f, g: co_located(f, g) and has(f, "light_on", value(f, "at", g)),
            lambda f, g: f.add(("sees", g, "player")),
        )
        # Одноразовое событие открытия двери превращается в слышимый шум.
        add(
            "door_opened",
            90,
            lambda f, g: has(f, "door_opened", value(f, "at", g)),
            lambda f, g: f.add(("hears", g, "noise")),
        )
        # Запомнить последнюю видимую зону; память сохраняется и после потери игрока.
        add(
            "remember_target",
            85,
            lambda f, g: has(f, "sees", g, "player") and value(f, "at", "player") is not None,
            lambda f, g: replace(f, "last_seen", g, value(f, "at", "player")),
        )
        # Зрение важнее шума: приоритет 80 против 50, поэтому выбирается погоня.
        add(
            "see_player",
            80,
            lambda f, g: has(f, "sees", g, "player") and not has(f, "state", g, "chase"),
            lambda f, g: set_state(f, g, "chase"),
        )
        # Общая тревога связывает решения двух стражников.
        add(
            "raise_alarm",
            75,
            lambda f, g: has(f, "state", g, "chase") and not has(f, "alarm"),
            lambda f, g: f.add(("alarm",)),
        )
        # Если во время погони зрение потеряно, начать поиск и отсчёт его времени.
        add(
            "lost_target",
            70,
            lambda f, g: has(f, "state", g, "chase") and not has(f, "sees", g, "player"),
            lambda f, g: set_state(f, g, "search"),
        )
        # Тревога прерывает патруль или проверку. responded блокирует повторный ответ на ту же тревогу.
        add(
            "alarm_join",
            65,
            lambda f, g: (
                has(f, "alarm") and value(f, "state", g) in ("patrol", "investigate") and not has(f, "responded", g)
            ),
            lambda f, g: (set_state(f, g, "search"), f.add(("responded", g))),
        )
        # Шум переводит в проверку только патрулирующего стражника.
        add(
            "hear_noise",
            50,
            lambda f, g: has(f, "hears", g, "noise") and has(f, "state", g, "patrol"),
            lambda f, g: set_state(f, g, "investigate"),
        )
        # Отказ освещения во время патруля назначает проверку выключателя.
        add(
            "light_off",
            45,
            lambda f, g: has(f, "power_failed", value(f, "at", g)) and has(f, "state", g, "patrol"),
            lambda f, g: (set_state(f, g, "investigate"), f.add(("target", g, "switch"))),
        )
        # Завершить поиск через 10 секунд при отсутствии зрения и шума.
        add(
            "search_timeout",
            30,
            lambda f, g: (
                has(f, "state", g, "search")
                and age(f, g) >= 10
                and not has(f, "sees", g, "player")
                and not has(f, "hears", g, "noise")
            ),
            lambda f, g: (set_state(f, g, "patrol"), f.add(("responded", g))),
        )
        # Завершить проверку через 5 секунд, если нет шума, зрения и сигнала отказа света.
        add(
            "return_post",
            20,
            lambda f, g: (
                has(f, "state", g, "investigate")
                and age(f, g) >= 5
                and not has(f, "sees", g, "player")
                and not has(f, "hears", g, "noise")
                and not has(f, "power_failed", value(f, "at", g))
            ),
            lambda f, g: (set_state(f, g, "patrol"), f.discard(("target", g, "switch"))),
        )
    # Когда оба вернулись к патрулю, снять тревогу и отметки ответа на неё.
    e.add(
        Rule(
            "alarm_reset",
            lambda f: has(f, "alarm") and all(has(f, "state", g, "patrol") for g in guards),
            lambda f: f.difference_update({x for x in f if x[0] in ("alarm", "responded")}),
            10,
        )
    )
    return e
