"""
This generates a table in the database. 
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from db_conn import DbConn


app = Flask(__name__)
connections = DbConn().get_connection()
app.config['SQLALCHEMY_DATABASE_URI'] = connections["DB_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserData(db.Model):

   __tablename__ = 'user_data'

   id = db.Column(db.Integer, primary_key = True, nullable=False)
   elec_stand_charge = db.Column(db.Float())
   elec_unit_charge = db.Column(db.Float())
   gas_stand_charge = db.Column(db.Float())
   gas_unit_charge = db.Column(db.Float())
   gas_heat_consumption = db.Column(db.Float())
   gas_nonheat_consumption = db.Column(db.Float())
   elec_nonheat_consumption = db.Column(db.Float())
   boiler_efficiency = db.Column(db.Float())
   hp_scop = db.Column(db.Float())
   elec_upweighting = db.Column(db.Float())
   created_at = db.Column(db.DateTime)

def __init__(self, 
             id, 
             elec_unit_charge, 
             gas_stand_charge, 
             gas_unit_charge, 
             gas_heat_consumption, 
             gas_nonheat_consumption, 
             elec_nonheat_consumption, 
             boiler_efficiency, 
             hp_scop,
             elec_upweighting, 
             elec_stand_charge, 
             created_at):
   self.id = id
   self.elec_stand_charge = elec_stand_charge 
   self.elec_unit_charge = elec_unit_charge 
   self.gas_stand_charge = gas_stand_charge 
   self.gas_unit_charge = gas_unit_charge 
   self.gas_heat_consumption = gas_heat_consumption 
   self.gas_nonheat_consumption = gas_nonheat_consumption 
   self.elec_nonheat_consumption = elec_nonheat_consumption 
   self.boiler_efficiency = boiler_efficiency 
   self.hp_scop = hp_scop
   self.elec_upweighting = elec_upweighting 
   self.created_at = created_at

def __repr__(self):
        return f'<User {self.name!r}>'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)