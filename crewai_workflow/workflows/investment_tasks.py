"""
Investment Analysis Tasks for CrewAI Workflow
Task definitions for each agent in the investment analysis process
"""

from crewai import Task
from agents.financial_agents import financial_agents

class InvestmentAnalysisTasks:
    """
    Task definitions for comprehensive investment analysis workflow
    """
    
    def __init__(self):
        self.agents = financial_agents
    
    def plan_analysis_task(self, ticker: str, company_name: str) -> Task:
        """
        Task for Portfolio Manager to plan the analysis strategy
        """
        return Task(
            description=f"""
            As the Senior Portfolio Manager, develop a comprehensive analysis plan for {company_name} ({ticker}).
            
            Your task is to:
            1. Define the scope of analysis for {ticker}
            2. Set analysis parameters and timeframes
            3. Coordinate team assignments and priorities
            4. Establish success criteria for the investment evaluation
            
            Consider both quantitative metrics (financial ratios, technical indicators) and qualitative factors 
            (market sentiment, news flow, competitive position).
            
            Company: {company_name}
            Ticker: {ticker}
            """,
            agent=self.agents.portfolio_manager(),
            expected_output="""
            A structured analysis plan including:
            - Analysis scope and objectives
            - Key metrics to evaluate
            - Risk factors to assess
            - Timeline and methodology
            - Team coordination strategy
            """
        )
    
    def gather_financial_data_task(self, ticker: str, company_name: str) -> Task:
        """
        Task for Quantitative Analyst to gather and analyze financial data
        """
        return Task(
            description=f"""
            As the Senior Quantitative Analyst, conduct comprehensive quantitative analysis of {company_name} ({ticker}).
            
            Your task is to:
            1. Retrieve current stock data, financial metrics, and key ratios
            2. Calculate technical indicators and analyze price trends
            3. Assess valuation metrics (P/E, market cap, etc.)
            4. Evaluate financial performance and market position
            
            Use your available tools to gather accurate, up-to-date financial data and provide data-driven insights.
            
            Company: {company_name}
            Ticker: {ticker}
            """,
            agent=self.agents.quantitative_analyst(),
            async_execution=True,
            expected_output="""
            Comprehensive quantitative analysis including:
            - Current stock price and performance metrics
            - Key financial ratios (P/E, EPS, market cap)
            - Technical indicators (RSI, moving averages)
            - 52-week performance analysis
            - Valuation assessment and peer comparison insights
            """
        )
    
    def research_market_sentiment_task(self, ticker: str, company_name: str) -> Task:
        """
        Task for Market Intelligence Researcher to analyze news and sentiment
        """
        return Task(
            description=f"""
            As the Senior Market Intelligence Researcher, analyze market sentiment and news flow for {company_name} ({ticker}).
            
            Your task is to:
            1. Gather recent news articles and market developments
            2. Analyze overall market sentiment and investor mood
            3. Identify key events, announcements, or trends affecting the stock
            4. Assess qualitative factors that could impact investment performance
            
            Use your news research tools to provide comprehensive market intelligence.
            
            Company: {company_name}
            Ticker: {ticker}
            """,
            agent=self.agents.market_intelligence_researcher(),
            async_execution=True,
            expected_output="""
            Market intelligence report including:
            - Recent news summary and key developments
            - Overall market sentiment analysis
            - Positive and negative sentiment drivers
            - Key events or announcements affecting the stock
            - Qualitative risk and opportunity assessment
            """
        )
    
    def assess_investment_risks_task(self, ticker: str, company_name: str) -> Task:
        """
        Task for Risk Assessment Specialist to evaluate potential risks
        """
        return Task(
            description=f"""
            As the Senior Risk Assessment Specialist, conduct comprehensive risk analysis for {company_name} ({ticker}).
            
            Your task is to:
            1. Analyze the quantitative data and market intelligence gathered by your colleagues
            2. Identify financial, market, and operational risks
            3. Assess risk levels and potential impact on investment performance
            4. Provide balanced risk assessment with mitigation considerations
            
            Consider both the financial metrics and market sentiment data provided by the team.
            
            Company: {company_name}
            Ticker: {ticker}
            """,
            agent=self.agents.risk_assessment_specialist(),
            expected_output="""
            Comprehensive risk assessment including:
            - Financial risk evaluation (leverage, liquidity, profitability)
            - Market risk analysis (volatility, beta, sector risks)
            - Operational and business model risks
            - Overall risk rating and key risk factors
            - Risk mitigation recommendations
            """
        )
    
    def write_investment_report_task(self, ticker: str, company_name: str, current_date: str) -> Task:
        """
        Task for Investment Report Writer to synthesize analysis into report
        """
        return Task(
            description=f"""
            As the Senior Investment Report Writer, synthesize all analysis into a comprehensive investment report for {company_name} ({ticker}).
            The report must be dated for today: {current_date}.
            
            Your task is to:
            1. Combine quantitative analysis, market intelligence, and risk assessment
            2. Develop a clear investment thesis and recommendation
            3. Structure the report professionally with clear sections
            4. Provide actionable insights for investment decision-making
            
            Use all the analysis provided by your team members to create a cohesive, well-reasoned report.
            Important: Do not include any placeholder text like '[Your Firm Name]' or '[Your Name]'. The report should be clean and final.
            
            Company: {company_name}
            Ticker: {ticker}
            """,
            agent=self.agents.investment_report_writer(),
            expected_output="""
            Professional investment report in Markdown format including:
            - Executive Summary with clear recommendation
            - Quantitative Analysis section
            - Market Sentiment Analysis section  
            - Risk Assessment section
            - Investment Thesis and Rationale
            - Conclusion and Next Steps
            """
        )
    
    def validate_compliance_task(self, ticker: str, company_name: str, current_date: str) -> Task:
        """
        Task for Compliance Validator to review and finalize report
        """
        return Task(
            description=f"""
            As the Senior Compliance Validator, review and validate the investment report for {company_name} ({ticker}), dated {current_date}.
            
            Your task is to:
            1. Review the report for accuracy and completeness
            2. Ensure proper disclaimers and risk disclosures (without firm-specific placeholders)
            3. Validate professional formatting and presentation
            4. Confirm compliance with investment advisory standards
            
            Provide the final, validated investment report ready for client presentation.
            Important: Do not include any placeholder text like '[Your Firm Name]' or '[Your Name]'. Ensure the final output is a complete document.
            
            Company: {company_name}
            Ticker: {ticker}
            """,
            agent=self.agents.compliance_validator(),
            expected_output="""
            Final validated investment report including:
            - Reviewed and verified analysis
            - Proper disclaimers and disclosures
            - Professional formatting
            - Compliance certification
            - Investment recommendation summary
            """
        )

# global instance
investment_tasks = InvestmentAnalysisTasks()

