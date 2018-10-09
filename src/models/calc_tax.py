"""
Input:
    millage_rate (float):
    num_unit (int)
    
"""


from sqlalchemy import create_engine
import numpy as np


COUNTY_RATE = 0.0405
MEMPHS_RATE = 0.03195986
MILL_RATE = {"C": .4, "R": .25, "I": .4, "E": 0, "A": .25}
MF_CODES = ["002", "003", "059", "061", "067"]

def current_revenu():
    pass

def predict_

if __name__=="__main__":
    rates = np.linspace(.25, .375, 6)
    units = range(2, 21, 1)
    p_rates = []
    p_units = []
    taxes = []
    for rate, unit in itertools.product(rates, units):
        p_taxes = (t[(t.luc.isin(MF_CODES)) & 
                  (t.livunit.between(2,unit))].rtotapr.sum() * rate * MEMPHS_RATE
                  )

        c_taxes = (t[(t.luc.isin(MF_CODES)) & 
                  (t.livunit > unit)].rtotasmt.sum() * MEMPHS_RATE
                  )
        taxes.append(p_taxes + c_taxes)
        p_units.append(unit)
        p_rates.append(rate)
        ax.scatter(rate, p_taxes + c_taxes, c=rate, label=rate, s=.8)
    x = p_rates.copy()
    x[0] = .22
    x[-1] = .4
    y = [tot for i in range(len(p_rates))]
    plt.scatter(p_rates, taxes, c=p_units, cmap='tab20c', label=list(units))
    bar = plt.colorbar(label="Number of Living Units")
    bar.ax.tick_params(width=0)
    plt.scatter(.4, tot, marker="*", c="g", s=60)
    plt.text(.4, tot-250000, "Current Revenue\n${0:.1f}M".format(tot/1000000),
            horizontalalignment="center", fontsize=7.5)

    # plt.plot(x,y, label="Current Revenue")
    # ax.legend()
    y_tick_fmt = lambda val, pos: "${0:.1f}M".format(val/1000000)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(tick.FuncFormatter(y_tick_fmt))
    plt.ylabel("Estimated Tax Revenue")
    plt.xlabel("Assessment Rate")
    plt.xlim(.23, .425)
    plt.tight_layout()




        

