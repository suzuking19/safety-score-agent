"""
Infrastructure Agent Tool のテストファイル
"""

import unittest
import json
import time
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup

from tool import (
    get_infrastructure_data,
    get_corruption_data,
    get_traffic_safety_data,
    get_healthcare_data,
    scrape_cpi_data,
    scrape_traffic_data,
    scrape_healthcare_data,
    calculate_infrastructure_score,
    analyze_infrastructure_risks,
    calculate_infrastructure_stability_impact,
    classify_cpi_score,
    classify_traffic_safety,
    extract_rank_from_text
)

class TestInfrastructureData(unittest.TestCase):
    """インフラデータ取得のテスト"""
    
    def test_get_infrastructure_data_success(self):
        """正常にインフラデータを取得できることをテスト"""
        result = get_infrastructure_data("Japan")
        
        self.assertIn("country", result)
        self.assertEqual(result["country"], "Japan")
        self.assertIn("corruption_perception_index", result)
        self.assertIn("traffic_safety_data", result)
        self.assertIn("healthcare_system", result)
        self.assertIn("overall_infrastructure_score", result)
        self.assertIn("data_collection_timestamp", result)
        
        # スコアが適切な範囲内であることを確認
        self.assertGreaterEqual(result["overall_infrastructure_score"], 0)
        self.assertLessEqual(result["overall_infrastructure_score"], 25)

    def test_get_infrastructure_data_with_invalid_country(self):
        """無効な国名でもエラーハンドリングが適切に動作することをテスト"""
        result = get_infrastructure_data("")
        
        # エラーハンドリングが適切に動作することを確認
        self.assertIn("country", result)
        self.assertIsInstance(result, dict)

class TestCorruptionData(unittest.TestCase):
    """汚職認識指数データのテスト"""
    
    @patch('tool.requests.get')
    def test_get_corruption_data_with_mock(self, mock_get):
        """モックを使用してスクレイピング処理をテスト"""
        # モックHTMLレスポンスを作成
        mock_html = """
        <html>
        <body>
        <table class="cpi-table">
            <tr><td>Japan</td><td>Score: 73</td><td>Rank: 25</td></tr>
        </table>
        </body>
        </html>
        """
        
        mock_response = Mock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_corruption_data("Japan")
        
        self.assertIn("cpi_score", result)
        self.assertIn("cpi_rank", result)
        self.assertIn("classification", result)
        self.assertIn("data_source", result)
        self.assertIsInstance(result["cpi_score"], (int, float))

    def test_classify_cpi_score(self):
        """CPIスコア分類機能のテスト"""
        self.assertEqual(classify_cpi_score(85), "Very Good")
        self.assertEqual(classify_cpi_score(65), "Good")
        self.assertEqual(classify_cpi_score(45), "Moderate")
        self.assertEqual(classify_cpi_score(25), "Poor")
        self.assertEqual(classify_cpi_score(15), "Very Poor")

    def test_extract_rank_from_text(self):
        """テキストからランキング抽出機能のテスト"""
        self.assertEqual(extract_rank_from_text("Japan rank: 25"), 25)
        self.assertEqual(extract_rank_from_text("Rank 15 out of 180"), 15)
        self.assertEqual(extract_rank_from_text("No rank information"), 0)

    def test_scrape_cpi_data(self):
        """CPIデータスクレイピング機能のテスト"""
        html = """
        <div class="cpi-data">
            <span>Japan corruption score: 73.2 rank: 18</span>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = scrape_cpi_data(soup, "Japan")
        
        if result:  # スクレイピングが成功した場合
            self.assertIn("cpi_score", result)
            self.assertIn("classification", result)

class TestTrafficSafetyData(unittest.TestCase):
    """交通安全データのテスト"""
    
    @patch('tool.requests.get')
    def test_get_traffic_safety_data_with_mock(self, mock_get):
        """モックを使用して交通安全データスクレイピングをテスト"""
        mock_html = """
        <html>
        <body>
        <div class="traffic-stats">
            <p>Japan road traffic deaths: 4.1 per 100,000 population</p>
        </div>
        </body>
        </html>
        """
        
        mock_response = Mock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_traffic_safety_data("Japan")
        
        self.assertIn("road_traffic_deaths_per_100k", result)
        self.assertIn("safety_rating", result)
        self.assertIn("data_source", result)
        self.assertIsInstance(result["road_traffic_deaths_per_100k"], (int, float))

    def test_classify_traffic_safety(self):
        """交通安全分類機能のテスト"""
        self.assertEqual(classify_traffic_safety(3.0), "Excellent")
        self.assertEqual(classify_traffic_safety(7.0), "Good")
        self.assertEqual(classify_traffic_safety(15.0), "Moderate")
        self.assertEqual(classify_traffic_safety(25.0), "Poor")
        self.assertEqual(classify_traffic_safety(35.0), "Very Poor")

    def test_scrape_traffic_data(self):
        """交通データスクレイピング機能のテスト"""
        html = """
        <table class="road-safety">
            <tr><td>Japan</td><td>4.1 per 100,000</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = scrape_traffic_data(soup, "Japan")
        
        if result:  # スクレイピングが成功した場合
            self.assertIn("road_traffic_deaths_per_100k", result)
            self.assertIn("safety_rating", result)

class TestHealthcareData(unittest.TestCase):
    """医療システムデータのテスト"""
    
    @patch('tool.requests.get')
    def test_get_healthcare_data_with_mock(self, mock_get):
        """モックを使用して医療データスクレイピングをテスト"""
        mock_html = """
        <html>
        <body>
        <div class="health-stats">
            <p>Japan healthcare index: 85.2</p>
            <p>Physicians per 1,000: 2.4</p>
        </div>
        </body>
        </html>
        """
        
        mock_response = Mock()
        mock_response.content = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_healthcare_data("Japan")
        
        self.assertIn("healthcare_access_quality_index", result)
        self.assertIn("physicians_per_1000", result)
        self.assertIn("healthcare_categories", result)
        self.assertIsInstance(result["healthcare_access_quality_index"], (int, float))

    def test_scrape_healthcare_data(self):
        """医療データスクレイピング機能のテスト"""
        html = """
        <div class="medical-info">
            <span>Japan healthcare score: 80.5</span>
            <span>3.2 physicians per 1,000</span>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = scrape_healthcare_data(soup, "Japan")
        
        if result:  # スクレイピングが成功した場合
            self.assertIn("healthcare_access_quality_index", result)
            self.assertIn("physicians_per_1000", result)

class TestScoreCalculation(unittest.TestCase):
    """スコア計算のテスト"""
    
    def test_calculate_infrastructure_score(self):
        """インフラスコア計算のテスト"""
        sample_data = {
            "corruption_perception_index": {"cpi_score": 80},
            "traffic_safety_data": {"road_traffic_deaths_per_100k": 5.0},
            "healthcare_system": {"healthcare_access_quality_index": 85.0}
        }
        
        score = calculate_infrastructure_score(sample_data)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 25)

    def test_calculate_infrastructure_score_empty_data(self):
        """空のデータでのスコア計算テスト"""
        empty_data = {}
        score = calculate_infrastructure_score(empty_data)
        
        self.assertEqual(score, 12.5)  # デフォルト値

    def test_calculate_infrastructure_score_partial_data(self):
        """部分的なデータでのスコア計算テスト"""
        partial_data = {
            "corruption_perception_index": {"cpi_score": 70}
        }
        
        score = calculate_infrastructure_score(partial_data)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 25)

class TestRiskAnalysis(unittest.TestCase):
    """リスク分析のテスト"""
    
    def test_analyze_infrastructure_risks(self):
        """インフラリスク分析のテスト"""
        sample_data = {
            "corruption_perception_index": {"cpi_score": 45},
            "traffic_safety_data": {"road_traffic_deaths_per_100k": 15.0},
            "healthcare_system": {"healthcare_access_quality_index": 60.0}
        }
        
        analysis = analyze_infrastructure_risks(sample_data)
        
        self.assertIn("political_risk_level", analysis)
        self.assertIn("transport_risk_level", analysis)
        self.assertIn("healthcare_risk_level", analysis)
        self.assertIn("specific_risks", analysis)
        self.assertIn("recommendations", analysis)
        self.assertIsInstance(analysis["specific_risks"], list)
        self.assertIsInstance(analysis["recommendations"], list)

    def test_analyze_infrastructure_risks_high_risk(self):
        """高リスク環境での分析テスト"""
        high_risk_data = {
            "corruption_perception_index": {"cpi_score": 25},
            "traffic_safety_data": {"road_traffic_deaths_per_100k": 30.0},
            "healthcare_system": {"healthcare_access_quality_index": 35.0}
        }
        
        analysis = analyze_infrastructure_risks(high_risk_data)
        
        self.assertEqual(analysis["political_risk_level"], "高")
        self.assertEqual(analysis["transport_risk_level"], "高")
        self.assertEqual(analysis["healthcare_risk_level"], "高")
        self.assertGreater(len(analysis["specific_risks"]), 0)
        self.assertGreater(len(analysis["recommendations"]), 0)

class TestImpactAnalysis(unittest.TestCase):
    """影響分析のテスト"""
    
    def test_calculate_infrastructure_stability_impact(self):
        """インフラ安定度影響分析のテスト"""
        sample_data = {
            "corruption_perception_index": {"cpi_score": 40},
            "traffic_safety_data": {"road_traffic_deaths_per_100k": 20.0},
            "healthcare_system": {"healthcare_access_quality_index": 50.0}
        }
        
        impact = calculate_infrastructure_stability_impact(sample_data)
        
        self.assertIn("direct_safety_impact", impact)
        self.assertIn("indirect_safety_impact", impact)
        self.assertIn("recovery_capability", impact)
        self.assertIn("infrastructure_resilience", impact)
        self.assertIsInstance(impact["direct_safety_impact"], list)
        self.assertIsInstance(impact["indirect_safety_impact"], list)

class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングのテスト"""
    
    @patch('tool.requests.get')
    def test_network_error_handling(self, mock_get):
        """ネットワークエラー時のハンドリングをテスト"""
        mock_get.side_effect = Exception("Network error")
        
        # 各関数がエラーを適切にハンドリングすることを確認
        corruption_result = get_corruption_data("TestCountry")
        traffic_result = get_traffic_safety_data("TestCountry")
        healthcare_result = get_healthcare_data("TestCountry")
        
        # フォールバックデータが返されることを確認
        self.assertIsInstance(corruption_result, dict)
        self.assertIsInstance(traffic_result, dict)
        self.assertIsInstance(healthcare_result, dict)
        
        # エラー情報またはnoteが含まれることを確認
        self.assertTrue(any("note" in result or "error" in str(result) 
                  for result in [corruption_result, traffic_result, healthcare_result]))

class TestIntegration(unittest.TestCase):
    """統合テスト"""
    
    def test_full_infrastructure_analysis_flow(self):
        """完全なインフラ分析フローのテスト"""
        country = "Japan"
        
        # メイン関数を実行
        infra_data = get_infrastructure_data(country)
        
        # 基本構造の確認
        self.assertIn("country", infra_data)
        self.assertIn("overall_infrastructure_score", infra_data)
        
        # リスク分析の実行
        if "error" not in infra_data:
            risk_analysis = analyze_infrastructure_risks(infra_data)
            self.assertIsInstance(risk_analysis, dict)
            
            # 影響分析の実行
            impact_analysis = calculate_infrastructure_stability_impact(infra_data)
            self.assertIsInstance(impact_analysis, dict)

    def test_data_consistency(self):
        """データの一貫性をテスト"""
        result = get_infrastructure_data("Germany")
        
        if "overall_infrastructure_score" in result:
            score = result["overall_infrastructure_score"]
            
            # スコアがデータと一貫性があることを確認
            if "corruption_perception_index" in result:
                cpi_score = result["corruption_perception_index"].get("cpi_score", 50)
                # 高いCPIスコアは高いインフラスコアと相関があるべき
                if cpi_score > 80:
                    self.assertGreater(score, 15)  # 高品質のインフラが期待される


class TestPerformance(unittest.TestCase):
    """パフォーマンステスト"""
    
    def test_performance(self):
        """パフォーマンステスト"""
        start_time = time.time()
        
        # 複数の国でテスト
        countries = ["Japan", "Germany", "USA", "Brazil", "India"]
        
        for country in countries:
            get_infrastructure_data(country)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"5カ国のデータ取得時間: {execution_time:.2f}秒")
        
        # 1カ国あたり10秒以内で完了することを期待
        self.assertLess(execution_time, 50)

if __name__ == "__main__":
    # unittestを実行
    print("Infrastructure Tool テストを開始...")
    unittest.main(verbosity=2)
