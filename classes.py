import re

def email_validator(email):
  pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  result = re.match(pattern, email)
  if result:
    return True
  else: False
  
def final_energy(electricity_bill, natural_gas, fuel_bill):
  electricity = electricity_bill* 12 * 0.0005
  gas = natural_gas * 12 * 0.0053
  fuel = fuel_bill * 12 * 2.32
  return electricity + gas + fuel

def final_waste(waste_generate, waste_recycle):
  co2_from_waste = waste_generate * 12 * (0.57 - waste_recycle)
  return co2_from_waste

def final_travel(km_travel, fuel_effeciency):
    co2_from_travel = km_travel * (1 / fuel_effeciency) * 2.31
    return co2_from_travel