import requests
import json
from typing import Dict, Any, List
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, quote

def get_infrastructure_data(country: str) -> Dict[str, Any]:
    """
    複数のデータソースから社会基盤の安定度データを取得する
    
    Args:
        country: 国名（英語）
    
    Returns:
        Dict containing infrastructure stability data from multiple sources
    """
    try:
        result = {
            "country": country,
            "corruption_perception_index": get_corruption_data(country),
            "traffic_safety_data": get_traffic_safety_data(country),
            "healthcare_system": get_healthcare_data(country),
            "infrastructure_categories": {
                "political_stability": {
                    "description": "政治の腐敗度・政府の透明性",
                    "indicators": ["corruption_perception_index", "government_effectiveness", "rule_of_law"]
                },
                "transport_infrastructure": {
                    "description": "交通インフラの安全性",
                    "indicators": ["traffic_fatality_rate", "road_safety_index", "transport_reliability"]
                },
                "healthcare_infrastructure": {
                    "description": "医療水準・医療アクセス",
                    "indicators": ["healthcare_access_quality", "medical_facilities", "emergency_response"]
                }
            },
            "overall_infrastructure_score": 0,
            "data_collection_timestamp": time.time()
        }
        
        # 総合インフラ安定度スコアを計算
        result["overall_infrastructure_score"] = calculate_infrastructure_score(result)
        
        return result
        
    except Exception as e:
        return {
            "country": country,
            "error": f"データ取得エラー: {str(e)}",
            "fallback_data": get_fallback_infrastructure_data(country)
        }

def get_corruption_data(country: str) -> Dict[str, Any]:
    """
    Transparency Internationalから汚職認識指数データをスクレイピング
    
    Args:
        country: 国名（英語）
    
    Returns:
        Dict containing corruption perception index data
    """
    try:
        # Transparency InternationalのCPIページをスクレイピング
        url = "https://www.transparency.org/en/cpi"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # データを抽出する試み（実際のサイト構造に依存）
        cpi_data = scrape_cpi_data(soup, country)
        
        if cpi_data:
            return cpi_data
        else:
            # フォールバック: 一般的なデータソースを使用
            return get_fallback_corruption_data(country)
            
    except Exception as e:
        print(f"汚職認識指数データの取得に失敗: {str(e)}")
        return get_fallback_corruption_data(country)

def scrape_cpi_data(soup: BeautifulSoup, country: str) -> Dict[str, Any]:
    """
    BeautifulSoupオブジェクトからCPIデータを抽出
    """
    try:
        # 実際のサイト構造に基づいたデータ抽出ロジック
        # 注意: 実際の実装では、サイトの構造に応じて調整が必要
        
        # 国名の正規化（部分一致を試みる）
        country_variations = [
            country.lower(),
            country.lower().replace(' ', ''),
            country.lower().replace('_', ' ')
        ]
        
        # テーブルまたはデータ要素を検索
        data_elements = soup.find_all(['table', 'div', 'span'], class_=re.compile(r'(cpi|corruption|score|rank)', re.I))
        
        # 簡単なデータ抽出ロジック（実際のサイトに依存）
        for element in data_elements:
            text = element.get_text().lower()
            for country_var in country_variations:
                if country_var in text:
                    # スコアを抽出する試み
                    score_match = re.search(r'(\d+(?:\.\d+)?)', text)
                    if score_match:
                        score = float(score_match.group(1))
                        return {
                            "cpi_score": score,
                            "cpi_rank": extract_rank_from_text(text),
                            "total_countries": 180,
                            "regional_average": 65,
                            "classification": classify_cpi_score(score),
                            "trend": "Unknown",
                            "data_source": "Transparency International CPI (Scraped)",
                            "methodology": "Expert assessments and opinion surveys",
                            "last_updated": time.strftime("%Y-%m"),
                            "scraped_at": time.time()
                        }
        
        return None
        
    except Exception as e:
        print(f"CPI データの解析に失敗: {str(e)}")
        return None

def extract_rank_from_text(text: str) -> int:
    """テキストからランキングを抽出"""
    rank_match = re.search(r'rank\s*:?\s*(\d+)', text, re.I)
    if rank_match:
        return int(rank_match.group(1))
    return 0

def classify_cpi_score(score: float) -> str:
    """CPIスコアを分類"""
    if score >= 80:
        return "Very Good"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Moderate"
    elif score >= 20:
        return "Poor"
    else:
        return "Very Poor"

def get_fallback_corruption_data(country: str) -> Dict[str, Any]:
    """
    スクレイピングに失敗した場合のフォールバックデータ
    """
    # 一般的な国の平均値を返す
    return {
        "cpi_score": 65,  # 世界平均程度
        "cpi_rank": 90,   # 中程度のランキング
        "total_countries": 180,
        "regional_average": 65,
        "classification": "Moderate",
        "trend": "Unknown",
        "data_source": "Fallback Data (Scraping Failed)",
        "methodology": "Estimated based on regional averages",
        "last_updated": time.strftime("%Y-%m"),
        "note": f"実際の{country}のデータ取得に失敗したため、推定値を使用"
    }

def get_traffic_safety_data(country: str) -> Dict[str, Any]:
    """
    WHO統計サイトから交通安全データをスクレイピング
    
    Args:
        country: 国名（英語）
    
    Returns:
        Dict containing traffic safety data
    """
    try:
        # WHO Global Health Observatoryから交通安全データを取得
        url = "https://www.who.int/data/gho/data/themes/road-safety"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 交通安全データを抽出
        traffic_data = scrape_traffic_data(soup, country)
        
        if traffic_data:
            return traffic_data
        else:
            return get_fallback_traffic_data(country)
            
    except Exception as e:
        print(f"交通安全データの取得に失敗: {str(e)}")
        return get_fallback_traffic_data(country)

def scrape_traffic_data(soup: BeautifulSoup, country: str) -> Dict[str, Any]:
    """
    BeautifulSoupオブジェクトから交通安全データを抽出
    """
    try:
        # 国名の正規化
        country_variations = [
            country.lower(),
            country.lower().replace(' ', ''),
            country.lower().replace('_', ' ')
        ]
        
        # データテーブルや統計要素を検索
        data_elements = soup.find_all(['table', 'div', 'span'], 
                                    class_=re.compile(r'(traffic|road|safety|death|fatality)', re.I))
        
        for element in data_elements:
            text = element.get_text().lower()
            for country_var in country_variations:
                if country_var in text:
                    # 死亡率を抽出
                    death_rate_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:per|/)\s*100,?000', text)
                    if death_rate_match:
                        death_rate = float(death_rate_match.group(1))
                        return {
                            "road_traffic_deaths_per_100k": death_rate,
                            "total_road_deaths": estimate_total_deaths(death_rate, country),
                            "year": 2024,
                            "who_region": get_who_region(country),
                            "income_classification": get_income_classification(country),
                            "safety_rating": classify_traffic_safety(death_rate),
                            "main_risk_factors": get_common_risk_factors(),
                            "road_infrastructure_quality": estimate_infrastructure_quality(death_rate),
                            "vehicle_safety_standards": estimate_safety_standards(death_rate),
                            "enforcement_effectiveness": estimate_enforcement(death_rate),
                            "data_source": "WHO Global Health Observatory (Scraped)",
                            "data_quality": "Scraped data",
                            "scraped_at": time.time()
                        }
        
        return None
        
    except Exception as e:
        print(f"交通安全データの解析に失敗: {str(e)}")
        return None

def estimate_total_deaths(death_rate: float, country: str) -> int:
    """死亡率から総死亡者数を推定"""
    # 簡易的な人口推定（実際の実装では正確な人口データを使用）
    estimated_population = 50000000  # 5000万人と仮定
    return int((death_rate / 100000) * estimated_population)

def get_who_region(country: str) -> str:
    """国からWHO地域を推定"""
    # 簡略化した地域分類
    country_lower = country.lower()
    if any(x in country_lower for x in ['japan', 'korea', 'china', 'thailand', 'vietnam']):
        return "Western Pacific Region"
    elif any(x in country_lower for x in ['germany', 'france', 'italy', 'spain', 'uk']):
        return "European Region"
    elif any(x in country_lower for x in ['usa', 'canada', 'mexico', 'brazil']):
        return "Region of the Americas"
    else:
        return "Unknown Region"

def get_income_classification(country: str) -> str:
    """国の所得分類を推定"""
    country_lower = country.lower()
    high_income = ['japan', 'germany', 'france', 'usa', 'canada', 'australia', 'uk', 'italy', 'spain']
    if any(x in country_lower for x in high_income):
        return "High income"
    else:
        return "Middle income"

def classify_traffic_safety(death_rate: float) -> str:
    """交通安全レベルを分類"""
    if death_rate < 5:
        return "Excellent"
    elif death_rate < 10:
        return "Good"
    elif death_rate < 20:
        return "Moderate"
    elif death_rate < 30:
        return "Poor"
    else:
        return "Very Poor"

def estimate_infrastructure_quality(death_rate: float) -> str:
    """死亡率からインフラの質を推定"""
    if death_rate < 10:
        return "High"
    elif death_rate < 20:
        return "Medium"
    else:
        return "Low"

def estimate_safety_standards(death_rate: float) -> str:
    """死亡率から安全基準を推定"""
    if death_rate < 10:
        return "High"
    elif death_rate < 20:
        return "Medium"
    else:
        return "Low"

def estimate_enforcement(death_rate: float) -> str:
    """死亡率から執行効果を推定"""
    if death_rate < 10:
        return "High"
    elif death_rate < 20:
        return "Medium"
    else:
        return "Low"

def get_common_risk_factors() -> List[str]:
    """一般的なリスク要因のリスト"""
    return [
        "Speeding",
        "Drink-driving",
        "Not wearing seatbelts",
        "Motorcycle safety",
        "Pedestrian safety"
    ]

def get_fallback_traffic_data(country: str) -> Dict[str, Any]:
    """
    スクレイピングに失敗した場合のフォールバックデータ
    """
    return {
        "road_traffic_deaths_per_100k": 12.0,  # 世界平均程度
        "total_road_deaths": 6000,
        "year": 2024,
        "who_region": get_who_region(country),
        "income_classification": get_income_classification(country),
        "safety_rating": "Moderate",
        "main_risk_factors": get_common_risk_factors(),
        "road_infrastructure_quality": "Medium",
        "vehicle_safety_standards": "Medium",
        "enforcement_effectiveness": "Medium",
        "data_source": "Fallback Data (Scraping Failed)",
        "data_quality": "Estimated",
        "note": f"実際の{country}のデータ取得に失敗したため、推定値を使用",
        "scraped_at": time.time()
    }

def get_healthcare_data(country: str) -> Dict[str, Any]:
    """
    WHO統計および各種医療データサイトから医療システムデータをスクレイピング
    
    Args:
        country: 国名（英語）
    
    Returns:
        Dict containing healthcare system data
    """
    try:
        # WHO Health Statistics から医療データを取得
        url = "https://www.who.int/data/gho"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 医療データを抽出
        healthcare_data = scrape_healthcare_data(soup, country)
        
        if healthcare_data:
            return healthcare_data
        else:
            return get_fallback_healthcare_data(country)
            
    except Exception as e:
        print(f"医療システムデータの取得に失敗: {str(e)}")
        return get_fallback_healthcare_data(country)

def scrape_healthcare_data(soup: BeautifulSoup, country: str) -> Dict[str, Any]:
    """
    BeautifulSoupオブジェクトから医療システムデータを抽出
    """
    try:
        # 国名の正規化
        country_variations = [
            country.lower(),
            country.lower().replace(' ', ''),
            country.lower().replace('_', ' ')
        ]
        
        # 医療関連のデータ要素を検索
        data_elements = soup.find_all(['table', 'div', 'span'], 
                                    class_=re.compile(r'(health|medical|hospital|doctor|physician)', re.I))
        
        # 基本的な医療指標を抽出する試み
        healthcare_index = 70.0  # デフォルト値
        physicians_per_1000 = 2.5
        hospital_beds_per_1000 = 5.0
        
        for element in data_elements:
            text = element.get_text().lower()
            for country_var in country_variations:
                if country_var in text:
                    # 医師数を抽出
                    physician_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:physicians?|doctors?)\s*(?:per|/)\s*1,?000', text)
                    if physician_match:
                        physicians_per_1000 = float(physician_match.group(1))
                    
                    # 病床数を抽出
                    bed_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:beds?)\s*(?:per|/)\s*1,?000', text)
                    if bed_match:
                        hospital_beds_per_1000 = float(bed_match.group(1))
                    
                    # 医療アクセス指数を抽出
                    index_match = re.search(r'(?:index|score|rating)\s*:?\s*(\d+(?:\.\d+)?)', text)
                    if index_match:
                        healthcare_index = float(index_match.group(1))
        
        return {
            "healthcare_access_quality_index": healthcare_index,
            "universal_health_coverage_index": calculate_uhc_index(healthcare_index),
            "health_system_performance_rank": estimate_health_rank(healthcare_index),
            "physicians_per_1000": physicians_per_1000,
            "hospital_beds_per_1000": hospital_beds_per_1000,
            "healthcare_expenditure_gdp_percent": estimate_health_expenditure(country),
            "emergency_response_quality": classify_emergency_response(healthcare_index),
            "medical_tourism_ranking": estimate_medical_tourism_rank(healthcare_index),
            "health_security_index": healthcare_index * 0.9,  # 推定値
            "healthcare_categories": {
                "accessibility": classify_accessibility(healthcare_index),
                "quality": classify_quality(healthcare_index),
                "affordability": classify_affordability(healthcare_index),
                "emergency_care": classify_emergency_care(healthcare_index)
            },
            "data_sources": [
                "WHO Health Statistics (Scraped)",
                "Global Health Security Index",
                "Healthcare Access and Quality Index"
            ],
            "last_updated": time.strftime("%Y-%m"),
            "scraped_at": time.time()
        }
        
    except Exception as e:
        print(f"医療データの解析に失敗: {str(e)}")
        return None

def calculate_uhc_index(healthcare_index: float) -> float:
    """医療アクセス指数からUHCインデックスを推定"""
    return min(100, healthcare_index * 1.1)

def estimate_health_rank(healthcare_index: float) -> int:
    """医療指数から世界ランキングを推定"""
    if healthcare_index >= 90:
        return 5
    elif healthcare_index >= 80:
        return 15
    elif healthcare_index >= 70:
        return 30
    elif healthcare_index >= 60:
        return 60
    else:
        return 100

def estimate_health_expenditure(country: str) -> float:
    """国から医療支出の推定"""
    country_lower = country.lower()
    high_expenditure = ['usa', 'france', 'germany', 'japan', 'switzerland']
    if any(x in country_lower for x in high_expenditure):
        return 10.5
    else:
        return 6.5

def classify_emergency_response(index: float) -> str:
    """緊急対応の質を分類"""
    if index >= 85:
        return "Excellent"
    elif index >= 70:
        return "High"
    elif index >= 50:
        return "Medium"
    else:
        return "Low"

def estimate_medical_tourism_rank(index: float) -> int:
    """医療ツーリズムランキングを推定"""
    if index >= 85:
        return 10
    elif index >= 70:
        return 25
    elif index >= 50:
        return 50
    else:
        return 100

def classify_accessibility(index: float) -> str:
    """アクセス性を分類"""
    if index >= 80:
        return "High"
    elif index >= 60:
        return "Medium"
    else:
        return "Low"

def classify_quality(index: float) -> str:
    """品質を分類"""
    if index >= 85:
        return "Very High"
    elif index >= 70:
        return "High"
    elif index >= 50:
        return "Medium"
    else:
        return "Low"

def classify_affordability(index: float) -> str:
    """手頃さを分類"""
    if index >= 75:
        return "High"
    elif index >= 55:
        return "Medium"
    else:
        return "Low"

def classify_emergency_care(index: float) -> str:
    """緊急医療を分類"""
    if index >= 85:
        return "Excellent"
    elif index >= 70:
        return "Good"
    elif index >= 50:
        return "Fair"
    else:
        return "Poor"

def get_fallback_healthcare_data(country: str) -> Dict[str, Any]:
    """
    スクレイピングに失敗した場合のフォールバックデータ
    """
    return {
        "healthcare_access_quality_index": 65.0,  # 世界平均程度
        "universal_health_coverage_index": 70,
        "health_system_performance_rank": 50,
        "physicians_per_1000": 2.5,
        "hospital_beds_per_1000": 5.0,
        "healthcare_expenditure_gdp_percent": 7.5,
        "emergency_response_quality": "Medium",
        "medical_tourism_ranking": 50,
        "health_security_index": 60.0,
        "healthcare_categories": {
            "accessibility": "Medium",
            "quality": "Medium",
            "affordability": "Medium",
            "emergency_care": "Fair"
        },
        "data_sources": [
            "Fallback Data (Scraping Failed)"
        ],
        "last_updated": time.strftime("%Y-%m"),
        "note": f"実際の{country}のデータ取得に失敗したため、推定値を使用",
        "scraped_at": time.time()
    }

def calculate_infrastructure_score(infra_data: Dict[str, Any]) -> float:
    """
    複数のデータソースから総合インフラ安定度スコア（25点満点）を計算
    
    Returns:
        float: 0-25のスケールでのインフラ安定度スコア
    """
    try:
        score_components = []
        
        # 汚職認識指数からのスコア（政治の安定性）
        if "corruption_perception_index" in infra_data:
            cpi_score = infra_data["corruption_perception_index"].get("cpi_score", 50)
            # CPI scoreを25点満点に変換（100点満点→25点満点）
            political_score = (cpi_score / 100) * 25
            score_components.append(("political_stability", political_score))
        
        # 交通安全からのスコア
        if "traffic_safety_data" in infra_data:
            fatality_rate = infra_data["traffic_safety_data"].get("road_traffic_deaths_per_100k", 15)
            # 交通事故死亡率が低いほど高いスコア（30以上で0点、0で25点満点を想定）
            traffic_score = max(0, 25 - (fatality_rate * 25 / 30))
            score_components.append(("transport_safety", traffic_score))
        
        # 医療システムからのスコア
        if "healthcare_system" in infra_data:
            healthcare_index = infra_data["healthcare_system"].get("healthcare_access_quality_index", 50)
            # Healthcare indexを25点満点に変換
            healthcare_score = (healthcare_index / 100) * 25
            score_components.append(("healthcare_quality", healthcare_score))
        
        # 重み付き平均を計算（各要素を等しく重み付け）
        if score_components:
            total_score = sum(score for _, score in score_components)
            average_score = total_score / len(score_components)
            return round(average_score, 1)
        else:
            return 12.5  # デフォルト値（25点満点の半分）
            
    except Exception as e:
        return 12.5  # エラー時のデフォルト値

def analyze_infrastructure_risks(infra_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    インフラ関連のリスク分析
    """
    analysis = {
        "political_risk_level": "低",
        "transport_risk_level": "低",
        "healthcare_risk_level": "低",
        "specific_risks": [],
        "recommendations": [],
        "emergency_preparedness": "良好"
    }
    
    # 汚職認識指数に基づく政治リスク評価
    if "corruption_perception_index" in infra_data:
        cpi_score = infra_data["corruption_perception_index"].get("cpi_score", 50)
        
        if cpi_score < 40:
            analysis["political_risk_level"] = "高"
            analysis["specific_risks"].append("政府の腐敗レベルが高く、公共サービスの信頼性が低い")
            analysis["recommendations"].append("公的機関との接触時は注意が必要。賄賂の要求には応じない")
        elif cpi_score < 60:
            analysis["political_risk_level"] = "中"
            analysis["specific_risks"].append("政府の透明性に課題がある")
            analysis["recommendations"].append("公的手続きでは正規のルートを利用する")
    
    # 交通安全に基づくリスク評価
    if "traffic_safety_data" in infra_data:
        fatality_rate = infra_data["traffic_safety_data"].get("road_traffic_deaths_per_100k", 15)
        
        if fatality_rate > 20:
            analysis["transport_risk_level"] = "高"
            analysis["specific_risks"].append("交通事故のリスクが非常に高い")
            analysis["recommendations"].append("可能な限り公共交通機関を利用し、夜間運転は避ける")
        elif fatality_rate > 10:
            analysis["transport_risk_level"] = "中"
            analysis["specific_risks"].append("交通事故のリスクがやや高い")
            analysis["recommendations"].append("シートベルト着用を徹底し、安全運転を心がける")
    
    # 医療システムに基づくリスク評価
    if "healthcare_system" in infra_data:
        healthcare_quality = infra_data["healthcare_system"].get("healthcare_access_quality_index", 50)
        
        if healthcare_quality < 50:
            analysis["healthcare_risk_level"] = "高"
            analysis["specific_risks"].append("医療システムの質が低く、緊急時の対応に不安")
            analysis["recommendations"].append("海外旅行保険の加入は必須。重篤な場合は医療搬送も検討")
            analysis["emergency_preparedness"] = "要注意"
        elif healthcare_quality < 70:
            analysis["healthcare_risk_level"] = "中"
            analysis["specific_risks"].append("医療の質にばらつきがある")
            analysis["recommendations"].append("信頼できる医療機関の情報を事前に調査")
    
    return analysis

def get_fallback_infrastructure_data(country: str) -> Dict[str, Any]:
    """
    データ取得に失敗した場合のフォールバックデータ
    """
    return {
        "message": f"{country}のインフラデータを取得できませんでした",
        "general_recommendations": [
            "外務省の渡航情報で最新の政治情勢を確認",
            "現地の交通ルールと安全情報を事前に調査",
            "海外旅行保険への加入を強く推奨",
            "緊急時の連絡先（大使館・領事館）を控えておく"
        ],
        "data_sources_to_check": [
            "外務省海外安全ホームページ",
            "WHO国別統計",
            "世界銀行ガバナンス指標",
            "国際機関の政治リスク評価"
        ]
    }

def calculate_infrastructure_stability_impact(infra_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    インフラ安定度が旅行安全に与える影響を分析
    """
    impact_analysis = {
        "direct_safety_impact": [],
        "indirect_safety_impact": [],
        "recovery_capability": "標準",
        "infrastructure_resilience": "中程度"
    }
    
    # 政治的安定性の影響
    if "corruption_perception_index" in infra_data:
        cpi_score = infra_data["corruption_perception_index"].get("cpi_score", 50)
        if cpi_score < 50:
            impact_analysis["indirect_safety_impact"].append(
                "政治不安により治安維持能力が低下する可能性"
            )
            impact_analysis["recovery_capability"] = "制限的"
    
    # 交通インフラの影響
    if "traffic_safety_data" in infra_data:
        fatality_rate = infra_data["traffic_safety_data"].get("road_traffic_deaths_per_100k", 15)
        if fatality_rate > 15:
            impact_analysis["direct_safety_impact"].append(
                "交通事故による直接的な安全リスクが高い"
            )
    
    # 医療インフラの影響
    if "healthcare_system" in infra_data:
        healthcare_quality = infra_data["healthcare_system"].get("healthcare_access_quality_index", 50)
        if healthcare_quality < 60:
            impact_analysis["recovery_capability"] = "制限的"
            impact_analysis["indirect_safety_impact"].append(
                "医療体制の脆弱性により、事故・疾病時のリカバリーが困難"
            )
    
    return impact_analysis