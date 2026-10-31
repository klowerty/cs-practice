"""Статистика по журналу сервиса: разбор строк, подсчёты, отчёт."""

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
    parts = line.split(maxsplit=2)
    if len(parts) != 3:
        raise ValueError(f"bad line: {line!r}")
    time, level, message = parts
    if level not in VALID_LEVELS:
        raise ValueError(f"unknown level: {level!r}")
    message = message.rstrip("\n")
    if not message.strip():
        raise ValueError(f"empty message: {line!r}")
    return {"time": time, "level": level, "message": message}

def count_levels(lines) -> dict:
    """Сколько строк каждого уровня. Испорченные - под ключом BROKEN."""
    counts = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line.rstrip("\n"))
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
        else:
            counts[event["level"]] = counts.get(event["level"], 0) + 1
    return counts


def top_errors(lines, n: int) -> list[list]:
    """n самых частых сообщений уровня ERROR: [[сообщение, сколько раз], ...].

    При равенстве частот - по алфавиту.
    """
    freq = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line.rstrip("\n"))
        except ValueError:
            continue
        if event["level"] != "ERROR":
            continue
        msg = event["message"]
        freq[msg] = freq.get(msg, 0) + 1

    ordered = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return [[msg, cnt] for msg, cnt in ordered[:n]]


def format_report(counts: dict, errors: list[list]) -> str:
    """Текст отчёта по готовым подсчётам. Уровни - по алфавиту, в конце \\n."""
    out = ["Отчёт по журналу", ""]
    for level in sorted(counts):
        out.append(f"{level}: {counts[level]}")
    out.append("")
    out.append("Частые ошибки:")
    for msg, cnt in errors:
        out.append(f"- {msg} - {cnt}")
    return "\n".join(out) + "\n"