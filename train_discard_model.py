"""Train DiscardCNN using parsed data."""
from pathlib import Path
import json
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from models.discard_cnn import DiscardCNN
from utils.mahjong import tile_to_index, parse_tiles

class DiscardDataset(Dataset):
    def __init__(self, json_file: Path):
        with open(json_file) as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        hand_tiles = item['hand']
        if isinstance(hand_tiles, str):
            hand_tiles = parse_tiles(hand_tiles)
        elif isinstance(hand_tiles, list) and hand_tiles and isinstance(hand_tiles[0], int):
            # old integer format from Tenhou parser
            hand_tiles = [hand_tiles[i] for i in range(len(hand_tiles))]
        tiles = torch.zeros(34)
        for t in hand_tiles:
            if isinstance(t, int):
                tiles[t % 34] += 1
            else:
                tiles[tile_to_index(t)] += 1
        x = tiles.view(1, -1, 1)  # [C, T, 1]
        target_tile = item['tile']
        if isinstance(target_tile, int):
            y = torch.tensor(target_tile % 34, dtype=torch.long)
        else:
            y = torch.tensor(tile_to_index(target_tile), dtype=torch.long)
        return x, y

def train(data_path: Path, epochs: int = 5):
    dataset = DiscardDataset(data_path)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    model = DiscardCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(epochs):
        for x, y in loader:
            out = model(x.float())
            loss = criterion(out, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    Path('models/weights').mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), 'models/weights/discard_cnn.pt')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path('data/processed/parsed.json'))
    parser.add_argument('--epochs', type=int, default=5)
    args = parser.parse_args()
    train(args.data, args.epochs)
