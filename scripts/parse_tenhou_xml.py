"""Parse Tenhou XML logs and save feature-action pairs.

This script extracts states and actions from Tenhou XML log files.
"""
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import json

# Basic features example (tile counts only)
def parse_game(xml_path: Path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Each game consists of multiple rounds (<INIT>, <T>, <D> etc.)
    data = []
    hand = []
    for elem in root.iter():
        if elem.tag == 'INIT':
            # starting hand for player 0 (first 13 tiles)
            tiles = elem.attrib.get('hai0')
            if tiles:
                hand = [int(t) for t in tiles.split(',')]
        elif elem.tag in ('D', 'T'):  # draw and discard
            actor = int(elem.attrib['who'])
            tile = int(elem.attrib['tile'])
            data.append({'actor': actor, 'tile': tile, 'hand': hand.copy()})
            if elem.tag == 'D':
                hand.append(tile)
            else:
                if tile in hand:
                    hand.remove(tile)
    return data

def main():
    parser = argparse.ArgumentParser(description="Parse Tenhou XML logs")
    parser.add_argument('xml', type=Path, help='Path to XML log file')
    parser.add_argument('--out', type=Path, default=Path('data/processed/parsed.json'))
    args = parser.parse_args()

    result = parse_game(args.xml)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
