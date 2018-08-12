from dash.dependencies import Input, Output, State
from constants import SparkStates, JobStates, OutputStatus, DashIds
from jobs import get_job_data
from utils import prettify_json, parse_json, LivyRequests
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


spark_states = SparkStates()
job_states = JobStates()
output_status = OutputStatus()
dash_ids = DashIds()

results = sessions = LivyRequests().kill_sessions()
print(results)

spark_info = LivyRequests().run_session()


app = dash.Dash()
server = app.server


app.layout = html.Div(
    [
        dcc.Interval(
            id=dash_ids.SPARK_INFO_INTERVAL,
            interval=5 * 1000,  # in milliseconds
            n_intervals=0,
        ),
        dcc.Interval(
            id=dash_ids.JOB_INFO_INTERVAL,
            interval=5 * 1000,
            n_intervals=0,  # in milliseconds
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id=dash_ids.MODIFIER_SELECT,
                            options=[{"label": i, "value": i} for i in range(1, 4)],
                            value=1,
                        )
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id=dash_ids.TRANSFORM_FUNC_SELECT,
                            options=[
                                {"label": "log", "value": "log"},
                                {"label": "sine", "value": "sin"},
                            ],
                            value="log",
                        )
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
            ]
        ),
        html.Button("RUN", id=dash_ids.RUN_BUTTON, n_clicks=0),
        dcc.Graph(id=dash_ids.CHART_1),
        html.Div(id=dash_ids.SPARK_SESSION_INFO, children=prettify_json(spark_info)),
        html.Div(
            id=dash_ids.CURRENT_STATEMENT_URL, children="", style={"display": "none"}
        ),
        html.Div(
            id=dash_ids.CURRENT_JOB_INFO,
            children=prettify_json({"state": job_states.NONE}),
        ),
    ]
)


@app.callback(
    Output(dash_ids.CURRENT_STATEMENT_URL, "children"),
    [Input(dash_ids.RUN_BUTTON, "n_clicks")],
    [
        State(dash_ids.SPARK_SESSION_INFO, "children"),
        State(dash_ids.MODIFIER_SELECT, "value"),
        State(dash_ids.TRANSFORM_FUNC_SELECT, "value"),
    ],
)
def run_job(n_clicks, session_info_text, modifier, transform_func):
    print("run_job")
    session_info = parse_json(session_info_text)
    if session_info["state"] != spark_states.IDLE:
        return ""

    job = get_job_data(modifier, transform_func)
    livy = LivyRequests()
    job_info = livy.run_job(session_info["session-url"], job)

    return job_info["statement-url"]


@app.callback(
    Output(dash_ids.CURRENT_JOB_INFO, "children"),
    [Input(dash_ids.JOB_INFO_INTERVAL, "n_intervals")],
    [State(dash_ids.CURRENT_STATEMENT_URL, "children")],
)
def update_job_info(n_intervals, statement_url):
    print("update_job_info")
    if "http" not in statement_url:
        return prettify_json({"state": None})

    livy = LivyRequests()
    job_info = livy.job_info(statement_url)
    return prettify_json(job_info)


@app.callback(
    Output(dash_ids.CHART_1, "figure"), [Input(dash_ids.CURRENT_JOB_INFO, "children")]
)
def visualize_job(job_info_text):
    print("visualize_job")
    job_info = parse_json(job_info_text)
    if job_info["state"] == job_states.AVAILABLE:
        output = job_info["output"]
        if output["status"] == output_status.OK:
            data = output["data"]
            payload = parse_json(data["text/plain"])
            x = payload["x"]
            y = payload["y"]
        else:
            x = []
            y = []
    else:
        x = []
        y = []

    return {
        "data": [
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker={
                    "size": 15,
                    "opacity": 0.5,
                    "line": {"width": 0.5, "color": "white"},
                },
            )
        ],
        "layout": go.Layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        ),
    }


@app.callback(
    Output(dash_ids.SPARK_SESSION_INFO, "children"),
    [Input(dash_ids.SPARK_INFO_INTERVAL, "n_intervals")],
    [State(dash_ids.SPARK_SESSION_INFO, "children")],
)
def update_spark_info(n, spark_info_text):
    spark_info = parse_json(spark_info_text)
    livy = LivyRequests()
    if "session-url" not in spark_info.keys():
        print(spark_info)
        return prettify_json(spark_info)

    spark_info = livy.session_info(spark_info["session-url"])
    return prettify_json(spark_info)


if __name__ == "__main__":
    app.run_server()
