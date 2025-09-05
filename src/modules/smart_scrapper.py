from scrapegraphai.graphs import SmartScraperGraph
from src.utils.configs import graph_config


class SmartScraper:
    def __init__(self, source):
        self.smart_scraper_graph = SmartScraperGraph(
            prompt="This website lists mini gt diecast cars, find details on which cars are listed. Give Name and Price",
            source=source,
            config=graph_config,
        )

    def run(self):
        result = self.smart_scraper_graph.run()
        return result

    def get_execution_info(self):
        graph_exec_info = self.smart_scraper_graph.get_execution_info()
        return graph_exec_info
