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
    * Contains a list of the number of living units used throughout the analysis. Created from the `table_tax_rates_livunits` method in `make_dataset.py` module.
3. revenue_estimates
    * Contains estimated revenue based upon the number of living units and tax rates established previously. Generated from `table_revenue_estimate` method in `make_dataset.py` module.
4. tax_rates
    * Contains a list of the tax rates to be used in the analysis. Created from the `table_tax_rates_livunits` method in `make_dataset.py` module.
5. mdn_apr_by_luc
    * Median total appraisal by Census tract and land use code. Used to estiamte projected revenue
6. vacancy_by_zoning
    * Total number of vacant units within eac
