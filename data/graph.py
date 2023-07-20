import pygraphviz as pgv

# Create a new graph
graph = pgv.AGraph(directed=True)

# Add nodes
graph.add_node("Client")
graph.add_node("IDM Server")
graph.add_node("Database")

# Add edges
graph.add_edge("Client", "IDM Server", label="register()")
graph.add_edge("IDM Server", "Database", label="storeUser()")
graph.add_edge("Client", "IDM Server", label="authenticate()")
graph.add_edge("IDM Server", "Database", label="fetchUser()")
graph.add_edge("IDM Server", "Client", label="sendAuthResponse()")

# Set layout and properties
graph.layout(prog="dot")
graph.node_attr.update(color="lightblue2", style="filled")
graph.edge_attr.update(color="blue", arrowhead="vee")

# Save the diagram to a file
graph.draw("architecture_diagram.png")