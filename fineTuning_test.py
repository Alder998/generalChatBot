from Model import fineTuningGeneral as model
import pandas as pd
from sqlalchemy import create_engine
from fineTuningDatasetGenerator import fineTuning_Utils as utils

# Fine-tuning Data from SQL
engine = create_engine('postgresql://postgres:Lavagna123!@localhost:5432/News_Data')
query = 'SELECT * FROM public."News_Scraping_Data_V2"'
baseData = pd.read_sql(query, engine)
newsDataForFineTuning = utils.fineTuning_utils().loadAndProcessFinancialNews(baseData)

fineTunedModel = model.fineTuningGeneral().fineTuningModel('gpt2-medium', newsDataForFineTuning, epochs=30,
                                                          saved_model_name='fine_tuned_gpt2_medium')

