import plotly.graph_objects as go

fig = go.Figure(go.Waterfall(
    name="Waterfall Chart",
    orientation="v",
    measure=["relative", "relative", "total", "relative", "total"],
    x=["Start", "Increase", "Total", "Decrease", "End"],
    y=[100, 50, 150, -30, 120],
    textposition="outside",
    text=["", "+50", "", "-30", ""],
    connector={"line": {"color": "gray"}},
    increasing={"marker": {"color": "green"}},
    decreasing={"marker": {"color": "red"}},
    totals={"marker": {"color": "blue"}}
))
fig.write_html("waterfall_chart.html")  # To save and open manually when in python
fig.show()  # Display the chart