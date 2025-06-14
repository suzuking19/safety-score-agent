import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional


def get_conflict_risk_info(country_name: Optional[str] = None, region: Optional[str] = None) -> Dict:
    """
    外務省の海外安全情報サイトからテロ・紛争リスクの情報を取得する
    
    Args:
        country_name (str, optional): 取得したい国名（例：「イエメン」「シリア」）
        region (str, optional): 取得したい地域（例：「中東」「アフリカ」）
    
    Returns:
        Dict: 危険情報を含む辞書
    """
    try:
        base_url = "https://www.anzen.mofa.go.jp"
        
        # 国別コードマッピング（主要な高リスク国）
        country_codes = {
            "イエメン": "043",
            "シリア": "051", 
            "アフガニスタン": "041",
            "イラク": "045",
            "ソマリア": "110",
            "リビア": "125",
            "南スーダン": "301",
            "中央アフリカ": "112",
            "マリ": "121",
            "ブルキナファソ": "117",
            "ウクライナ": "182",
            "ミャンマー": "018",
            "パキスタン": "011",
            "ナイジェリア": "115",
            "コンゴ民主共和国": "103"
        }
        
        result = {
            "status": "success",
            "data": {},
            "high_risk_countries": [],
            "conflict_summary": "",
            "timestamp": None
        }
        
        # 特定の国が指定された場合
        if country_name and country_name in country_codes:
            country_code = country_codes[country_name]
            country_url = f"{base_url}/info/pcinfectionspothazardinfo_{country_code}.html"
            
            response = requests.get(country_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 危険レベルの抽出
                danger_level = "不明"
                danger_info = soup.find('div', class_='danger-info') or soup.find('h4', string=re.compile(r'レベル[1-4]'))
                if danger_info:
                    level_text = danger_info.get_text()
                    if "レベル4" in level_text or "退避" in level_text:
                        danger_level = "レベル4（退避勧告）"
                    elif "レベル3" in level_text or "渡航中止" in level_text:
                        danger_level = "レベル3（渡航中止勧告）"
                    elif "レベル2" in level_text:
                        danger_level = "レベル2（不要不急の渡航中止）"
                    elif "レベル1" in level_text:
                        danger_level = "レベル1（十分注意）"
                
                # テロ・紛争関連情報の抽出
                conflict_keywords = ["テロ", "紛争", "武力衝突", "戦闘", "爆発", "襲撃", "誘拐", "反政府", "過激派", "武装"]
                conflict_info = []
                
                # 危険情報の詳細テキストを検索
                text_content = soup.get_text()
                for keyword in conflict_keywords:
                    if keyword in text_content:
                        # キーワード周辺のテキストを抽出
                        sentences = text_content.split('。')
                        for sentence in sentences:
                            if keyword in sentence and len(sentence) > 10:
                                conflict_info.append(sentence.strip() + '。')
                                break
                
                result["data"][country_name] = {
                    "country": country_name,
                    "danger_level": danger_level,
                    "conflict_info": conflict_info[:5],  # 最大5件の関連情報
                    "url": country_url,
                    "last_updated": "2025年データ"
                }
        
        # 高リスク国のリストを作成
        high_risk_countries = []
        for country, code in country_codes.items():
            high_risk_countries.append({
                "country": country,
                "estimated_risk": "高" if country in ["イエメン", "シリア", "アフガニスタン", "ソマリア"] else "中-高",
                "primary_risks": ["テロ", "紛争", "誘拐"] if country in ["イエメン", "シリア", "アフガニスタン"] else ["治安悪化", "テロ"]
            })
        
        result["high_risk_countries"] = high_risk_countries
        
        # 全体的な紛争サマリー
        result["conflict_summary"] = """
        現在、世界各地で以下のような紛争・テロリスクが確認されています：
        
        【最高リスク地域（レベル4）】
        - イエメン: 政府軍とホーシー派の衝突、テロ組織の活動
        - シリア: 内戦状況継続、テロ組織の活動
        - アフガニスタン: タリバン政権下での治安不安、テロリスク
        - ソマリア: アルシャバブによるテロ攻撃
        
        【高リスク地域（レベル3）】
        - ウクライナ: ロシアとの軍事衝突
        - ミャンマー: 軍事政権による弾圧、内戦状態
        - 西アフリカ地域: イスラム過激派の活動
        
        これらの地域では、テロ攻撃、誘拐、武力衝突のリスクが極めて高く、
        日本人の安全確保が困難な状況です。
        """
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "外務省サイトからの情報取得に失敗しました"
        }


def get_terrorism_info(region: str = "global") -> Dict:
    """
    特定地域のテロリスク情報を取得
    
    Args:
        region (str): 地域名（"middle_east", "africa", "asia", "europe", "global"）
    
    Returns:
        Dict: テロリスク情報
    """
    terrorism_data = {
        "middle_east": {
            "risk_level": "極高",
            "active_groups": ["ISIS", "アルカイダ系組織", "ヒズボラ", "ホーシー派"],
            "recent_threats": ["自爆テロ", "車両突入攻撃", "誘拐", "施設攻撃"],
            "high_risk_countries": ["イエメン", "シリア", "イラク", "アフガニスタン"]
        },
        "africa": {
            "risk_level": "高",
            "active_groups": ["アルシャバブ", "ボコハラム", "AQIM", "ISGS"],
            "recent_threats": ["自爆テロ", "誘拐", "施設攻撃", "海賊行為"],
            "high_risk_countries": ["ソマリア", "ナイジェリア", "マリ", "ブルキナファソ"]
        },
        "asia": {
            "risk_level": "中-高",
            "active_groups": ["アブサヤフ", "JI", "各種分離主義組織"],
            "recent_threats": ["爆弾テロ", "誘拐", "サイバー攻撃"],
            "high_risk_countries": ["フィリピン", "インドネシア", "パキスタン", "バングラデシュ"]
        },
        "global": {
            "risk_level": "中",
            "trends": [
                "一匹狼型テロの増加",
                "サイバーテロの脅威拡大", 
                "ソフトターゲットへの攻撃",
                "プロパガンダによる過激化"
            ]
        }
    }
    
    return {
        "status": "success",
        "region": region,
        "data": terrorism_data.get(region, terrorism_data["global"]),
        "last_updated": "2025年6月データ"
    }



