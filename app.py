import os

from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

import config

DAYS_PER_YEAR = 365
ELEC_GHG_DENSITY = 0.21
GAS_GHG_DENSITY = 0.18  
KG_PER_TONNE = 1000

config_env = getattr(config, os.getenv('APP_SETTINGS', 'DevelopmentConfig'))

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
        html.Div(id="annual-gas-standing-charge"),
        html.Div(id="spark-gap"),
        html.Div(id='break-even-point'), 
        html.Div(id='cost-with-gas-boiler'), 
        html.Div(id='cost-with-hp-no-gas'), 
        html.Div(id='cost-saving'), 

        html.H2('Greenhouse gas impact'), 

        html.Div(id='emissions-from-gas-boiler'), 
        html.Div(id='emissions-from-hp'), 
        html.Div(id='annual-carbon-saving'), 
    ], fluid=True
)


# def emissions_from_gas(gas_consumption, gas_factor=GAS_GHG_DENSITY):
#     return gas_consumption*gas_factor/KG_PER_TONNE


# def emissions_from_electricity(gas_consumption, boiler_efficiency, modelled_scop, elec_factor=ELEC_GHG_DENSITY): 
#     return elec_factor*gas_consumption*boiler_efficiency/modelled_scop/KG_PER_TONNE


# @callback(
#     Output(component_id='emissions-from-gas-boiler', component_property='children'), 
#     Input(component_id='gas-consumption', component_property='value')
# )
# def emission_fom_gas_string(gas_consumption): 
#     emissions = emissions_from_gas(gas_consumption)
#     return f"Emissions from heating with a gas boiler: Annual tonnes CO2e: {emissions:4.2f}"


# @callback(
#     Output(component_id='emissions-from-hp', component_property='children'), 
#     Input(component_id='gas-consumption', component_property='value'), 
#     Input(component_id='boiler-efficiency', component_property='value'), 
#     Input(component_id='modelled-scop', component_property='value'), 
# )
# def emission_from_hp_string(gas_consumption, boiler_eff, modelled_scop): 
#     emissions = emissions_from_electricity(gas_consumption, boiler_eff, modelled_scop)
#     return f"Emissions from heating witha heat pump: Annual tonnes CO2e: {emissions:4.2f}"


# @callback(
#    Output(component_id='annual-carbon-saving', component_property='children'), 
#    Input(component_id='gas-consumption', component_property='value'), 
#    Input(component_id='boiler-efficiency', component_property='value'), 
#    Input(component_id='modelled-scop', component_property='value'), 
# )
# def carbon_saving_string(gas_consumption, boiler_eff, modelled_scop):
#     gas_emissions = emissions_from_gas(gas_consumption)
#     hp_emissions = emissions_from_electricity(gas_consumption, boiler_eff, modelled_scop)
#     saving = f"Annual carbon saving: Annual tonnes CO2e: {gas_emissions-hp_emissions:4.2f}\
#             ({100*(gas_emissions - hp_emissions)/gas_emissions:4.1f}%)"
#     return saving


# def gas_standing_charge(gas_charge):
#     total_charge = DAYS_PER_YEAR * gas_charge
#     return total_charge


# @callback(
#     Output(component_id="annual-gas-standing-charge", component_property="children"),
#     Input(component_id="gas-stand-charge", component_property="value"),
# )
# def gas_standing_charge_string(gas_charge):
#     total_charge = gas_standing_charge(gas_charge)
#     return f"Annual standing charge (£/year): {total_charge:4.2f}"


# @callback(
#     Output(component_id="spark-gap", component_property="children"),
#     Input(component_id="elec-unit-charge", component_property="value"),
#     Input(component_id="gas-unit-charge", component_property="value"),
# )
# def spark_gap(elec_charge, gas_charge):
#     return f"Ratio of electrical to gas unit rate ('spark gap'): {elec_charge/gas_charge: 4.2f}"

# @callback(
#     Output(component_id='break-even-point', component_property='children'), 
#     Input(component_id='gas-consumption', component_property='value'), 
#     Input(component_id='boiler-efficiency', component_property='value'), 
#     Input(component_id='elec-unit-charge', component_property='value'), 
#     Input(component_id='gas-unit-charge', component_property='value'), 
#     Input(component_id='gas-stand-charge', component_property='value') 
# )
# def break_even_point(gas_consumption, boiler_efficiency, elec_unit_charge, 
#                      gas_unit_charge, gas_standing_charge):
#     output_elec_cost = gas_consumption*boiler_efficiency*elec_unit_charge
#     input_gas_cost = gas_consumption*gas_unit_charge + DAYS_PER_YEAR*gas_standing_charge
#     target_scop = output_elec_cost/input_gas_cost
#     return f"Break even point (target SCOP or SPF): {target_scop: 4.2f}"


# def cost_with_gas_boiler(gas_consumption, gas_unit_charge, gas_stand_charge): 
#     total_annual_charge = gas_standing_charge(gas_stand_charge)
#     total_cost = gas_consumption*gas_unit_charge+total_annual_charge
#     return total_cost

# @callback(
#     Output(component_id='cost-with-gas-boiler', component_property='children'), 
#     Input(component_id='gas-consumption', component_property='value'), 
#     Input(component_id='gas-unit-charge', component_property='value'), 
#     Input(component_id='gas-stand-charge', component_property='value') 
# )
# def cost_with_gas_boiler_string(gas_consumption, gas_unit_charge, gas_stand_charge): 
#     total_costs = cost_with_gas_boiler(gas_consumption, gas_unit_charge, gas_stand_charge)
#     return f"Cost with gas boiler £{total_costs:4.2f}"


# def cost_with_hp_no_gas(gas_consumption, boiler_efficiency, modelled_scop, elec_unit_charge): 
#     return elec_unit_charge*gas_consumption*boiler_efficiency/modelled_scop


# @callback(
#    Output(component_id='cost-with-hp-no-gas', component_property='children'), 
#    Input(component_id='gas-consumption', component_property='value'), 
#    Input(component_id='boiler-efficiency', component_property='value'), 
#    Input(component_id='modelled-scop', component_property='value'), 
#    Input(component_id='elec-unit-charge', component_property='value')
# )
# def cost_with_hp_no_gas_string(gas_consumption,boiler_eff, modelled_scop, elec_unit_charge):
#     total_costs = cost_with_hp_no_gas(gas_consumption, boiler_eff, modelled_scop, elec_unit_charge)
#     return f"Cost with heat pump and no gas meter £{total_costs:4.2f}" 



# @callback(
#    Output(component_id='cost-saving', component_property='children'), 
#    Input(component_id='gas-consumption', component_property='value'), 
#    Input(component_id='boiler-efficiency', component_property='value'), 
#    Input(component_id='modelled-scop', component_property='value'), 
#    Input(component_id='gas-unit-charge', component_property='value'), 
#    Input(component_id='gas-stand-charge', component_property='value'), 
#    Input(component_id='elec-unit-charge', component_property='value')
# )
# def cost_saving_string(gas_consumption, boiler_eff, modelled_scop, gas_unit_charge, gas_stand_charge, elec_unit_charge):
#     gas_cost = cost_with_gas_boiler(gas_consumption, gas_unit_charge, gas_stand_charge)
#     hp_cost = cost_with_hp_no_gas(gas_consumption, boiler_eff, modelled_scop, elec_unit_charge)
#     saving = f"Cost saving: £{gas_cost-hp_cost:4.2f} ({100*(gas_cost - hp_cost)/gas_cost:4.1f}%)"
#     return saving


# @callback(
#     Input(component_id='save-button', component_property='n_clicks')
# )
# def write_data_to_db(onclick): 
#     pass

if __name__ == "__main__":
    app.run(debug=True, port=8888)
