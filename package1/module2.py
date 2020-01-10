import requests
import pandas as pd



def web_scrapper(url, country):
    df1 = pd.read_html(url + country, attrs={'class': 'table tabledat table-striped table-condensed table-hover'})[0]
    df1.drop(1, axis=1,  inplace=True)
    df1 = df1.T
    df1.columns = df1.iloc[0]
    df1 = df1.drop(0).drop("Gouvernement", axis=1)
    return_df = df1.loc[:, ["Annual GDP [+]", "GDP per capita [+]"]].iloc[:, [1, 3]]
    return return_df


def forbes_api(url):
    r = requests.get("https://www.forbes.com/ajax/list/data?year=2018&uri=billionaires&type=person")
    df = pd.read_csv(url + '/data/processed/forbes_clean.csv')
    df_2 = pd.DataFrame(r.json())
    df_2 = df_2.loc[:, ["age", "name", "gender", "country"]]
    df_def = df.drop(["age", "gender", "country"], axis=1)
    df_def = df_def.merge(df_2, on=['name'], how='left')
    df_def.to_csv(url + '/data/processed/forbes_definitive.csv')


def countries_data(url_abs, countries):
    url = "https://countryeconomy.com/countries/"
    countries_df = pd.DataFrame()
    if countries:
        countries = list(map(lambda x: x.lower().replace(' ', '-') if type(x) == str else None, countries))
        country_col = []
        for i in range(0, len(countries)):
            try:
                df1 = web_scrapper(url, countries[i])
            except:
                continue
            country_col.append(countries[i])
            countries_df = pd.concat([countries_df, df1], sort=False)
        countries_df["Country"] = country_col
        countries_df["Country"] = countries_df.Country.str.replace("-", " ").str.title()
        countries_df = countries_df.reset_index().drop("index", axis=1)
    countries_df.to_csv(url_abs + '/data/processed/economic_values.csv')


def regions_world(url):
    df = pd.read_csv(url + '/data/raw/countries-of-the-world.zip')
    df = df.loc[:, ["Country", "Region"]]
    df.Region = df.Region.str.title().str.strip()
    df.Country = df.Country.str.strip()
    df_d = pd.read_csv(url + '/data/processed/forbes_definitive.csv')
    df_d = df_d.merge(df, left_on="country", right_on="Country", how="left")
    df_d = df_d.loc[:, ["country", "Region"]]
    df_d.columns = ["Country", "Region"]
    df_d = df_d.drop_duplicates()
    df_d.to_csv(url + "/data/processed/regions_world.csv")
