# SPARC RAR Residual Environment Test

- Environment metric: `eenv`, the independent external gravitational field estimate from Chae et al. (2020)
- Residual sample loaded from: `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/sparc-rar-residuals/output/sparc_galaxy_mean_residuals.csv`
- Matched galaxies with environment data: 153
- Q<=2 galaxies without environment data in Chae et al. table: 10
- `eenv` range: 0.005 to 0.743
- `eenv` quartiles: 0.021, 0.026, 0.031

## Main Result

- Spearman residual vs `eenv`: rho = -0.116, p = 0.1536
- Partial Spearman controlling for distance: rho = -0.108, p = 0.1855
- Distance vs `eenv`: rho = -0.097, p = 0.2321

No statistically significant environmental dependence is detected.

## Binary Splits

- Median split in `eenv`: p = 0.4424, mean difference (high minus low) = -0.011 dex
- Quartile split in `eenv`: p = 0.09646, mean difference (high minus low) = -0.045 dex
- Quartile split 95% bootstrap CI on mean difference: [-0.118, +0.033] dex

## Robustness

- Q=1 only: rho = -0.197, p = 0.05798
- Q=2 only: rho = -0.018, p = 0.8924
- Excluding the 5 Chae rows with `x0 = L`: rho = -0.088, p = 0.2872
- Excluding the one extreme `eenv > 0.1` outlier: rho = -0.108, p = 0.1856

## Power

- Estimated power for a 0.05 dex shift with the median split Mann-Whitney test: 44.1%
- Estimated power for a 0.05 dex shift with the quartile split Mann-Whitney test: 26.5%

This means the continuous null test is reasonably informative, but the isolated-vs-dense binary comparison is underpowered for small (~0.05 dex) shifts.

## Missing Galaxies

F563-1, F563-V2, F568-1, F579-V1, NGC4214, UGC01230, UGC02023, UGC05999, UGC06628, UGC07608

## Conclusion

Within the 153 SPARC galaxies with published environment estimates, galaxies in denser environments do not show a statistically significant offset from the same RAR followed by more isolated galaxies.
This supports no detected environmental dependence in the present SPARC sample and environment metric.
