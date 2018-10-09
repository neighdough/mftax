Schema Information
===========================

Connection Information
---------------------------
All data created as part of the analysis is stored in the `mftax` schema within the `blight_data` database on caeser-midt.memphis.edu

Table definitions
---------------------------

1. asmt
    * Table containing all of the relevant assessment information used to perform analysis
2. livunits
    * Contains a list of the number of living units used throughout the analysis. Created from the `set_units_and_rates` method in `make_dataset.py` module.
3. revenue_estimates
    * Contains estimated revenue based upon the number of living units and tax rates established previously. Generated from `build_tax_estimate` method in `make_dataset.py` module.
4. tax_rates
    * Contains a list of the tax rates to be used in the analysis. Created from the `set_units_and_rates` method in `make_dataset.py` module.
