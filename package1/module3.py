import sys
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


def plotting(df_1, df_c, name, url):
    df_2 = df_1.groupby("country").count()[["id", "worth (BUSD)"]].merge(df_c, left_on=["country"],
                                                                         right_on=["Country"])
    df_2["Times_GDP"] = (df_2["worth (BUSD)"] * 1000000000) / (
            df_2["GDP per capita [+]"].str.replace(",", "").str[:-1].astype("int64"))
    df_2["%GDP"] = (df_2["worth (BUSD)"] * 1000000000) / (
            df_2["Annual GDP [+]"].str.replace(",", "").str[:-3].astype("int64") * 1000000) * 100
    name = name.lower()
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 12))
    df_1.groupby(["country", "gender"]).count()[["id"]].unstack(level="gender").plot.bar(ax=axes[0, 0])
    df_1[["age"]].plot.hist(bins=[20, 30, 40, 50, 60, 70, 80, 90, 100], ax=axes[0, 1])
    df_1.groupby("area").count().sort_values(by="id", ascending=False).id.plot.bar(ax=axes[1, 0])
    df_1.groupby("area").sum().sort_values(by="worth (BUSD)", ascending=False)["worth (BUSD)"].plot.bar(ax=axes[1, 1])
    df_2.sort_values(by="%GDP", ascending=False).plot.bar(x="Country", y="%GDP", ax=axes[2, 1])
    df_2.sort_values(by="Times_GDP", ascending=False).plot.bar(x="Country", y="Times_GDP", ax=axes[2, 0])
    axes[0, 0].set_title("Number of males and females by country")
    axes[0, 1].set_title("Distribution of age")
    axes[1, 0].set_title("Number of people by area")
    axes[1, 1].set_title("BUSD worth each area")
    axes[2, 0].set_title("Times the GDP per capita")
    axes[2, 1].set_title("% of yearly GDP worth")
    plt.tight_layout()
    plt.savefig(f'{url}/data/results/{name}.png', dpi=100)
    plt.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(80)
    pdf.cell(1, 1, f'{name.title()}', 'C')
    pdf.image(f'{url}/data/results/{name}.png', x=50, y=30, w=100, h=120)
    pdf.output(f'{url}/data/results/{name}.pdf', 'F')


def report(url, all_c=[], all_r=[], countries=[], regions=[]):
    df_r = pd.read_csv(url + '/data/processed/regions_world.csv')
    if countries:
        for country in countries:
            if country not in all_c:
                print(f'Please select a valid country from {all_c}')
                sys.exit()
    if regions:
        for region in regions:
            if region not in all_r:
                print(f'Please select a valid region from {all_r}')
                sys.exit()
    df = pd.read_csv(url + '/data/processed/forbes_definitive.csv')
    df_c = pd.read_csv(url + '/data/processed/economic_values.csv')
    if not countries and not regions:
        plotting(df, df_c, "world", url)
        sys.exit()
    df_c = df_c.reset_index().drop("index", axis=1)
    if regions:
        for region in regions:
            df_s = df.merge(df_r, left_on="country", right_on="Country")
            df_1 = df_s.loc[df_s["Region"] == region]
            df_1 = df_1.drop_duplicates()
            plotting(df_1, df_c, region, url)
        sys.exit()
    if countries:
        countries = [i.title() for i in countries]
        df_1 = df.loc[df["country"].isin(countries)]
        name = countries if len(countries) == 1 else "comparation"
        plotting(df_1, df_c, name, url)
