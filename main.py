import argparse
from package1.module1 import importing_merging, data_cleaning
from package1.module2 import forbes_api, countries_data
from package1.module3 import report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", required=False, help="Choose a country to get a report from.")
    parser.add_argument("-l", "--list", required=False, help="List of countries.", default=False, action="store_true")
    args = parser.parse_args()
    df = importing_merging('data/raw/JulenC.db')
    df = data_cleaning(df)
    df.to_csv("data/processed/forbes_clean.csv")
    df_countries = countries_data(df)
    df_countries.to_csv("data/processed/economic_values.csv")
    df_def = forbes_api(df)
    df_def.to_csv("data/processed/forbes_definitive.csv")
    report(df_def, df_countries, args)

