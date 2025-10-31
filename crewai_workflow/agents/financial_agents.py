"""
Financial Analysis Agents for Investment Report Generation
CrewAI agent definitions with specialized roles
"""

from crewai import Agent, LLM
from crewai.tools import tool
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from tools.market_data_tools import yahoo_finance_tools
from tools.news_tools import news_api_tools

# Configure LLM for agents
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

from crewai import LLM
from config.settings import LLM_MODEL, LLM_PROVIDER, LLM_TEMPERATURE

def create_gemini_llm():
    return LLM(
        model="gemini/gemini-2.5-flash", 
        api_key=GOOGLE_API_KEY,
        temperature=LLM_TEMPERATURE
    )


class FinancialAgents:
    """
    Collection of specialized financial analysis agents
    """
    
    def __init__(self):
        self.llm = create_gemini_llm()
    
    def portfolio_manager(self) -> Agent:
        """
        Portfolio Manager Agent - The orchestrator and planner
        Coordinates the overall investment analysis strategy
        """
        return Agent(
            role="Senior Portfolio Manager",
            goal="Orchestrate comprehensive investment analysis and coordinate team efforts to produce high-quality investment recommendations",
            backstory="""You are a seasoned Senior Portfolio Manager with 15 years of experience 
            in equity research and portfolio management. You excel at coordinating diverse teams 
            of analysts to produce thorough, well-researched investment reports. You understand 
            both quantitative metrics and qualitative factors that drive investment decisions.
            
            Your responsibility is to:
            - Define the scope and methodology of investment analysis
            - Coordinate parallel research efforts across your team
            - Ensure all critical aspects of investment analysis are covered
            - Set quality standards for the final investment recommendation""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            max_iter=3,
            memory=True
        )

    def quantitative_analyst(self) -> Agent:
        """
        Quantitative Analyst Agent - Financial data specialist
        Handles numerical analysis and financial metrics
        """
        return Agent(
            role="Senior Quantitative Analyst",
            goal="Conduct thorough quantitative analysis of financial metrics, stock performance, and technical indicators to assess investment attractiveness",
            backstory="""You are a highly skilled Quantitative Analyst with expertise in 
            financial modeling, statistical analysis, and technical analysis. You have a PhD 
            in Finance and 8 years of experience at top-tier investment firms.
            
            Your expertise includes:
            - Financial ratio analysis and valuation metrics
            - Technical indicator analysis and chart patterns
            - Statistical modeling and risk metrics calculation
            - Market performance comparison and benchmarking
            
            You provide precise, data-driven insights that form the quantitative foundation 
            of investment decisions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2,
            tools=[get_stock_data_tool, get_technical_indicators_tool]  
        )
    
    def market_intelligence_researcher(self) -> Agent:
        """
        Market Intelligence Researcher Agent - News and sentiment specialist
        Handles qualitative analysis and market sentiment
        """
        return Agent(
            role="Senior Market Intelligence Researcher",
            goal="Gather and analyze market news, sentiment, and qualitative factors that could impact investment performance",
            backstory="""You are an experienced Market Intelligence Researcher with a 
            background in journalism and financial analysis. You have 10 years of experience 
            tracking market trends, corporate developments, and macroeconomic factors.
            
            Your specialties include:
            - News analysis and sentiment assessment
            - Corporate event tracking and impact analysis
            - Market trend identification and interpretation
            - Qualitative risk factor assessment
            
            You excel at translating complex market dynamics and news flow into actionable 
            investment insights.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2,
            tools=[get_company_news_tool, get_market_news_tool]  # ← Fixed reference
        )
    
    def risk_assessment_specialist(self) -> Agent:
        """
        Risk Assessment Specialist Agent - Risk analysis expert
        Evaluates potential risks and downside scenarios
        """
        return Agent(
            role="Senior Risk Assessment Specialist",
            goal="Conduct comprehensive risk analysis by evaluating financial, market, and operational risks to provide balanced investment perspective",
            backstory="""You are a seasoned Risk Assessment Specialist with 12 years of 
            experience in investment risk management. You hold the FRM (Financial Risk Manager) 
            certification and have worked at both hedge funds and institutional investment firms.
            
            Your expertise covers:
            - Financial risk assessment (credit, liquidity, leverage)
            - Market risk analysis (volatility, correlation, beta)
            - Operational and business model risks
            - Regulatory and compliance risk evaluation
            
            You are known for your ability to identify potential pitfalls and provide 
            balanced, realistic risk assessments that help investors make informed decisions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2
        )
    
    def investment_report_writer(self) -> Agent:
        """
        Investment Report Writer Agent - Synthesis and documentation specialist
        Creates comprehensive, well-structured investment reports
        """
        return Agent(
            role="Senior Investment Report Writer",
            goal="Synthesize quantitative analysis, market intelligence, and risk assessment into a comprehensive, professional investment report",
            backstory="""You are an accomplished Investment Report Writer with a background 
            in financial journalism and equity research. You have 8 years of experience 
            writing research reports for institutional investors and have a talent for 
            translating complex financial analysis into clear, actionable recommendations.
            
            Your strengths include:
            - Clear, professional financial writing
            - Data synthesis and narrative construction
            - Investment thesis development
            - Executive summary creation
            
            You excel at taking diverse analytical inputs and weaving them into a coherent, 
            compelling investment narrative that helps decision-makers understand both 
            opportunities and risks.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2
        )
    
    def compliance_validator(self) -> Agent:
        """
        Compliance Validator Agent - Quality assurance and compliance specialist
        Ensures report accuracy, completeness, and regulatory compliance
        """
        return Agent(
            role="Senior Compliance Validator",
            goal="Review and validate investment reports for accuracy, completeness, and compliance with regulatory standards and firm policies",
            backstory="""You are a meticulous Compliance Validator with 10 years of experience 
            in financial services compliance and quality assurance. You hold Series 7, 66, 
            and 24 licenses and have deep knowledge of investment advisory regulations.
            
            Your responsibilities include:
            - Factual accuracy verification
            - Regulatory compliance review
            - Disclaimer and disclosure validation
            - Professional presentation standards
            
            You are known for your attention to detail and commitment to ensuring that all 
            investment communications meet the highest standards of accuracy and compliance.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2
        )

# Tool definitions 
@tool
def get_stock_data_tool(ticker: str, period: str = "1y") -> str:
    """Retrieve comprehensive stock data for analysis"""
    data = yahoo_finance_tools.get_stock_data(ticker, period)
    return str(data)

@tool 
def get_technical_indicators_tool(ticker: str, period: str = "3mo") -> str:
    """Calculate technical indicators for stock analysis"""
    data = yahoo_finance_tools.get_technical_indicators(ticker, period)
    return str(data)

@tool
def get_company_news_tool(company_name: str, ticker: str, days_back: int = 7) -> str:
    """Retrieve recent news about a company"""
    data = news_api_tools.get_company_news(company_name, ticker, days_back)
    return str(data)

@tool
def get_market_news_tool(category: str = "business", country: str = "us") -> str:
    """Retrieve general market news"""
    data = news_api_tools.get_market_news(category, country)
    return str(data)

# global instance
financial_agents = FinancialAgents()
