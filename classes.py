import re
from flask import Flask, jsonify, request

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
  co2_from_waste = waste_generate * 12 * (0.57 - (waste_recycle/100))
  return co2_from_waste

def final_travel(km_travel, fuel_effeciency):
    co2_from_travel = km_travel * (1 / fuel_effeciency) * 2.31
    return co2_from_travel
  
def generate_dynamic_suggestions(energy_usage, waste, business_travel, stats):
    suggestions = []

    # Helper function to format suggestions with icons
    def format_suggestion(category, text, status):
        # status could be 'high', 'low', or 'normal'
        icon = "high" if status == "high" else "low" if status == "low" else "med"
        return {"icon": icon, "category": category, "text": text, "status": status}

    # Compare Energy Usage
    if energy_usage > stats['energy_usage']['avg']:
        if energy_usage >= stats['energy_usage']['max'] * 0.9:  # Near max
            suggestions.append(format_suggestion(
                "Energy Usage",
                "Your energy usage is quite high compared to others. Consider switching to renewable energy sources or more efficient appliances to reduce your carbon footprint.",
                "high"
            ))
        else:
            suggestions.append(format_suggestion(
                "Energy Usage",
                "Your energy usage is above average. You can reduce it by optimizing your energy consumption and considering green energy solutions.",
                "high"
            ))
    elif energy_usage < stats['energy_usage']['avg']:
        if energy_usage <= stats['energy_usage']['min'] * 1.1:  # Near min
            suggestions.append(format_suggestion(
                "Energy Usage",
                "Great job! Your energy usage is among the lowest. Keep up the sustainable practices!",
                "low"
            ))
        else:
            suggestions.append(format_suggestion(
                "Energy Usage",
                "Your energy usage is below average. You're doing well, but there's always room for improvement, like using energy-efficient appliances.",
                "low"
            ))

    # Compare Waste
    if waste > stats['waste']['avg']:
        if waste >= stats['waste']['max'] * 0.9:
            suggestions.append(format_suggestion(
                "Waste",
                "Your waste generation is near the maximum. Try reducing waste, reusing materials, and increasing your recycling efforts.",
                "high"
            ))
        else:
            suggestions.append(format_suggestion(
                "Waste",
                "Your waste generation is above average. Consider composting and recycling to manage your waste better.",
                "high"
            ))
    elif waste < stats['waste']['avg']:
        if waste <= stats['waste']['min'] * 1.1:
            suggestions.append(format_suggestion(
                "Waste",
                "Excellent! Your waste generation is minimal. Keep up your efforts to reduce and recycle waste.",
                "low"
            ))
        else:
            suggestions.append(format_suggestion(
                "Waste",
                "Your waste generation is below average. Good work! Consider reducing even further by minimizing single-use products.",
                "low"
            ))

    # Compare Business Travel
    if business_travel > stats['business_travel']['avg']:
        if business_travel >= stats['business_travel']['max'] * 0.9:
            suggestions.append(format_suggestion(
                "Business Travel",
                "Your business travel is very high. Consider reducing travel or opting for virtual meetings to cut down on emissions.",
                "high"
            ))
        else:
            suggestions.append(format_suggestion(
                "Business Travel",
                "Your business travel is above average. Try using public transportation or carpooling to lower your travel footprint.",
                "high"
            ))
    elif business_travel < stats['business_travel']['avg']:
        if business_travel <= stats['business_travel']['min'] * 1.1:
            suggestions.append(format_suggestion(
                "Business Travel",
                "Fantastic! Your travel footprint is among the lowest. Keep utilizing virtual options and sustainable travel methods.",
                "low"
            ))
        else:
            suggestions.append(format_suggestion(
                "Business Travel",
                "Your business travel is below average. Good job! Keep looking for ways to reduce unnecessary travel and opt for eco-friendly transportation.",
                "low"
            ))

    return suggestions
