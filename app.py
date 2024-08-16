import os

from dash import Dash, html
import dash_bootstrap_components as dbc
from impact import calculate_impact
import config

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP
                                 ]) 

server = app.server

button = dbc.Button(
    [
        'Calculate', 
        dbc.Badge("", color='light', text_color='primary', className='ms-1')
    ], 
    color='primary', 
    id='save-button'
)


gas_costs = dbc.Row(
    [
    dbc.Label('Gas', width='auto'), 
    dbc.Col(
        dbc.InputGroup(
                [
                    dbc.InputGroupText("Unit cost"),
                    dbc.Input(type="number", 
                             id='gas-unit-charge', 
                             min=0.01, 
                             max=1.00, 
                             step=0.01, 
                             value=0.06),
                    dbc.InputGroupText("£/kWh"),
                ],
                className="mb-3",
            )
        ),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupText("Standing charge"), 
                dbc.Input(value=0.32, 
                          type="number", 
                          id='gas-stand-charge', 
                          min=0.01, 
                          max=1.00, 
                          step=0.01),
                dbc.InputGroupText("£/day"),
            ],
            className="mb-3",
        )
    ),
    ])
elec_costs = dbc.Row(
    [
    dbc.Label('Electricity', width='auto'), 
    dbc.Col(
        dbc.InputGroup(
                [
                    dbc.InputGroupText("Unit cost"),
                    dbc.Input(type="number", 
                             id='elec-unit-charge', 
                             min=0.01, 
                             max=1.00, 
                             step=0.01, 
                             value=0.25),
                    dbc.InputGroupText("£/kWh"),
                ],
                className="mb-3",
            )
        ),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupText("Standing charge"), 
                dbc.Input(value=0.63, 
                          type="number", 
                          id='elec-stand-charge', 
                          min=0.01, 
                          max=1.00, 
                          step=0.01),
                dbc.InputGroupText("£/day"),
            ],
            className="mb-3",
        )
    ),
    ])

hardware_spec = dbc.Row(
    [
    dbc.Label('Heating system efficiency', width='auto'), 

    dbc.Col(
        dbc.InputGroup(
                [
                    dbc.InputGroupText("Gas boiler"), 
                    dbc.Input(type="number", 
                             id='boiler-efficiency', 
                             min=0, 
                             max=100, 
                             step=1, 
                             value=80),
                    dbc.InputGroupText("%"),
                ],
                className="mb-3",
            )
        ),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupText("Heat pump"), 
                dbc.Input(value=3, 
                          type="number", 
                          id='modelled-scop', 
                          min=0.5, 
                          max=5, 
                          step=0.1),
                dbc.InputGroupText("SCOP"),
            ],
            className="mb-3",
        )
    ),
    ])

gas_consumption = dbc.Row(
    [
    dbc.Label('Gas consumption', width='auto'), 

    dbc.Col(
        dbc.InputGroup(
                [
                    dbc.InputGroupText("Heating"), 
                    dbc.Input(type="number", 
                             id='gas-heat-consumption', 
                             min=1, 
                             max=100000, 
                             step=10, 
                             value=11500),
                    dbc.InputGroupText("kWh/year"),
                ],
                className="mb-3",
            )
        ),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupText("Cooking"), 
                dbc.Input(value=3, 
                          type="number", 
                          id='gas-cook-consumption', 
                          min=1, 
                          max=1000, 
                          step=1),
                dbc.InputGroupText("kWh/year"),
            ],
            className="mb-3",
        )
    ),
])



app.layout = dbc.Container(
    [
        html.H1("Loco Home Retrofit - impact Calculator"),
        html.H2("User inputs"),
        elec_costs, 
        gas_costs,
        hardware_spec,
        gas_consumption, 
        button, 
        html.H2('Cost impact'), 

        html.P(["Annual gas standing charge", dbc.Badge(id="annual-gas-standing-charge", class_name='ms-1')]),
        html.P(['Spark gap', dbc.Badge(id="spark-gap", class_name='ms-1')]),
        html.P(['Break even SCOP (lower is better)', dbc.Badge(id='break-even-point', class_name='ms-1')]), 
        html.P(['Cost of gas-boiler system', dbc.Badge(id='cost-with-gas-boiler', class_name='ms-1')]), 
        html.P(['Cost of HP with no Gas', dbc.Badge(id='cost-with-hp-no-gas', class_name='ms-1')]), 
        html.P(['Annual cost saving', dbc.Badge(id='annual-cost-saving', class_name='ms-1')]), 
        html.P(['Annual cost saving (%)', dbc.Badge(id='annual-cost-saving-pc', class_name='ms-1')]), 

        html.H2('Greenhouse gas impact'), 

        html.P(['Emissions from gas boiler', dbc.Badge(id='emissions-from-gas-boiler', class_name='ms-1')]), 
        html.P(['Emissions from HP', dbc.Badge(id='emissions-from-hp', class_name='ms-1')]), 
        html.P(['Annual emissions saving', dbc.Badge(id='annual-carbon-saving', class_name='ms-1')]), 
        html.P(['Annual emissions saving (%)', dbc.Badge(id='annual-carbon-saving-pc', class_name='ms-1')]), 
    ], fluid=True
)




if __name__ == "__main__":
    app.run(debug=True, port=8888)
