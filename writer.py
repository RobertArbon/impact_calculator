import os

from sqlalchemy.orm import sessionmaker
from datetime import datetime
import datetime
from sqlalchemy import create_engine

from models import UserData
import config

config_env = getattr(config, os.getenv('APP_SETTINGS', 'DevelopmentConfig'))


class WriteUserData: 
    def __init__(self):
        print('Writing to DB')
    
    def committing_data(self, 
             elec_unit_charge, 
             gas_stand_charge, 
             gas_unit_charge, 
             gas_heat_consumption, 
             gas_nonheat_consumption, 
             elec_nonheat_consumption, 
             boiler_efficiency, 
             hp_scop,
             elec_upweighting, 
             elec_stand_charge):
        conn = config_env.DATABASE_URL
        engine = create_engine(conn, echo = True, pool_size=500, max_overflow=-1, pool_pre_ping=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        try: 
            userdata = UserData(
                elec_unit_charge = elec_unit_charge, 
                 gas_stand_charge = gas_stand_charge, 
                 gas_unit_charge = gas_unit_charge, 
                 gas_heat_consumption = gas_heat_consumption,  
                 gas_nonheat_consumption = gas_nonheat_consumption, 
                 elec_nonheat_consumption = elec_nonheat_consumption, 
                 boiler_efficiency = boiler_efficiency, 
                 hp_scop = hp_scop,
                 elec_upweighting = elec_upweighting, 
                 elec_stand_charge = elec_stand_charge, 
                 created_at = datetime.datetime.now())
            session.add(userdata)
            session.commit()

        except Exception as e: 
            print('Error! ', e) 

        session.close()
        