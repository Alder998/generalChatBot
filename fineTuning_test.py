from Model import fineTuningGeneral as model
import pandas as pd
from sqlalchemy import create_engine

# Fine-tuning Data from SQL
engine = create_engine('postgresql://postgres:Lavagna123!@localhost:5432/fineTuningData')
query = 'SELECT * FROM public."ItalianCitiesData"'
baseData = pd.read_sql(query, engine)
baseData.fillna('No Data Available')

fineTunedModel = model.fineTuningGeneral().fineTuningModel('gpt2-medium', baseData, epochs=5,
                                                           saved_model_name='fine_tuned_gpt2_medium')

