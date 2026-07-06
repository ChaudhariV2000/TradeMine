from pathlib import Path


class ReportGenerator:

    def generate(
        self,
        artifact,
        backtest,
        position,
    ):

        reports = Path("reports")
        reports.mkdir(exist_ok=True)

        file = reports / f"{artifact.symbol}_report.txt"

        with open(file, "w", encoding="utf-8") as f:

            f.write("=" * 60 + "\n")
            f.write("TRADEMINE AI RESEARCH REPORT\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Symbol : {artifact.symbol}\n")
            f.write(f"Recommendation : {artifact.metadata['decision']['recommendation']}\n")
            f.write(f"Confidence : {artifact.metadata['decision']['confidence']}%\n")
            f.write(f"Preferred Strategy : {artifact.metadata['preferred_strategy']}\n\n")

            f.write("Technical Reasons\n")

            for reason in artifact.metadata["technical_reasons"]:
                f.write(f" - {reason}\n")

            f.write("\n")

            f.write(f"News : {artifact.metadata['news_sentiment']}\n")
            f.write(f"Risk : {artifact.metadata['risk_level']}\n")

            f.write("\nTrade Plan\n")

            f.write(f"Entry : {artifact.metadata['entry_price']}\n")
            f.write(f"Stop Loss : {artifact.metadata['stop_loss']}\n")
            f.write(f"Target : {artifact.metadata['take_profit']}\n")
            f.write(f"Risk Reward : {artifact.metadata['risk_reward']}\n")

            f.write("\nPosition Size\n")

            f.write(f"Shares : {position['shares']}\n")
            f.write(f"Investment : {position['investment']}\n")

            f.write("\nBacktest\n")

            f.write(f"Return : {backtest['return_percent']}%\n")
            f.write(f"Win Rate : {backtest['win_rate']}%\n")
            f.write(f"Max Drawdown : {backtest['max_drawdown']}%\n")

        return str(file)