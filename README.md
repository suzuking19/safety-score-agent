# 安全スコア評価エージェントシステム

## 🌍 概要

このプロジェクトは、Google Agent Development Kit (ADK) を使用して開発された**旅行安全度評価システム**です。
指定された国・地域の安全性を 4 つの専門分野から総合的に分析し、100 点満点のスコアで評価します。

## 🎬 デモ動画

システムの動作を詳しく見たい場合は、以下のデモ動画をご覧ください：

[サンプル -フィリピンの安全性を評価](./demo/detail-demo.mp4)

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
│   ├── conflict_agent     # テロ・紛争リスク評価
│   ├── crime_agent            # 犯罪・治安評価
│   ├── infra_agent            # 社会基盤安定度評価
│   └── law_agent              # 法執行機関信頼性評価
└── safety_score_synthesizer   # 統合評価・レポート生成
```

### 📊 評価項目（各 25 点満点）

#### 1. テロ・紛争リスク評価 (25 点満点)

- **主要データソース**:
  - 外務省海外安全情報 (`https://www.anzen.mofa.go.jp/`)
- **評価基準**: 危険レベル（レベル 1-4）、テロ組織活動、武力衝突リスク
- **取得データ**:
  - 国別危険情報（退避勧告・渡航中止勧告等）
  - テロ・紛争関連キーワード（テロ、武力衝突、誘拐、過激派など）による情報抽出
- **対象国**: 主要高リスク国（イエメン、シリア、アフガニスタン、イラク、ソマリア等）

#### 2. 犯罪・治安評価 (25 点満点)

- **主要データソース**:
  - Numbeo 犯罪データベース (`https://www.numbeo.com/crime/`)
  - Vision of Humanity - 世界平和度指数 (`https://www.visionofhumanity.org/maps/`)
  - UNODC 犯罪統計 (`https://dataunodc.un.org/dp-intentional-homicide-victims`)
  - WHO 死亡統計 (`https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates`)
- **評価基準**:
  - 凶悪犯罪率（殺人・強盗・暴行）
  - 軽犯罪率（スリ・置き引き・詐欺）
  - 治安維持能力
- **取得データ**: 犯罪指数、殺人率、安全度指標

#### 3. 社会基盤安定度評価 (25 点満点)

- **主要データソース**:
  - Transparency International 汚職認識指数 (`https://www.transparency.org/en/cpi`)
  - WHO 交通安全データ (`https://www.who.int/data/gho/data/themes/road-safety`)
  - WHO 世界保健統計 (`https://www.who.int/data/gho`)
- **評価基準**:
  - 政治腐敗度（汚職認識指数）
  - 交通安全（交通事故死亡率）
  - 医療水準（医療アクセス・品質）
- **取得データ**: CPI 指数、交通事故統計、医療システム評価

#### 4. 法執行機関信頼性評価 (25 点満点)

- **主要データソース**:
  - Vision of Humanity - 世界平和度指数 (`https://www.visionofhumanity.org`)
  - 世界銀行ガバナンス指標 (`https://info.worldbank.org`)
  - Transparency International (`https://www.transparency.org/en/cpi`)
  - Gallup 世論調査 (`https://www.gallup.com/analytics/232838/world-poll.aspx`)
- **評価基準**:
  - 警察信頼度・効率性
  - 汚職度合い（司法・警察）
  - 司法制度機能（法の支配）
- **取得データ**: 警察信頼性指標、司法独立性、法の支配指数

## 📁 プロジェクト構造

```
myagent/
├── README.md                          # プロジェクト説明文書
├── requirements.txt                   # Python依存関係
├── demo/                              # デモ動画・資料
│   ├── demo.gif                       # メインデモGIF
│   ├── detailed-demo.mp4              # 詳細デモ動画
│   └── usage-example.mp4              # 使用例動画
├── screenshots/                       # スクリーンショット
│   ├── startup.png                    # 起動画面
│   ├── processing.png                 # 評価中画面
│   └── result.png                     # 結果表示画面
│
└── safety_score_agent/                # メインエージェントパッケージ
    ├── agent.py                       # メインエージェント定義
    ├── .env.example                   # 環境変数設定テンプレート
    │
    └── sub_agents/                    # サブエージェント群
        ├── conflict_agent/            # テロ・紛争リスク評価
        │   ├── agent.py               # エージェント定義
        │   ├── tool.py                # 外務省データ取得ツール
        │   └── test_tool.py           # ツールテストファイル
        │
        ├── crime_agent/               # 犯罪・治安評価
        │   ├── agent.py               # エージェント定義
        │   ├── tool.py                # 犯罪統計分析ツール
        │   └── test_tool.py           # ツールテストファイル
        │
        ├── infra_agent/               # 社会基盤安定度評価
        │   ├── agent.py               # エージェント定義
        │   ├── tool.py                # インフラ分析ツール
        │   └── test_tool.py           # ツールテストファイル
        │
        ├── law_agent/                 # 法執行機関信頼性評価
        │   ├── agent.py               # エージェント定義
        │   ├── tool.py                # 法執行機関分析ツール
        │   └── test_tool.py           # ツールテストファイル
        │
        └── synthesizer_agent/         # 統合評価エージェント
            └── agent.py               # 総合レポート生成
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

### 📞 緊急連絡先
```

## 💻 実行例

### 📱 基本的な使い方

1. **システム起動**

   ```bash
   adk web
   ```

2. **国名入力**

   - 評価したい国名を入力（例：「日本」「アメリカ」「フランス」）

3. **自動評価開始**

   - 4 つのエージェントが並列でデータ収集
   - リアルタイムで進捗表示

4. **総合レポート生成**
   - 100 点満点のスコア表示
   - 詳細な安全対策提言
   - 緊急連絡先一覧

### 📊 サンプル出力

```
🌍 日本の安全スコア評価結果

📊 総合安全スコア: 92/100 点
🟢 安全レベル: 優秀

📋 詳細評価:
1. テロ・紛争リスク: 24/25 点
2. 犯罪・治安評価: 23/25 点
3. 社会基盤安定度: 23/25 点
4. 法執行機関信頼性: 22/25 点
```

## 🔧 セットアップ・使用方法

### 🚀 クイックスタート

#### 1. リポジトリのクローン

```bash
git clone https://github.com/suzuking19/safety-score-agent.git
cd myagent
```

#### 2. 環境変数の設定

```bash
# .envファイルを作成
cp safety_score_agent/.env.example safety_score_agent/.env

# Google API Keyを設定
echo "GOOGLE_API_KEY=あなたのAPIキー" >> safety_score_agent/.env
```

または、`.env`ファイルを直接編集：

```bash
# safety_score_agent/.env
GOOGLE_API_KEY=your_actual_api_key_here
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

### 🌐 実際に使用されているウェブサイト・API

#### テロ・紛争リスク評価

- **外務省海外安全情報**: `https://www.anzen.mofa.go.jp/`
  - 国別危険情報ページ（例：イエメン、シリア、アフガニスタンなど）
  - 危険レベル（レベル 1-4）の自動判定
  - テロ・紛争関連キーワードによる情報抽出

#### 犯罪・治安評価

- **Numbeo 犯罪データベース**: `https://www.numbeo.com/crime/`
  - 国別犯罪指数データの取得
  - リアルタイム安全度スコア
- **Vision of Humanity**: `https://www.visionofhumanity.org/maps/`
  - 世界平和度指数（Global Peace Index）
  - 国別平和・治安指標
- **UNODC**: `https://dataunodc.un.org/dp-intentional-homicide-victims`
  - 国際殺人統計データ
- **WHO**: `https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates`
  - 死亡統計・健康指標

#### 社会基盤安定度評価

- **Transparency International**: `https://www.transparency.org/en/cpi`
  - 汚職認識指数（Corruption Perceptions Index）
- **WHO 交通安全**: `https://www.who.int/data/gho/data/themes/road-safety`
  - 国別交通事故死亡率データ
- **WHO 世界保健統計**: `https://www.who.int/data/gho`
  - 医療システム評価・医療アクセス指標

#### 法執行機関信頼性評価

- **世界銀行**: `https://info.worldbank.org`
  - ガバナンス指標（Worldwide Governance Indicators）
  - 法の支配指数
- **Vision of Humanity**: `https://www.visionofhumanity.org`
  - 警察信頼性・司法制度指標
- **Gallup**: `https://www.gallup.com/analytics/232838/world-poll.aspx`
  - 世論調査データ（警察信頼度等）

### 📊 データ取得の特徴

- **リアルタイム取得**: 各 API から最新データを動的に取得
- **フォールバック機能**: データ取得失敗時の代替データ提供
- **多言語対応**: 国名の表記揺れに対して複数パターンで検索
- **エラーハンドリング**: 接続エラー時の適切な処理とログ出力

## 🛠️ 技術スタック

- **フレームワーク**: Google Agent Development Kit (ADK) 1.3.0
- **LLM モデル**: Gemini 2.0 Flash
- **言語**: Python 3.8+
- **主要ライブラリ**:
  - `google-adk==1.3.0` - メインエージェントフレームワーク
  - `google-genai==1.20.0` - Gemini AI 統合
  - `requests==2.32.4` - HTTP 通信
  - `beautifulsoup4==4.12.3` - HTML 解析
  - `pydantic==2.11.6` - データ検証
  - `fastapi==0.115.12` - Web API（ADK 内部使用）
  - `httpx==0.28.1` - 非同期 HTTP 通信
- **データ処理**:
  - BeautifulSoup4 による Web スクレイピング
  - Requests ライブラリによる多重データソースアクセス
  - Pydantic によるデータ検証・構造化

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

## 🤖 robots.txt 準拠状況

このプロジェクトでは複数のウェブサイトからデータを取得しており、各サイトの robots.txt 規約への準拠状況を調査しました。

### 📋 調査結果

| サイト                                              | robots.txt 状況                   | 準拠性      | 備考                                            |
| --------------------------------------------------- | --------------------------------- | ----------- | ----------------------------------------------- |
| **外務省海外安全情報** (`anzen.mofa.go.jp`)         | ❌ robots.txt なし                | ✅ 問題なし | 政府サイト、公開情報のため制限なし              |
| **Numbeo** (`numbeo.com`)                           | ⚠️ `/heavy_crawling.any` のみ禁止 | ✅ 準拠     | 軽度なアクセスは許可されている                  |
| **Transparency International** (`transparency.org`) | ✅ 一般的な制限のみ               | ✅ 準拠     | `/cpresources/`, `/vendor/`, `/cache/` 等を禁止 |
| **WHO** (`who.int`)                                 | 🔴 多数のボット禁止               | ✅ 準拠     | 悪質ボットを禁止、一般アクセスは許可            |
| **Vision of Humanity** (`visionofhumanity.org`)     | ✅ 標準的な制限                   | ✅ 準拠     | `/wp-admin/`, `/wp-content/plugins/` 等を禁止   |
| **UNODC** (`dataunodc.un.org`)                      | ⚠️ `Crawl-delay: 10`              | ✅ 準拠     | 10 秒のクロール間隔を要求                       |
| **Gallup** (`gallup.com`)                           | ⚠️ 画像・アセット禁止             | ✅ 準拠     | データページへのアクセスは許可                  |

### 🔧 実装における配慮事項

#### ✅ 適切に実装されている点

1. **適切な User-Agent 設定**:
   ```
   Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
   ```
2. **タイムアウト設定**:

   - 全リクエストに 10-15 秒のタイムアウトを設定
   - サーバー負荷軽減に配慮

3. **エラーハンドリング**:

   - 接続失敗時の適切なフォールバック処理
   - リトライ制限による無制限アクセス防止

4. **レスポンシブ設計**:
   - HTTP ステータスコードの確認
   - 403/404 エラー時の適切な処理

#### ⚠️ 改善推奨事項

1. **UNODC サイト用の Crawl-delay 実装**:

   - 現在：遅延なし
   - 推奨：10 秒間隔での複数リクエスト制限

2. **リクエスト頻度の制限**:
   - 同一サイトへの連続アクセス制限機能追加を推奨

### 🎯 結論

**✅ 全体的な準拠状況：良好**

- 調査対象の全サイトにおいて robots.txt 規約に準拠
- データ取得対象ページは全て許可範囲内
- 悪質なクローリング行為は行っていない
- 公開データの適切な利用範囲内

このプロジェクトは各サイトの robots.txt 規約を尊重し、適切なウェブスクレイピング手法を採用しています。取得データは全て一般公開されている情報であり、各機関の提供する公開データへのアクセスは許可範囲内です。

---

**🌍 安全な旅行のために、客観的データに基づいた評価システムをご活用ください。**
