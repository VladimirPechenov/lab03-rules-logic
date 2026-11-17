# Лабораторная работа № 3

Логическая модель стелс-NPC на основе правил. Дисциплина «Игровой искусственный интеллект».

**Студент:** Печенов В. В. · **Группа:** ИВТ-465 · **Дата:** 17.11.2026.
**Вариант B:** Python, собственный forward-chaining движок, прямо предусмотренный исходным шаблоном.
Оставлен один вариант реализации; SWI-Prolog и Unity не требуются.

**[Скачать общее видео, 3 минуты](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/lab03_demo_full.mp4)** · **[Видео на Google Диске](https://drive.google.com/file/d/1wGrz-D0AGtpuXALSuGZdxv9ZnYAvjoFJ/view?usp=drivesdk)** · **[Release v1.0](https://github.com/VladimirPechenov/lab03-rules-logic/releases/tag/v1.0)**

Копия на Диске загружена в аккаунт владельца; доступ для преподавателя необходимо включить
в меню «Поделиться → Общий доступ → Все, у кого есть ссылка → Читатель».
Ролики в Release доступны из публичного репозитория без доступа к Google-аккаунту.
MP4 исключены из истории Git и размещаются отдельными файлами Release.

## Соответствие заданию

- [x] 10+ правил: **13 разных типов**, 25 экземпляров (12 × 2 стражника + одно общее).
- [x] Два стражника G1 и G2 одновременно в анимированной сцене.
- [x] Для каждого сценария: входные факты, цепочка правил, изменения фактов, итоговые состояния.
- [x] Видео каждого из 10 сценариев; отдельные MP4 и общий ролик с теми же сценариями.
- [x] Полный порядок выполнения приведён ниже; дополнительный протокол [Markdown](docs/report.md) и [PDF](docs/report.pdf).
- [x] История по этапам step-1, step-2, step-3; тег v1.0 и Release.
- [ ] Открыть доступ к копии видео на Google Диске, если сдаётся именно эта ссылка.

Источник требований: [README преподавательского шаблона](https://github.com/kolesnikov-vstu-gameai/lab03-rules-logic).
Полные методические указания и официальный титульный шаблон кафедры в репозитории не приложены.
Протокол PDF имеет 7 страниц и содержит фактическое выполнение работы; его оформление не заявляется
как официальный шаблон кафедры. Сверка выполнена по опубликованному README.

## Запуск и повторная проверка

Нужен Python 3.10+ с Tkinter (в обычном установщике Python для Windows входит в комплект).
Быстрый запуск Windows: **RUN_DEMO.cmd**. Полная проверка: **CHECK.cmd**.
При первом запуске устанавливаются зависимости. Команды вручную из корня проекта:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e "./python[dev,report]"
.\.venv\Scripts\python.exe -m ruff check python
.\.venv\Scripts\python.exe -m pytest python/tests
.\.venv\Scripts\python.exe -m rules.scenarios
.\.venv\Scripts\python.exe -m rules.demo
```

Управление: пробел — пауза; стрелки влево/вправо — сценарии; кнопка «Повторить» — начало сценария.
Окно показывает G1/G2, игрока, освещение, тревогу, память, факты и реальные сработавшие правила.
На Linux/macOS путь к интерпретатору среды: `.venv/bin/python`; при необходимости установите Tkinter отдельно.

## Полный порядок выполнения

1. Изучен исходный README; зафиксированы четыре обязательных результата и правила публикации.
   Получен шаблон репозитория, создана рабочая ветка `lab03-completed`.
2. Выбран вариант B. Неиспользуемые Unity/Prolog удалены, зависимость pyswip убрана.
3. Определены факты-кортежи: `at`, `light_on`, `sees`, `hears`, `state`, `alarm`,
   `last_seen`, `since`, `time`, `target`, `responded`, `door_opened`, `power_failed`, `hidden`.
4. Реализован детерминированный прямой вывод: выбирается применимое правило с наибольшим
   приоритетом, применяется, повестка строится заново. При равенстве приоритетов выбирается имя по алфавиту.
5. Добавлены 13 типов правил из таблицы ниже. `set_state` удаляет старое состояние и записывает время входа.
   Экземпляр правила срабатывает не более одного раза за такт. Пустые действия не попадают в лог.
6. Созданы два стражника и три зоны: `hall`, `corridor`, `storage`. Для простоты видимость определяется
   совпадением зоны и включённым светом. Зоны разделены стенами; межзональной видимости нет.
7. Подготовлены 10 JSON-сценариев (20 шагов). Каждый шаг задаёт `dt`, добавляемые/удаляемые факты,
   ожидаемые состояния, обязательные и запрещённые факты. В начале такта старые сенсорные факты и события
   очищаются; позиции, состояния, память и освещение сохраняются.
8. Выполнен `python -m rules.scenarios`: получены текстовые и JSON-логи в `results/`.
   Для каждого срабатывания сохранены приоритет, добавленные/удалённые факты и полный снимок базы.
9. Выполнены тесты и линтер: **18 тестов пройдено**, замечаний Ruff нет.
   Проверены состояния, их единственность, положительные и отрицательные ожидания,
   детерминированность трасс, границы таймеров, приоритеты, лимит вывода и покрытие всех 13 типов правил.
10. Реализована сцена на Pillow/Tkinter. Она воспроизводит снимки именно этого движка:
    сначала вход, затем правила по очереди, затем проверенный результат. Один шаг занимает 9 секунд видео,
    при этом модельное время `t` изменяется согласно JSON, а не реальному времени воспроизведения.
11. Через FFmpeg экспортированы 10 MP4 и общий ролик 180 секунд, H.264, 1280×720, 12 кадров/с.
    Видео содержит подписи на русском языке; звуковая дорожка отсутствует.
12. Оформлены README, протокол, скриншоты и результаты. Изменения сохранены этапными коммитами,
    подготовлены тег v1.0 и Release. Видео хранятся вне Git.

## Архитектура и принятые ограничения

`scenarios/*.json → scenarios.play → Engine → журнал снимков → demo.frame → окно / MP4`.
`tools/build_report.py` строит документацию из тех же прогонов.
Состояния: `patrol`, `investigate`, `chase`, `search`. Тревога общая для обоих стражников.
Память `last_seen` сохраняется при потере видимости; таймер поиска равен 10 с, проверки — 5 с.
`responded` предотвращает повторный вход в поиск по той же тревоге после завершения таймера;
при сбросе тревоги эта отметка удаляется. Новый шум не даёт завершить текущую проверку на этом такте.

Это дискретная зональная модель принятия решений. Движения значков внутри зон иллюстрируют состояния,
не участвуют в расчёте видимости и не являются физической симуляцией или поиском пути.
Событие `door_opened` обозначает переход двери из закрытого состояния в открытое и действует один такт.
Постоянно открытая дверь повторно шум не создаёт. `power_failed` — внешний сигнал отказа освещения;
для продолжающегося отказа он передаётся каждый такт. `sees`/`hidden` вычисляются заново каждый такт.
Готовые сенсорные факты допустимы для модульных тестов; сценарии демонстрации получают зрение из света и зон.

## База правил

| Правило | Приоритет | Если | То |
|---|---:|---|---|
| dark_zone | 100 | Игрок и стражник в одной неосвещённой зоне | hidden; зрение не выводится |
| light_visible | 95 | Одна зона, свет включён | sees(G, player) |
| door_opened | 90 | Открыта дверь в зоне стражника | hears(G, noise) |
| remember_target | 85 | Стражник видит игрока | Сохранить зону в last_seen |
| see_player | 80 | Игрок виден, стражник ещё не преследует | state = chase |
| raise_alarm | 75 | Стражник преследует, тревоги нет | Установить общий alarm |
| lost_target | 70 | Погоня, но игрок больше не виден | state = search |
| alarm_join | 65 | Тревога, патруль/проверка, ещё не ответил | Поиск и отметка responded |
| hear_noise | 50 | Шум во время патруля | state = investigate |
| light_off | 45 | Сбой света во время патруля | Проверка, цель switch |
| search_timeout | 30 | Поиск >= 10 с; нет зрения и шума | Патруль, responded |
| return_post | 20 | Проверка >= 5 с; нет новых стимулов | Патруль, убрать цель switch |
| alarm_reset | 10 | Тревога, оба стражника патрулируют | Снять alarm и responded |

## Сводка сценариев и видео

| № | Сценарий | Шаги | Срабатывания | Результат | Видео с |
|---|---|---:|---:|---|---|
| 01 | Обнаружение игрока и общая тревога | 1 | 5 | OK | 00:00 |
| 02 | Реакция на шум | 1 | 1 | OK | 00:09 |
| 03 | Игрок в тёмной зоне | 1 | 2 | OK | 00:18 |
| 04 | Открытие двери | 1 | 2 | OK | 00:27 |
| 05 | Потеря цели и завершение поиска | 3 | 9 | OK | 00:36 |
| 06 | Проверка выключателя | 2 | 2 | OK | 01:03 |
| 07 | Приоритет зрения над шумом | 1 | 5 | OK | 01:21 |
| 08 | Тревога прерывает расследование | 2 | 6 | OK | 01:30 |
| 09 | Граница таймера поиска | 4 | 9 | OK | 01:48 |
| 10 | Возврат на пост и спокойное патрулирование | 4 | 2 | OK | 02:24 |


Для всех 20 шагов ожидания совпали с результатом. Всего 43 продуктивных срабатываний;
покрытие типов правил — 13/13. Это проверки заданных сценариев, а не доказательство для всех игровых ситуаций.


### 01_player_seen — Обнаружение игрока и общая тревога

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/01_player_seen.mp4) · [Лог](results/01_player_seen.log) · [JSON-трасса](results/01_player_seen.json)

**Шаг 1, t=0 с.** Игрок входит в освещённый зал.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: light_visible_g1 → remember_target_g1 → see_player_g1 → raise_alarm_g1 → alarm_join_g2
Итог: g1=chase, g2=search; OK
```

### 02_noise_only — Реакция на шум

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/02_noise_only.mp4) · [Лог](results/02_noise_only.log) · [JSON-трасса](results/02_noise_only.json)

**Шаг 1, t=0 с.** Стражник G2 слышит шум на складе.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (hears,g2,noise) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: hear_noise_g2
Итог: g1=patrol, g2=investigate; OK
```

### 03_player_in_dark — Игрок в тёмной зоне

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/03_player_in_dark.mp4) · [Лог](results/03_player_in_dark.log) · [JSON-трасса](results/03_player_in_dark.json)

**Шаг 1, t=0 с.** Игрок в тёмном зале шумит, но остаётся невидимым.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,hall) (hears,g1,noise) (light_on,corridor) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: dark_zone_g1 → hear_noise_g1
Итог: g1=investigate, g2=patrol; OK
```

### 04_door_opened — Открытие двери

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/04_door_opened.mp4) · [Лог](results/04_door_opened.log) · [JSON-трасса](results/04_door_opened.json)

**Шаг 1, t=0 с.** Событие открытия двери на складе создаёт шум.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (door_opened,storage) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: door_opened_g2 → hear_noise_g2
Итог: g1=patrol, g2=investigate; OK
```

### 05_lost_target — Потеря цели и завершение поиска

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/05_lost_target.mp4) · [Лог](results/05_lost_target.log) · [JSON-трасса](results/05_lost_target.json)

**Шаг 1, t=0 с.** G1 видит игрока; G2 получает тревогу.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: light_visible_g1 → remember_target_g1 → see_player_g1 → raise_alarm_g1 → alarm_join_g2
Итог: g1=chase, g2=search; OK
```

**Шаг 2, t=1 с.** Игрок уходит в коридор; G1 запоминает зал.

```text
Вход: (alarm) (at,g1,hall) (at,g2,storage) (at,player,corridor) (last_seen,g1,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (responded,g2) (since,g1,0) (since,g2,0) (state,g1,chase) (state,g2,search) (time,1)
Правила: lost_target_g1
Итог: g1=search, g2=search; OK
```

**Шаг 3, t=11 с.** Прошло 10 секунд поиска; оба возвращаются на пост.

```text
Вход: (alarm) (at,g1,hall) (at,g2,storage) (at,player,corridor) (last_seen,g1,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (responded,g2) (since,g1,1) (since,g2,0) (state,g1,search) (state,g2,search) (time,11)
Правила: search_timeout_g1 → search_timeout_g2 → alarm_reset
Итог: g1=patrol, g2=patrol; OK
```

### 06_light_failure — Проверка выключателя

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/06_light_failure.mp4) · [Лог](results/06_light_failure.log) · [JSON-трасса](results/06_light_failure.json)

**Шаг 1, t=0 с.** В зале отключается свет; G1 проверяет выключатель.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (light_on,corridor) (light_on,hall) (light_on,storage) (power_failed,hall) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: light_off_g1
Итог: g1=investigate, g2=patrol; OK
```

**Шаг 2, t=5 с.** Свет восстановлен; за 5 секунд подозрений не найдено.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,investigate) (state,g2,patrol) (target,g1,switch) (time,5)
Правила: return_post_g1
Итог: g1=patrol, g2=patrol; OK
```

### 07_vision_over_noise — Приоритет зрения над шумом

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/07_vision_over_noise.mp4) · [Лог](results/07_vision_over_noise.log) · [JSON-трасса](results/07_vision_over_noise.json)

**Шаг 1, t=0 с.** G1 одновременно видит игрока и слышит шум.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,hall) (hears,g1,noise) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: light_visible_g1 → remember_target_g1 → see_player_g1 → raise_alarm_g1 → alarm_join_g2
Итог: g1=chase, g2=search; OK
```

### 08_alarm_interrupt — Тревога прерывает расследование

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/08_alarm_interrupt.mp4) · [Лог](results/08_alarm_interrupt.log) · [JSON-трасса](results/08_alarm_interrupt.json)

**Шаг 1, t=0 с.** G2 начинает расследование шума.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (hears,g2,noise) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: hear_noise_g2
Итог: g1=patrol, g2=investigate; OK
```

**Шаг 2, t=1 с.** G1 обнаруживает игрока; G2 переключается на поиск.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,investigate) (time,1)
Правила: light_visible_g1 → remember_target_g1 → see_player_g1 → raise_alarm_g1 → alarm_join_g2
Итог: g1=chase, g2=search; OK
```

### 09_timeout_boundary — Граница таймера поиска

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/09_timeout_boundary.mp4) · [Лог](results/09_timeout_boundary.log) · [JSON-трасса](results/09_timeout_boundary.json)

**Шаг 1, t=0 с.** G1 обнаруживает игрока.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: light_visible_g1 → remember_target_g1 → see_player_g1 → raise_alarm_g1 → alarm_join_g2
Итог: g1=chase, g2=search; OK
```

**Шаг 2, t=1 с.** Игрок уходит; начинается поиск G1.

```text
Вход: (alarm) (at,g1,hall) (at,g2,storage) (at,player,corridor) (last_seen,g1,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (responded,g2) (since,g1,0) (since,g2,0) (state,g1,chase) (state,g2,search) (time,1)
Правила: lost_target_g1
Итог: g1=search, g2=search; OK
```

**Шаг 3, t=10 с.** Через 9 секунд G1 ещё ищет, G2 уже закончил.

```text
Вход: (alarm) (at,g1,hall) (at,g2,storage) (at,player,corridor) (last_seen,g1,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (responded,g2) (since,g1,1) (since,g2,0) (state,g1,search) (state,g2,search) (time,10)
Правила: search_timeout_g2
Итог: g1=search, g2=patrol; OK
```

**Шаг 4, t=11 с.** Ровно через 10 секунд G1 завершает поиск.

```text
Вход: (alarm) (at,g1,hall) (at,g2,storage) (at,player,corridor) (last_seen,g1,hall) (light_on,corridor) (light_on,hall) (light_on,storage) (responded,g2) (since,g1,1) (since,g2,10) (state,g1,search) (state,g2,patrol) (time,11)
Правила: search_timeout_g1 → alarm_reset
Итог: g1=patrol, g2=patrol; OK
```

### 10_quiet_return — Возврат на пост и спокойное патрулирование

[Отдельное видео](https://github.com/VladimirPechenov/lab03-rules-logic/releases/download/v1.0/10_quiet_return.mp4) · [Лог](results/10_quiet_return.log) · [JSON-трасса](results/10_quiet_return.json)

**Шаг 1, t=0 с.** G1 проверяет шум.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (hears,g1,noise) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,0)
Правила: hear_noise_g1
Итог: g1=investigate, g2=patrol; OK
```

**Шаг 2, t=4 с.** Через 4 секунды проверка ещё продолжается.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,investigate) (state,g2,patrol) (time,4)
Правила: нет новых срабатываний
Итог: g1=investigate, g2=patrol; OK
```

**Шаг 3, t=5 с.** На пятой секунде G1 возвращается на пост.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,0) (since,g2,0) (state,g1,investigate) (state,g2,patrol) (time,5)
Правила: return_post_g1
Итог: g1=patrol, g2=patrol; OK
```

**Шаг 4, t=25 с.** Без новых событий состояние остаётся стабильным.

```text
Вход: (at,g1,hall) (at,g2,storage) (at,player,corridor) (light_on,corridor) (light_on,hall) (light_on,storage) (since,g1,5) (since,g2,0) (state,g1,patrol) (state,g2,patrol) (time,25)
Правила: нет новых срабатываний
Итог: g1=patrol, g2=patrol; OK
```

## Как заново получить видео и документы

Для экспорта видео нужен FFmpeg в PATH. Для титров нужен Arial (Windows) или DejaVu Sans (Linux).

```powershell
.\.venv\Scripts\python.exe -m rules.demo --render
.\.venv\Scripts\python.exe tools/build_report.py
```

Для одного сценария: `python -m rules.demo --scenario 05_lost_target`.
Для его отдельного экспорта добавьте `--render`. После полного экспорта в `videos/` находятся
10 отдельных MP4, `lab03_demo_full.mp4`, таблица глав `chapters.json`.
Не добавляйте MP4 в Git: `.gitignore` уже исключает их.

## Структура проекта

- `python/src/rules/engine.py` — прямой вывод и аудит изменений фактов.
- `python/src/rules/guard_rules.py` — 13 типов правил.
- `python/src/rules/scenarios.py` — общий исполнитель сценариев, экспорт логов.
- `python/src/rules/demo.py` — сцена и экспорт MP4.
- `python/tests/` — тесты движка и сценариев.
- `scenarios/` — исходные сценарии; `results/` — проверенные результаты.
- `docs/` — протокол, скриншоты, описание Release.
- `RUN_DEMO.cmd`, `CHECK.cmd` — запуск и проверка в Windows.

## Краткие ответы для защиты

**Почему это система правил?** Решение получается сопоставлением фактов с условиями продукций.
Переходы не зашиты в отрисовку: `Engine` не знает о графическом интерфейсе.

**Как решён конфликт «увидел и услышал»?** Зрение имеет приоритет 80, шум — 50.
После перехода в chase условие шумового правила для patrol уже ложно.

**Зачем память и время?** `last_seen` хранит последнюю известную зону. `since` вместе с `time`
позволяет завершить поиск через 10 секунд модельного времени и проверку через 5 секунд.

**Как избежать бесконечной тревоги?** Отметка responded блокирует повторный поиск по той же тревоге.
После возвращения обоих стражников в patrol общее правило alarm_reset снимает тревогу и отметки.

**Что доказывает видео?** Оно показывает состояние сцены на реальных снимках вывода,
с теми же JSON-входами и ожидаемыми результатами, которые проверены тестами и сохранены в логах.
