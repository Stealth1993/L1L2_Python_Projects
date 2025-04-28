import plotly.graph_objects as go

stages = ['A', 'B', 'C', 'D']
values = [100, 80, 60, 40]

fig = go.Figure(go.Funnel(
    name = "Funnel Chart",
    y = stages,
    x = values,
    textinfo = "value+percent initial"
))
fig.update_layout(title_text='Funnel Chart Example', title_x=0.5)       
fig.show()