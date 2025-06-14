import requests
import json
from typing import Dict, Any, List
import time

def get_crime_data(country: str) -> Dict[str, Any]:
    """
    複数のデータソースから犯罪データを取得する
    
    Args:
        country: 国名（英語）
    
    Returns:
        Dict containing crime data from multiple sources
    """
    try:
        result = {
            "country": country,
            "numbeo_data": get_numbeo_crime_data(country),
            "global_peace_index": get_global_peace_index_data(country),
            "unodc_homicide_rate": get_unodc_homicide_data(country),
            "crime_categories": {
                "violent_crimes": {
                    "description": "殺人・強盗・暴行などの凶悪犯罪",
                    "indicators": ["homicide_rate", "violent_crime_index", "assault_probability"]
                },
                "petty_crimes": {
                    "description": "スリ・置き引き・詐欺などの軽犯罪",
                    "indicators": ["theft_probability", "pickpocket_risk", "fraud_incidents"]
                }
            },
            "overall_safety_score": 0,
            "data_collection_timestamp": time.time()
        }
        
        # 総合安全スコアを計算
        result["overall_safety_score"] = calculate_safety_score(result)
        
        return result
        
    except Exception as e:
        return {
            "country": country,
            "error": f"データ取得エラー: {str(e)}",
            "fallback_data": get_fallback_crime_data(country)
        }

def get_numbeo_crime_data(country: str) -> Dict[str, Any]:
    """
    Numbeoから犯罪指数データを取得（シミュレート）
    実際の実装では、NumbeoのAPIまたはスクレイピングを使用
    """
    # シミュレートデータ（実際の実装では外部APIを使用）
    numbeo_data = {
        "crime_index": 45.2,
        "safety_index": 54.8,
        "violent_crime_level": "Medium",
        "property_crime_level": "Medium-High",
        "pickpocket_probability": "Medium",
        "theft_probability": "Medium-High",
        "assault_probability": "Low-Medium",
        "data_source": "Numbeo Crime Database",
        "last_updated": "2024-12"
    }
    
    return numbeo_data

def get_global_peace_index_data(country: str) -> Dict[str, Any]:
    """
    世界平和度指数から安全データを取得（シミュレート）
    """
    gpi_data = {
        "overall_peace_rank": 25,
        "peace_score": 1.85,
        "violent_crime_perception": 2.1,
        "weapons_access": 2.3,
        "security_apparatus": 1.9,
        "data_source": "Global Peace Index 2024",
        "methodology": "社会の安全・安心ドメイン指標"
    }
    
    return gpi_data

def get_unodc_homicide_data(country: str) -> Dict[str, Any]:
    """
    国連薬物犯罪事務所から殺人率データを取得（シミュレート）
    """
    unodc_data = {
        "homicide_rate_per_100k": 1.2,
        "total_homicides": 156,
        "year": 2023,
        "data_quality": "High",
        "data_source": "UNODC Global Study on Homicide",
        "comparative_ranking": "Low homicide rate country"
    }
    
    return unodc_data

def calculate_safety_score(crime_data: Dict[str, Any]) -> float:
    """
    複数のデータソースから総合安全スコアを計算
    
    Returns:
        float: 0-100のスケールでの安全スコア（100が最も安全）
    """
    try:
        score_components = []
        
        # Numbeoデータからのスコア
        if "numbeo_data" in crime_data and "safety_index" in crime_data["numbeo_data"]:
            score_components.append(crime_data["numbeo_data"]["safety_index"])
        
        # 世界平和度指数からのスコア（逆スケール調整）
        if "global_peace_index" in crime_data and "peace_score" in crime_data["global_peace_index"]:
            # 平和度指数は低いほど良いので、100から引く
            peace_score = max(0, 100 - (crime_data["global_peace_index"]["peace_score"] * 20))
            score_components.append(peace_score)
        
        # 殺人率からのスコア
        if "unodc_homicide_rate" in crime_data and "homicide_rate_per_100k" in crime_data["unodc_homicide_rate"]:
            homicide_rate = crime_data["unodc_homicide_rate"]["homicide_rate_per_100k"]
            # 殺人率が低いほど高いスコア（10以上で0点、0で100点）
            homicide_score = max(0, 100 - (homicide_rate * 10))
            score_components.append(homicide_score)
        
        # 平均を計算
        if score_components:
            return round(sum(score_components) / len(score_components), 1)
        else:
            return 50.0  # デフォルト値
            
    except Exception as e:
        return 50.0  # エラー時のデフォルト値

def get_fallback_crime_data(country: str) -> Dict[str, Any]:
    """
    データ取得に失敗した場合のフォールバックデータ
    """
    return {
        "message": f"{country}の犯罪データを取得できませんでした",
        "general_advice": [
            "外務省の海外安全情報を確認してください",
            "現地の最新治安情報を入手してください",
            "貴重品の管理に注意してください",
            "夜間の単独行動は避けてください"
        ],
        "data_sources_to_check": [
            "外務省海外安全ホームページ",
            "現地日本国領事館情報",
            "国際機関の治安レポート"
        ]
    }

def analyze_travel_safety_risks(crime_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    旅行者向けの安全リスク分析
    """
    analysis = {
        "violent_crime_risk": "低",
        "petty_crime_risk": "中",
        "specific_risks": [],
        "recommendations": []
    }
    
    # Numbeoデータに基づくリスク評価
    if "numbeo_data" in crime_data:
        numbeo = crime_data["numbeo_data"]
        
        if numbeo.get("pickpocket_probability") in ["High", "Very High"]:
            analysis["specific_risks"].append("スリ・置き引きのリスクが高い")
            analysis["recommendations"].append("貴重品は分散して携帯し、混雑した場所では特に注意")
        
        if numbeo.get("theft_probability") in ["High", "Very High"]:
            analysis["specific_risks"].append("窃盗被害のリスクが高い")
            analysis["recommendations"].append("ホテルのセーフティボックスを活用し、車内に荷物を残さない")
        
        if numbeo.get("assault_probability") in ["High", "Very High"]:
            analysis["violent_crime_risk"] = "高"
            analysis["specific_risks"].append("暴行事件のリスクが高い")
            analysis["recommendations"].append("夜間の外出を控え、人通りの少ない場所を避ける")
    
    # 殺人率に基づく評価
    if "unodc_homicide_rate" in crime_data:
        homicide_rate = crime_data["unodc_homicide_rate"].get("homicide_rate_per_100k", 0)
        if homicide_rate > 10:
            analysis["violent_crime_risk"] = "高"
            analysis["specific_risks"].append("殺人事件の発生率が高い")
            analysis["recommendations"].append("危険地域を事前に把握し、絶対に近づかない")
        elif homicide_rate > 5:
            analysis["violent_crime_risk"] = "中"
    
    return analysis