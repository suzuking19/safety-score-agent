# My AI Agent

## 概要

このプロジェクトは、Google Agent Development Kit (ADK) を使用して開発されたカスタム AI エージェントです。
エージェントの機能や特徴について詳細を記載してください。

## 特徴

- Google ADK を活用した効率的な開発
- カスタマイズ可能なエージェント機能
- Web インターフェース対応

## プロジェクト構造

```
myagent/
├── README.md           # プロジェクトの説明文書
├── requirements.txt    # Python依存関係
└── [開発中のファイル・フォルダが追加されます]
```

## 開発・学習ガイド

### 学習リソース

このプロジェクトの開発には以下のリソースを参考にしています：

- **[Google Agent Development Kit (ADK) 入門](https://speakerdeck.com/mickey_kubo/google-agent-development-kit-adk-ru-men-b921f3e5-49da-4ebc-ac65-2a3cea793e76)**
  - ADK の基本概念と使用方法
  - エージェント開発のベストプラクティス

### 環境構築

#### 1. サンプルプロジェクトのクローン

まず、参考用のサンプルプロジェクトを取得します：

```bash
git clone https://github.com/suzuking19/my-adk-agent.git
```

#### 2. 仮想環境の設定（WSL2/Ubuntu）

```bash
# 仮想環境を作成
python3 -m venv .venv

# 仮想環境をアクティベート
source .venv/bin/activate
```

#### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

#### 4. エージェントの起動

```bash
adk web
```

エージェントが起動したら、ブラウザでアクセスして使用できます。
終了するには `Ctrl + C` を押してください。

> **💡 ヒント**: 環境構築で問題が発生した場合は、上記の学習リソースのスライドを参照してください。
