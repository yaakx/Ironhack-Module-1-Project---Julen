import argparse
import pandas as pd
import sys
import matplotlib.pyplot as plt


def report(df, df_c, args):
    countries = df_c.Country.to_list()
    options = countries + [i.lower() for i in countries]
    df_c = df_c.reset_index().drop("index", axis=1)
    if args.list:
        print(f'The list of countries is {countries}')
        sys.exit()
    if not args.country:
        fig, axes = plt.subplots(nrows=2, ncols=2)
        d = df.groupby("country").count()[["id", "worth (BUSD)"]].merge(df_c, left_on=["country"], right_on=["Country"])
        d["%GDP"] = (d["worth (BUSD)"] * 1000000000) / (
                    d["Annual GDP [+]"].str.replace(",", "").str[:-3].astype("int64") * 1000000) * 100
        f1 = df.groupby(["country", "gender"]).count()[["id"]].unstack(level="gender").plot.barh(ax=axes[0, 0])
        f2 = df[["age"]].plot.hist(bins=[20, 30, 40, 50, 60, 70, 80, 90, 100], ax=axes[0, 1])
        f3 = df.groupby("area").count().sort_values(by="id", ascending=False).id.plot.barh(ax=axes[1, 0])
        f4 = d.sort_values(by="%GDP", ascending=False).plot.barh(x="Country", y="%GDP", ax=axes[1, 1])
        plt.show()
    elif args.country not in options:
        print(f'Please select a valid country from {countries}')
        sys.exit()
    else:
        fig, axes = plt.subplots(nrows=2, ncols=2)
        df = df.loc[df["country"] == args.country.title()]
        d = df.groupby("country").count()[["id", "worth (BUSD)"]].merge(df_c, left_on=["country"], right_on=["Country"])
        d["%GDP"] = (d["worth (BUSD)"] * 1000000000) / (
                    d["Annual GDP [+]"].str.replace(",", "").str[:-3].astype("int64") * 1000000) * 100
        f1 = df.groupby(["country", "gender"]).count()[["id"]].unstack(level="gender").plot.bar(ax=axes[0, 0])
        f2 = df[["age"]].plot.hist(bins=[20, 30, 40, 50, 60, 70, 80, 90, 100], ax=axes[0, 1])
        f3 = df.groupby("area").count().sort_values(by="id", ascending=False).id.plot.bar(ax=axes[1, 0])
        f4 = d.sort_values(by="%GDP", ascending=False).plot.bar(x="Country", y="%GDP", ax=axes[1, 1])
        plt.show()


if __name__ == "__name__":
    df_country = pd.read_csv("../data/processed/economic_values.csv")
    df_def = pd.read_csv("../data/processed/forbes_definitive.csv")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", required=False, help="Choose a country to get a report from.")
    parser.add_argument("-l", "--list", required=False, help="List of countries.", default=False, action="store_true")
    args = parser.parse_args()
    report(df_def, df_country, args)
