def parse_line(line):
    if not line:
        return None
    parts = line.split('=')
    if len(parts) != 2:
        return None
    return parts[0].strip(), parts[1].strip()
