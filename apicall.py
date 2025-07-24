from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io
import random
from faker import Faker
app = FastAPI()
fake = Faker()
def generate_dummy_data():
    property_types = ["Detached", "Semi-Detached", "Condo", "Townhouse"]
    cities = ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf"]
    states = ["Berlin", "Bavaria", "Hesse", "Baden-Württemberg", "North Rhine-Westphalia", "Lower Saxony"]
    country = "Germany"
    data = []
    n = 400
    for _ in range(n):
        city = random.choice(cities) 
        state = random.choice(states)
        year_built = random.randint(1970, 2022)
        size = random.randint(600, 4000)
        bedrooms = random.randint(1, 5)
        bathrooms = random.randint(1, 4)
        price = size * random.uniform(300, 800)
        data.append({
            "address": fake.street_address(),
            "city": city,
            "state": state,
            "country": country,
            "propertyType": random.choice(property_types),
            "yearBuilt": year_built,
            "size": size,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "mostRecentPriceAmount": round(price, 2)
        })
    return pd.DataFrame(data)
@app.get("/generate-properties/csv")
def get_properties_csv():
    df = generate_dummy_data()
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=property_data.csv"}
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apicall:app", host="127.0.0.1", port=8000, reload=True) 