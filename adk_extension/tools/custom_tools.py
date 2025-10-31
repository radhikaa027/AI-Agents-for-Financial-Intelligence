from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def calculate_investment_score(financial_data: Dict[str, Any], news_sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates a proprietary investment score based on financial metrics and news sentiment.

    This is our custom tool. It takes structured data, applies a simple scoring
    logic, and returns a score and recommendation.
    """
    logger.info("CUSTOM TOOL: Calculating proprietary investment score...")
    
    scores = {}
    
    # 1. Valuation Score (based on P/E Ratio)
    pe_ratio = financial_data.get("pe_ratio")
    if isinstance(pe_ratio, (int, float)):
        if pe_ratio < 15:
            scores['valuation'] = 10  # Very Undervalued
        elif pe_ratio < 25:
            scores['valuation'] = 7   # Fairly Valued
        elif pe_ratio < 40:
            scores['valuation'] = 4   # Overvalued
        else:
            scores['valuation'] = 1   # Highly Overvalued
    else:
        scores['valuation'] = 3 # Default score if data is missing

    # 2. Profitability Score (based on Profit Margin)
    profit_margin = financial_data.get("profit_margin")
    if isinstance(profit_margin, (int, float)):
        if profit_margin > 0.20: # 20%
            scores['profitability'] = 10 # Excellent
        elif profit_margin > 0.10: # 10%
            scores['profitability'] = 7  # Good
        elif profit_margin > 0:
            scores['profitability'] = 4  # Average
        else:
            scores['profitability'] = 1  # Poor
    else:
        scores['profitability'] = 3

    # 3. Sentiment Score (based on news analysis)
    sentiment = news_sentiment.get('overall_sentiment', {}).get('sentiment', 'Neutral').lower()
    if sentiment == 'positive':
        scores['sentiment'] = 9
    elif sentiment == 'neutral':
        scores['sentiment'] = 5
    else: # Negative
        scores['sentiment'] = 1

    # Calculate final weighted score (out of 10)
    # Weighting: 40% Valuation, 40% Profitability, 20% Sentiment
    total_score = (scores['valuation'] * 0.4) + (scores['profitability'] * 0.4) + (scores['sentiment'] * 0.2)
    
    # Determine final recommendation
    if total_score > 7.5:
        recommendation = "Strong Buy"
    elif total_score > 6.0:
        recommendation = "Buy"
    elif total_score > 4.0:
        recommendation = "Hold"
    else:
        recommendation = "Sell"
        
    result = {
        "total_score": round(total_score, 2),
        "recommendation": recommendation,
        "component_scores": scores
    }
    
    logger.info(f"CUSTOM TOOL: Investment score calculated: {result}")
    return result