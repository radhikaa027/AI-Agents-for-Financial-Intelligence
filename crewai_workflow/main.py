"""
Main Entry Point for Investment Analysis System
Run complete investment analysis workflow
"""

from workflows.investment_crew import investment_crew
from config.settings import validate_config
import sys
import logging
import re
import os
from datetime import datetime 

# Set up logging for tree output
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',  
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_clean_report(result: dict) -> str:
    """
    Extracts the final clean report from the crew's full output.
    """
    if isinstance(result, dict) and 'final_output' in result:
        return result['final_output']
    else:
        return str(result)

def main():
    """Main function to run investment analysis"""
    print("🚀 Investment Analysis System - CrewAI Implementation")
    print("=" * 60)
    
    try:
        print("🔧 Validating system configuration...")
        validate_config()
        print("✅ Configuration validated successfully!")
        
        summary = investment_crew.get_crew_summary()
        print(f"\n📊 System Summary:")
        print(f"   Agents: {summary['total_agents']}")
        print(f"   Tasks: {summary['total_tasks']}")
        print(f"   Tools: {summary['tools_available']}")
        print(f"   Process: Hierarchical with Parallel Data Gathering")
        
        # Get user input for ticker
        if len(sys.argv) > 1:
            ticker = sys.argv[1].upper()
        else:
            ticker = input("\n📈 Enter stock ticker (or press Enter for TSLA): ").strip().upper()
            if not ticker:
                ticker = "TSLA"

        # Get the current date and format it
        current_date = datetime.now().strftime("%B %d, %Y")
        
        print(f"\n🎯 Starting analysis for: {ticker} (Report Date: {current_date})") 
        print("⏳ Watch the parallel execution below...")
        print("-" * 60)
        
        print(f"\n🎯 Starting analysis for: {ticker}")
        print("⏳ Watch the parallel execution below...")
        print("-" * 60)
        
        # Execute the analysis with verbose output
        raw_result = investment_crew.execute_analysis(ticker=ticker, current_date=current_date) 
        
        final_report = get_clean_report(raw_result)
        
        # Display results
        print("\n" + "=" * 60)
        print("📄 INVESTMENT ANALYSIS REPORT")
        print("=" * 60)
        print(final_report)
        
        os.makedirs("outputs", exist_ok=True)
        
        output_file = f"outputs/investment_report_{ticker.lower()}.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_report)
            print(f"\n💾 Report saved to: {output_file}")
        except Exception as e:
            print(f"\n⚠️ Could not save report: {str(e)}")
            logger.error(f"File save error: {str(e)}")
        
        print("\n🎉 Analysis completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logger.error(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    main()