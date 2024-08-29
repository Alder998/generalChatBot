from Model import fineTuningGeneral as model
import pandas as pd
from sqlalchemy import create_engine

# Fine-tuning Data from SQL
engine = create_engine('postgresql://postgres:Lavagna123!@localhost:5432/News_Data')
query = 'SELECT * FROM public."News_Scraping_Data_V2"'
baseData = pd.read_sql(query, engine)

fineTunedModel = model.fineTuningGeneral().fineTuningModel('gpt2', baseData, epochs=30)

