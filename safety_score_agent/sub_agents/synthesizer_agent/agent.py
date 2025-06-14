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
        self.agent = self._create_agent()
        self.categories = SafetyScoreCategories()
        self.thresholds = SafetyScoreThresholds()
        self.levels = SafetyScoreLevels()
    
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
        return f"""あなたは安全スコア統合評価エージェントです。

4つの専門エージェントから取得した安全情報を総合的に評価し、指定された国・地域の総合安全スコア（{TOTAL_MAX_SCORE}点満点）を算出します。

各エージェントからの情報:
- テロ・紛争リスク情報: {{conflict_info}}
- 犯罪・治安情報: {{crime_info}}  
- 社会基盤安定度情報: {{infra_info}}
- 法執行機関信頼性情報: {{law_info}}

{self._get_evaluation_criteria()}

{self._get_output_format()}

{self._get_evaluation_guidelines()}
"""
    
    def _get_evaluation_criteria(self) -> str:
        """評価基準を取得"""
        return f"""評価項目（各{MAX_SCORE_PER_CATEGORY}点満点）:
1. **テロ・紛争リスク評価** ({MAX_SCORE_PER_CATEGORY}点満点)
   - 外務省危険レベル、テロ組織活動状況、武力衝突リスクを評価
   - 25点: リスクなし、20点: 軽微なリスク、15点: 中程度のリスク、10点: 高リスク、5点: 極高リスク

2. **犯罪・治安評価** ({MAX_SCORE_PER_CATEGORY}点満点)
   - 凶悪犯罪率、軽犯罪率、治安維持能力を評価
   - 25点: 非常に安全、20点: 安全、15点: 普通、10点: やや危険、5点: 危険

3. **社会基盤安定度評価** ({MAX_SCORE_PER_CATEGORY}点満点)
   - 政治腐敗度、交通安全、医療水準を総合評価
   - 25点: 非常に安定、20点: 安定、15点: 普通、10点: やや不安定、5点: 不安定

4. **法執行機関信頼性評価** ({MAX_SCORE_PER_CATEGORY}点満点)
   - 警察信頼度、汚職度合い、司法制度機能レベルを評価
   - 25点: 非常に信頼できる、20点: 信頼できる、15点: 普通、10点: やや信頼できない、5点: 信頼できない"""
    
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
        return """重要な評価基準:
- 客観的データに基づいた点数付けを行う
- 各項目の相互作用・影響を考慮する
- 旅行者の実際の安全リスクに焦点を当てる
- 具体的で実行可能な安全対策を提案する"""
    
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