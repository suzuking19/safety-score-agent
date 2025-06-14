import unittest
from unittest.mock import patch, Mock, MagicMock
import requests
from bs4 import BeautifulSoup
import json
import time
from tool import (
    get_law_enforcement_data,
    get_gpi_law_enforcement_data,
    get_world_bank_governance_data,
    get_police_trust_data,
    calculate_law_enforcement_score,
    analyze_law_enforcement_risks,
    assess_traveler_law_enforcement_support,
    calculate_law_enforcement_reliability_impact,
    extract_gpi_data,
    extract_worldbank_data,
    scrape_transparency_international_data,
    scrape_gallup_trust_data,
    scrape_oecd_safety_data,
    get_default_gpi_data,
    get_default_worldbank_data,
    get_default_police_trust_data,
    get_fallback_law_enforcement_data
)


class TestLawEnforcementData(unittest.TestCase):
    """法執行機関データ取得機能のテスト"""
    
    def setUp(self):
        """テスト前の設定"""
        self.test_country = "Japan"
        self.sample_gpi_html = """
        <html>
            <body>
                <table>
                    <tr><td>Peace Score</td><td>1.85</td></tr>
                    <tr><td>Security Officers and Police</td><td>2.1</td></tr>
                    <tr><td>Internal Security Apparatus</td><td>1.9</td></tr>
                    <tr><td>Level of Violent Crime</td><td>2.0</td></tr>
                </table>
                <div>Rank: 10</div>
            </body>
        </html>
        """
        
        self.sample_wb_html = """
        <html>
            <body>
                <table>
                    <tr><td>Rule of Law</td><td>85.2%</td></tr>
                    <tr><td>Government Effectiveness</td><td>82.1%</td></tr>
                    <tr><td>Control of Corruption</td><td>79.8%</td></tr>
                </table>
            </body>
        </html>
        """

    @patch('tool.requests.Session')
    def test_get_gpi_law_enforcement_data_success(self, mock_session):
        """GPI法執行データ取得の成功テスト"""
        # 最初のレスポンス（国別ページへのリンクを含む）
        initial_html = f"""
        <html>
            <body>
                <a href="/country/{self.test_country.lower()}">{self.test_country}</a>
            </body>
        </html>
        """
        mock_initial_response = Mock()
        mock_initial_response.content = initial_html.encode('utf-8')
        
        # 2回目のレスポンス（実際のデータページ）
        mock_data_response = Mock()
        mock_data_response.content = self.sample_gpi_html.encode('utf-8')
        
        # セッションのgetメソッドが2回呼ばれる設定
        mock_session.return_value.get.side_effect = [mock_initial_response, mock_data_response]
        
        result = get_gpi_law_enforcement_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("peace_score", result)
        self.assertIn("police_reliability_score", result)
        self.assertEqual(result["data_source"], "Global Peace Index - Vision of Humanity")

    @patch('tool.requests.Session')
    def test_get_gpi_law_enforcement_data_failure(self, mock_session):
        """GPI法執行データ取得の失敗テスト"""
        # ネットワークエラーをシミュレート
        mock_session.return_value.get.side_effect = requests.exceptions.RequestException("Connection error")
        
        result = get_gpi_law_enforcement_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertEqual(result["data_source"], "Default GPI estimates")
        self.assertIn("note", result)

    def test_extract_gpi_data(self):
        """GPIデータ抽出のテスト"""
        soup = BeautifulSoup(self.sample_gpi_html, 'html.parser')
        result = extract_gpi_data(soup, self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertEqual(result["security_officers_and_police"], 2.1)
        self.assertEqual(result["internal_security_apparatus"], 1.9)
        self.assertEqual(result["level_of_violent_crime"], 2.0)

    @patch('tool.requests.Session')
    def test_get_world_bank_governance_data_success(self, mock_session):
        """世界銀行ガバナンスデータ取得の成功テスト"""
        mock_response = Mock()
        mock_response.content = self.sample_wb_html.encode('utf-8')
        mock_session.return_value.get.return_value = mock_response
        
        result = get_world_bank_governance_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("rule_of_law_percentile", result)
        self.assertEqual(result["data_source"], "World Bank Worldwide Governance Indicators")

    def test_extract_worldbank_data(self):
        """世界銀行データ抽出のテスト"""
        soup = BeautifulSoup(self.sample_wb_html, 'html.parser')
        result = extract_worldbank_data(soup, self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertEqual(result["rule_of_law_percentile"], 85.2)
        self.assertEqual(result["government_effectiveness_percentile"], 82.1)
        self.assertEqual(result["control_of_corruption_percentile"], 79.8)

    @patch('tool.scrape_oecd_safety_data')
    @patch('tool.scrape_gallup_trust_data')
    @patch('tool.scrape_transparency_international_data')
    def test_get_police_trust_data(self, mock_ti, mock_gallup, mock_oecd):
        """警察信頼度データ取得のテスト"""
        # モックデータの設定
        mock_ti.return_value = {"corruption_perception": 20.0, "sources": ["TI"]}
        mock_gallup.return_value = {"public_trust_score": 75.0, "sources": ["Gallup"]}
        mock_oecd.return_value = {"reporting_rate": 70.0, "sources": ["OECD"]}
        
        result = get_police_trust_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("public_trust_in_police", result)
        self.assertIn("corruption_in_police_force", result)
        self.assertIn("police_accountability_measures", result)

    @patch('tool.requests.Session')
    def test_scrape_transparency_international_data(self, mock_session):
        """Transparency Internationalデータスクレイピングのテスト"""
        sample_ti_html = """
        <table>
            <tr><td>Japan</td><td>73</td></tr>
        </table>
        """
        mock_response = Mock()
        mock_response.content = sample_ti_html.encode('utf-8')
        mock_session.return_value.get.return_value = mock_response
        
        result = scrape_transparency_international_data(self.test_country)
        
        self.assertIn("corruption_perception", result)
        self.assertIn("sources", result)

    def test_calculate_law_enforcement_score(self):
        """法執行機関スコア計算のテスト"""
        test_data = {
            "global_peace_index_data": {"police_reliability_score": 2.0},
            "world_bank_governance": {"rule_of_law_percentile": 80.0},
            "police_trust_indicators": {
                "public_trust_in_police": 75.0,
                "corruption_in_police_force": 20.0
            }
        }
        
        score = calculate_law_enforcement_score(test_data)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 25)

    def test_calculate_law_enforcement_score_empty_data(self):
        """空データでの法執行機関スコア計算テスト"""
        empty_data = {}
        score = calculate_law_enforcement_score(empty_data)
        
        self.assertEqual(score, 12.5)  # デフォルト値

    def test_analyze_law_enforcement_risks(self):
        """法執行機関リスク分析のテスト"""
        test_data = {
            "global_peace_index_data": {"police_reliability_score": 2.0},
            "world_bank_governance": {"rule_of_law_percentile": 80.0},
            "police_trust_indicators": {"corruption_in_police_force": 15.0}
        }
        
        analysis = analyze_law_enforcement_risks(test_data)
        
        self.assertIn("police_reliability_level", analysis)
        self.assertIn("corruption_risk_level", analysis)
        self.assertIn("judicial_system_trust", analysis)
        self.assertIn("specific_risks", analysis)
        self.assertIn("recommendations", analysis)

    def test_analyze_law_enforcement_risks_high_risk(self):
        """高リスク状況での法執行機関リスク分析テスト"""
        high_risk_data = {
            "global_peace_index_data": {"police_reliability_score": 4.0},  # 高い値（悪い）
            "world_bank_governance": {"rule_of_law_percentile": 25.0},  # 低い値（悪い）
            "police_trust_indicators": {"corruption_in_police_force": 70.0}  # 高い値（悪い）
        }
        
        analysis = analyze_law_enforcement_risks(high_risk_data)
        
        self.assertEqual(analysis["police_reliability_level"], "低")
        self.assertEqual(analysis["corruption_risk_level"], "高")
        self.assertEqual(analysis["judicial_system_trust"], "低")
        self.assertTrue(len(analysis["specific_risks"]) > 0)

    def test_assess_traveler_law_enforcement_support(self):
        """旅行者向け法執行機関サポート評価テスト"""
        test_data = {
            "police_trust_indicators": {
                "specialized_units": {"tourist_police": "Available"},
                "police_response_time_minutes": 8.0,
                "victim_satisfaction_rate": 80.0
            }
        }
        
        assessment = assess_traveler_law_enforcement_support(test_data)
        
        self.assertIn("emergency_response_quality", assessment)
        self.assertIn("language_support_availability", assessment)
        self.assertIn("tourist_specific_services", assessment)
        self.assertIn("recommended_contact_priority", assessment)

    def test_calculate_law_enforcement_reliability_impact(self):
        """法執行機関信頼性影響分析のテスト"""
        test_data = {
            "global_peace_index_data": {"police_reliability_score": 3.5},
            "world_bank_governance": {"rule_of_law_percentile": 35.0},
            "police_trust_indicators": {"corruption_in_police_force": 50.0}
        }
        
        impact = calculate_law_enforcement_reliability_impact(test_data)
        
        self.assertIn("direct_safety_impact", impact)
        self.assertIn("indirect_safety_impact", impact)
        self.assertIn("emergency_response_reliability", impact)
        self.assertIn("legal_protection_level", impact)

    def test_get_default_gpi_data(self):
        """デフォルトGPIデータのテスト"""
        result = get_default_gpi_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("police_reliability_score", result)
        self.assertEqual(result["data_source"], "Default GPI estimates")

    def test_get_default_worldbank_data(self):
        """デフォルト世界銀行データのテスト"""
        result = get_default_worldbank_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("rule_of_law_percentile", result)
        self.assertEqual(result["data_source"], "Default World Bank estimates")

    def test_get_default_police_trust_data(self):
        """デフォルト警察信頼度データのテスト"""
        result = get_default_police_trust_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("public_trust_in_police", result)
        self.assertIn("police_accountability_measures", result)

    def test_get_fallback_law_enforcement_data(self):
        """フォールバック法執行機関データのテスト"""
        result = get_fallback_law_enforcement_data(self.test_country)
        
        self.assertIn("message", result)
        self.assertIn("general_recommendations", result)
        self.assertIn("emergency_contacts_to_prepare", result)

    @patch('tool.get_police_trust_data')
    @patch('tool.get_world_bank_governance_data')
    @patch('tool.get_gpi_law_enforcement_data')
    def test_get_law_enforcement_data_integration(self, mock_gpi, mock_wb, mock_police):
        """法執行機関データ取得の統合テスト"""
        # モックデータの設定
        mock_gpi.return_value = {"police_reliability_score": 2.0}
        mock_wb.return_value = {"rule_of_law_percentile": 80.0}
        mock_police.return_value = {"public_trust_in_police": 75.0}
        
        result = get_law_enforcement_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("global_peace_index_data", result)
        self.assertIn("world_bank_governance", result)
        self.assertIn("police_trust_indicators", result)
        self.assertIn("overall_law_enforcement_score", result)
        self.assertIn("law_enforcement_categories", result)

    @patch('tool.get_police_trust_data')
    @patch('tool.get_world_bank_governance_data')
    @patch('tool.get_gpi_law_enforcement_data')
    def test_get_law_enforcement_data_with_errors(self, mock_gpi, mock_wb, mock_police):
        """エラー発生時の法執行機関データ取得テスト"""
        # すべてのモック関数でエラーを発生させる
        mock_gpi.side_effect = Exception("GPI error")
        mock_wb.side_effect = Exception("WB error")
        mock_police.side_effect = Exception("Police error")
        
        result = get_law_enforcement_data(self.test_country)
        
        self.assertEqual(result["country"], self.test_country)
        self.assertIn("error", result)
        self.assertIn("fallback_data", result)


class TestDataValidation(unittest.TestCase):
    """データ検証のテスト"""
    
    def test_score_bounds(self):
        """スコアの境界値テスト"""
        # 最高スコアのテスト
        high_score_data = {
            "global_peace_index_data": {"police_reliability_score": 1.0},
            "world_bank_governance": {"rule_of_law_percentile": 100.0},
            "police_trust_indicators": {
                "public_trust_in_police": 100.0,
                "corruption_in_police_force": 0.0
            }
        }
        
        score = calculate_law_enforcement_score(high_score_data)
        self.assertLessEqual(score, 25.0)
        
        # 最低スコアのテスト
        low_score_data = {
            "global_peace_index_data": {"police_reliability_score": 5.0},
            "world_bank_governance": {"rule_of_law_percentile": 0.0},
            "police_trust_indicators": {
                "public_trust_in_police": 0.0,
                "corruption_in_police_force": 100.0
            }
        }
        
        score = calculate_law_enforcement_score(low_score_data)
        self.assertGreaterEqual(score, 0.0)

    def test_data_types(self):
        """データ型の検証テスト"""
        result = get_default_gpi_data("TestCountry")
        
        self.assertIsInstance(result["country"], str)
        self.assertIsInstance(result["peace_score"], (int, float))
        self.assertIsInstance(result["police_reliability_score"], (int, float))


if __name__ == '__main__':
    # テストの実行
    unittest.main(verbosity=2)
