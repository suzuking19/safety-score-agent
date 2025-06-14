import unittest
from unittest.mock import patch, MagicMock
import requests
from tool import get_conflict_risk_info, get_terrorism_info


class TestConflictRiskFunction(unittest.TestCase):
    """紛争リスク情報取得関数のテストクラス"""
    
    def setUp(self):
        """各テスト前の初期化"""
        self.sample_html = """
        <html>
            <div class="danger-info">レベル4：退避勧告</div>
            <div>この地域ではテロ組織による爆発テロが頻発しています。武力衝突も継続中です。</div>
        </html>
        """
    
    @patch('tool.requests.get')
    def test_get_conflict_risk_info_success(self, mock_get):
        """正常なHTTPレスポンスの場合のテスト"""
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = self.sample_html
        mock_get.return_value = mock_response
        
        # 関数実行
        result = get_conflict_risk_info(country_name="イエメン")
        
        # アサーション
        self.assertEqual(result["status"], "success")
        self.assertIn("イエメン", result["data"])
        self.assertEqual(result["data"]["イエメン"]["country"], "イエメン")
        self.assertIn("レベル4", result["data"]["イエメン"]["danger_level"])
        self.assertIsInstance(result["data"]["イエメン"]["conflict_info"], list)
    
    @patch('tool.requests.get')
    def test_get_conflict_risk_info_http_error(self, mock_get):
        """HTTP エラーの場合のテスト"""
        # HTTPエラーのモック
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        # 関数実行
        result = get_conflict_risk_info(country_name="イエメン")
        
        # アサーション
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertIn("Connection error", result["error"])
    
    def test_get_conflict_risk_info_no_country(self):
        """国名が指定されない場合のテスト"""
        result = get_conflict_risk_info()
        
        # 基本的な構造の確認
        self.assertEqual(result["status"], "success")
        self.assertIn("high_risk_countries", result)
        self.assertIn("conflict_summary", result)
        self.assertIsInstance(result["high_risk_countries"], list)
        self.assertGreater(len(result["high_risk_countries"]), 0)
    
    def test_get_conflict_risk_info_invalid_country(self):
        """存在しない国名の場合のテスト"""
        result = get_conflict_risk_info(country_name="存在しない国")
        
        # 基本的な構造は返されるが、個別データは含まれない
        self.assertEqual(result["status"], "success")
        self.assertNotIn("存在しない国", result["data"])
        self.assertIn("high_risk_countries", result)
    
    def test_get_conflict_risk_info_high_risk_countries_structure(self):
        """高リスク国リストの構造テスト"""
        result = get_conflict_risk_info()
        
        high_risk_countries = result["high_risk_countries"]
        
        # リストが空でない
        self.assertGreater(len(high_risk_countries), 0)
        
        # 各要素の構造を確認
        for country_info in high_risk_countries:
            self.assertIn("country", country_info)
            self.assertIn("estimated_risk", country_info)
            self.assertIn("primary_risks", country_info)
            self.assertIsInstance(country_info["primary_risks"], list)
    
    @patch('tool.requests.get')
    def test_get_conflict_risk_info_danger_level_parsing(self, mock_get):
        """危険レベルの解析テスト"""
        test_cases = [
            ('<div class="danger-info">レベル1：十分注意してください</div>', "レベル1"),
            ('<div class="danger-info">レベル2：不要不急の渡航は止めてください</div>', "レベル2"),
            ('<div class="danger-info">レベル3：渡航は止めてください</div>', "レベル3"),
            ('<div class="danger-info">レベル4：退避してください</div>', "レベル4"),
            ("<div>特に危険情報なし</div>", "不明")
        ]
        
        for html_content, expected_level in test_cases:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = f"<html>{html_content}</html>"
            mock_get.return_value = mock_response
            
            result = get_conflict_risk_info(country_name="イエメン")
            
            if expected_level != "不明":
                self.assertIn(expected_level, result["data"]["イエメン"]["danger_level"])
            else:
                self.assertEqual(result["data"]["イエメン"]["danger_level"], "不明")


class TestTerrorismInfoFunction(unittest.TestCase):
    """テロリスク情報取得関数のテストクラス"""
    
    def test_get_terrorism_info_middle_east(self):
        """中東地域のテロ情報取得テスト"""
        result = get_terrorism_info(region="middle_east")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["region"], "middle_east")
        self.assertIn("data", result)
        
        data = result["data"]
        self.assertEqual(data["risk_level"], "極高")
        self.assertIn("active_groups", data)
        self.assertIn("recent_threats", data) 
        self.assertIn("high_risk_countries", data)
        self.assertIsInstance(data["active_groups"], list)
        self.assertIn("ISIS", data["active_groups"])
    
    def test_get_terrorism_info_africa(self):
        """アフリカ地域のテロ情報取得テスト"""
        result = get_terrorism_info(region="africa")
        
        self.assertEqual(result["status"], "success")
        data = result["data"]
        self.assertEqual(data["risk_level"], "高")
        self.assertIn("アルシャバブ", data["active_groups"])
        self.assertIn("ソマリア", data["high_risk_countries"])
    
    def test_get_terrorism_info_asia(self):
        """アジア地域のテロ情報取得テスト"""
        result = get_terrorism_info(region="asia")
        
        self.assertEqual(result["status"], "success")
        data = result["data"]
        self.assertEqual(data["risk_level"], "中-高")
        self.assertIn("アブサヤフ", data["active_groups"])
        self.assertIn("フィリピン", data["high_risk_countries"])
    
    def test_get_terrorism_info_global(self):
        """グローバルテロ情報取得テスト"""
        result = get_terrorism_info(region="global")
        
        self.assertEqual(result["status"], "success")
        data = result["data"]
        self.assertEqual(data["risk_level"], "中")
        self.assertIn("trends", data)
        self.assertIsInstance(data["trends"], list)
        self.assertIn("一匹狼型テロの増加", data["trends"])
    
    def test_get_terrorism_info_invalid_region(self):
        """存在しない地域の場合のテスト"""
        result = get_terrorism_info(region="invalid_region")
        
        # 無効な地域の場合はglobalデータが返される
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["region"], "invalid_region")
        data = result["data"]
        self.assertIn("trends", data)  # globalデータの特徴
    
    def test_get_terrorism_info_default_region(self):
        """デフォルト地域（引数なし）のテスト"""
        result = get_terrorism_info()
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["region"], "global")
        self.assertIn("trends", result["data"])
    
    def test_get_terrorism_info_response_structure(self):
        """レスポンス構造の一貫性テスト"""
        regions = ["middle_east", "africa", "asia", "global"]
        
        for region in regions:
            result = get_terrorism_info(region=region)
            
            # 共通のレスポンス構造を確認
            self.assertIn("status", result)
            self.assertIn("region", result)
            self.assertIn("data", result)
            self.assertIn("last_updated", result)
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["region"], region)
            
            # データの基本構造を確認
            data = result["data"]
            self.assertIn("risk_level", data)


class TestIntegrationFunctions(unittest.TestCase):
    """関数統合テストクラス"""
    
    def test_country_codes_completeness(self):
        """国別コードマッピングの完全性テスト"""
        result = get_conflict_risk_info()
        high_risk_countries = result["high_risk_countries"]
        
        # 定義された国がすべて含まれているか確認
        expected_countries = [
            "イエメン", "シリア", "アフガニスタン", "イラク", "ソマリア",
            "リビア", "南スーダン", "中央アフリカ", "マリ", "ブルキナファソ",
            "ウクライナ", "ミャンマー", "パキスタン", "ナイジェリア", "コンゴ民主共和国"
        ]
        
        actual_countries = [country["country"] for country in high_risk_countries]
        
        for expected_country in expected_countries:
            self.assertIn(expected_country, actual_countries)
    
    @patch('tool.requests.get')
    def test_timeout_handling(self, mock_get):
        """タイムアウトの処理テスト"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        result = get_conflict_risk_info(country_name="イエメン")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("timeout", result["error"].lower())


if __name__ == '__main__':
    # テストの実行
    unittest.main(verbosity=2)
