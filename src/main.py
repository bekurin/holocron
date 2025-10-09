from agent.trade_information_collector import TradeInformationCollectorAgent

if __name__ == "__main__":
    agent = TradeInformationCollectorAgent()
    kospi100_list = agent.run()

    if kospi100_list:
        for item in kospi100_list:
            print(item)
