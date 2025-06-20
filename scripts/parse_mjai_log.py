"""Parse Mahjong game logs in the mjai JSON format and save feature/action pairs."""
import argparse
import json
from pathlib import Path
from typing import List

from utils.mahjong import parse_tiles, normalize_tile


def parse_game(json_path: Path) -> List[dict]:
    with open(json_path, 'r') as f:
        game = json.load(f)

    data = []
    for kyoku in game.get('log', []):
        hands = [[] for _ in range(4)]
        valid = False
        for event in kyoku:
            if 'qipai' in event:
                shoupai = event['qipai']['shoupai']
                hands = [parse_tiles(s) for s in shoupai]
                valid = True
            elif not valid:
                continue
            elif 'zimo' in event:
                l = event['zimo']['l']
                p = normalize_tile(event['zimo']['p'])
                hands[l].append(p)
            elif 'dapai' in event:
                l = event['dapai']['l']
                p = normalize_tile(event['dapai']['p'])
                data.append({'actor': l, 'tile': p, 'hand': hands[l].copy()})
                if p in hands[l]:
                    hands[l].remove(p)
            else:
                # Unsupported event, stop using this round
                valid = False
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse mjai JSON logs")
    parser.add_argument('json', type=Path, help='Path to mjai log (JSON)')
    parser.add_argument('--out', type=Path, default=Path('data/processed/parsed.json'))
    args = parser.parse_args()

    result = parse_game(args.json)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
