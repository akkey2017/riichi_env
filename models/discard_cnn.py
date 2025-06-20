"""Simple CNN model for discard decision prediction."""
from typing import Tuple

import torch
from torch import nn

class DiscardCNN(nn.Module):
    def __init__(self, input_channels: int = 1, num_tiles: int = 34):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * num_tiles, 128),
            nn.ReLU(),
            nn.Linear(128, num_tiles),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch = x.size(0)
        out = self.conv(x)
        out = out.view(batch, -1)
        return self.fc(out)
