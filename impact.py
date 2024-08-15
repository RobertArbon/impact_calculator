from dash import Input, Output, callback, State

DAYS_PER_YEAR = 365
ELEC_GHG_DENSITY = 0.21
GAS_GHG_DENSITY = 0.18  
KG_PER_TONNE = 1000


def calc_emissions_from_gas(gas_consumption, gas_factor=GAS_GHG_DENSITY):
    return gas_consumption*gas_factor/KG_PER_TONNE


def calc_emissions_from_electricity(gas_consumption, boiler_efficiency, modelled_scop, elec_factor=ELEC_GHG_DENSITY): 
    return elec_factor*gas_consumption*boiler_efficiency/modelled_scop/KG_PER_TONNE


def calc_gas_standing_charge(gas_charge):
    total_charge = DAYS_PER_YEAR * gas_charge
    return total_charge


def calc_spark_gap(elec_charge, gas_charge):
    return elec_charge/gas_charge

def calc_break_even_point(gas_consumption, boiler_efficiency, elec_unit_charge, 
                     gas_unit_charge, gas_standing_charge):
    output_elec_cost = gas_consumption*boiler_efficiency*elec_unit_charge
    input_gas_cost = gas_consumption*gas_unit_charge + DAYS_PER_YEAR*gas_standing_charge
    target_scop = output_elec_cost/input_gas_cost
    return target_scop


def calc_cost_with_gas_boiler(gas_consumption, gas_unit_charge, gas_stand_charge): 
    total_annual_charge = calc_gas_standing_charge(gas_stand_charge)
    total_cost = gas_consumption*gas_unit_charge+total_annual_charge
    return total_cost

def calc_cost_with_hp_no_gas(gas_consumption, boiler_efficiency, modelled_scop, elec_unit_charge): 
    return elec_unit_charge*gas_consumption*boiler_efficiency/modelled_scop



@callback(
    Output(component_id='annual-gas-standing-charge', component_property='children'), 
    Output(component_id='spark-gap', component_property='children'), 
    Output(component_id='break-even-point', component_property='children'), 
    Output(component_id='cost-with-gas-boiler', component_property='children'), 
    Output(component_id='cost-with-hp-no-gas', component_property='children'), 
    Output(component_id='annual-cost-saving', component_property='children'), 
    Output(component_id='annual-cost-saving-pc', component_property='children'), 
    Output(component_id='emissions-from-gas-boiler', component_property='children'), 
    Output(component_id='emissions-from-hp', component_property='children'), 
    Output(component_id='annual-carbon-saving', component_property='children'), 
    Output(component_id='annual-carbon-saving-pc', component_property='children'), 

    Input(component_id='save-button', component_property='n_clicks'), 

    State(component_id='gas-heat-consumption', component_property='value'), 
    State(component_id='gas-cook-consumption', component_property='value'), 
    State(component_id='boiler-efficiency', component_property='value'), 
    State(component_id='modelled-scop', component_property='value'), 
    State(component_id='gas-unit-charge', component_property='value'), 
    State(component_id='gas-stand-charge', component_property='value'), 
    State(component_id='elec-unit-charge', component_property='value'), 
    State(component_id='elec-stand-charge', component_property='value')
)
def calculate_impact(n_clicks, gas_heat_cons, gas_cook_cons, boiler_eff, 
                     modelled_scop, gas_unit_charge, gas_stand_charge,
                     elec_unit_charge, elec_stand_charge): 
    annual_gas_stand_charge = calc_gas_standing_charge(gas_stand_charge)
    spark_gap = calc_spark_gap(elec_unit_charge, gas_unit_charge)
    break_even_point = calc_break_even_point(gas_heat_cons, boiler_eff, elec_unit_charge, 
                     gas_unit_charge, gas_stand_charge)
    cost_with_gas_boiler = calc_cost_with_gas_boiler(gas_heat_cons, gas_unit_charge, gas_stand_charge) 
    cost_with_hp_no_gas = calc_cost_with_hp_no_gas(gas_heat_cons, boiler_eff, modelled_scop, elec_unit_charge)
    emissions_from_gas_boiler = calc_emissions_from_electricity(gas_heat_cons, boiler_eff, 
                                                                 modelled_scop)
    emissions_from_hp = calc_cost_with_hp_no_gas(gas_heat_cons, boiler_eff, modelled_scop, elec_unit_charge)
    return (
        annual_gas_stand_charge, 
        spark_gap, 
        break_even_point, 
        cost_with_gas_boiler, 
        cost_with_hp_no_gas, 
        cost_with_gas_boiler - cost_with_hp_no_gas, 
        100**(cost_with_gas_boiler/cost_with_hp_no_gas-1), 
        emissions_from_gas_boiler, 
        emissions_from_hp, 
        emissions_from_gas_boiler - emissions_from_hp,
        100*(emissions_from_gas_boiler/emissions_from_hp-1)
    )


     

