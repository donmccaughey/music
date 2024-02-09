def to_ints(s: str, separator: str) -> list[int]:
    return [int(token) for token in s.split(separator) if token.isdigit()]


def to_tokens(s: str) -> list[str]:
    return [token for token in s.split() if token]
