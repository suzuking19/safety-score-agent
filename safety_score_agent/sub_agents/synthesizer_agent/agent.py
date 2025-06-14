from typing import Dict, Any, Optional
from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"
MAX_SCORE_PER_CATEGORY = 25
TOTAL_MAX_SCORE = 100
NUM_CATEGORIES = 4


class SafetyScoreCategories:
    """安全スコア評価カテゴリの定義"""
    CONFLICT = "conflict"
    CRIME = "crime"
    INFRASTRUCTURE = "infrastructure"
    LAW_ENFORCEMENT = "law_enforcement"


class SafetyScoreThresholds:
    """安全レベルの閾値定義"""
    EXCELLENT = 90
    GOOD = 70
    AVERAGE = 50
    CAUTION = 30
    DANGEROUS = 0


class SafetyScoreLevels:
    """安全レベルラベル"""
    EXCELLENT = "優秀"
    GOOD = "良好"
    AVERAGE = "普通"
    CAUTION = "注意"
    DANGEROUS = "危険"


class SafetyScoreSynthesizerAgent:
    """安全スコア統合評価エージェント"""
    
    def __init__(self):
        self.categories = SafetyScoreCategories()
        self.thresholds = SafetyScoreThresholds()
        self.levels = SafetyScoreLevels()
        self.agent = self._create_agent()
    
    def _create_agent(self) -> LlmAgent:
        """LlmAgentインスタンスを作成"""
        return LlmAgent(
            name="SafetyScoreSynthesizer",
            model=GEMINI_MODEL,
            instruction=self._build_instruction(),
            description="4つの専門エージェントからの安全情報を統合し、総合安全スコア（100点満点）を算出します",
        )
    
    def _build_instruction(self) -> str:
        """エージェントの指示文を構築"""
        return f"""あなたは高度な安全スコア統合評価エージェントです。

## 🎯 主要任務
4つの専門エージェントから取得した多角的な安全情報を総合的に分析・評価し、指定された国・地域の総合安全スコア（{TOTAL_MAX_SCORE}点満点）を科学的かつ客観的に算出します。

## 📥 入力データソース
各専門エージェントからの詳細情報を統合処理します：
- **テロ・紛争リスク情報**: {{conflict_info}}
  - 外務省危険レベル、テロ組織動向、武力衝突データ、政治不安定度指標
- **犯罪・治安情報**: {{crime_info}}
  - 犯罪統計、治安当局対応能力、街頭犯罪率、観光客被害データ
- **社会基盤安定度情報**: {{infra_info}}
  - 政治腐敗指数、交通安全統計、医療システム評価、経済安定性指標
- **法執行機関信頼性情報**: {{law_info}}
  - 警察信頼度調査、司法制度評価、汚職度測定、法の支配指数

## 🧠 分析アプローチ
1. **多次元データ統合**: 各エージェントの情報を相互関連性を考慮して統合
2. **リスク重み付け評価**: 旅行者への実際の影響度に基づく重要度調整
3. **動的評価調整**: 最新情勢変化を反映した柔軟なスコア算出
4. **予測的リスク分析**: 現在のトレンドから将来リスクを予測
5. **地域特性考慮**: 文化的・地理的特性を踏まえた個別評価

{self._get_evaluation_criteria()}

{self._get_output_format()}

{self._get_evaluation_guidelines()}

## 🔍 品質保証要件
- データの信頼性と最新性を常に検証
- バイアスを排除した客観的評価の実施
- 明確な根拠に基づく透明性の高い評価プロセス
- 実用性と精度のバランスを重視した実践的提言の提供
"""
    
    def _get_evaluation_criteria(self) -> str:
        """評価基準を取得"""
        return f"""## 📊 詳細評価基準（各{MAX_SCORE_PER_CATEGORY}点満点）

### 1. 🚨 テロ・紛争リスク評価 ({MAX_SCORE_PER_CATEGORY}点満点)
**評価要素**: 外務省危険レベル、テロ組織活動状況、武力衝突リスク、政治不安定度
- **25点**: 危険レベル1、テロ活動なし、政治的安定
- **20点**: 危険レベル2、軽微なテロリスク、政治的摩擦あり
- **15点**: 危険レベル3、中程度のテロリスク、地域的紛争可能性
- **10点**: 危険レベル4、高テロリスク、武力衝突発生中
- **5点**: 危険レベル4以上、極高テロリスク、全面的武力衝突

### 2. 🔐 犯罪・治安評価 ({MAX_SCORE_PER_CATEGORY}点満点)
**評価要素**: 凶悪犯罪率、軽犯罪率、治安維持能力、観光客被害状況
- **25点**: 世界最高水準の治安、犯罪率極低、効果的な治安維持
- **20点**: 優秀な治安状況、低犯罪率、適切な警察対応
- **15点**: 平均的治安水準、中程度犯罪率、標準的警察機能
- **10点**: やや危険な治安状況、高犯罪率、警察対応に課題
- **5点**: 深刻な治安悪化、極高犯罪率、治安維持機能不全

### 3. 🏗️ 社会基盤安定度評価 ({MAX_SCORE_PER_CATEGORY}点満点)
**評価要素**: 政治腐敗度、交通安全、医療水準、経済安定性、災害対応能力
- **25点**: 透明性高い政治、優秀な交通・医療、強固な経済基盤
- **20点**: 政治的安定、良好な社会インフラ、安定した経済
- **15点**: 中程度の政治腐敗、平均的インフラ、標準的経済状況
- **10点**: 政治腐敗問題、インフラ課題、経済不安定要素
- **5点**: 深刻な政治腐敗、インフラ機能不全、経済危機状態

### 4. ⚖️ 法執行機関信頼性評価 ({MAX_SCORE_PER_CATEGORY}点満点)
**評価要素**: 警察信頼度、汚職度合い、司法制度機能、人権保護水準
- **25点**: 国際的に信頼される法執行機関、透明な司法制度
- **20点**: 高い警察信頼度、効果的な司法システム、適切な人権保護
- **15点**: 平均的な法執行機関、標準的司法機能、基本的人権保護
- **10点**: 警察への不信、司法制度の課題、人権問題の存在
- **5点**: 法執行機関への深刻な不信、司法制度機能不全、人権侵害"""
    
    def _get_output_format(self) -> str:
        """出力フォーマットを取得"""
        return f"""出力形式:
## 🌍 総合安全スコア評価レポート

### 📊 総合評価
- **総合安全スコア**: XX/{TOTAL_MAX_SCORE}点
- **安全レベル**: [{self.levels.EXCELLENT}({self.thresholds.EXCELLENT}-{TOTAL_MAX_SCORE}点)/{self.levels.GOOD}({self.thresholds.GOOD}-89点)/{self.levels.AVERAGE}({self.thresholds.AVERAGE}-69点)/{self.levels.CAUTION}({self.thresholds.CAUTION}-49点)/{self.levels.DANGEROUS}({self.thresholds.DANGEROUS}-29点)]

### 📋 詳細評価

#### 1. テロ・紛争リスク評価: XX/{MAX_SCORE_PER_CATEGORY}点
**評価理由**: [取得した情報に基づく具体的な評価根拠]
**主要リスク**: [特定されたリスク要因]

#### 2. 犯罪・治安評価: XX/{MAX_SCORE_PER_CATEGORY}点  
**評価理由**: [取得した情報に基づく具体的な評価根拠]
**主要リスク**: [特定されたリスク要因]

#### 3. 社会基盤安定度評価: XX/{MAX_SCORE_PER_CATEGORY}点
**評価理由**: [取得した情報に基づく具体的な評価根拠]
**主要課題**: [特定された課題]

#### 4. 法執行機関信頼性評価: XX/{MAX_SCORE_PER_CATEGORY}点
**評価理由**: [取得した情報に基づく具体的な評価根拠]
**信頼性課題**: [特定された課題]

### 🚨 総合的な安全対策提言
[各項目の評価結果を踏まえた総合的な安全対策の推奨事項]

### 📞 緊急時連絡先
[重要度順の緊急連絡先リスト]"""
    
    def _get_evaluation_guidelines(self) -> str:
        """評価ガイドラインを取得"""
        return """## 📋 評価実施ガイドライン

### 🎯 評価の基本原則
1. **データ駆動型評価**: 感情的判断を排除し、統計データと事実に基づく客観的評価
2. **多角的視点統合**: 各専門エージェントの視点を適切に重み付けして統合
3. **実用性重視**: 旅行者が実際に直面するリスクに焦点を当てた実践的評価
4. **時系列変化考慮**: 過去のトレンドと現在の状況を分析した動的評価

### 🔄 相互作用分析の重要性
- **テロリスク×治安状況**: テロ活動が一般犯罪率に与える影響を評価
- **政治不安×法執行**: 政治混乱が警察機能に与える影響を分析
- **経済状況×犯罪率**: 経済指標と犯罪発生率の相関関係を考慮
- **社会基盤×緊急対応**: インフラ状況が緊急時対応能力に与える影響を評価

### 📊 スコア算出の精密化
- **地域差分析**: 首都部と地方部での安全レベル格差を反映
- **季節変動考慮**: 観光シーズンや政治イベント時期の影響を加味
- **特定集団リスク**: 外国人観光客が特に注意すべきリスク要因を強調
- **緊急事態対応**: 自然災害や突発的事件への対応能力を評価

### 🚨 提言の具体性要件
- **段階別対策**: リスクレベルに応じた段階的安全対策の提示
- **地域別注意点**: エリア毎の具体的な注意事項と回避すべき場所
- **時間帯別リスク**: 時間帯や曜日による安全性の変化を明示
- **緊急時行動計画**: 具体的な緊急時対応手順と連絡先情報の提供

### 🔍 品質チェックポイント
- すべての評価項目に対して明確な根拠を提示
- 数値的評価と定性的分析のバランスを保持
- 最新の情勢変化を適切に反映
- 利用者の安全確保を最優先とした実践的提言の提供"""
    
    def get_safety_level(self, total_score: int) -> str:
        """総合スコアから安全レベルを判定"""
        if total_score >= self.thresholds.EXCELLENT:
            return self.levels.EXCELLENT
        elif total_score >= self.thresholds.GOOD:
            return self.levels.GOOD
        elif total_score >= self.thresholds.AVERAGE:
            return self.levels.AVERAGE
        elif total_score >= self.thresholds.CAUTION:
            return self.levels.CAUTION
        else:
            return self.levels.DANGEROUS
    
    def validate_scores(self, scores: Dict[str, int]) -> bool:
        """スコアの妥当性を検証"""
        if len(scores) != NUM_CATEGORIES:
            return False
        
        for category, score in scores.items():
            if not (0 <= score <= MAX_SCORE_PER_CATEGORY):
                return False
        
        return True
    
    def calculate_total_score(self, scores: Dict[str, int]) -> int:
        """各カテゴリのスコアから総合スコアを計算"""
        if not self.validate_scores(scores):
            raise ValueError("Invalid scores provided")
        
        return sum(scores.values())
    
    def synthesize_safety_report(self, 
                               conflict_info: str,
                               crime_info: str,
                               infra_info: str,
                               law_info: str) -> str:
        """安全情報を統合してレポートを生成"""
        prompt_data = {
            "conflict_info": conflict_info,
            "crime_info": crime_info,
            "infra_info": infra_info,
            "law_info": law_info
        }
        
        return self.agent.generate_response(prompt_data)


# インスタンス作成（後方互換性のため）
synthesizer_agent = SafetyScoreSynthesizerAgent()
safety_score_synthesizer = synthesizer_agent.agent