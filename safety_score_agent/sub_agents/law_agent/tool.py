import requests
import json
from typing import Dict, Any, List
import time

def get_law_enforcement_data(country: str) -> Dict[str, Any]:
    """
    複数のデータソースから法執行機関の信頼性データを取得する
    
    Args:
        country: 国名（英語）
    
    Returns:
        Dict containing law enforcement reliability data from multiple sources
    """
    try:
        result = {
            "country": country,
            "global_peace_index_data": get_gpi_law_enforcement_data(country),
            "world_bank_governance": get_world_bank_governance_data(country),
            "police_trust_indicators": get_police_trust_data(country),
            "law_enforcement_categories": {
                "police_reliability": {
                    "description": "警察活動の信頼性・効率性",
                    "indicators": ["police_trust_score", "response_time", "crime_clearance_rate", "public_confidence"]
                },
                "corruption_level": {
                    "description": "法執行機関の汚職度合い",
                    "indicators": ["police_corruption_index", "judicial_corruption", "bribery_incidents"]
                },
                "judicial_system": {
                    "description": "司法制度の機能レベル",
                    "indicators": ["rule_of_law_index", "judicial_independence", "court_efficiency"]
                }
            },
            "overall_law_enforcement_score": 0,
            "data_collection_timestamp": time.time()
        }
        
        # 総合法執行機関信頼性スコアを計算
        result["overall_law_enforcement_score"] = calculate_law_enforcement_score(result)
        
        return result
        
    except Exception as e:
        return {
            "country": country,
            "error": f"データ取得エラー: {str(e)}",
            "fallback_data": get_fallback_law_enforcement_data(country)
        }

def get_gpi_law_enforcement_data(country: str) -> Dict[str, Any]:
    """
    世界平和度指数から法執行関連データを取得（シミュレート）
    """
    gpi_law_data = {
        "overall_peace_rank": 25,
        "peace_score": 1.85,
        "police_reliability_score": 2.1,  # 1-5スケール（1が最良）
        "internal_security_apparatus": 1.9,
        "security_officers_and_police": 2.2,
        "relations_with_neighboring_countries": 1.8,
        "level_of_violent_crime": 2.0,
        "likelihood_of_violent_demonstrations": 1.7,
        "data_source": "Global Peace Index 2024",
        "methodology": "Expert panel assessments and quantitative data",
        "confidence_level": "High",
        "regional_comparison": {
            "region": "Western Europe",
            "regional_average": 2.3,
            "country_performance": "Better than average"
        }
    }
    
    return gpi_law_data

def get_world_bank_governance_data(country: str) -> Dict[str, Any]:
    """
    世界銀行のガバナンス指標から法の支配データを取得（シミュレート）
    """
    wb_governance_data = {
        "rule_of_law_percentile": 85.2,  # 0-100パーセンタイル
        "rule_of_law_estimate": 1.45,    # -2.5 to 2.5スケール
        "regulatory_quality_percentile": 88.7,
        "government_effectiveness_percentile": 82.1,
        "control_of_corruption_percentile": 79.8,
        "voice_and_accountability_percentile": 91.3,
        "political_stability_percentile": 77.4,
        "data_year": 2023,
        "data_source": "World Bank Worldwide Governance Indicators",
        "methodology": "Perception-based governance indicators",
        "number_of_sources": 15,
        "margin_of_error": 0.18,
        "confidence_interval_90": {
            "lower_bound": 1.27,
            "upper_bound": 1.63
        }
    }
    
    return wb_governance_data

def get_police_trust_data(country: str) -> Dict[str, Any]:
    """
    警察信頼度に関する詳細データを取得（シミュレート）
    """
    police_trust_data = {
        "public_trust_in_police": 78.5,  # 0-100スケール
        "police_effectiveness_rating": 82.1,
        "corruption_in_police_force": 15.2,  # 0-100スケール（低いほど良い）
        "police_response_time_minutes": 8.5,
        "crime_reporting_rate": 71.3,
        "victim_satisfaction_rate": 68.9,
        "police_accountability_measures": {
            "internal_affairs_department": "Present",
            "civilian_oversight_board": "Present",
            "body_cameras_usage": "Widespread",
            "complaint_resolution_system": "Effective"
        },
        "specialized_units": {
            "tourist_police": "Available",
            "cybercrime_unit": "Available", 
            "anti_corruption_unit": "Available",
            "emergency_response_team": "Available"
        },
        "international_cooperation": {
            "interpol_membership": "Active",
            "regional_police_cooperation": "Strong",
            "information_sharing": "Good"
        },
        "data_sources": [
            "National Crime Victimization Survey",
            "Police Performance Indicators",
            "Public Opinion Surveys"
        ],
        "last_updated": "2024-02"
    }
    
    return police_trust_data

def calculate_law_enforcement_score(law_data: Dict[str, Any]) -> float:
    """
    複数のデータソースから総合法執行機関信頼性スコア（25点満点）を計算
    
    Returns:
        float: 0-25のスケールでの法執行機関信頼性スコア
    """
    try:
        score_components = []
        
        # 世界平和度指数からのスコア（警察の信頼性）
        if "global_peace_index_data" in law_data:
            police_reliability = law_data["global_peace_index_data"].get("police_reliability_score", 3.0)
            # GPIスコアは1-5（1が最良）なので、25点満点に変換
            gpi_score = max(0, 25 - ((police_reliability - 1) * 6.25))
            score_components.append(("police_reliability", gpi_score))
        
        # 世界銀行の法の支配指標からのスコア
        if "world_bank_governance" in law_data:
            rule_of_law_percentile = law_data["world_bank_governance"].get("rule_of_law_percentile", 50)
            # パーセンタイルを25点満点に変換
            wb_score = (rule_of_law_percentile / 100) * 25
            score_components.append(("rule_of_law", wb_score))
        
        # 警察信頼度指標からのスコア
        if "police_trust_indicators" in law_data:
            public_trust = law_data["police_trust_indicators"].get("public_trust_in_police", 50)
            corruption_level = law_data["police_trust_indicators"].get("corruption_in_police_force", 50)
            
            # 信頼度スコア（高いほど良い）
            trust_score = (public_trust / 100) * 12.5
            # 汚職度スコア（低いほど良い）
            anti_corruption_score = ((100 - corruption_level) / 100) * 12.5
            
            police_score = trust_score + anti_corruption_score
            score_components.append(("police_trust", police_score))
        
        # 重み付き平均を計算
        if score_components:
            total_score = sum(score for _, score in score_components)
            average_score = total_score / len(score_components)
            return round(average_score, 1)
        else:
            return 12.5  # デフォルト値（25点満点の半分）
            
    except Exception as e:
        return 12.5  # エラー時のデフォルト値

def analyze_law_enforcement_risks(law_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    法執行機関関連のリスク分析
    """
    analysis = {
        "police_reliability_level": "標準",
        "corruption_risk_level": "低",
        "judicial_system_trust": "高",
        "specific_risks": [],
        "recommendations": [],
        "emergency_support_availability": "良好"
    }
    
    # 世界平和度指数に基づく警察信頼性評価
    if "global_peace_index_data" in law_data:
        police_reliability = law_data["global_peace_index_data"].get("police_reliability_score", 3.0)
        
        if police_reliability > 3.5:
            analysis["police_reliability_level"] = "低"
            analysis["specific_risks"].append("警察の対応能力・信頼性に重大な問題がある")
            analysis["recommendations"].append("緊急時は大使館・領事館への連絡を優先する")
            analysis["emergency_support_availability"] = "制限的"
        elif police_reliability > 2.5:
            analysis["police_reliability_level"] = "中程度"
            analysis["specific_risks"].append("警察の対応にばらつきがある可能性")
            analysis["recommendations"].append("重要事案では複数の機関に相談を検討")
    
    # 汚職レベルに基づくリスク評価
    if "police_trust_indicators" in law_data:
        corruption_level = law_data["police_trust_indicators"].get("corruption_in_police_force", 50)
        
        if corruption_level > 60:
            analysis["corruption_risk_level"] = "高"
            analysis["specific_risks"].append("警察による汚職・賄賂要求のリスクが高い")
            analysis["recommendations"].append("警察との接触時は記録を残し、不当な要求には応じない")
        elif corruption_level > 30:
            analysis["corruption_risk_level"] = "中"
            analysis["specific_risks"].append("一部の警察官による汚職の可能性")
            analysis["recommendations"].append("正規の手続きを確実に踏み、領収書等を保管")
    
    # 法の支配に基づく司法システム評価
    if "world_bank_governance" in law_data:
        rule_of_law_percentile = law_data["world_bank_governance"].get("rule_of_law_percentile", 50)
        
        if rule_of_law_percentile < 30:
            analysis["judicial_system_trust"] = "低"
            analysis["specific_risks"].append("司法制度の独立性・公正性に重大な懸念")
            analysis["recommendations"].append("法的問題が生じた場合は即座に法的支援を求める")
        elif rule_of_law_percentile < 60:
            analysis["judicial_system_trust"] = "中程度"
            analysis["specific_risks"].append("司法制度の予測可能性にばらつき")
            analysis["recommendations"].append("現地の法的要件を事前に十分調査")
    
    return analysis

def assess_traveler_law_enforcement_support(law_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    旅行者が法執行機関から受けられるサポートを評価
    """
    support_assessment = {
        "emergency_response_quality": "良好",
        "language_support_availability": "制限的",
        "tourist_specific_services": [],
        "recommended_contact_priority": [],
        "expected_response_time": "標準"
    }
    
    # 警察信頼度データに基づく評価
    if "police_trust_indicators" in law_data:
        police_data = law_data["police_trust_indicators"]
        
        # 観光警察の有無
        if police_data.get("specialized_units", {}).get("tourist_police") == "Available":
            support_assessment["tourist_specific_services"].append("観光警察による専門サポート")
            support_assessment["language_support_availability"] = "良好"
            support_assessment["recommended_contact_priority"].append("観光警察（第1優先）")
        
        # 緊急対応時間
        response_time = police_data.get("police_response_time_minutes", 15)
        if response_time <= 10:
            support_assessment["expected_response_time"] = "迅速"
            support_assessment["emergency_response_quality"] = "優秀"
        elif response_time > 20:
            support_assessment["expected_response_time"] = "遅延"
            support_assessment["emergency_response_quality"] = "要改善"
        
        # 被害者満足度
        victim_satisfaction = police_data.get("victim_satisfaction_rate", 50)
        if victim_satisfaction < 50:
            support_assessment["emergency_response_quality"] = "制限的"
    
    # 常に推奨する連絡先を追加
    support_assessment["recommended_contact_priority"].extend([
        "現地日本国領事館・大使館（重要事案）",
        "一般警察（110番等の緊急番号）",
        "海外旅行保険会社（24時間サポート）"
    ])
    
    return support_assessment

def get_fallback_law_enforcement_data(country: str) -> Dict[str, Any]:
    """
    データ取得に失敗した場合のフォールバックデータ
    """
    return {
        "message": f"{country}の法執行機関データを取得できませんでした",
        "general_recommendations": [
            "外務省の海外安全情報で治安機関の状況を確認",
            "現地日本国領事館の連絡先を必ず控えておく", 
            "緊急時の現地警察・救急の番号を事前に調査",
            "海外旅行保険の24時間サポートサービスを活用",
            "重要な法的文書は事前に現地語に翻訳準備"
        ],
        "emergency_contacts_to_prepare": [
            "現地日本国領事館・大使館",
            "現地警察の緊急番号",
            "海外旅行保険会社の緊急連絡先",
            "現地の法的支援サービス"
        ],
        "data_sources_to_check": [
            "外務省海外安全ホームページ",
            "世界銀行ガバナンス指標",
            "国際透明性機構レポート",
            "各国政府の治安機関公式情報"
        ]
    }

def calculate_law_enforcement_reliability_impact(law_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    法執行機関の信頼性が旅行安全に与える影響を分析
    """
    impact_analysis = {
        "direct_safety_impact": [],
        "indirect_safety_impact": [],
        "emergency_response_reliability": "標準",
        "legal_protection_level": "適切"
    }
    
    # 警察信頼性の影響
    if "global_peace_index_data" in law_data:
        police_reliability = law_data["global_peace_index_data"].get("police_reliability_score", 3.0)
        if police_reliability > 3.0:
            impact_analysis["direct_safety_impact"].append(
                "警察の対応能力不足により、犯罪被害時の適切な支援が期待できない"
            )
            impact_analysis["emergency_response_reliability"] = "制限的"
    
    # 汚職レベルの影響
    if "police_trust_indicators" in law_data:
        corruption_level = law_data["police_trust_indicators"].get("corruption_in_police_force", 50)
        if corruption_level > 40:
            impact_analysis["indirect_safety_impact"].append(
                "警察の汚職により、適切な法執行が期待できず治安悪化要因となる"
            )
            impact_analysis["legal_protection_level"] = "不安定"
    
    # 司法制度の影響
    if "world_bank_governance" in law_data:
        rule_of_law = law_data["world_bank_governance"].get("rule_of_law_percentile", 50)
        if rule_of_law < 40:
            impact_analysis["indirect_safety_impact"].append(
                "司法制度の脆弱性により、法的トラブル時の公正な解決が困難"
            )
            impact_analysis["legal_protection_level"] = "脆弱"
    
    return impact_analysis

