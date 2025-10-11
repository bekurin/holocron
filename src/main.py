from agent.trade_information_collector import tradeInformationCollectorAgent
from agent.rss_collector import RssCollectorAgent

if __name__ == "__main__":
    tradeInformationCollectorAgent = tradeInformationCollectorAgent()
    rssCollectorAgent = RssCollectorAgent()

    kospi100_list = tradeInformationCollectorAgent.run()

    for item in kospi100_list:
        today_news = rssCollectorAgent.run(company_name=item.name)
        if (len(today_news) == 0):
            continue

        print(f"{item.name}의 오늘 기사 검색")
        for news in today_news:
            print(news)
        print("\n\n")
