def save_graph_image(graph, filename="graph.png"):
    img = graph.get_graph(xray=True).draw_mermaid_png()
    with open(filename, "wb") as f:
        f.write(img)