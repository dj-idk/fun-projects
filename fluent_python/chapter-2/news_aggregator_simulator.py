import asyncio
import random
import time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class NewsItem:
    def __init__(self, headline, source, is_breaking=False):
        self.headline = headline
        self.source = source
        self.is_breaking = is_breaking
        self.timestamp = datetime.now()

    def __str__(self):
        prefix = (
            f"{Fore.RED}[BREAKING NEWS]"
            if self.is_breaking
            else f"{Fore.BLUE}[{self.source.upper()}]"
        )
        return f"{prefix} {Style.BRIGHT}{self.headline}{Style.RESET_ALL}"


TECH_TOPICS = [
    "AI",
    "Blockchain",
    "Cloud Computing",
    "5G",
    "Quantum Computing",
    "IoT",
    "Cybersecurity",
]
TECH_COMPANIES = ["Google", "Apple", "Microsoft", "Amazon", "Tesla", "Meta", "Netflix"]
TECH_ACTIONS = [
    "announces",
    "launches",
    "reveals",
    "develops",
    "acquires",
    "partners with",
    "invests in",
]

SPORTS_TEAMS = [
    "Lakers",
    "Real Madrid",
    "Yankees",
    "Patriots",
    "Manchester United",
    "Warriors",
    "Chiefs",
]
SPORTS_EVENTS = ["championship", "tournament", "match", "game", "series", "competition"]
SPORTS_ACTIONS = [
    "wins",
    "loses",
    "dominates",
    "struggles in",
    "celebrates",
    "prepares for",
]

POLITICS_FIGURES = [
    "President",
    "Senator",
    "Prime Minister",
    "Governor",
    "Mayor",
    "Diplomat",
]
POLITICS_TOPICS = [
    "election",
    "policy",
    "legislation",
    "scandal",
    "debate",
    "summit",
    "agreement",
]
POLITICS_ACTIONS = [
    "announces",
    "criticizes",
    "supports",
    "opposes",
    "discusses",
    "signs",
    "vetoes",
]

BREAKING_PREFIXES = ["Urgent", "Just in", "Developing", "Alert", "Exclusive"]
BREAKING_EVENTS = [
    "major breakthrough",
    "unexpected discovery",
    "crisis",
    "emergency situation",
    "surprising announcement",
    "critical update",
    "historic decision",
]


async def tech_news_producer(queue, breaking_queue):
    """Produces technology news items"""
    while True:
        is_breaking = random.random() < 0.1

        if is_breaking:
            prefix = random.choice(BREAKING_PREFIXES)
            company = random.choice(TECH_COMPANIES)
            topic = random.choice(TECH_TOPICS)
            headline = f"{prefix}: {company} announces revolutionary {topic} technology that changes everything"
            news = NewsItem(headline, "Tech News", is_breaking=True)
            await breaking_queue.put(news)
        else:
            company = random.choice(TECH_COMPANIES)
            action = random.choice(TECH_ACTIONS)
            topic = random.choice(TECH_TOPICS)
            headline = f"{company} {action} new {topic} solution"
            news = NewsItem(headline, "Tech News")
            await queue.put(news)

        await asyncio.sleep(random.uniform(2, 8))


async def sports_news_producer(queue, breaking_queue):
    """Produces sports news items"""
    while True:
        is_breaking = random.random() < 0.05

        if is_breaking:
            prefix = random.choice(BREAKING_PREFIXES)
            team = random.choice(SPORTS_TEAMS)
            event = random.choice(SPORTS_EVENTS)
            headline = (
                f"{prefix}: {team} makes shocking comeback in championship {event}"
            )
            news = NewsItem(headline, "Sports", is_breaking=True)
            await breaking_queue.put(news)
        else:
            team = random.choice(SPORTS_TEAMS)
            action = random.choice(SPORTS_ACTIONS)
            event = random.choice(SPORTS_EVENTS)
            headline = f"{team} {action} the {event} against all odds"
            news = NewsItem(headline, "Sports")
            await queue.put(news)

        await asyncio.sleep(random.uniform(3, 10))


async def politics_news_producer(queue, breaking_queue):
    """Produces political news items"""
    while True:
        is_breaking = random.random() < 0.15

        if is_breaking:
            prefix = random.choice(BREAKING_PREFIXES)
            figure = random.choice(POLITICS_FIGURES)
            event = random.choice(BREAKING_EVENTS)
            headline = f"{prefix}: {figure} involved in {event}"
            news = NewsItem(headline, "Politics", is_breaking=True)
            await breaking_queue.put(news)
        else:
            figure = random.choice(POLITICS_FIGURES)
            action = random.choice(POLITICS_ACTIONS)
            topic = random.choice(POLITICS_TOPICS)
            headline = f"{figure} {action} controversial {topic}"
            news = NewsItem(headline, "Politics")
            await queue.put(news)

        await asyncio.sleep(random.uniform(4, 12))


async def news_consumer(queue, breaking_queue, consumer_id):
    """Consumes and processes news items"""
    processed_count = 0
    breaking_count = 0

    while True:
        try:
            news = breaking_queue.get_nowait()
            breaking_count += 1
            print(f"{Fore.YELLOW}Consumer {consumer_id} processing: {news}")
            breaking_queue.task_done()

            await asyncio.sleep(random.uniform(1, 2))
        except asyncio.QueueEmpty:
            try:
                news = await asyncio.wait_for(queue.get(), timeout=1)
                processed_count += 1
                print(f"{Fore.GREEN}Consumer {consumer_id} processing: {news}")
                queue.task_done()

                await asyncio.sleep(random.uniform(0.5, 1))
            except asyncio.TimeoutError:
                await asyncio.sleep(0.5)

        if (processed_count + breaking_count) % 5 == 0 and (
            processed_count + breaking_count
        ) > 0:
            print(
                f"{Fore.CYAN}Consumer {consumer_id} stats: Processed {processed_count} regular and {breaking_count} breaking news items"
            )


async def main():
    try:
        duration = int(input("How many seconds to run the simulation? "))
        num_consumers = int(input("How many news processors to run? "))
    except ValueError:
        print("Invalid input. Using default values.")
        duration = 60
        num_consumers = 2

    print(
        f"\n{Fore.CYAN}Starting News Aggregator Simulation for {duration} seconds with {num_consumers} processors..."
    )
    print(f"{Fore.CYAN}Press Ctrl+C to stop early.\n")

    news_queue = asyncio.Queue()
    breaking_news_queue = asyncio.Queue()

    tasks = []

    tasks.append(
        asyncio.create_task(tech_news_producer(news_queue, breaking_news_queue))
    )
    tasks.append(
        asyncio.create_task(sports_news_producer(news_queue, breaking_news_queue))
    )
    tasks.append(
        asyncio.create_task(politics_news_producer(news_queue, breaking_news_queue))
    )

    for i in range(num_consumers):
        tasks.append(
            asyncio.create_task(news_consumer(news_queue, breaking_news_queue, i + 1))
        )

    try:
        await asyncio.sleep(duration)
    except asyncio.CancelledError:
        pass
    finally:
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        print(f"\n{Fore.CYAN}Simulation complete!")
        print(f"{Fore.CYAN}Regular news queue size: {news_queue.qsize()}")
        print(f"{Fore.CYAN}Breaking news queue size: {breaking_news_queue.qsize()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
