from dash import Dash, html, dcc, Input, Output, callback

DAYS_PER_YEAR = 365

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Loco Home Retrofit"),
        html.Div("Impact Calculator (running costs and carbon)"),
        html.H2("Running Costs"),
        dcc.Markdown(
            "Simple scenario assuming gas meter removed when heat pump installed"
        ),
        html.H3("Energy bill tariffs"),
        html.H4("Electricity"),
        html.Div(
            [
                "Cost per unit (£/kWh) ",
                dcc.Input(id="elec-unit-charge", value=0.25, type="number"),
            ]
        ),
        html.Div(
            [
                "Standing costs (£/day) ",
                dcc.Input(id="elec-stand-charge", value=0.63, type="number"),
            ]
        ),
        html.H4("Gas"),
        html.Div(
            [
                "Cost per unit (£/kWh) ",
                dcc.Input(id="gas-unit-charge", value=0.06, type="number"),
            ]
        ),
        html.Div(
            [
                "Standing costs (£/day) ",
                dcc.Input(id="gas-stand-charge", value=0.32, type="number"),
            ]
        ),
        html.Div(id="annual-gas-standing-charge"),
        html.Div(id="spark-gap"),
    ]
)


@callback(
    Output(component_id="annual-gas-standing-charge", component_property="children"),
    Input(component_id="gas-stand-charge", component_property="value"),
)
def gas_standing_charge(gas_charge):
    total_charge = DAYS_PER_YEAR * gas_charge
    return f"Annual standing charge (£/year): {total_charge:4.2f}"


@callback(
    Output(component_id="spark-gap", component_property="children"),
    Input(component_id="elec-unit-charge", component_property="value"),
    Input(component_id="gas-unit-charge", component_property="value"),
)
def spark_gap(elec_charge, gas_charge):
    return f"Ratio of electrical to gas unit rate ('spark gap'): {elec_charge/gas_charge: 4.2f}"


if __name__ == "__main__":
    app.run(debug=True)
