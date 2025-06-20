# Mahjong CNN AI Project

This repository demonstrates how to train a Mahjong AI using Mortal (libriichi) and convolutional neural networks.
This repository contains sample code for building a Mahjong AI pipeline.

* `scripts/parse_tenhou_xml.py` – convert Tenhou XML logs to a simple dataset
* `scripts/parse_mjai_log.py` – parse the mjai-style JSON format described in
  `docs/01_project_overview.md`
* `train_discard_model.py` – train a small CNN to predict discards from the
  processed data
* `eval/evaluate_against_rulebase.py` – evaluate the trained model

See [docs/01_project_overview.md](docs/01_project_overview.md) for a full project outline.

## Usage

1. Parse a game log:

   ```bash
   python scripts/parse_mjai_log.py path/to/game.json --out data/processed/parsed.json
   ```

2. Train the discard model:

   ```bash
   python train_discard_model.py --data data/processed/parsed.json --epochs 5
   ```
