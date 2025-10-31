"""
Financial Market Data Tools
Yahoo Finance integration for stock data retrieval
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YahooFinanceTools:
    """
    Yahoo Finance data retrieval tools for quantitative analysis
    """
    
    def __init__(self):
        self.logger = logger
    
    def get_stock_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Fetch comprehensive stock data for analysis
        
        Args:
            ticker: Stock symbol (e.g., 'TSLA')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            Dict containing stock data and metrics
        """
        try:
            self.logger.info(f"Fetching stock data for {ticker}")
            
            # Create ticker object
            stock = yf.Ticker(ticker)
            
            # Get stock info
            info = stock.info
            
            # Get historical data
            history = stock.history(period=period)
            
            # Calculate additional metrics
            current_price = history['Close'].iloc[-1] if not history.empty else None
            price_change = history['Close'].iloc[-1] - history['Close'].iloc[-2] if len(history) > 1 else 0
            price_change_percent = (price_change / history['Close'].iloc[-2] * 100) if len(history) > 1 else 0
            
            # Organize data
            stock_data = {
                "ticker": ticker,
                "company_name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "current_price": round(current_price, 2) if current_price else None,
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "eps": info.get("trailingEps", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "52_week_high": round(history["High"].max(), 2) if not history.empty else None,
                "52_week_low": round(history["Low"].min(), 2) if not history.empty else None,
                "volume": history["Volume"].iloc[-1] if not history.empty else None,
                "avg_volume": round(history["Volume"].mean(), 0) if not history.empty else None,
                "beta": info.get("beta", "N/A"),
                "revenue": info.get("totalRevenue", "N/A"),
                "profit_margin": info.get("profitMargins", "N/A"),
                "data_retrieved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.logger.info(f"✅ Successfully retrieved data for {ticker}")
            return stock_data
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching data for {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "error": str(e),
                "data_retrieved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_technical_indicators(self, ticker: str, period: str = "3mo") -> Dict[str, Any]:
        """
        Calculate basic technical indicators
        
        Args:
            ticker: Stock symbol
            period: Time period for calculation
            
        Returns:
            Dict containing technical indicators
        """
        try:
            self.logger.info(f"Calculating technical indicators for {ticker}")
            
            stock = yf.Ticker(ticker)
            history = stock.history(period=period)
            
            if history.empty:
                return {"error": "No historical data available"}
            
            # Calculate moving averages
            history['MA_20'] = history['Close'].rolling(window=20).mean()
            history['MA_50'] = history['Close'].rolling(window=50).mean()
            
            # Calculate RSI (simplified)
            delta = history['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            current_price = history['Close'].iloc[-1]
            ma_20 = history['MA_20'].iloc[-1]
            ma_50 = history['MA_50'].iloc[-1]
            current_rsi = rsi.iloc[-1]
            
            indicators = {
                "ticker": ticker,
                "current_price": round(current_price, 2),
                "moving_average_20": round(ma_20, 2) if not pd.isna(ma_20) else None,
                "moving_average_50": round(ma_50, 2) if not pd.isna(ma_50) else None,
                "rsi_14": round(current_rsi, 2) if not pd.isna(current_rsi) else None,
                "price_vs_ma20": "Above" if current_price > ma_20 else "Below" if not pd.isna(ma_20) else "N/A",
                "price_vs_ma50": "Above" if current_price > ma_50 else "Below" if not pd.isna(ma_50) else "N/A",
                "rsi_signal": "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral" if not pd.isna(current_rsi) else "N/A",
                "calculated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.logger.info(f"✅ Technical indicators calculated for {ticker}")
            return indicators
            
        except Exception as e:
            self.logger.error(f"❌ Error calculating indicators for {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "error": str(e),
                "calculated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

# global instance
yahoo_finance_tools = YahooFinanceTools()