import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns 


df = pd.read_csv("info_storage/GLM_9_7_filtered2.csv")
df.head() 
df.describe() 
sns.pairplot(df) 