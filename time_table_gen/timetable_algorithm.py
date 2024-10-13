import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from datetime import datetime
import itertools
import os

def timetable_algorithm(FILENAME):
    FILEPATH = os.path.join(os.getcwd(), 'uploads', FILENAME)

    student_data = pd.read_csv(FILEPATH)
    student_data = student_data.fillna(value=False)
    student_data.set_index("uid", inplace=True)
    courses = list(student_data.columns)
    class_network = nx.Graph()
    class_network.add_nodes_from(courses)

    without_subj = student_data.T
    
    list_of_overlaps = []
    name_list = without_subj.columns
    for student in name_list:
        list_of_overlaps.append(list(without_subj.loc[without_subj[student]].index))

    for sublist in list_of_overlaps:
        for pair in itertools.combinations(sublist, 2):
            class_network.add_edge(pair[0], pair[1])

    colors = ["lightcoral", "gray", "lightgray", "firebrick", "red", "chocolate", "darkorange", 
              "moccasin", "gold", "yellow", "darkolivegreen", "chartreuse", "forestgreen", 
              "lime", "mediumaquamarine", "turquoise", "teal", "cadetblue", "dodgerblue", 
              "blue", "slateblue", "blueviolet", "magenta", "lightsteelblue"]
    
    def greedy_coloring_algorithm(network, colors, colors_used):
        """Apply a greedy coloring algorithm to the class network.

        Assigns colors to nodes in the network such that no adjacent nodes share the same color.

        Args:
            network (nx.Graph): The class network graph.
            colors (list): A list of colors to be used for coloring the graph.
        """
        nodes = list(network.nodes())
        random.shuffle(nodes)
        for node in nodes:
            dict_neighbors = dict(network[node])
            nodes_neighbors = list(dict_neighbors.keys())

            forbidden_colors = []
            for neighbor in nodes_neighbors:
                if 'color' in network.nodes[neighbor]:  # Check if the 'color' attribute exists
                    forbidden_color = network.nodes[neighbor]['color']
                    forbidden_colors.append(forbidden_color)
            for color in colors:
                if color not in forbidden_colors:
                    network.nodes[node]['color'] = color
                    colors_used.add(color)
                    break
    
    colors_used = set()
    greedy_coloring_algorithm(class_network, colors, colors_used)
    max_rows = len(colors_used)

    dates = []
    calendar = {}
    for i in range(0, max_rows):
        date = datetime(2024, 5, i+1, 11, 0)
        dates.append(date)
        calendar[date] = []

    #Mapping colors to dates
    from_color_to_date = {col: dates[i] for i, col in enumerate(colors) if i < len(dates)}

    #Iterating each node(course) and node having same color will be assigned same date
    for v, data in class_network.nodes(data=True):
        color = data.get('color')
        if color in from_color_to_date:
            calendar[from_color_to_date[color]].append(v)

    # Ensure that rooms do not exceed the specified number
    # rooms = ["Room " + str(i) for i in range(num_rooms)]
    
    # Create a DataFrame to hold the timetable
    # if len(calendar) > 0:
    #     max_exams = len(max(list(calendar.values()), key=len))
    #     df = pd.DataFrame.from_dict(calendar, orient='index', columns=rooms[:max_exams])
    # else:
    #     df = pd.DataFrame(columns=rooms)

    df = pd.DataFrame.from_dict(calendar, orient="index")
    # Save to CSV
    timetable_csv_path = os.path.join(os.getcwd(), "uploads", "timetable.csv")
    df.to_csv(timetable_csv_path)
    return
    # # Generate class network image
    # plt.figure(figsize=(10, 8))
    # pos = nx.spring_layout(class_network)
    # nx.draw(class_network, pos, with_labels=True, node_color=[data['color'] for _, data in class_network.nodes(data=True)])
    # plt.title('Class Network Graph')
    # graph_image_path = 'class_network.png'
    # plt.savefig(graph_image_path)
    # plt.close()