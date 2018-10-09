from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import itertools
import warnings
import click
from src.data.make_dataset import current_revenue

warnings.filterwarnings("ignore")


MF_CODES = ["002", "003", "059", "061", "067"]
TAX_RATES = {"0": 0.03195986, "D": 0.0405}
load_dotenv(find_dotenv())
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
os.chdir(os.path.dirname(__file__))
df = pd.read_sql("select * from mftax.asmt", engine)
tax_rates = [i[0] for i in engine.execute("select tax_rate from mftax.tax_rates").fetchall()]
liv_units = [i for i in engine.execute("select min(livunit), max(livunit) from mftax.livunits").fetchall()][0]

@click.group()
def main():
    pass


@main.command()
@click.argument("city", default="0")
@click.option("--rates", default=tax_rates)
@click.option("--units", default=liv_units, type=click.Tuple([int, int]))
def projected_revenue_scatter(city, rates, units):
    """
    Creates scatter plot for each combination of units and assessment rates
    """
    q = "select * from mftax.revenue_estimates where num_units between {0} and {1}"
#    min_max = (min(units), max(units))

    tax = pd.read_sql(q.format(*units), engine)
    tot = current_revenue(city)

    plt.scatter(tax.tax_rate, tax.est_tax, c=tax.num_units, 
            cmap='tab20c', label=tax.num_units.unique())
    bar = plt.colorbar(label="Number of Living Units")
#    bar.ax.tick_params(width=0)
    plt.scatter(.4, tot, marker="*", c="g", s=60)
    label_x = max(rates)
    label_y = np.percentile(tax.est_tax, 85) #set y-pos for label using 85th y-percentile
    plt.text(label_x, label_y, "Current Revenue\n${0:.3f}M".format(tot/1000000),
            horizontalalignment="center", fontsize=7.5)

    y_tick_fmt = lambda val, pos: "${0:.3f}M".format(val/1000000)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(y_tick_fmt))
    plt.ylabel("Estimated Tax Revenue")
    plt.xlabel("Assessment Rate")
    xmin = min(tax.tax_rate) - .02
    xmax = max(tax.tax_rate) + .025
    plt.xlim(xmin, xmax)
    plt.tight_layout()
    f_name = "../../reports/figures/projected_revenue_scatter_{0}_to_{1}_{2}.png"
    plt.savefig(f_name.format(*units, city), dpi=300)

@main.command()
@click.argument("city", default="0")
@click.option("--units", default=liv_units)
def rtotapr_bar_chart(city, units):
    """
    Bar chart comparing total appraised value for multi-family units that are assessed
    commercial taxes
    """
    min_unit = min(units)
    max_unit = max(units)
    d = (df[(df.parcelid.str[0] == city) &
                      (df["class"] == "C") &
                      (df.luc.isin(MF_CODES)) & 
                      (df.livunit.between(min_unit, max_unit))
            ].groupby("livunit").rtotapr.sum())

    x = [int(i) for i in d.index]
    plt.bar(x, d, tick_label=x)
    y_tick_fmt = lambda val, pos: "${0:.0f}M".format(val/1000000)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(y_tick_fmt))
    plt.xlabel("Number of Units")
    plt.ylabel("Total Appraised Value")
    plt.tight_layout()
    plt.savefig("../../reports/figures/total_appraisal_{}".format(city), dpi=300)

def format_label(max_value):
    """

    """

@main.command()
@click.argument("city", default="0")
@click.option("--rates")
@click.option("--units")
def stacked_area(city, rates, units):
    tot = current_revenue()
    all_taxes = []
    for unit in range(5, max(units)+5, 5):
        taxes = []
        for rate in rates:
            p_taxes = (df[(df["class"] == "C") &
                          (df.luc.isin(MF_CODES)) & 
                          (df.livunit.between(2,unit))].rtotapr.sum() * rate * MEMPHS_RATE
                      )

            c_taxes = (df[(df["class"] == "C") &
                          (df.luc.isin(MF_CODES)) & 
                          (df.livunit > unit)].rtotasmt.sum() * MEMPHS_RATE
                      )

            # diff = (tot - (p_taxes + c_taxes))/tot
            # taxes.append(diff)
            taxes.append(p_taxes+c_taxes)
        all_taxes.append(taxes)

@main.command()
@click.argument("city", default="0")
@click.argument("num_units", default=list(range(2,21)))
def appraisal_per_unit_bar(city, num_units):
    """
    generate bar chart displaying average total appraisal by number of living units
    """
    grp = df[(df.luc.isin(MF_CODES)) &
             (df["class"] == "C") &
             (df.livunit.between(min(num_units), max(num_units))) &
             (df.parcelid.str[0] == city)].groupby("livunit").rtotapr.mean()
    x = [int(i) for i in grp.index]
    plt.bar(x, grp, tick_label=x)
    y_tick_fmt = lambda val, pos: "${0:,.0f}".format(val)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(y_tick_fmt))
    plt.xlabel("Number of Living Units")
    plt.ylabel("Total Appraisal per Living Unit")
    plt.tight_layout()
    plt.savefig("../../reports/figures/bar_rtotapr_per_livunit.png", dpi=300)

@main.command()
def current_projected_revenue_comparison():
    df = pd.read_csv("../../data/processed/current_projected_tax.csv", index_col="rate")
    plt.plot(df.index, df.current_trends, label="Current Residential Distribution")
    plt.plot(df.index, df.mf_projections, label="Multi-family Projections")
    plt.legend()
    y_tick_fmt = lambda val, pos: "${0:,.0f}M".format(val/1000000)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(y_tick_fmt))
    plt.xlabel("Assessment Rates")
    plt.ylabel("Projected Revenue")
    plt.tight_layout()
    plt.savefig("../../reports/figures/current_projected_revenue_comparison.png", dpi=300)



@main.command()
@click.argument("city", default="0")
@click.option("--rates")
@click.option("--units")
def run_all(city, rates, units):
    """
    Generate all plots.
    """
    stacked_area(city, rates, units)
    projected_revenue_scatter(city)
    stacked_area(city, rates, units)
    appraisal_per_unit_bar(city, units)
    current_projected_revenue_comparison()

# def current_revenue(city="0"):
    # return df[(df.parcelid.str[0] == city) &
              # (df["class"] == "C") &
              # (df.luc.isin(MF_CODES)) & 
              # (df.livunit >= 2)].rtotasmt.sum() * TAX_RATES[city]

if __name__=="__main__":
    # projected_revenue_scatter(rates, units)
    main()


