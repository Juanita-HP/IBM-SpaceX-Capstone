import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


# Load SpaceX dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# Create Dash application
app = dash.Dash(__name__)


# ---------------------------------------------------
# Layout
# ---------------------------------------------------

app.layout = html.Div([

    html.H1(
        "SpaceX Launch Records Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "font-size": 40
        }
    ),

    # TASK 1 - Launch Site Dropdown
    dcc.Dropdown(
        id="site-dropdown",

        options=[
            {"label": "All Sites", "value": "ALL"}
        ] + [
            {"label": site, "value": site}
            for site in spacex_df["Launch Site"].unique()
        ],

        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    html.Div(
        dcc.Graph(id="success-pie-chart")
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3 - Payload Slider
    dcc.RangeSlider(
        id="payload-slider",
        min=0,
        max=10000,
        step=1000,

        marks={
            0: "0",
            1000: "1000",
            2000: "2000",
            3000: "3000",
            4000: "4000",
            5000: "5000",
            6000: "6000",
            7000: "7000",
            8000: "8000",
            9000: "9000",
            10000: "10000"
        },

        value=[min_payload, max_payload]
    ),

    html.Br(),

    # Scatter chart
    html.Div(
        dcc.Graph(id="success-payload-scatter-chart")
    )
])


# ---------------------------------------------------
# TASK 2 - Pie Chart Callback
# ---------------------------------------------------

@app.callback(
    Output(
        component_id="success-pie-chart",
        component_property="figure"
    ),
    Input(
        component_id="site-dropdown",
        component_property="value"
    )
)
def get_pie_chart(entered_site):

    if entered_site == "ALL":

        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Successful Launches by Site"
        )

        return fig

    else:

        filtered_df = spacex_df[
            spacex_df["Launch Site"] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names="class",
            title=f"Launch Outcomes for {entered_site}"
        )

        return fig


# ---------------------------------------------------
# TASK 4 - Scatter Plot Callback
# ---------------------------------------------------

@app.callback(
    Output(
        component_id="success-payload-scatter-chart",
        component_property="figure"
    ),
    [
        Input(
            component_id="site-dropdown",
            component_property="value"
        ),

        Input(
            component_id="payload-slider",
            component_property="value"
        )
    ]
)
def get_payload_chart(entered_site, payload_range):

    low_payload = payload_range[0]
    high_payload = payload_range[1]

    filtered_payload = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low_payload)
        &
        (spacex_df["Payload Mass (kg)"] <= high_payload)
    ]

    if entered_site == "ALL":

        fig = px.scatter(
            filtered_payload,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Payload vs Launch Outcome for All Sites"
        )

        return fig

    else:

        filtered_site = filtered_payload[
            filtered_payload["Launch Site"] == entered_site
        ]

        fig = px.scatter(
            filtered_site,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Payload vs Launch Outcome for {entered_site}"
        )

        return fig


# ---------------------------------------------------
# Run application
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=True
    )