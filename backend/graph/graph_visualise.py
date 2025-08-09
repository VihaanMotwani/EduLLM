from backend.graph.langgraph_agent import agent

img = agent.get_graph(xray=True).draw_mermaid_png()

# Save the image to a file
with open("agent.png", "wb") as f:
    f.write(img)