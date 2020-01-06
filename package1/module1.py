import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def importing_merging(rel_url):
    engine = create_engine('sqlite:///' + rel_url)
    df_business = pd.read_sql_table('business_info', engine)
    df_personal = pd.read_sql_table('personal_info', engine)
    df_rank = pd.read_sql_table('rank_info', engine)
    df = df_business.merge(df_rank, on=['id', 'Unnamed: 0'], how='left')
    df = df.merge(df_personal, on=['id', 'Unnamed: 0'], how='outer')
    return df


def data_cleaning(df):
    df["area"] = df["Source"].str.split("==>").str[0]
    df["source"] = df["Source"].str.split("==>").str[1]
    df.drop(['Unnamed: 0', 'lastName', "Source", "realTimeWorth", "image"], axis=1, inplace=True)
    df.name = df.name.str.title()
    df.position = df.position.astype("int64")
    df.worth = df.worth.str.replace('BUSD', '').astype('float64')
    newcols = list(df.columns)
    newcols[1] = "worth (BUSD)"
    newcols[2] = "worthChage (millions USD)"
    df.columns = newcols
    df["worthChage (millions USD)"] = df["worthChage (millions USD)"].str.replace(" millions USD", "")
    df.loc[df["worthChage (millions USD)"] == "nan", "worthChage (millions USD)"] = np.nan
    df["worthChage (millions USD)"] = df["worthChage (millions USD)"].astype("float64")
    df.loc[df["country"] == 'None', "country"] = None
    return df


if __name__ == "__main__":
    df = importing_merging('../data/raw/JulenC.db')
    print(df)
    df = data_cleaning(df)
    print(df)
