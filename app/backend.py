from fastapi import FastAPI
import pandas as pd
import os 

app = FastAPI()

DATA_DIR = '/Users/parkjuyong/Desktop/4-1/data-crawling-project/data/region_data'

@app.get("/api/regions")
def get_regions():
  regions = []
  for file in os.listdir(DATA_DIR):
    if file.endswith('.csv'):
      region = file.replace('.csv','')
      regions.append(region)
  return {"regions":sorted(regions)}


@app.get("/api/centers/{region}")
def get_centers(region:str):
  safe_region_name = region
  file_path = os.path.join(DATA_DIR, f'{safe_region_name}.csv')

  if os.path.exists(file_path):
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    return {
      "region":region,
      "centers" : df.to_dict('records'),
      "count":len(df)
    }
  return {"region":region, "centers":[], "count":0} 