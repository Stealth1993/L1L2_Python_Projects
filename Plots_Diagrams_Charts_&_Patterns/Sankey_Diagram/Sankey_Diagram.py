import plotly.graph_objects as go

labels = ["Source A", "Source B", "Source C", "Target A", "Target B", "Target C"]

sources = [0, 1, 0, 2, 3, 4, 5]
targets = [3, 4, 5, 3, 4, 5]
values = [10, 20, 30, 40, 50, 60]

# Create a Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
    ))])

# Update layout
fig.update_layout(title_text="Sankey Diagram Example", font_size=10)
fig.show()