# nexsci
Tools to query data from [NExSci](https://exoplanetarchive.ipac.caltech.edu) database using the [API](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html).

## Installation
```shell
$ git clone git@github.com:jpdeleon/nexsci.git
```

Create a new conda environment and install
```shell
$ conda create -n test && source activate test
(test) $ cd nexsci
(test) $ pip install .
```
## Scripts
```shell
(test) $ query_transit_params WASP-4
Querying WASP-1...

Main reference: Maciejewski et al. 2014
Discovery reference: Collier Cameron et al. 2007

See meaning of columns here:
https://exoplanetarchive.ipac.caltech.edu/docs/API_exoplanet_columns.html

                    value          err1          err2  unit
pl_imppar    0.000000e+00  1.200000e-01 -1.200000e-01     -
pl_orbeccen  0.000000e+00           NaN           NaN     -
pl_orbincl   9.000000e+01  1.300000e+00 -1.300000e+00   deg
pl_orbper    2.519945e+00  5.000000e-07 -5.000000e-07     d
pl_trandep            NaN           NaN           NaN     %
pl_trandur            NaN           NaN           NaN     d
pl_tranmid   2.453913e+06  2.700000e-04 -2.700000e-04    JD
Rp/Rs        1.036715e-01  2.191888e-03 -3.182085e-03     -
a/Rs         5.688844e+00  1.095506e-01 -1.577400e-01     -

(test) $ query_summary WASP-2
Querying WASP-2...

Main reference: Torres et al. 2008
Discovery reference: Collier Cameron et al. 2007

See meaning of columns here:
https://exoplanetarchive.ipac.caltech.edu/docs/API_exoplanet_columns.html

                   value      err1       err2        unit
pl_eqt       1304.000000   54.0000  -54.00000           K
pl_imppar       0.724000    0.0170   -0.02800           -
pl_insol             NaN       NaN        NaN  Earth flux
pl_massj        0.915000    0.0900   -0.09300        Mjup
pl_orbeccen          NaN       NaN        NaN           -
pl_orbincl     84.810000    0.3500   -0.27000         deg
pl_orbper       2.152226       NaN        NaN           d
pl_orbsmax      0.031380    0.0013   -0.00154          au
pl_radj         1.071000    0.0800   -0.08300        Rjup
st_dens         2.050000    0.2600   -0.15000       g/cm3
st_logg         4.540000    0.0400   -0.05000  log(cm/s2)
st_metfe        0.100000    0.2000   -0.20000        Fe/H
st_rad          0.840000    0.0600   -0.07000        Rsun
st_teff      5200.000000  200.0000 -200.00000           K

(test) $ query_summary WASP-3

	param				value
1         dec                         35.6615
2     st_nglc                               0
3     st_elon                         283.573
4     pl_name                         ASP-3 b
...
```
See also notebook/NExSci.ipynb for other examples.
