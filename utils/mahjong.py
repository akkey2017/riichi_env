import re
from typing import List

SUIT_OFFSETS = {'m': 0, 'p': 9, 's': 18, 'z': 27}


def normalize_tile(tile: str) -> str:
    """Strip special symbols and convert red tiles (0) to 5."""
    tile = re.sub(r'[\*_]', '', tile)
    if not tile:
        return tile
    suit = tile[0]
    num = tile[1]
    if num == '0':
        num = '5'
    return f"{suit}{num}"


def parse_tiles(tiles: str) -> List[str]:
    """Parse koba-style tile string into a list of tile codes (e.g. 'm1')."""
    result = []
    suit = ''
    for ch in tiles:
        if ch in 'mpsz':
            suit = ch
        elif ch.isdigit():
            if suit:
                num = '5' if ch == '0' else ch
                result.append(f"{suit}{num}")
    return result


def tile_to_index(tile: str) -> int:
    """Convert tile code like 'm1' to 0-33 index."""
    suit = tile[0]
    num = int(tile[1])
    return SUIT_OFFSETS[suit] + num - 1

