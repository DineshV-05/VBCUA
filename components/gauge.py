import plotly.graph_objects as go


def create_gauge(title, value):

    fig = go.Figure(
        go.Indicator(

            mode="gauge+number",

            value=value,

            number={
                "suffix": "%",
                "font": {"size": 38}
            },

            title={
                "text": f"<b>{title}</b>",
                "font": {"size": 22}
            },

            gauge={

                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1
                },

                "bar": {
                    "thickness": 0.35
                },

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "#ff4b4b"
                    },

                    {
                        "range": [40, 70],
                        "color": "#ffb703"
                    },

                    {
                        "range": [70, 100],
                        "color": "#2ecc71"
                    }

                ]

            }

        )
    )

    fig.update_layout(

        height=320,

        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20
        )

    )

    return fig