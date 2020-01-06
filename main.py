from package1.module1 import importing_merging, data_cleaning
from package1.module2 import forbes_api, countries_data

if __name__ == "__main__":
    df = importing_merging('data/raw/JulenC.db')
    df = data_cleaning(df)
    df.to_csv("data/processed/forbes_clean.csv")
    df_countries = countries_data(df)
    df_countries.to_csv("data/processed/economic_values.csv")
    df_def = forbes_api(df)
    df_def.to_csv("data/processed/forbes_definitive.csv")
