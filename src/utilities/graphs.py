"""
Different helper methods to work with graphs, based on networkx
"""
import re

import networkx as nx
from networkx.classes.multidigraph import MultiDiGraph
from networkx.drawing.nx_agraph import read_dot, write_dot, graphviz_layout

import matplotlib.pyplot as plt

PATTERN = re.compile("^\(.*\)$")

"""
    Convert weights from string to float.
    If not done this will cause errors in the further process
"""
def convertWeigthsToFloat(graph: MultiDiGraph) -> MultiDiGraph:
    for u,v,d in graph.edges(data=True):
        if "weight" in d:
            d['weight'] = float(d['weight'])
    return graph


def drawDiffernce(g1: MultiDiGraph, g2: MultiDiGraph, pos: dict, labels: dict = None, color_map = [None, None], shift: int = 20) -> None:
    plt.figure(figsize=(20, 10))
    pos_shifted = {}
    for k,v in pos.items():
        pos_shifted[k] = (v[0] + shift, v[1])

    if labels is not None:
        l1 = dict((k, labels[k]) for k in list(g1.nodes())[1:])
        l2 = dict((k, labels[k]) for k in list(g2.nodes())[1:])
        l2 = dict(l2.items() - l1.items()) 

        nx.draw_networkx_labels(g1, pos, l1, font_size=8)
        nx.draw_networkx_labels(g2, pos_shifted, l2, font_size=8)

    nx.draw(g1, pos, with_labels=False, arrows=True, node_color=(color_map[0] or 'red'))
    nx.draw(g2, pos_shifted, with_labels=False, arrows=True, node_color=(color_map[1] or'blue'))
    plt.show()



def loadGraphFromDot(path: str) -> MultiDiGraph:
    return convertWeigthsToFloat(read_dot(path))


def printNodes(g: MultiDiGraph) -> None:
    for node in g.nodes(data=True):
        labels = node[1]["label"].split("\\n")
        try:
            if PATTERN.match(labels[1]):
                print(node[0], "-".join(labels[0:3]))
            else:
                print(node[0], "-".join(labels[0:2]))
        except IndexError:
            print(f"ERROR: {labels}")


def getNodeNameMapping(g: MultiDiGraph) -> dict[str, str]:
    mapping = {}
    for node in g.nodes(data=True):
        labels = node[1]["label"].split("\\n")
        try:
            if PATTERN.match(labels[1]):
                mapping[node[0]] = "-".join(labels[0:3])
            else:
                mapping[node[0]] = "-".join(labels[0:2])
        except IndexError:
            print(f"ERROR: {labels}")
    return mapping


def generateUniqueNodeMapping(graphs: list[MultiDiGraph]) -> dict[str, str]:
    nameMapping = {}
    nodecount = 1

    for g in graphs:
        mapping = getNodeNameMapping(g)
        for key in mapping:
            if mapping[key] not in nameMapping:
                nameMapping[mapping[key]] = f"N{nodecount}"
                nodecount += 1

    return nameMapping


def recalculate_percentages_based_on_seconds(graph):
    # extract seconds x.xxs using regex
    REGEX_RUNTIME = re.compile(r"(\d+(\.\d+)?)[s| ]")

    total_time = 0
    for node in graph.nodes(data=True):
        try:
            seconds = REGEX_RUNTIME.findall(node[1]['label'])[0][0]
            total_time += float(seconds)
        except AttributeError:
            print(f"There was an error extracting seconds from {node[1]['label']}")
            continue

    # recalculate percentages
    for node in graph.nodes(data=True):
        try:
            seconds = REGEX_RUNTIME.findall(node[1]['label'])[0][0]
        except AttributeError:
            print(f"There was an error extracting seconds from {node[1]['label']}")
            continue

        # calculate percentage of total time
        percentage = float(seconds) / total_time * 100
        node[1]['totalPerc'] = percentage


# check if first graph overlaps graph 2 sufficeintly
def calculate_overlap_value(graph1, graph2):

    # Calculate percentages based on total seconds of reduced graph
    recalculate_percentages_based_on_seconds(graph1)
    recalculate_percentages_based_on_seconds(graph2)

    perc = 0
    for node in graph2.nodes(data=True):
        if node[0] in graph1.nodes():
            # print(f"Found {node[1]['label']} with {node[1]['totalPerc']}")
            perc += node[1]['totalPerc']
    return perc / 100