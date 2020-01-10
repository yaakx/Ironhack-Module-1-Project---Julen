import argparse
import os
import pandas as pd
import sys
from package1.module1 import importing_merging
from package1.module2 import forbes_api, countries_data, regions_world
from package1.module3 import report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", required=False, help="Get a report from a region.", action="append", nargs='+')
    parser.add_argument("-l", "--list", required=False, help="List of countries and regions.", default=False, action="store_true")
    parser.add_argument("-r", "--region", required=False, help="Get a report from a region.", action="append", nargs='+')
    args = parser.parse_args()
    path = os.getcwd()
    importing_merging(path)
    regions_world(path)
    forbes_api(path)
    df = pd.read_csv(path + '/data/processed/forbes_definitive.csv')
    df_r = pd.read_csv(path + '/data/processed/regions_world.csv')
    all_r = [i for i in (set(df_r.Region.to_list())) if type(i) != float]
    countries = [i for i in set(df.country.to_list()) if type(i) == str]
    all_c = countries
    if args.list:
        print(f'The list of countries is {all_c}')
        print(f'The list of regions is {all_r}')
        sys.exit()
    if args.country:
        if args.country[0][0] != "all":
            countries = args.country[0]
        countries_data(path, countries=countries)
        report(path, all_c=all_c, countries=countries)
    if args.region:
        countries = []
        for i in args.region[0]:
            countries += df_r.loc[df_r["Region"] == i].Country.to_list()
        countries = list(set(countries))
        regions = args.region[0]
        countries_data(path, countries=countries)
        report(path, all_c, countries=countries, regions=regions, all_r=all_r)
    if not args.country and not args.region:
        countries_data(path, countries=countries)
        report(path)


if __name__ == "__main__":
    main()
