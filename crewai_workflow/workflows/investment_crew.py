"""
Investment Analysis Crew - Main Workflow Orchestration
Coordinates all agents and tasks for comprehensive investment analysis
"""

from crewai import Crew, Process
from agents.financial_agents import financial_agents
from workflows.investment_tasks import investment_tasks
from config.settings import DEFAULT_COMPANY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvestmentAnalysisCrew:
    """
    Main crew orchestration for investment analysis workflow
    """
    
    def __init__(self):
        self.agents = financial_agents
        self.tasks = investment_tasks
        self.logger = logger
        
    def create_analysis_crew(self, ticker: str, company_name: str, current_date: str) -> Crew:
        """Create and configure the investment analysis crew"""
        self.logger.info(f"Creating investment analysis crew for {company_name} ({ticker})")
        
        # Create all agents
        portfolio_manager = self.agents.portfolio_manager()
        quantitative_analyst = self.agents.quantitative_analyst()
        market_researcher = self.agents.market_intelligence_researcher()
        risk_specialist = self.agents.risk_assessment_specialist()
        report_writer = self.agents.investment_report_writer()
        compliance_validator = self.agents.compliance_validator()
        
        # Create all tasks
        plan_task = self.tasks.plan_analysis_task(ticker, company_name)
        data_task = self.tasks.gather_financial_data_task(ticker, company_name)
        news_task = self.tasks.research_market_sentiment_task(ticker, company_name)
        risk_task = self.tasks.assess_investment_risks_task(ticker, company_name)
        report_task = self.tasks.write_investment_report_task(ticker, company_name, current_date)
        compliance_task = self.tasks.validate_compliance_task(ticker, company_name, current_date)
        
        # Configure task assignments
        plan_task.agent = portfolio_manager
        data_task.agent = quantitative_analyst
        news_task.agent = market_researcher
        risk_task.agent = risk_specialist
        report_task.agent = report_writer
        compliance_task.agent = compliance_validator
        
        # parallel execution for data gathering tasks
        data_task.async_execution = True
        news_task.async_execution = True
        
        # task dependencies for proper workflow
        risk_task.context = [data_task, news_task]
        report_task.context = [risk_task]
        compliance_task.context = [report_task]
        
        # Create the crew 
        crew = Crew(
            agents=[
                quantitative_analyst,
                market_researcher,
                risk_specialist,
                report_writer,
                compliance_validator
            ],
            tasks=[
                plan_task,
                data_task,
                news_task,
                risk_task,
                report_task,
                compliance_task
            ],
            process=Process.hierarchical,
            manager_agent=portfolio_manager,  
            verbose=True,
            full_output=True
        )
        
        self.logger.info("✅ Investment analysis crew created successfully")
        return crew
    
    def log_step(self, step):
        """Log each step for better visibility"""
        if hasattr(step, 'action') and hasattr(step, 'tool'):
            print(f"    🔧 Using {step.tool} ({step.action})")
    
    def log_task_completion(self, task_output):
        """Log task completion"""
        if hasattr(task_output, 'agent'):
            print(f"✅ Task completed by {task_output.agent}")


    def execute_analysis(self, ticker: str = None, company_name: str = None, current_date: str = None) -> str:
        """
        Execute the complete investment analysis workflow
        
        Args:
            ticker: Stock symbol (defaults to settings)
            company_name: Company name (will be retrieved if not provided)
            
        Returns:
            Final investment report as string
        """
        # Use defaults if not provided
        if not ticker:
            ticker = DEFAULT_COMPANY
            
        if not company_name:
            try:
                from tools.market_data_tools import yahoo_finance_tools
                stock_data = yahoo_finance_tools.get_stock_data(ticker)
                company_name = stock_data.get('company_name', ticker)
            except:
                company_name = ticker
        
        self.logger.info(f"🚀 Starting investment analysis for {company_name} ({ticker})")
        
        try:
            # Create the crew
            crew = self.create_analysis_crew(ticker, company_name, current_date)
            
            # Execute the workflow
            self.logger.info("⚡ Executing investment analysis workflow...")
            result = crew.kickoff(inputs={
                "ticker": ticker,
                "company_name": company_name
            })
            
            self.logger.info("✅ Investment analysis completed successfully")
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during analysis execution: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def get_crew_summary(self) -> dict:
        """
        Get summary information about the crew configuration
        
        Returns:
            Dict containing crew configuration details
        """
        return {
            "total_agents": 6,
            "agent_roles": [
                "Senior Portfolio Manager",
                "Senior Quantitative Analyst", 
                "Senior Market Intelligence Researcher",
                "Senior Risk Assessment Specialist",
                "Senior Investment Report Writer",
                "Senior Compliance Validator"
            ],
            "total_tasks": 6,
            "workflow_type": "Sequential with parallel data gathering",
            "tools_available": 4,
            "process_flow": "Plan → [Data + News] → Risk → Report → Compliance"
        }

# global instance
investment_crew = InvestmentAnalysisCrew()
