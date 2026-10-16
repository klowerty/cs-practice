def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("не ровно три поля")
    city, temp, date = parts
    if not city or not date:
        raise ValueError("пустой город или дата")
    try:
        temperature = float(temp)
    except ValueError as exc:
        raise ValueError(f"температура не число: {temp!r}") from exc
    return {"city": city, "temperature": temperature, "date": date}

def read_valid(lines: list[str]) -> list[dict]:
    records = []
    for line in lines:
        if not line.strip():
            continue
        try:
            records.append(parse_record(line))
        except ValueError:
            continue
    return records

def average_by_city(records: list[dict]) -> dict:
    total = {}
    count = {}
    for r in records:
        c = r["city"]
        total[c] = total.get(c, 0.0) + r["temperature"]
        count[c] = count.get(c, 0) + 1
    return {c: round(total[c] / count[c], 1) for c in total}

def warmest_city(records: list[dict]) -> str:
    averages = average_by_city(records)
    if not averages:
        return ""
    return min(averages, key=lambda c: (-averages[c], c))