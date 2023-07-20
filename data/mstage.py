import pygraphviz as pgv

# Create a new directed graph
graph = pgv.AGraph(directed=True)

# Add nodes to the graph
graph.add_node("Literature Review")
graph.add_node("Implementation and Experiment Setup")
graph.add_node("Experiment Execution")
graph.add_node("Data analysis")
graph.add_node("Conclusion")

# Add edges between nodes
graph.add_edge("Literature Review", "Implementation and Experiment Setup")
graph.add_edge("Implementation and Experiment Setup", "Experiment Execution")
graph.add_edge("Experiment Execution", "Data analysis")
graph.add_edge("Data analysis", "Conclusion")


# Save the flowchart as an image
graph.draw("flowchart_method.png", prog="dot", format="png")