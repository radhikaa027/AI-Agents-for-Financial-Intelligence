import logging
import os
import google.generativeai as genai
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Import our custom modules
from utils.logging_setup import setup_logging
from config import GOOGLE_API_KEY
from agents.financial_agent_functions import (
    run_quantitative_analysis,
    run_market_research,
    run_risk_assessment,
    run_report_writing,
    run_compliance_validation
)
from tools.custom_tools import calculate_investment_score
from tools.market_data_tools import yahoo_finance_tools # Needed to get company name

def main():
    """
    Main orchestrator function for the ADK-based investment analysis workflow.
    """
    logger = setup_logging()
    genai.configure(api_key=GOOGLE_API_KEY)
    
    logger.info("ADK Investment Analysis System - Initiated")
    
    # User Input
    ticker = input("\n Enter stock ticker (or press Enter for 'AAPL'): ").strip().upper()
    if not ticker:
        ticker = "AAPL"
    
    # Get the full company name
    try:
        company_name = yahoo_finance_tools.get_stock_data(ticker).get('company_name', ticker)
    except Exception:
        company_name = ticker
        
    logger.info(f"Starting analysis for: {company_name} ({ticker})")
    
    # Initialize the State (Memory)
    analysis_state = {
        "ticker": ticker,
        "company_name": company_name,
        "current_date": datetime.now().strftime("%B %d, %Y")
    }
    
    # Parallel Execution for Data Gathering
    logger.info("--- Starting Parallel Data Gathering ---")
    with ThreadPoolExecutor(max_workers=2) as executor:
        
        quant_future = executor.submit(run_quantitative_analysis, analysis_state)
        market_future = executor.submit(run_market_research, analysis_state)
        
        quant_success = quant_future.result()
        market_success = market_future.result()

    if not (quant_success and market_success):
        logger.error("Data gathering failed. Aborting workflow.")
        return
    logger.info("--- Parallel Data Gathering Complete ---")

    # Sequential Execution
    logger.info("--- Starting Sequential Analysis & Synthesis ---")
    
    # Run Risk Assessment
    if not run_risk_assessment(analysis_state):
        logger.error("Risk assessment failed. Aborting workflow.")
        return

    # Run Report Writing
    if not run_report_writing(analysis_state):
        logger.error("Report writing failed. Aborting workflow.")
        return
        
    # Run Compliance Validation (Hallucination Check)
    if not run_compliance_validation(analysis_state):
        logger.error("Compliance validation failed. Aborting workflow.")
        return
    logger.info("--- Sequential Analysis & Synthesis Complete ---")

    # 6. Run Custom Tool for Final Score
    logger.info("--- Running Custom Tool ---")
    investment_score = calculate_investment_score(
        analysis_state["raw_financial_data"],
        analysis_state["raw_news_data"]
    )
    analysis_state["investment_score"] = investment_score
    logger.info("--- Custom Tool Execution Complete ---")

    # 7. Final Output
    final_report = analysis_state.get("final_report", "Report could not be generated.")
    score_summary = f"Proprietary Investment Score: {investment_score['total_score']}/10 ({investment_score['recommendation']})"
    
    full_output = f"# Investment Report: {company_name} ({ticker})\n\n"
    full_output += f"**{score_summary}**\n\n"
    full_output += final_report

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(full_output)
    
    # Save the final report
    output_file = f"outputs/investment_report_{ticker.lower()}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_output)
    logger.info(f"💾 Report saved to: {output_file}")
    logger.info("🎉 Workflow finished successfully!")

if __name__ == "__main__":
    main() 