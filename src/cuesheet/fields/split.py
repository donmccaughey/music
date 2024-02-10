def split_quoted_string(type_name: str, s: str) -> str | None:
    tokens = split_tokens(s)
    if len(tokens) < 2:
        return None

    if tokens[0].upper() != type_name:
        return None

    del tokens[0]
    if tokens[0].startswith('"'):
        tokens[0] = tokens[0][1:]
    else:
        return None
    if tokens[-1].endswith('"'):
        tokens[-1] = tokens[-1][:-1]
    else:
        return None

    return ' '.join([token for token in tokens if token])


def split_ints(s: str, separator: str) -> list[int]:
    return [int(token) for token in s.split(separator) if token.isdigit()]


def split_tokens(s: str) -> list[str]:
    return [token for token in s.split() if token]
