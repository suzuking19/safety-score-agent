# 安全スコア評価エージェントシステム

## 🌍 概要

このプロジェクトは、Google Agent Development Kit (ADK) を使用して開発された**旅行安全度評価システム**です。
指定された国・地域の安全性を 4 つの専門分野から総合的に分析し、100 点満点のスコアで評価します。

## ✨ 主な特徴

- **多層エージェント構造**: 4 つの専門評価エージェント + 1 つの統合エージェント
- **包括的安全評価**: テロ・紛争、犯罪・治安、社会基盤、法執行機関の 4 領域を評価
- **客観的スコアリング**: 各項目 25 点満点、総合 100 点満点での定量評価
- **実用的レポート**: 具体的な安全対策提言と緊急連絡先を含む詳細レポート
- **リアルタイムデータ**: 外務省、WHO、世界銀行等の最新データソースを活用

## 🏗️ システム構造

### エージェント構成

```
root_agent (SequentialAgent)
├── safety_score_gatherer (ParallelAgent) ── 並列データ収集
│   ├── conflict_info_agent     # テロ・紛争リスク評価
│   ├── crime_agent            # 犯罪・治安評価
│   ├── infra_agent            # 社会基盤安定度評価
│   └── law_agent              # 法執行機関信頼性評価
└── safety_score_synthesizer   # 統合評価・レポート生成
```

### 📊 評価項目（各 25 点満点）

#### 1. テロ・紛争リスク評価 (25 点満点)

- **データソース**: 外務省海外安全情報
- **評価基準**: 危険レベル、テロ組織活動、武力衝突リスク
- **ツール**: 外務省危険情報取得、テロリスク分析

#### 2. 犯罪・治安評価 (25 点満点)

- **データソース**: Numbeo、世界平和度指数、UNODC
- **評価基準**: 凶悪犯罪率、軽犯罪率、治安維持能力
- **ツール**: 犯罪統計分析、旅行者リスク評価

#### 3. 社会基盤安定度評価 (25 点満点)

- **データソース**: 汚職認識指数、WHO 交通安全、医療システム評価
- **評価基準**: 政治腐敗度、交通安全、医療水準
- **ツール**: インフラ安定度分析、緊急対応能力評価

#### 4. 法執行機関信頼性評価 (25 点満点)

- **データソース**: 世界銀行ガバナンス指標、警察信頼度調査
- **評価基準**: 警察信頼度、汚職度合い、司法制度機能
- **ツール**: 法執行機関信頼性分析、旅行者サポート評価

## 📁 プロジェクト構造

```
myagent/
├── README.md                    # プロジェクト説明文書
├── requirements.txt             # Python依存関係
├── .gitignore                   # Git除外設定
│
└── safety_score_agent/          # メインエージェントパッケージ
    ├── __init__.py              # パッケージ初期化
    ├── agent.py                 # メインエージェント定義
    ├── .env.example             # 環境変数設定例
    │
    └── sub_agents/              # サブエージェント群
        ├── conflict_agent/      # テロ・紛争リスク評価
        │   ├── agent.py         # エージェント定義
        │   └── tool.py          # 外務省データ取得ツール
        │
        ├── crime_agent/         # 犯罪・治安評価
        │   ├── agent.py         # エージェント定義
        │   └── tool.py          # 犯罪統計分析ツール
        │
        ├── infra_agent/         # 社会基盤安定度評価
        │   ├── agent.py         # エージェント定義
        │   └── tool.py          # インフラ分析ツール
        │
        ├── law_agent/           # 法執行機関信頼性評価
        │   ├── agent.py         # エージェント定義
        │   └── tool.py          # 法執行機関分析ツール
        │
        └── synthesizer_agent/   # 統合評価エージェント
            └── agent.py         # 総合レポート生成
```

## 🎯 安全レベル分類

| スコア    | 安全レベル | 説明                                   |
| --------- | ---------- | -------------------------------------- |
| 90-100 点 | 🟢 優秀    | 非常に安全、一般的な注意のみで問題なし |
| 70-89 点  | 🔵 良好    | 安全、基本的な注意を払えば問題なし     |
| 50-69 点  | 🟡 普通    | 標準的なリスク、適切な準備と注意が必要 |
| 30-49 点  | 🟠 注意    | 注意が必要、詳細な事前調査と対策が必要 |
| 0-29 点   | 🔴 危険    | 危険、渡航の再検討を強く推奨           |

## 📄 出力レポート形式

```markdown
## 🌍 総合安全スコア評価レポート

### 📊 総合評価

- **総合安全スコア**: XX/100 点
- **安全レベル**: [優秀/良好/普通/注意/危険]

### 📋 詳細評価

#### 1. テロ・紛争リスク評価: XX/25 点

#### 2. 犯罪・治安評価: XX/25 点

#### 3. 社会基盤安定度評価: XX/25 点

#### 4. 法執行機関信頼性評価: XX/25 点

### 🚨 総合的な安全対策提言
```

## 🔧 セットアップ・使用方法

### 🚀 クイックスタート

#### 1. リポジトリのクローン

```bash
git clone https://github.com/suzuking19/safety-score-agent.git
```

該当ディレクトリへの移動

#### 2. 環境変数の設定

```bash
# .envファイルを作成
cp safety_score_agent/.env.example safety_score_agent/.env

# Google API Keyを設定
echo "GOOGLE_API_KEY=あなたのAPIキー" > safety_score_agent/.env
```

#### 3. 仮想環境の作成とアクティベート

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# または
.venv\Scripts\activate     # Windows
```

#### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

#### 5. エージェントの起動

```bash
adk web
```

## 🔑 必要な環境変数

| 変数名           | 説明                   | 必須 |
| ---------------- | ---------------------- | ---- |
| `GOOGLE_API_KEY` | Google Gemini API キー | ✅   |

## 📚 データソース

- **外務省**: 海外安全情報・危険情報
- **世界平和度指数 (GPI)**: 暴力犯罪認識・警察信頼性
- **Numbeo**: クラウドソース犯罪指数
- **国連薬物犯罪事務所 (UNODC)**: 殺人率統計
- **世界銀行**: ガバナンス指標・法の支配
- **汚職認識指数 (CPI)**: 政治透明性
- **WHO**: 交通安全・医療システム評価

## �️ 技術スタック

- **フレームワーク**: Google Agent Development Kit (ADK)
- **LLM モデル**: Gemini 2.0 Flash
- **言語**: Python 3.8+
- **主要ライブラリ**:
  - `google-adk`
  - `requests`
  - `beautifulsoup4`
  - `pydantic`

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Request を作成

## 📜 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

## 🔗 参考リンク

- **[Google Agent Development Kit (ADK) 入門](https://speakerdeck.com/mickey_kubo/google-agent-development-kit-adk-ru-men-b921f3e5-49da-4ebc-ac65-2a3cea793e76)** - ADK 開発の基礎学習
- **[外務省海外安全情報](https://www.anzen.mofa.go.jp/)** - 海外安全・危険情報
- **[世界平和度指数](https://www.visionofhumanity.org/maps/)** - 平和度・治安指標
- **[Transparency International](https://www.transparency.org/en/cpi)** - 汚職認識指数
- **[WHO Global Health Observatory](https://www.who.int/data/gho)** - 世界保健統計

---

**🌍 安全な旅行のために、客観的データに基づいた評価システムをご活用ください。**
