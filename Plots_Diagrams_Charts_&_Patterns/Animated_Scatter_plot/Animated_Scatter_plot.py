import plotly.express as px

data = px.data.gapminder()

fig = px.scatter(
    data,
    x="gdpPercap",
    y="lifeExp",
    animation_frame="year",
    animation_group="country",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=55,
    range_x=[100, 100000],
    range_y=[25, 90],
    title="Gapminder Data",
    labels={"gdpPercap": "GDP per Capita", "lifeExp": "Life Expectancy"},
    template="plotly_dark",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))
fig.update_layout(
    title_font=dict(size=24),
    xaxis_title_font=dict(size=18),
    yaxis_title_font=dict(size=18),
    legend_title_font=dict(size=18),
    font=dict(size=14),
)
fig.update_xaxes(title_standoff=25)
fig.update_yaxes(title_standoff=25)
fig.show()
fig.write_html("animated_scatter_plot.html")