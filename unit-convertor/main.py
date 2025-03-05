from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

conversion_factors = {
    "length": {
        "millimeter": 0.001,
        "centimeter": 0.01,
        "meter": 1,
        "kilometer": 1000,
        "inch": 0.0254,
        "foot": 0.3048,
        "yard": 0.9144,
        "mile": 1609.34,
    },
    "weight": {
        "milligram": 0.001,
        "gram": 1,
        "kilogram": 1000,
        "ounce": 28.3495,
        "pound": 453.592,
    },
    "temperature": {},
}


def convert_units(value: float, from_unit: str, to_unit: str, category: str):
    if category == "temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9 / 5) + 32
        if from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5 / 9
        if from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        if from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        if from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5 / 9 + 273.15
        if from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9 / 5 + 32
        return value

    base_value = value * conversion_factors[category][from_unit]

    converted_value = base_value / conversion_factors[category][to_unit]

    return converted_value


@app.get("/convert")
def convert(value: float, from_unit: str, to_unit: str, category: str):
    try:
        result = convert_units(value, from_unit, to_unit, category)
        return {
            "input": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "converted_value": result,
        }
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Something went wrong:{e}")


@app.get("/")
def serve_html():
    return FileResponse("index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
