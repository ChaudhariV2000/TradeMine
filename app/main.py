from fastapi import FastAPI
from app.portfolio.portfolio_engine import PortfolioEngine
from app.repositories.decision_journal_repository import DecisionJournalRepository
from app.core.artifact import ResearchArtifact
from app.trading.trading_engine import TradingEngine
from app.collectors.market_collector import MarketCollector
from app.config.logging import logger
from app.services.strategy_analytics_service import StrategyAnalyticsService
from app.services.symbol_analytics_service import SymbolAnalyticsService
from app.config.settings import settings
from app.agents.technical_agent import TechnicalAgent
from app.services.watchlist_service import WatchlistService
from app.backtesting.backtester import Backtester
from app.strategy_manager.strategy_manager import StrategyManager
from app.backtesting.portfolio_backtester import PortfolioBacktester
from app.services.ranking_service import RankingService
from app.services.paper_trade_analytics import PaperTradeAnalytics
from app.agents.news_agent import NewsAgent
from app.agents.risk_agent import RiskAgent
from app.managers.agent_manager import AgentManager
from app.ml.dataset_builder import DatasetBuilder
from app.engine.research_engine import ResearchEngine
from app.services.position_sizing import PositionSizing
from app.strategy_manager.strategy_comparator import StrategyComparator
from app.reports.report_generator import ReportGenerator
from app.services.portfolio_service import PortfolioService
from app.repositories.settings_repository import SettingsRepository
from app.paper_trading.paper_trader import PaperTrader
from app.services.trading_service import TradingService
from app.portfolio.portfolio_manager import PortfolioManager

trading_service = TradingService()
watchlist = WatchlistService()


app = FastAPI(title=settings.APP_NAME)

from app.database.database import engine
from app.database.database import Base

Base.metadata.create_all(bind=engine)

collector = MarketCollector()
paper_trade_analytics = PaperTradeAnalytics()
decision_journal_repo = DecisionJournalRepository()
# technical_agent = TechnicalAgent()
backtester = Backtester()
strategy_manager = StrategyManager()
portfolio_backtester = PortfolioBacktester()
ranking_service = RankingService()
# news_agent = NewsAgent()
# risk_agent = RiskAgent()
strategy_analytics = StrategyAnalyticsService()
portfolio_manager = PortfolioManager()
agent_manager = AgentManager()
dataset_builder = DatasetBuilder()
research_engine = ResearchEngine()
position_sizing = PositionSizing()
strategy_comparator = StrategyComparator()
report_generator = ReportGenerator()
portfolio_service = PortfolioService()
paper_trader = PaperTrader()
settings_repo = SettingsRepository()
trading_engine = TradingEngine()
symbol_analytics = SymbolAnalyticsService()

@app.get("/")
def home():
    return {
        "status": "running",
        "application": settings.APP_NAME
    }


@app.get("/research/{symbol}")
def research(symbol: str, refresh: bool = False, capital: float = 100000,
    risk_percent: float = 1,):

    symbol = symbol.upper()

    # df = collector.collect(symbol)

    # collector.save(symbol, df)
    # df = collector.collect(
    # symbol.upper(),
    # refresh=refresh
    # )

    # artifact = ResearchArtifact(
    #     symbol=symbol,
    #     timeframe=settings.DEFAULT_PERIOD,
    #     market_data=df,
    # )
    artifact = research_engine.analyze(
        symbol.upper(),
        refresh=refresh,
    )

    df = artifact.market_data

    # artifact = technical_agent.analyze(artifact)
    # artifact = news_agent.analyze(artifact)
    # artifact = risk_agent.analyze(artifact)
    artifact = agent_manager.run(artifact)
    latest = df.iloc[-1]
    position = position_sizing.calculate(
        capital=capital,
        risk_percent=risk_percent,
        entry=artifact.metadata["entry_price"],
        stop_loss=artifact.metadata["stop_loss"],
    )

    return {
        "symbol": artifact.symbol,
        "timeframe": artifact.timeframe,

        "price": round(float(latest["close"]), 2),

        "technical_score": artifact.scores["technical"],

        "signal": artifact.metadata["signal"],

        "trend": artifact.metadata["trend"],

        "confidence": artifact.metadata["confidence"],

        "reasons": artifact.metadata["technical_reasons"],

        "indicators": {
            "ema20": round(float(latest["ema20"]), 2),
            "ema50": round(float(latest["ema50"]), 2),
            "ema200": round(float(latest["ema200"]), 2),
            "rsi": round(float(latest["rsi"]), 2),
            "macd": round(float(latest["macd"]), 2),
            "macd_signal": round(float(latest["macd_signal"]), 2),
            "adx": round(float(latest["adx"]), 2),
            "atr": round(float(latest["atr"]), 2),
        },
        "features": {
            "price_above_ema20": bool(latest["price_above_ema20"]),
            "price_above_ema50": bool(latest["price_above_ema50"]),
            "price_above_ema200": bool(latest["price_above_ema200"]),
            "rsi_overbought": bool(latest["rsi_overbought"]),
            "rsi_oversold": bool(latest["rsi_oversold"]),
            "macd_bullish": bool(latest["macd_bullish"]),
            "strong_trend": bool(latest["strong_trend"]),
            "high_volume": bool(latest["high_volume"]),
        },
        "news": {
            "score": artifact.scores["news"],
            "sentiment": artifact.metadata["news_sentiment"],
            "confidence": artifact.metadata["news_confidence"],
            "headlines": artifact.metadata["news_headlines"],
        },
        "risk": {
            "score": artifact.scores["risk"],
            "level": artifact.metadata["risk_level"],
            "volatility": artifact.metadata["volatility"],
        },
        "fundamentals": artifact.metadata["fundamental"],
        "fundamental_score": artifact.scores["fundamental"],
        "trade_plan": {
            "entry": artifact.metadata["entry_price"],
            "stop_loss": artifact.metadata["stop_loss"],
            "take_profit": artifact.metadata["take_profit"],
            "risk_reward": artifact.metadata["risk_reward"],
        },
        "position": {
            "capital": capital,
            "risk_percent": risk_percent,
            "shares": position["shares"],
            "investment": position["investment"],
        },
        "preferred_strategy":
        artifact.metadata["preferred_strategy"],

        "strategy_comparison":
        artifact.metadata["strategy_results"],
        "decision": artifact.metadata["decision"],

        "market": {
            "regime": artifact.metadata["market_regime"],
            "volatility": artifact.metadata["market_volatility"],
        },
        "committee": artifact.metadata["committee"],
       
    }
@app.get("/scan")
def scan():
    results = []

    for symbol in watchlist.get_symbols():
        try:
            artifact = research_engine.analyze(
                symbol,
                refresh=False,
            )

            latest = artifact.market_data.iloc[-1]
            decision = artifact.metadata["decision"]

            results.append({
                "symbol": symbol,
                "price": round(float(latest["close"]), 2),

                "recommendation": decision["recommendation"],
                "confidence": decision["confidence"],

                "technical_score": artifact.scores["technical"],
                "news_score": artifact.scores["news"],
                "risk_score": artifact.scores["risk"],
                "fundamental_score": artifact.scores["fundamental"],

                "signal": artifact.metadata["signal"],
                "trend": artifact.metadata["trend"],

                "preferred_strategy": artifact.metadata["preferred_strategy"],
                "market_regime": artifact.metadata["market_regime"],
                "market_volatility": artifact.metadata["market_volatility"],

                "risk_level": artifact.metadata["risk_level"],
                "news_sentiment": artifact.metadata["news_sentiment"],

                "overall_score": decision["confidence"],
            })

        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e),
            })

    results.sort(
        key=lambda x: x.get("overall_score", 0),
        reverse=True,
    )

    return results

@app.get("/dataset/{symbol}")
def dataset(symbol: str):

    df = collector.collect(symbol.upper())

    dataset = dataset_builder.build(df)

    return {
        "symbol": symbol.upper(),
        "rows": len(dataset),
        "columns": list(dataset.columns),
    }

@app.get("/compare-strategies/{symbol}")
def compare_strategies(
    symbol: str,
    refresh: bool = False,
):

    df = collector.collect(
        symbol.upper(),
        refresh=refresh,
    )

    return strategy_comparator.compare(df)

@app.get("/report/{symbol}")
def report(
    symbol: str,
    refresh: bool = False,
    capital: float = 100000,
    risk_percent: float = 1,
):
    symbol = symbol.upper()

    artifact = research_engine.analyze(
        symbol,
        refresh=refresh,
    )

    preferred_strategy = artifact.metadata["preferred_strategy"]

    backtest_result = backtester.run(
        artifact.market_data,
        strategy_name=preferred_strategy,
    )

    position = position_sizing.calculate(
        capital=capital,
        risk_percent=risk_percent,
        entry=artifact.metadata["entry_price"],
        stop_loss=artifact.metadata["stop_loss"],
    )

    report_path = report_generator.generate(
        artifact=artifact,
        backtest=backtest_result,
        position=position,
    )

    return {
        "symbol": symbol,
        "report": report_path,
    }

@app.get("/dataset/export/{symbol}")
def export_dataset(symbol: str):

    df = collector.collect(symbol.upper())

    dataset = dataset_builder.build(df)

    file = settings.DATA_DIR / f"{symbol}_dataset.csv"

    dataset.to_csv(file, index=False)

    return {
        "saved_to": str(file),
        "rows": len(dataset),
    }

@app.get("/backtest/{symbol}")
def backtest(
    symbol: str,
    refresh: bool = False,
    strategy: str = "EMA_MACD",
):

    df = collector.collect(
        symbol.upper(),
        refresh=refresh,
    )

    # result = backtester.run(df)
    result = backtester.run(df, strategy_name=strategy)

    return result
@app.get("/strategies")
def strategies():

    return {
        "available_strategies": strategy_manager.list()
    }
@app.get("/portfolio-backtest")
def portfolio_backtest():

    return portfolio_backtester.run()

# @app.get("/")
# def home():
#     return {"status": "running"}


@app.get("/download/{symbol}")
def download(symbol: str):

    df = collector.collect(symbol.upper())

    collector.save(symbol.upper(), df)

    return {
        "symbol": symbol.upper(),
        "rows": len(df),
        "columns": list(df.columns),
    }

@app.get("/agents")
def agents():

    return {
        "agents": agent_manager.list_agents()
    }

# @app.get("/portfolio")
# def portfolio(capital: float = 5000):
#     scan_results = scan()

#     return portfolio_service.build(
#         scan_results,
#         capital,
#     )

# @app.post("/paper-trade/open/{symbol}")
# def open_paper_trade(symbol: str):
#     symbol = symbol.upper()

#     artifact = research_engine.analyze(symbol)

#     s = settings_repo.get_settings()

#     position = position_sizing.calculate(
#         capital=s.monthly_budget,
#         risk_percent=1,
#         entry=artifact.metadata["entry_price"],
#         stop_loss=artifact.metadata["stop_loss"],
#     )
#     if position["shares"] <= 0:
#         return {
#             "symbol": symbol,
#             "status": "SKIPPED",
#             "reason": "Budget too small for this trade setup",
#             "monthly_budget": s.monthly_budget,
#         }

#     trade = paper_trader.open_trade({
#         "symbol": symbol,
#         "strategy": artifact.metadata["preferred_strategy"],
#         "entry_price": artifact.metadata["entry_price"],
#         "stop_loss": artifact.metadata["stop_loss"],
#         "target": artifact.metadata["take_profit"],
#         "shares": position["shares"],
#     })

#     return trade

@app.post("/paper-trade/open/{symbol}")
def open_paper_trade(symbol: str):
    return trading_service.execute_trade(symbol)
    # return trading_engine.execute_paper_trade(symbol)


@app.get("/paper-trades")
def paper_trades():
    return paper_trader.list_trades()

@app.post("/paper-trades/update")
def update_paper_trades():
    return paper_trader.update_open_trades()
@app.get("/settings")
def get_settings():
    s = settings_repo.get_settings()

    return {
        "monthly_budget": s.monthly_budget,
        "risk_profile": s.risk_profile,
        "max_positions": s.max_positions,
        "paper_trading": s.paper_trading,
    }


@app.post("/settings")
def update_settings(
    monthly_budget: float = 5000,
    risk_profile: str = "MODERATE",
    max_positions: int = 5,
    paper_trading: str = "ON",
):
    s = settings_repo.update_settings({
        "monthly_budget": monthly_budget,
        "risk_profile": risk_profile,
        "max_positions": max_positions,
        "paper_trading": paper_trading,
    })

    return {
        "monthly_budget": s.monthly_budget,
        "risk_profile": s.risk_profile,
        "max_positions": s.max_positions,
        "paper_trading": s.paper_trading,
    }
# @app.get("/technical/{symbol}")
# def technical(symbol: str):

#     df = collector.collect(symbol.upper())

#     collector.save(symbol.upper(), df)

#     artifact = ResearchArtifact(
#         symbol=symbol.upper(),
#         timeframe=settings.DEFAULT_PERIOD,
#         market_data=df,
#     )

#     artifact = technical_agent.analyze(artifact)

#     return {
#         "symbol": artifact.symbol,
#         "technical_score": artifact.scores["technical"],
#         "signal": artifact.metadata["signal"],
#         "trend": artifact.metadata["trend"],
#         "confidence": artifact.metadata["confidence"],
#         "reasons": artifact.metadata["technical_reasons"],
#     }

@app.post("/market/open-best-trades")
def open_best_trades():
    scan_results = scan()

    return trading_engine.open_best_paper_trades(
        scan_results
    )

# @app.get("/portfolio")
# def portfolio():

#     holdings = portfolio_manager.get_holdings()

#     return {
#         "cash": portfolio_manager.available_cash(),
#         "invested": portfolio_manager.total_invested(),
#         "holdings": [
#             {
#                 "symbol": h.symbol,
#                 "quantity": h.quantity,
#                 "average_price": h.average_price,
#                 "invested": h.invested,
#             }
#             for h in holdings
#         ],
#     }
@app.get("/portfolio")
def portfolio():
    return portfolio_service.current_portfolio()
@app.get("/decision-journal")
def decision_journal():
    rows = decision_journal_repo.all()

    return [
        {
            "id": r.id,
            "symbol": r.symbol,
            "recommendation": r.recommendation,
            "confidence": r.confidence,
            "technical_score": r.technical_score,
            "news_score": r.news_score,
            "risk_score": r.risk_score,
            "fundamental_score": r.fundamental_score,
            "market_regime": r.market_regime,
            "preferred_strategy": r.preferred_strategy,
            "executed": r.executed,
            "created_at": r.created_at,
        }
        for r in rows
    ]
@app.get("/test")
def test():
    engine = PortfolioEngine()

    # holdings = [
    #     {
    #         "symbol": "SBIN",
    #         "investment": 2500,
    #     },
    #     {
    #         "symbol": "ICICIBANK",
    #         "investment": 1500,
    #     },
    # ]

    # print(engine.portfolio_summary(holdings, 5000))
    # print(engine.has_position(holdings, "SBIN"))
    # print(engine.has_position(holdings, "TCS"))
    # print(
    #     engine.can_buy(
    #         symbol="SBIN",
    #         holdings=holdings,
    #         available_cash=2500,
    #         investment_required=1000,
    #     )
    # )
    # print(
    #     engine.can_buy(
    #         symbol="TCS",
    #         holdings=holdings,
    #         available_cash=500,
    #         investment_required=1000,
    #     )
    # )
    # print(
    #     engine.can_buy(
    #         symbol="TCS",
    #         holdings=holdings,
    #         available_cash=5000,
    #         investment_required=1000,
    #     )
    # )
#     holdings = [
#         {"symbol": "SBIN", "investment": 1000},
#         {"symbol": "TCS", "investment": 1000},
#         {"symbol": "INFY", "investment": 1000},
#         {"symbol": "ITC", "investment": 1000},
     
#     ]

    

#     print(engine.can_buy(
#     symbol="SBIN",
#     holdings=[],
#     available_cash=100000,
#     investment_required=50000,
#     capital=100000,
# ))
    from app.portfolio.portfolio_scorer import PortfolioScorer

    scorer = PortfolioScorer()

    print(
    scorer.score(
        duplicate_position=True,
        enough_cash=False,
        allocation_ok=False,
        positions_ok=False,
    )
)
@app.get("/paper-trades/summary")
def paper_trades_summary():
    return paper_trade_analytics.summary()

@app.get("/analytics/strategies")
def strategy_analytics_summary():
    return strategy_analytics.summary()

@app.get("/analytics/symbols")
def symbol_analytics_summary():
    return symbol_analytics.summary()
from app.services.trade_exit_service import TradeExitService
trade_exit_service = TradeExitService()
@app.post("/paper-trades/check-exits")
def check_paper_trade_exits():
    return trade_exit_service.check_exits()

from app.services.daily_scheduler_service import DailySchedulerService
daily_scheduler_service = DailySchedulerService()   
@app.post("/scheduler/run-daily")
def run_daily_scheduler():
    return daily_scheduler_service.run(scan)


from app.services.trade_cleanup_service import TradeCleanupService
trade_cleanup_service = TradeCleanupService()
@app.post("/paper-trades/cleanup")
def cleanup_paper_trades():
    return trade_cleanup_service.close_invalid_trades()

# @app.get("/daily-briefing")
# def daily_briefing():
#     return {
#         "portfolio": portfolio_service.current_portfolio(),
#         "paper_trading": paper_trade_analytics.summary(),
#         "strategy_analytics": strategy_analytics.summary(),
#         "symbol_analytics": symbol_analytics.summary(),
#     }

@app.get("/daily-briefing")
def daily_briefing():
    portfolio = portfolio_service.current_portfolio()
    paper_summary = paper_trade_analytics.summary()
    strategy_summary = strategy_analytics.summary()
    symbol_summary = symbol_analytics.summary()
    scan_results = scan()

    summary = portfolio["summary"]

    valid_scan = [
        s for s in scan_results
        if "error" not in s
    ]

    buy_candidates = [
        s for s in valid_scan
        if s.get("recommendation") in ["STRONG BUY", "BUY"]
    ]

    hold_candidates = [
        s for s in valid_scan
        if s.get("recommendation") == "HOLD"
    ]

    avoid_candidates = [
        s for s in valid_scan
        if s.get("recommendation") == "AVOID"
    ]

    best_opportunity = (
        valid_scan[0]
        if valid_scan
        else None
    )

    alerts = []

    for holding in portfolio["holdings"]:
        current_price = holding["current_price"]
        target = holding["target"]
        stop_loss = holding["stop_loss"]

        target_gap_percent = round(
            ((target - current_price) / current_price) * 100,
            2,
        )

        stop_gap_percent = round(
            ((current_price - stop_loss) / current_price) * 100,
            2,
        )

        if target_gap_percent <= 2:
            alerts.append({
                "symbol": holding["symbol"],
                "type": "TARGET_NEAR",
                "message": "Price is within 2% of target.",
                "current_price": current_price,
                "target": target,
            })

        if stop_gap_percent <= 2:
            alerts.append({
                "symbol": holding["symbol"],
                "type": "STOP_LOSS_NEAR",
                "message": "Price is within 2% of stop loss.",
                "current_price": current_price,
                "stop_loss": stop_loss,
            })

    if summary["positions"] == 0:
        recommendation = "No open positions. Run daily scheduler to find opportunities."

    elif alerts:
        recommendation = "Portfolio has active alerts. Review open positions."

    elif summary["cash"] > 0 and buy_candidates:
        recommendation = "Portfolio has cash available and new opportunities exist."

    elif summary["cash"] > 0:
        recommendation = "Portfolio has cash available, but no strong new opportunity currently."

    else:
        recommendation = "Portfolio is fully allocated. Monitor open trades and wait for exits."

    return {
        "recommendation": recommendation,
        "alerts": alerts,
        "market_status": {
            "stocks_scanned": len(valid_scan),
            "buy_candidates": len(buy_candidates),
            "hold_candidates": len(hold_candidates),
            "avoid_candidates": len(avoid_candidates),
            "best_opportunity": best_opportunity,
        },
        "portfolio": portfolio,
        "paper_trading": paper_summary,
        "strategy_analytics": strategy_summary,
        "symbol_analytics": symbol_summary,
    }

    # done

from app.services.trade_feedback_service import TradeFeedbackService
trade_feedback_service = TradeFeedbackService()
@app.get("/analytics/trade-feedback")
def trade_feedback_summary():
    return trade_feedback_service.summary()