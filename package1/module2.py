import pandas as pd
import requests


def web_scrapper(url, country):
    df1 = pd.read_html(url + country, attrs={'class': 'table tabledat table-striped table-condensed table-hover'})[0]
    df1.drop(1, axis=1,  inplace=True)
    df1 = df1.T
    df1.columns = df1.iloc[0]
    df1 = df1.drop(0).drop("Gouvernement", axis=1)
    return_df = df1.loc[:, ["Annual GDP [+]", "GDP per capita [+]"]].iloc[:, [1, 3]]
    return return_df


def forbes_api(df):
    r = requests.get("https://www.forbes.com/ajax/list/data?year=2018&uri=billionaires&type=person")
    df_2 = pd.DataFrame(r.json())
    df_2 = df_2.loc[:, ["age", "name", "gender", "country"]]
    df_def = df.drop(["age", "gender", "country"], axis=1)
    df_def = df_def.merge(df_2, on=['name'], how='left')
    return df_def


def countries_data(df):
    url = "https://countryeconomy.com/countries/"
    countries = list(set(df.country.to_list()))
    countries = list(map(lambda x: x.lower().replace(' ', '-') if type(x) == str else None, countries))
    countries_df = pd.DataFrame()
    country_col = []
    for i in range(1, len(countries)):
        try:
            df1 = web_scrapper(url, countries[i])
        except:
            continue
        country_col.append(countries[i])
        countries_df = pd.concat([countries_df, df1], sort=False)
    countries_df["Country"] = country_col
    countries_df["Country"] = countries_df.Country.str.replace("-", " ").str.title()
    countries_df = countries_df.reset_index().drop("index", axis=1)
    return countries_df


if __name__ == "__main__":
    df = pd.read_csv("../data/processed/forbes_definitive.csv", index_col=0)
    df_def = forbes_api(df)
    print(df_def)
    df_countries = countries_data(df)
    print(df_countries)
