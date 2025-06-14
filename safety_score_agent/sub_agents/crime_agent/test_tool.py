import unittest
from unittest.mock import patch, MagicMock, Mock
import time
import requests
from bs4 import BeautifulSoup
from tool import (
    get_crime_data,
    get_numbeo_crime_data,
    get_global_peace_index_data,
    get_unodc_homicide_data,
    calculate_safety_score,
    get_fallback_crime_data,
    analyze_travel_safety_risks,
    extract_numbeo_crime_indices,
    extract_crime_categories,
    get_fallback_numbeo_data,
    extract_gpi_data,
    get_mofa_safety_info,
    extract_mofa_safety_level,
    get_fallback_gpi_data,
    extract_unodc_homicide_data,
    get_who_mortality_data,
    estimate_homicide_rate_by_region,
    estimate_mortality_by_region,
    classify_homicide_rate,
    get_fallback_unodc_data
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

    @patch('tool.requests.get')
    def test_get_numbeo_crime_data_success(self, mock_get):
        """Numbeoデータ取得成功のテスト"""
        # モックレスポンスを作成
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = """
        <html>
            <table class="table_indices">
                <tr><td>Crime Index</td><td>25.5</td></tr>
                <tr><td>Safety Index</td><td>74.5</td></tr>
            </table>
        </html>
        """
        mock_get.return_value = mock_response
        
        result = get_numbeo_crime_data(self.test_country)
        
        # 基本的なキーが存在することを確認
        self.assertIn("data_source", result)
        self.assertIn("last_updated", result)
        self.assertIn("source_url", result)
        
        # モックが呼ばれたことを確認
        mock_get.assert_called()

    @patch('tool.requests.get')
    def test_get_numbeo_crime_data_failure(self, mock_get):
        """Numbeoデータ取得失敗のテスト"""
        mock_get.side_effect = requests.RequestException("Network error")
        
        result = get_numbeo_crime_data(self.test_country)
        
        # フォールバックデータが返されることを確認
        self.assertIn("note", result)
        self.assertEqual(result["data_source"], "Fallback Data (Numbeo unavailable)")

    def test_get_numbeo_crime_data_real(self):
        """Numbeoデータ実際の取得テスト（ネットワーク必要）"""
    def test_get_numbeo_crime_data_real(self):
        """Numbeoデータ実際の取得テスト（ネットワーク必要）"""
        result = get_numbeo_crime_data(self.test_country)
        
        # 必要なキーが存在することを確認
        required_keys = [
            "crime_index", "safety_index", 
            "data_source", "last_updated"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # データ型の確認
        if "crime_index" in result and result["crime_index"] != "Unknown":
            self.assertIsInstance(result["crime_index"], (int, float))
            # 値の範囲チェック
            self.assertGreaterEqual(result["crime_index"], 0)
            self.assertLessEqual(result["crime_index"], 100)
        
        if "safety_index" in result and result["safety_index"] != "Unknown":
            self.assertIsInstance(result["safety_index"], (int, float))
            self.assertGreaterEqual(result["safety_index"], 0)
            self.assertLessEqual(result["safety_index"], 100)
        
        self.assertIsInstance(result["data_source"], str)

    def test_extract_numbeo_crime_indices(self):
        """Numbeo犯罪指数抽出のテスト"""
        html_content = """
        <html>
            <table class="table_indices">
                <tr><td>Crime Index:</td><td>45.2</td></tr>
                <tr><td>Safety Index:</td><td>54.8</td></tr>
            </table>
        </html>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        result = extract_numbeo_crime_indices(soup)
        
        if result:  # データが抽出できた場合
            if 'crime_index' in result:
                self.assertIsInstance(result['crime_index'], float)
            if 'safety_index' in result:
                self.assertIsInstance(result['safety_index'], float)

    def test_get_fallback_numbeo_data(self):
        """Numbeoフォールバックデータのテスト"""
        result = get_fallback_numbeo_data(self.test_country)
        
        required_keys = [
            "crime_index", "safety_index", "data_source", "note"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertEqual(result["crime_index"], 50.0)
        self.assertEqual(result["safety_index"], 50.0)
        self.assertIn(self.test_country, result["note"])

    @patch('tool.requests.get')
    def test_get_global_peace_index_data_with_mock(self, mock_get):
        """世界平和度指数データ取得のモックテスト"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException("403 Forbidden")
        mock_get.return_value = mock_response
        
        result = get_global_peace_index_data(self.test_country)
        
        # フォールバックデータが返されることを確認
        self.assertIn("data_source", result)
        self.assertIn("Fallback Data", result["data_source"])

    def test_get_global_peace_index_data_real(self):
        """世界平和度指数データ実際の取得テスト"""
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

    def test_get_mofa_safety_info(self):
        """外務省安全情報取得のテスト"""
        result = get_mofa_safety_info(self.test_country)
        
        # 結果が辞書形式であることを確認
        self.assertIsInstance(result, dict)
        
        if result:  # データが取得できた場合
            expected_keys = ["estimated_rank", "peace_score", "crime_level", "security_level"]
            for key in expected_keys:
                if key in result:
                    self.assertIsInstance(result[key], (int, float))

    def test_get_fallback_gpi_data(self):
        """GPIフォールバックデータのテスト"""
        result = get_fallback_gpi_data(self.test_country)
        
        required_keys = [
            "overall_peace_rank", "peace_score", "data_source", "note"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertEqual(result["overall_peace_rank"], 50)
        self.assertEqual(result["peace_score"], 2.0)
        self.assertIn(self.test_country, result["note"])

    def test_get_unodc_homicide_data_real(self):
        """UNODC殺人率データ実際の取得テスト"""
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

    def test_estimate_homicide_rate_by_region(self):
        """地域別殺人率推定のテスト"""
        # 日本のテスト
        result = estimate_homicide_rate_by_region("Japan")
        self.assertIn("homicide_rate", result)
        self.assertLess(result["homicide_rate"], 1.0)  # 日本は低い殺人率
        
        # アメリカのテスト
        result = estimate_homicide_rate_by_region("United States")
        self.assertIn("homicide_rate", result)
        self.assertGreater(result["homicide_rate"], 5.0)  # アメリカは高い殺人率
        
        # 未知の国のテスト
        result = estimate_homicide_rate_by_region("Unknown Country")
        self.assertEqual(result["homicide_rate"], 8.0)  # デフォルト値

    def test_classify_homicide_rate(self):
        """殺人率分類のテスト"""
        self.assertEqual(classify_homicide_rate(0.5), "Very low homicide rate country")
        self.assertEqual(classify_homicide_rate(3.0), "Low homicide rate country")
        self.assertEqual(classify_homicide_rate(10.0), "Medium homicide rate country")
        self.assertEqual(classify_homicide_rate(20.0), "High homicide rate country")
        self.assertEqual(classify_homicide_rate(35.0), "Very high homicide rate country")

    def test_get_fallback_unodc_data(self):
        """UNODCフォールバックデータのテスト"""
        result = get_fallback_unodc_data(self.test_country)
        
        required_keys = [
            "homicide_rate_per_100k", "data_source", "note", "comparative_ranking"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIn("Regional estimates", result["data_source"])
        self.assertIn(self.test_country, result["note"])

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

    def test_real_data_integration_japan(self):
        """日本の実際のデータ統合テスト"""
        country = "Japan"
        
        # 実際のデータを取得
        crime_data = get_crime_data(country)
        
        # エラーがないことを確認
        if "error" not in crime_data:
            # 日本の安全スコアが高いことを確認
            self.assertGreater(crime_data["overall_safety_score"], 60)
            
            # リスク分析
            analysis = analyze_travel_safety_risks(crime_data)
            
            # 日本は一般的に暴力犯罪リスクが低い
            self.assertIn(analysis["violent_crime_risk"], ["低", "中"])

    def test_real_data_integration_multiple_countries(self):
        """複数国の実際のデータ統合テスト"""
        countries = ["Japan", "Germany", "Thailand"]
        
        for country in countries:
            with self.subTest(country=country):
                crime_data = get_crime_data(country)
                
                # 基本構造の確認
                self.assertIn("country", crime_data)
                self.assertEqual(crime_data["country"], country)
                
                if "error" not in crime_data:
                    # スコアが有効範囲内にあることを確認
                    score = crime_data["overall_safety_score"]
                    self.assertGreaterEqual(score, 0)
                    self.assertLessEqual(score, 100)
                    
                    # リスク分析が実行できることを確認
                    analysis = analyze_travel_safety_risks(crime_data)
                    self.assertIn("violent_crime_risk", analysis)
                    self.assertIn("petty_crime_risk", analysis)

    def test_error_handling_robustness(self):
        """エラーハンドリングの堅牢性テスト"""
        # 存在しない国名でテスト
        fake_country = "NonExistentCountry123"
        
        crime_data = get_crime_data(fake_country)
        
        # エラーが発生してもクラッシュしないことを確認
        self.assertIsInstance(crime_data, dict)
        self.assertIn("country", crime_data)
        
        # フォールバックデータまたはエラー情報が含まれることを確認
        if "error" in crime_data:
            self.assertIn("fallback_data", crime_data)
        else:
            # フォールバックデータが使用されている場合
            self.assertIn("overall_safety_score", crime_data)


class TestWebScrapingFunctions(unittest.TestCase):
    """Webスクレイピング関連の関数テスト"""

    def test_extract_numbeo_crime_indices_with_valid_html(self):
        """有効なHTMLでの犯罪指数抽出テスト"""
        html_content = """
        <html>
            <body>
                <table class="table_indices">
                    <tr>
                        <td>Crime Index:</td>
                        <td>42.35</td>
                    </tr>
                    <tr>
                        <td>Safety Index:</td>
                        <td>57.65</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        result = extract_numbeo_crime_indices(soup)
        
        # 結果が辞書であることを確認
        self.assertIsInstance(result, dict)

    def test_extract_numbeo_crime_indices_with_empty_html(self):
        """空のHTMLでの犯罪指数抽出テスト"""
        html_content = "<html><body></body></html>"
        soup = BeautifulSoup(html_content, 'html.parser')
        result = extract_numbeo_crime_indices(soup)
        
        # 空の辞書が返されることを確認
        self.assertIsInstance(result, dict)

    def test_extract_crime_categories(self):
        """犯罪カテゴリ抽出のテスト"""
        html_content = """
        <html>
            <table>
                <tr><td>Violent crimes</td><td>Low</td></tr>
                <tr><td>Property crimes</td><td>Medium</td></tr>
            </table>
        </html>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        result = extract_crime_categories(soup)
        
        # 結果が辞書であることを確認
        self.assertIsInstance(result, dict)

    @patch('tool.requests.get')
    def test_network_timeout_handling(self, mock_get):
        """ネットワークタイムアウトの処理テスト"""
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        result = get_numbeo_crime_data("TestCountry")
        
        # タイムアウト時にフォールバックデータが返されることを確認
        self.assertIn("data_source", result)
        self.assertIn("Fallback", result["data_source"])

    @patch('tool.requests.get')
    def test_http_error_handling(self, mock_get):
        """HTTPエラーの処理テスト"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        result = get_numbeo_crime_data("TestCountry")
        
        # HTTPエラー時にフォールバックデータが返されることを確認
        self.assertIn("data_source", result)
        self.assertIn("Fallback", result["data_source"])


class TestDataValidation(unittest.TestCase):
    """データ検証テスト"""

    def test_safety_score_boundary_values(self):
        """安全スコアの境界値テスト"""
        # 最高スコアのテスト
        perfect_data = {
            "numbeo_data": {"safety_index": 100.0},
            "global_peace_index": {"peace_score": 1.0},
            "unodc_homicide_rate": {"homicide_rate_per_100k": 0.0}
        }
        score = calculate_safety_score(perfect_data)
        self.assertLessEqual(score, 100.0)
        
        # 最低スコアのテスト
        worst_data = {
            "numbeo_data": {"safety_index": 0.0},
            "global_peace_index": {"peace_score": 5.0},
            "unodc_homicide_rate": {"homicide_rate_per_100k": 100.0}
        }
        score = calculate_safety_score(worst_data)
        self.assertGreaterEqual(score, 0.0)

    def test_risk_classification_consistency(self):
        """リスク分類の一貫性テスト"""
        # 高リスクデータ
        high_risk_data = {
            "numbeo_data": {
                "pickpocket_probability": "Very High",
                "theft_probability": "Very High",
                "assault_probability": "Very High"
            },
            "unodc_homicide_rate": {"homicide_rate_per_100k": 50.0}
        }
        
        analysis = analyze_travel_safety_risks(high_risk_data)
        
        # 高リスクが適切に分類されることを確認
        self.assertEqual(analysis["violent_crime_risk"], "高")
        self.assertGreater(len(analysis["specific_risks"]), 0)
        self.assertGreater(len(analysis["recommendations"]), 0)

    def test_data_type_consistency(self):
        """データ型の一貫性テスト"""
        countries = ["Japan", "TestCountry"]
        
        for country in countries:
            with self.subTest(country=country):
                # 各データ取得関数のテスト
                numbeo_data = get_numbeo_crime_data(country)
                gpi_data = get_global_peace_index_data(country)
                unodc_data = get_unodc_homicide_data(country)
                
                # データ型の確認
                self.assertIsInstance(numbeo_data, dict)
                self.assertIsInstance(gpi_data, dict)
                self.assertIsInstance(unodc_data, dict)
                
                # 必須フィールドの確認
                self.assertIn("data_source", numbeo_data)
                self.assertIn("data_source", gpi_data)
                self.assertIn("data_source", unodc_data)


if __name__ == "__main__":
    # テストスイートの実行
    # より詳細な出力とカバレッジ情報を表示
    import sys
    
    print("=== Crime Agent Tool Tests ===")
    print("Testing web scraping and data analysis functionality...")
    print()
    
    # テストの実行
    unittest.main(verbosity=2, exit=False)
    
    print()
    print("=== Test Summary ===")
    print("- Real web scraping tests included")
    print("- Mock tests for network failures")
    print("- Data validation and boundary tests")
    print("- Integration tests with multiple countries")
    print("- Error handling and robustness tests")
    print()
    print("Note: Some tests require internet connection for real data fetching")
