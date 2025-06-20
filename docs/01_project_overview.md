# Mortal/libriichi × CNN × 天鳳牌譜 AIプロジェクト

## 天鳳形式の牌譜でCNNモデルを教師あり学習させるまでの全工程まとめ

### 1. プロジェクトの目的・背景

本プロジェクトは、**4人打ちリーチ麻雀の最強AI開発**を目指して、以下の要素を組み合わせた学習パイプラインを構築します。

* **Mortal(libriichi) エンジン** – mjaiプロトコル対応の麻雀AI対戦エンジン
* **PyTorch実装のCNN** – 局面を多層テンソル表現し、打牌や鳴きを予測
* **天鳳特上卓の牌譜（XML形式）** – 実戦データを利用して教師あり学習

### 2. プロジェクト全体の流れ

1. **環境構築** – Python & Rust をセットアップし、libriichi-py をインストール
2. **データ準備** – 天鳳牌譜をパースして局面とアクションのペアを生成
3. **特徴量設計・モデル構築** – Suphx論文を参考に局面エンコーダとCNNモデルを実装
4. **教師あり学習** – 抽出データでモデルを学習し、精度検証
5. **評価・強化学習** – 学習モデルで自己対戦評価、必要に応じて強化学習へ発展

### 3. 詳細手順

#### Step 1. 環境構築

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
python -m venv .venv
source .venv/bin/activate  # Windowsは .venv\Scripts\activate
pip install maturin
pip install git+https://github.com/equim-chan/libriichi-py.git
```

#### Step 2. GitHubリポジトリ作成・連携

```bash
git init
git remote add origin https://github.com/ユーザ名/mahjong-cnn-ai.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

#### Step 3. 天鳳牌譜データ準備

1. `data/raw/` に XML 牌譜を配置
2. 牌譜パーサで局面ごとの **特徴量** と **アクション** を抽出し保存

#### Step 4. 特徴量エンコード / CNNモデル設計

* 局面を多層 one-hot テンソルへ変換（手牌・河・ドラ・点数など）
* PyTorch で打牌・鳴き判断モデルを実装

#### Step 5. 教師あり学習

```bash
python train_discard_model.py
```

クロスエントロピー損失で正解アクションを学習し、モデルを保存します。

#### Step 6. 評価・強化学習

学習モデルをMortal/libriichi環境で自己対戦させ、必要に応じてPPOやA2Cによる強化学習へ発展させます。

### 4. ディレクトリ構成例

```
mahjong-cnn-ai/
├── data/
│   ├── raw/          # 天鳳牌譜（XML）
│   └── processed/    # 学習用データ
├── scripts/
│   └── parse_tenhou_xml.py
├── models/
│   ├── discard_cnn.py
│   └── weights/
├── train_discard_model.py
├── eval/
│   └── evaluate_against_rulebase.py
└── requirements.txt
```

### 5. 開発の経緯・方針

* Mortal(libriichi)を利用し、mjaiプロトコルで高速対戦環境を構築
* 天鳳牌譜から教師あり学習し、Suphx論文を手がかりにモデルを改善
* 強化学習とのハイブリッドでより強いAIを目指します

### 6. 参考リンク

* [Suphx 論文](https://arxiv.org/abs/2003.13590)
* [Mortal GitHub](https://github.com/Mortal/naki)
* [libriichi-py](https://github.com/equim-chan/libriichi-py)
* [天鳳牌譜サンプル](https://tenhou.net/sc/raw/)
* [pytenhouparser](https://github.com/oyamad/pytenhouparser)
