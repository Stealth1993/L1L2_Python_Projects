import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=450,
    title={"text": "Speed"},
    gauge={
        "axis": {"range": [0, 500]},
        "bar": {"color": "darkblue"},
        "bgcolor": "lightgray",
        "steps": [
            {"range": [0, 250], "color": "cyan"},
            {"range": [250, 400], "color": "lime"},
            {"range": [400, 500], "color": "orange"},
        ],
    }
))
fig.update_layout(
    title={"text": "Speed Gauge Chart", "x": 0.5, "xanchor": "center"},
    height=400,
    width=600,
    paper_bgcolor="white",
    font={"color": "black", "size": 16}
)
fig.show()