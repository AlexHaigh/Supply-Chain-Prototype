import plotly.graph_objects as go
import networkx as nx
import random

n = 100
weight_range = [1, 2, 3, 4, 5]
G = nx.random_geometric_graph(n, 0.2)

node_structure_hover = {

    # Add the scores together
    'sov_design': random.choices(weight_range, k=n),

    #
    'sov_build': random.choices(weight_range, k=n),

    # this could be anything for source e.g. source materials
    'sov_source': random.choices(weight_range, k=n),

    # This is anything required for maintaining product - i.e. anything that supports function
    'sov_support': random.choices(weight_range, k=n),

    # Funding expiry - we could filter to check where is at risk
    'Out_of_service': 'date'
}

# total risk score
node_structure_hover['sov_total'] = [node_structure_hover['sov_design'][i] +
                                     node_structure_hover['sov_source'][i] +
                                     node_structure_hover['sov_build'][i] +
                                     node_structure_hover['sov_support'][i]
                                     for i in range(0, n)]

nx.set_node_attributes(G, node_structure_hover['sov_design'], "sov_design")

print(node_structure_hover)
"""
## do we want to long term create several instances of the same object
## these instances will have different values
## Same data model for the device

inventory = {
    'devices':  { 'devicea':{ instance
    }, deviceb},

}
}"""

link_structure_hover = {
    # objects to class only
    # we should be able to filter these out - or colour them
    'Confidence': "High - Medium - Low - NA",
}

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    hovertext=[node_structure_hover['sov_design'],
               node_structure_hover['sov_build'],
               node_structure_hover['sov_source'],
               node_structure_hover['sov_support']],
    marker=dict(
        showscale=True,
        # colorscale options
        # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='rdylgn',
        reversescale=True,
        # colour by the sum of the sov scores (l-m-h)
        # 0-8 or less - low risk (green)
        # 8-12 med (yellow)
        # 12+ high risk (red)
        color=[],
        size=15,
        colorbar=dict(
            thickness=15,
            title=dict(
                text='Total Risk Score',
                side='right'
            ),
            xanchor='left',
        ),

        line_width=2))
node_adjacencies = []

node_text = ['sov_design: ' + str(node_structure_hover['sov_design'][i]) + "\n" +
             'sov_source: ' + str(node_structure_hover['sov_source'][i]) + "\n" +
             'sov_build:' + str(node_structure_hover['sov_build'][i]) + "\n" +
             'sov_support: ' + str(node_structure_hover['sov_support'][i]) for i in range(0, n)]

node_trace.marker.color = node_structure_hover['sov_total']
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(
                        text="<br>Network graph made with Python",
                        font=dict(
                            size=16
                        )
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Python code: <a href='https://plotly.com/python/network-graphs/'> https://plotly.com/python/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

"""fig.update_traces(
    hovertemplate="<br>".join([
        "ColX: %{x}",
        "ColY: %{y}",
        "Col1: %{customdata[0]}",
        "Col2: %{customdata[1]}",
        "Col3: %{customdata[2]}",
    ])
)
"""

fig.show()