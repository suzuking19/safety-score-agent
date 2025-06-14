import unittest
from unittest.mock import patch, MagicMock
import time
from tool import (
    get_crime_data,
    get_numbeo_crime_data,
    get_global_peace_index_data,
    get_unodc_homicide_data,
    calculate_safety_score,
    get_fallback_crime_data,
    analyze_travel_safety_risks
)


class TestCrimeDataTools(unittest.TestCase):
    """犯罪データ取得ツールのテストクラス"""

    def setUp(self):
        """テスト前の初期化"""
        self.test_country = "Japan"
        self.sample_crime_data = {
            "country": "Japan",
            "numbeo_data": {
                "crime_index": 23.1,
                "safety_index": 76.9,
                "violent_crime_level": "Very Low",
                "property_crime_level": "Low",
                "pickpocket_probability": "Low",
                "theft_probability": "Low",
                "assault_probability": "Very Low",
                "data_source": "Numbeo Crime Database",
                "last_updated": "2024-12"
            },
            "global_peace_index": {
                "overall_peace_rank": 10,
                "peace_score": 1.34,
                "violent_crime_perception": 1.5,
                "weapons_access": 1.2,
                "security_apparatus": 1.8,
                "data_source": "Global Peace Index 2024",
                "methodology": "社会の安全・安心ドメイン指標"
            },
            "unodc_homicide_rate": {
                "homicide_rate_per_100k": 0.3,
                "total_homicides": 38,
                "year": 2023,
                "data_quality": "High",
                "data_source": "UNODC Global Study on Homicide",
                "comparative_ranking": "Very low homicide rate country"
            }
        }

    def test_get_numbeo_crime_data(self):
        """Numbeoデータ取得のテスト"""
        result = get_numbeo_crime_data(self.test_country)
        
        # 必要なキーが存在することを確認
        required_keys = [
            "crime_index", "safety_index", "violent_crime_level",
            "property_crime_level", "pickpocket_probability",
            "theft_probability", "assault_probability",
            "data_source", "last_updated"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # データ型の確認
        self.assertIsInstance(result["crime_index"], (int, float))
        self.assertIsInstance(result["safety_index"], (int, float))
        self.assertIsInstance(result["data_source"], str)
        
        # 値の範囲チェック
        self.assertGreaterEqual(result["crime_index"], 0)
        self.assertLessEqual(result["crime_index"], 100)
        self.assertGreaterEqual(result["safety_index"], 0)
        self.assertLessEqual(result["safety_index"], 100)

    def test_get_global_peace_index_data(self):
        """世界平和度指数データ取得のテスト"""
        result = get_global_peace_index_data(self.test_country)
        
        required_keys = [
            "overall_peace_rank", "peace_score", "violent_crime_perception",
            "weapons_access", "security_apparatus", "data_source", "methodology"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # データ型の確認
        self.assertIsInstance(result["overall_peace_rank"], int)
        self.assertIsInstance(result["peace_score"], (int, float))
        self.assertIsInstance(result["data_source"], str)
        
        # 値の妥当性チェック
        self.assertGreater(result["overall_peace_rank"], 0)
        self.assertGreater(result["peace_score"], 0)

    def test_get_unodc_homicide_data(self):
        """UNODC殺人率データ取得のテスト"""
        result = get_unodc_homicide_data(self.test_country)
        
        required_keys = [
            "homicide_rate_per_100k", "total_homicides", "year",
            "data_quality", "data_source", "comparative_ranking"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # データ型の確認
        self.assertIsInstance(result["homicide_rate_per_100k"], (int, float))
        self.assertIsInstance(result["total_homicides"], int)
        self.assertIsInstance(result["year"], int)
        
        # 値の妥当性チェック
        self.assertGreaterEqual(result["homicide_rate_per_100k"], 0)
        self.assertGreaterEqual(result["total_homicides"], 0)
        self.assertGreater(result["year"], 2000)

    def test_calculate_safety_score_with_complete_data(self):
        """完全なデータでの安全スコア計算テスト"""
        score = calculate_safety_score(self.sample_crime_data)
        
        # スコアが適切な範囲内にあることを確認
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # 日本のような安全な国では高いスコアが期待される
        self.assertGreater(score, 70)

    def test_calculate_safety_score_with_partial_data(self):
        """部分的なデータでの安全スコア計算テスト"""
        partial_data = {
            "numbeo_data": {"safety_index": 80.0}
        }
        
        score = calculate_safety_score(partial_data)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_calculate_safety_score_with_empty_data(self):
        """空データでの安全スコア計算テスト"""
        empty_data = {}
        score = calculate_safety_score(empty_data)
        
        # デフォルト値が返されることを確認
        self.assertEqual(score, 50.0)

    def test_calculate_safety_score_with_high_homicide_rate(self):
        """高い殺人率でのスコア計算テスト"""
        high_risk_data = {
            "unodc_homicide_rate": {"homicide_rate_per_100k": 15.0}
        }
        
        score = calculate_safety_score(high_risk_data)
        
        # 高い犯罪率では低いスコアが期待される
        self.assertLess(score, 50)

    def test_get_fallback_crime_data(self):
        """フォールバックデータ取得のテスト"""
        result = get_fallback_crime_data(self.test_country)
        
        required_keys = ["message", "general_advice", "data_sources_to_check"]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # アドバイスが適切に含まれていることを確認
        self.assertIsInstance(result["general_advice"], list)
        self.assertGreater(len(result["general_advice"]), 0)
        
        self.assertIsInstance(result["data_sources_to_check"], list)
        self.assertGreater(len(result["data_sources_to_check"]), 0)
        
        # メッセージに国名が含まれていることを確認
        self.assertIn(self.test_country, result["message"])

    @patch('tool.calculate_safety_score')
    def test_get_crime_data_success(self, mock_calculate_score):
        """犯罪データ取得成功のテスト"""
        mock_calculate_score.return_value = 75.5
        
        result = get_crime_data(self.test_country)
        
        # 必要なキーが存在することを確認
        required_keys = [
            "country", "numbeo_data", "global_peace_index",
            "unodc_homicide_rate", "crime_categories",
            "overall_safety_score", "data_collection_timestamp"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # 国名が正しく設定されていることを確認
        self.assertEqual(result["country"], self.test_country)
        
        # スコアが設定されていることを確認
        self.assertEqual(result["overall_safety_score"], 75.5)
        
        # タイムスタンプが現在時刻に近いことを確認
        current_time = time.time()
        self.assertLess(abs(result["data_collection_timestamp"] - current_time), 5)

    @patch('tool.calculate_safety_score')
    @patch('tool.get_numbeo_crime_data')
    def test_get_crime_data_with_exception(self, mock_numbeo, mock_calculate_score):
        """例外発生時の犯罪データ取得テスト"""
        mock_numbeo.side_effect = Exception("API Error")
        
        result = get_crime_data(self.test_country)
        
        # エラー情報が含まれていることを確認
        self.assertIn("error", result)
        self.assertIn("fallback_data", result)
        self.assertEqual(result["country"], self.test_country)

    def test_analyze_travel_safety_risks_low_risk(self):
        """低リスク国の旅行安全リスク分析テスト"""
        result = analyze_travel_safety_risks(self.sample_crime_data)
        
        required_keys = ["violent_crime_risk", "petty_crime_risk", "specific_risks", "recommendations"]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # データ型の確認
        self.assertIsInstance(result["specific_risks"], list)
        self.assertIsInstance(result["recommendations"], list)

    def test_analyze_travel_safety_risks_high_risk(self):
        """高リスク国の旅行安全リスク分析テスト"""
        high_risk_data = {
            "numbeo_data": {
                "pickpocket_probability": "Very High",
                "theft_probability": "High",
                "assault_probability": "High"
            },
            "unodc_homicide_rate": {
                "homicide_rate_per_100k": 15.0
            }
        }
        
        result = analyze_travel_safety_risks(high_risk_data)
        
        # 高リスクが適切に識別されることを確認
        self.assertEqual(result["violent_crime_risk"], "高")
        
        # 具体的なリスクと推奨事項が含まれていることを確認
        self.assertGreater(len(result["specific_risks"]), 0)
        self.assertGreater(len(result["recommendations"]), 0)
        
        # 高リスク項目が含まれていることを確認
        risk_text = " ".join(result["specific_risks"])
        self.assertIn("スリ", risk_text)
        self.assertIn("窃盗", risk_text)

    def test_analyze_travel_safety_risks_medium_homicide_rate(self):
        """中程度の殺人率での分析テスト"""
        medium_risk_data = {
            "unodc_homicide_rate": {
                "homicide_rate_per_100k": 7.0
            }
        }
        
        result = analyze_travel_safety_risks(medium_risk_data)
        self.assertEqual(result["violent_crime_risk"], "中")

    def test_analyze_travel_safety_risks_empty_data(self):
        """空データでの分析テスト"""
        result = analyze_travel_safety_risks({})
        
        # デフォルト値が設定されていることを確認
        self.assertIn("violent_crime_risk", result)
        self.assertIn("petty_crime_risk", result)
        self.assertIsInstance(result["specific_risks"], list)
        self.assertIsInstance(result["recommendations"], list)


class TestCrimeDataIntegration(unittest.TestCase):
    """統合テストクラス"""

    def test_full_workflow(self):
        """全体のワークフローテスト"""
        country = "TestCountry"
        
        # データ取得
        crime_data = get_crime_data(country)
        
        # 基本的な構造が正しいことを確認
        self.assertIn("country", crime_data)
        self.assertEqual(crime_data["country"], country)
        
        # エラーがない場合の分析
        if "error" not in crime_data:
            self.assertIn("overall_safety_score", crime_data)
            
            # リスク分析
            analysis = analyze_travel_safety_risks(crime_data)
            self.assertIn("violent_crime_risk", analysis)
            self.assertIn("petty_crime_risk", analysis)


if __name__ == "__main__":
    # テストスイートの実行
    unittest.main(verbosity=2)
