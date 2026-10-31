from pathlib import PurePath


def count_by_extension(paths: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for path in paths:
        suffix = PurePath(path).suffix  # ".PDF", ".txt", "" для Makefile
        ext = suffix[1:].lower() if suffix else ""
        result[ext] = result.get(ext, 0) + 1
    return result


def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    # ключ: (-вложенность, сам путь) - больше вложенность, при равенстве
    # алфавитно меньший путь идёт первым
    return min(paths, key=lambda p: (-p.count("/"), p))
