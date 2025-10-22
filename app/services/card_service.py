def sanitize_links(links: list) -> list:
    return [l for l in links if isinstance(l, dict) and "label" in l and "url" in l]
