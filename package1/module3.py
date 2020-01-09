import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def plotting(df_1, df_c):
    fig, axes = plt.subplots(nrows=2, ncols=2)
    df_2 = df_1.groupby("country").count()[["id", "worth (BUSD)"]].merge(df_c, left_on=["country"],
                                                                         right_on=["Country"])
    df_2["%GDP"] = (df_2["worth (BUSD)"] * 1000000000) / (
            df_2["Annual GDP [+]"].str.replace(",", "").str[:-3].astype("int64") * 1000000) * 100
    f1 = df_1.groupby(["country", "gender"]).count()[["id"]].unstack(level="gender").plot.barh(ax=axes[0, 0])
    f2 = df_1[["age"]].plot.hist(bins=[20, 30, 40, 50, 60, 70, 80, 90, 100], ax=axes[0, 1])
    f3 = df_1.groupby("area").count().sort_values(by="id", ascending=False).id.plot.barh(ax=axes[1, 0])
    f4 = df_2.sort_values(by="%GDP", ascending=False).plot.barh(x="Country", y="%GDP", ax=axes[1, 1])
    plt.show()
    plt.close()


def report(url, all_c=False, countries=False, regions=False):
    options = countries + [i.lower() for i in countries]
    df_r = pd.read_csv(url + '/data/processed/regions_world.csv')
    all_r = [i for i in (set(df_r.Region.to_list())) if type(i) != float]
    r_options = all_r + [i.lower() for i in all_r]
    if countries:
        for country in countries:
            if country not in options:
                print(f'Please select a valid country from {all_c}')
                sys.exit()
    if regions:
        for region in regions:
            if region not in r_options:
                print(f'Please select a valid region from {all_r}')
                sys.exit()
    df = pd.read_csv(url + '/data/processed/forbes_definitive.csv')
    df_c = pd.read_csv(url + '/data/processed/economic_values.csv')
    if not countries:
        plotting(df, df_c)
        sys.exit()
    df_c = df_c.reset_index().drop("index", axis=1)
    if regions:
        for region in regions:
            df_s = df.merge(df_r, left_on="country", right_on="Country")
            df_1 = df_s.loc[df_s["Region"] == region]
            plotting(df_1, df_c)
        sys.exit()
    if countries:
        for country in countries:
            df_1 = df.loc[df["country"] == country.title()]
            plotting(df_1, df_c)
