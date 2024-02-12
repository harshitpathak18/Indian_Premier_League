import pandas as pd


df = pd.read_csv('ScorePredictor\clean_full_ipl_data.csv')

def teams():
    return df['batting_team'].unique()

def city():
    return df['city'].unique()