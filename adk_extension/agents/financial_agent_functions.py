import logging
from typing import Dict, Any
import google.generativeai as genai

from tools.market_data_tools import yahoo_finance_tools
from tools.news_tools import news_api_tools

logger = logging.getLogger(__name__)

def run_quantitative_analysis(analysis_state: Dict[str, Any]) -> bool:
    ticker = analysis_state.get("ticker")
    logger.info(f"AGENT: Starting quantitative analysis for {ticker}...")
    try:
        financial_data = yahoo_finance_tools.get_stock_data(ticker)
        technical_data = yahoo_finance_tools.get_technical_indicators(ticker)
        analysis_state["raw_financial_data"] = financial_data
        analysis_state["raw_technical_data"] = technical_data
        
        prompt = f"""
        You are a Senior Quantitative Analyst, with expertise in financial modeling, statistical analysis, and technical analysis. 
        You have a PhD in Finance and 8 years of experience at top-tier investment firms. Your task is to provide an insightful, narrative summary
        of the following financial data for the stock ticker: {ticker}.

        Do not just list the numbers. For each key metric, provide a brief, italicized *Commentary*
        on what the number signifies in the context of the company's performance or valuation.

        Here is the financial data:
        ---
        {financial_data}
        ---
        Here is the technical indicator data:
        ---
        {technical_data}
        ---

        Based on the data provided, write a professional summary covering:
        1.  **Valuation:** Market Cap, P/E Ratio, and EPS.
        2.  **Profitability:** Comment on the Profit Margin.
        3.  **Technicals:** Interpret the current price relative to its moving averages and RSI.
        """
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')
        response = model.generate_content(prompt)
        analysis_state["quantitative_analysis"] = response.text
        logger.info(f"AGENT: Quantitative analysis for {ticker} completed successfully.")
        return True
    except Exception as e:
        logger.error(f"AGENT: Error during quantitative analysis for {ticker}: {e}")
        return False

def run_market_research(analysis_state: Dict[str, Any]) -> bool:
    ticker = analysis_state.get("ticker")
    company_name = analysis_state.get("company_name")
    logger.info(f"AGENT: Starting market research for {company_name}...")
    try:
        news_data = news_api_tools.get_company_news(company_name, ticker)
        analysis_state["raw_news_data"] = news_data
        
    
        prompt = f"""
        You are a Senior Market Intelligence Researcher with a background in journalism and financial analysis. 
        You have 10 years of experience tracking market trends, corporate developments, and macroeconomic factors. Your task is to analyze
        the market sentiment for {company_name} ({ticker}) based on the provided news articles.

        Instead of a simple list, please synthesize the findings into a cohesive, narrative summary.

        Here is the recent news data:
        ---
        {news_data}
        ---

        Based on the news, write a paragraph summarizing:
        - The **Overall Sentiment** (e.g., positive, cautiously optimistic, negative).
        - The **Key Drivers** behind this sentiment, referencing significant news stories.
        - Any **Potential Catalysts** or future events implied by the news.
        """
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')
        response = model.generate_content(prompt)
        analysis_state["market_sentiment_analysis"] = response.text
        logger.info(f"AGENT: Market research for {company_name} completed successfully.")
        return True
    except Exception as e:
        logger.error(f"AGENT: Error during market research for {company_name}: {e}")
        return False

def run_risk_assessment(analysis_state: Dict[str, Any]) -> bool:
    print(f"\n[Memory Check] Entering Risk Assessor. State contains keys: {list(analysis_state.keys())}")
    logger.info("AGENT: Starting risk assessment...")
    quantitative_summary = analysis_state.get("quantitative_analysis")
    sentiment_summary = analysis_state.get("market_sentiment_analysis")
    if not quantitative_summary or not sentiment_summary:
        logger.error("Previous analysis summaries not found in state.")
        return False


    prompt = f"""
    You are a Senior Risk Assessment Specialist with 12 years of experience in investment risk management. 
    You hold the FRM (Financial Risk Manager) certification and have worked at both hedge funds and institutional investment firms.
    Your task is to conduct a comprehensive risk analysis based on the provided quantitative and market sentiment reports.

    Synthesize the information into a clear, structured risk assessment. For each risk category,
    provide a brief explanation.

    Here is the Quantitative Analysis:
    ---
    {quantitative_summary}
    ---
    Here is the Market Sentiment Analysis:
    ---
    {sentiment_summary}
    ---

    Based on both reports, provide a detailed risk assessment covering:
    1.  **Financial Risks:** Focus on valuation concerns (like a high P/E ratio) and financial stability.
    2.  **Market Risks:** Analyze how market sentiment and broader trends could impact the stock.
    3.  **Operational & Business Model Risks:** Identify key business challenges or competitive threats.
    4.  **Conclude with an Overall Risk Rating** (e.g., Low, Moderate, Elevated) and list the top 3 key risk factors.
    """
    model = genai.GenerativeModel(model_name='gemini-1.5-pro')
    try:
        response = model.generate_content(prompt)
        analysis_state["risk_assessment"] = response.text
        logger.info("AGENT: Risk assessment completed successfully.")
        return True
    except Exception as e:
        logger.error(f"AGENT: Error during risk assessment: {e}")
        return False

def run_report_writing(analysis_state: Dict[str, Any]) -> bool:
    print(f"\n[Memory Check] Entering Report Writer. State contains keys: {list(analysis_state.keys())}")
    logger.info("AGENT: Starting final report synthesis...")
    quantitative_summary = analysis_state.get("quantitative_analysis")
    sentiment_summary = analysis_state.get("market_sentiment_analysis")
    risk_summary = analysis_state.get("risk_assessment")
    current_date = analysis_state.get("current_date")
    company_name = analysis_state.get("company_name")
    ticker = analysis_state.get("ticker")
    if not all([quantitative_summary, sentiment_summary, risk_summary, current_date, company_name, ticker]):
        logger.error("Missing one or more analysis components in state for report writing.")
        return False

    prompt = f"""
    You are a Senior Investment Report Writer for a top-tier investment firm, known for your
    clear, insightful, and professional analysis. You have 8 years of experience 
     writing research reports for institutional investors and have a talent for 
    translating complex financial analysis into clear, actionable recommendations.

    Your task is to synthesize the provided analyses into a single, comprehensive, and
    professionally formatted investment report for **{company_name} ({ticker})** in Markdown format.
    The report must be dated: **{current_date}**.

    **Source Information to Synthesize:**

    1. Quantitative Analysis:
    ---
    {quantitative_summary}
    ---

    2. Market Sentiment Analysis:
    ---
    {sentiment_summary}
    ---

    3. Risk Assessment:
    ---
    {risk_summary}
    ---

    **Instructions for Report Generation:**

    Using all the information above, construct a final report following this exact structure and tone:

    1.  **Executive Summary:** Begin with a concise, high-level overview. State the final investment
        recommendation (e.g., Buy, Hold, Sell) upfront and briefly justify it based on the key
        findings from the subsequent sections.

    2.  **Quantitative Analysis:** Present the quantitative findings. For each key metric, include the
        brief, italicized *Commentary* provided in the source analysis.

    3.  **Market Sentiment Analysis:** Present the narrative summary of market sentiment.

    4.  **Risk Assessment:** Detail the primary risks, organized by category, and state the overall risk rating.

    5.  **Investment Thesis and Rationale:** This is the most important section. Write a detailed,
        convincing argument for your final recommendation. Synthesize all the points—quantitative strengths,
        market mood, and potential risks—into a coherent investment thesis.

    6.  **Conclusion and Next Steps:** Briefly summarize the report and provide actionable next steps or key
        factors for an investor to monitor.

    **CRITICAL:**
    - Adopt a formal, institutional tone.
    - Ensure the report flows logically and reads as if written by a single, expert author.
    - Do not include any placeholders like '[Your Firm Name]'.
    """
    model = genai.GenerativeModel(model_name='gemini-1.5-pro')
    try:
        response = model.generate_content(prompt)
        analysis_state["draft_report"] = response.text
        logger.info("AGENT: Draft report generated successfully.")
        return True
    except Exception as e:
        logger.error(f"AGENT: Error during report writing: {e}")
        return False

def run_compliance_validation(analysis_state: Dict[str, Any]) -> bool:
    print(f"\n[Memory Check] Entering Compliance Validator. State contains keys: {list(analysis_state.keys())}")
    logger.info("AGENT: Starting compliance validation and fact-checking...")
    draft_report = analysis_state.get("draft_report")
    raw_financial_data = analysis_state.get("raw_financial_data")
    if not draft_report or not raw_financial_data:
        logger.error("Draft report or raw financial data not found in state.")
        return False
    prompt = f"""
    You are a Senior Compliance Validator with expertise in financial regulations
    and quality assurance. with 10 years of experience in financial services compliance and quality assurance. You hold Series 7, 66, 
    and 24 licenses and have deep knowledge of investment advisory regulations.
    Your task is to perform a final review of the investment report provided below.
    Your review must focus on two critical areas:
    1. Factual Accuracy (Hallucination Check): Cross-reference the financial metrics mentioned in the report's text against the raw data provided. Ensure that values like P/E Ratio, Market Cap, EPS, etc., in the report are IDENTICAL to the raw data. Correct any inconsistencies.
    2. Compliance and Formatting: Ensure the report includes a proper disclaimer, is professionally formatted, and is free of any placeholder text like '[Your Firm Name]'.
    Here is the Raw Financial Data for fact-checking:
    ---
    {raw_financial_data}
    ---
    Here is the Draft Report to be validated:
    ---
    {draft_report}
    ---
    Return the final, validated, and corrected version of the report. The output
    should be only the clean, final report text.
    """
    model = genai.GenerativeModel(model_name='gemini-1.5-pro')
    try:
        response = model.generate_content(prompt)
        analysis_state["final_report"] = response.text
        logger.info("AGENT: Compliance validation completed successfully.")
        return True
    except Exception as e:
        logger.error(f"AGENT: Error during compliance validation: {e}")
        return False