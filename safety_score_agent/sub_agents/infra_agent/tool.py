import requests
import json
from typing import Dict, Any, List
import time

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
    汚職認識指数データを取得（シミュレート）
    実際の実装では、Transparency Internationalのデータを使用
    """
    # シミュレートデータ（実際の実装では外部APIまたはデータベースを使用）
    corruption_data = {
        "cpi_score": 73,  # 0-100スケール（100が最もクリーン）
        "cpi_rank": 25,   # 世界ランキング
        "total_countries": 180,
        "regional_average": 68,
        "classification": "Good",  # Very Good (80+), Good (60-79), Moderate (40-59), Poor (20-39), Very Poor (<20)
        "trend": "Stable",  # Improving, Stable, Declining
        "data_source": "Transparency International CPI 2024",
        "methodology": "Expert assessments and opinion surveys",
        "last_updated": "2024-01"
    }
    
    return corruption_data

def get_traffic_safety_data(country: str) -> Dict[str, Any]:
    """
    WHO交通安全データを取得（シミュレート）
    """
    traffic_data = {
        "road_traffic_deaths_per_100k": 4.2,
        "total_road_deaths": 3500,
        "year": 2023,
        "who_region": "European Region",
        "income_classification": "High income",
        "safety_rating": "Good",  # Excellent (<5), Good (5-10), Moderate (10-20), Poor (20-30), Very Poor (>30)
        "main_risk_factors": [
            "Speeding",
            "Drink-driving", 
            "Not wearing seatbelts"
        ],
        "road_infrastructure_quality": "High",
        "vehicle_safety_standards": "High",
        "enforcement_effectiveness": "High",
        "data_source": "WHO Global Status Report on Road Safety 2023",
        "data_quality": "High quality"
    }
    
    return traffic_data

def get_healthcare_data(country: str) -> Dict[str, Any]:
    """
    医療システムデータを取得（シミュレート）
    """
    healthcare_data = {
        "healthcare_access_quality_index": 85.2,  # 0-100スケール
        "universal_health_coverage_index": 82,
        "health_system_performance_rank": 12,
        "physicians_per_1000": 4.1,
        "hospital_beds_per_1000": 8.2,
        "healthcare_expenditure_gdp_percent": 11.1,
        "emergency_response_quality": "High",
        "medical_tourism_ranking": 15,
        "health_security_index": 78.5,
        "healthcare_categories": {
            "accessibility": "High",
            "quality": "Very High", 
            "affordability": "High",
            "emergency_care": "Excellent"
        },
        "data_sources": [
            "WHO Health Statistics 2024",
            "Global Health Security Index",
            "Healthcare Access and Quality Index"
        ],
        "last_updated": "2024-03"
    }
    
    return healthcare_data

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