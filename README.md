# mp3-bpm-extractor

MP3ファイルから自動的にBPM（Beats Per Minute）を推定するPythonツールです。音楽ファイルのテンポ解析に興味のある方、音楽制作の補助に使いたい方におすすめです。

## 🧩 特徴

- MP3ファイルのBPMを自動解析
- Python製でカスタマイズが容易
- シンプルなコマンドライン操作

## 📦 必要な環境

- Python 3.8以上
- ffmpeg（MP3を読み込むために必要）
- 下記Pythonライブラリ：

```bash
pip install librosa numpy soundfile
````

## 🔧 インストール方法

1. このリポジトリをクローン：

```bash
git clone https://github.com/your-username/mp3-bpm-extractor.git
cd mp3-bpm-extractor
```

2. 依存ライブラリをインストール：

```bash
pip install -r requirements.txt
```

3. ffmpeg が未インストールの場合は、次のコマンドでインストール：

* macOS: `brew install ffmpeg`
* Ubuntu: `sudo apt install ffmpeg`
* Windows: [公式サイト](https://ffmpeg.org/download.html)からダウンロード

## 🚀 使い方

```bash
python bpm_extractor.py your_file.mp3
```

例：

```bash
python bpm_extractor.py sample.mp3
```

出力例：

```
Estimated BPM: 123.45
```

## 📁 ファイル構成

```
mp3-bpm-extractor/
├── bpm_extractor.py      # メインスクリプト
├── requirements.txt      # 必要ライブラリ一覧
└── README.md             # このファイル
```

## 📝 ライセンス

MIT License

## 📮 開発者メモ

* 精度は楽曲の構成や録音状態に依存します。
* より正確な解析を行いたい場合は、波形のプリプロセス（ノーマライズなど）を追加するとよいです。
