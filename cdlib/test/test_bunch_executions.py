import unittest
from cdlib import algorithms
from cdlib import ensemble
from cdlib import evaluation
import networkx as nx


class BunchExecTests(unittest.TestCase):

    def test_grid(self):
        g = nx.karate_club_graph()
        resolution = ensemble.Parameter(name="resolution", start=0.1, end=1, step=0.1)

        for communities in ensemble.grid_execution(graph=g, method=algorithms.louvain, parameters=[resolution]):
            self.assertIsInstance(communities.communities, list)

    def test_grid_search(self):
        g = nx.karate_club_graph()
        resolution = ensemble.Parameter(name="resolution", start=0.1, end=1, step=0.1)
        randomize = ensemble.BoolParameter(name="randomize")

        communities, scoring = ensemble.grid_search(graph=g, method=algorithms.louvain,
                                                    parameters=[resolution, randomize],
                                                    quality_score=evaluation.erdos_renyi_modularity,
                                                    aggregate=max)
        self.assertIsInstance(communities.communities, list)
        self.assertIsInstance(scoring, float)

    def test_random_search(self):
        g = nx.karate_club_graph()
        resolution = ensemble.Parameter(name="resolution", start=0.1, end=1, step=0.1)
        randomize = ensemble.BoolParameter(name="randomize")

        communities, scoring = ensemble.random_search(graph=g, method=algorithms.louvain,
                                                      parameters=[resolution, randomize],
                                                      quality_score=evaluation.erdos_renyi_modularity,
                                                      instances=5,
                                                      aggregate=max)
        self.assertIsInstance(communities.communities, list)
        self.assertIsInstance(scoring, float)

    def test_pool(self):
        g = nx.karate_club_graph()

        # Louvain
        resolution = ensemble.Parameter(name="resolution", start=0.1, end=1, step=0.1)
        randomize = ensemble.BoolParameter(name="randomize")
        louvain_conf = [resolution, randomize]

        # Angel
        threshold = ensemble.Parameter(name="threshold", start=0.1, end=1, step=0.1)
        angel_conf = [threshold]

        methods = [algorithms.louvain, algorithms.angel]

        for communities in ensemble.pool(g, methods, [louvain_conf, angel_conf]):
            self.assertIsInstance(communities.communities, list)

    def test_pool_filtered(self):
        g = nx.karate_club_graph()

        # Louvain
        resolution = ensemble.Parameter(name="resolution", start=0.1, end=1, step=0.1)
        randomize = ensemble.BoolParameter(name="randomize")
        louvain_conf = [resolution, randomize]

        # Angel
        threshold = ensemble.Parameter(name="threshold", start=0.1, end=1, step=0.1)
        angel_conf = [threshold]

        methods = [algorithms.louvain, algorithms.angel]

        for communities, scoring in \
                ensemble.pool_grid_filter(g, methods, [louvain_conf, angel_conf],
                                          quality_score=evaluation.erdos_renyi_modularity,
                                          aggregate=max):
            self.assertIsInstance(communities.communities, list)
            self.assertIsInstance(scoring, float)
