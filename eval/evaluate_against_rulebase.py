"""Evaluate trained model against a simple rule-based agent."""
from pathlib import Path
import torch
from models.discard_cnn import DiscardCNN


def load_model(path: Path) -> DiscardCNN:
    model = DiscardCNN()
    model.load_state_dict(torch.load(path, map_location='cpu'))
    model.eval()
    return model


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=Path, default=Path('models/weights/discard_cnn.pt'))
    args = parser.parse_args()

    model = load_model(args.model)
    # Placeholder for evaluation logic
    print('Loaded model with', sum(p.numel() for p in model.parameters()), 'parameters')
    print('Evaluation pipeline not yet implemented.')


if __name__ == '__main__':
    main()
