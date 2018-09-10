import numpy as np
import pytest
from scipy import stats

import statsmodels.api as sm


class BaseProbplotMixin(object):
    def setup(self):
        try:
            import matplotlib.pyplot as plt
            self.fig, self.ax = plt.subplots()
        except ImportError:
            pass
        self.other_array = np.random.normal(size=self.prbplt.data.shape)
        self.other_prbplot = sm.ProbPlot(self.other_array)

    @pytest.mark.requires_matplotlib
    def test_qqplot(self, close_figures):
        self.prbplt.qqplot(ax=self.ax, line=self.line)

    @pytest.mark.requires_matplotlib
    def test_ppplot(self, close_figures):
        self.prbplt.ppplot(ax=self.ax, line=self.line)

    @pytest.mark.requires_matplotlib
    def test_probplot(self, close_figures):
        self.prbplt.probplot(ax=self.ax, line=self.line)

    @pytest.mark.requires_matplotlib
    def test_qqplot_other_array(self, close_figures):
        self.prbplt.qqplot(ax=self.ax, line=self.line,
                           other=self.other_array)

    @pytest.mark.requires_matplotlib
    def test_ppplot_other_array(self, close_figures):
        self.prbplt.ppplot(ax=self.ax, line=self.line,
                           other=self.other_array)

    @pytest.mark.requires_matplotlib
    def t_est_probplot_other_array(self, close_figures):
        self.prbplt.probplot(ax=self.ax, line=self.line,
                             other=self.other_array)

    @pytest.mark.requires_matplotlib
    def test_qqplot_other_prbplt(self, close_figures):
        self.prbplt.qqplot(ax=self.ax, line=self.line,
                           other=self.other_prbplot)

    @pytest.mark.requires_matplotlib
    def test_ppplot_other_prbplt(self, close_figures):
        self.prbplt.ppplot(ax=self.ax, line=self.line,
                           other=self.other_prbplot)

    @pytest.mark.requires_matplotlib
    def t_est_probplot_other_prbplt(self, close_figures):
        self.prbplt.probplot(ax=self.ax, line=self.line,
                             other=self.other_prbplot)

    @pytest.mark.requires_matplotlib
    def test_qqplot_custom_labels(self, close_figures):
        self.prbplt.qqplot(ax=self.ax, line=self.line,
                           xlabel='Custom X-Label',
                           ylabel='Custom Y-Label')

    @pytest.mark.requires_matplotlib
    def test_ppplot_custom_labels(self, close_figures):
        self.prbplt.ppplot(ax=self.ax, line=self.line,
                           xlabel='Custom X-Label',
                           ylabel='Custom Y-Label')

    @pytest.mark.requires_matplotlib
    def test_probplot_custom_labels(self, close_figures):
        self.prbplt.probplot(ax=self.ax, line=self.line,
                             xlabel='Custom X-Label',
                             ylabel='Custom Y-Label')

    @pytest.mark.requires_matplotlib
    def test_qqplot_pltkwargs(self, close_figures):
        self.prbplt.qqplot(ax=self.ax, line=self.line,
                           marker='d',
                           markerfacecolor='cornflowerblue',
                           markeredgecolor='white',
                           alpha=0.5)

    @pytest.mark.requires_matplotlib
    def test_ppplot_pltkwargs(self, close_figures):
        self.prbplt.ppplot(ax=self.ax, line=self.line,
                           marker='d',
                           markerfacecolor='cornflowerblue',
                           markeredgecolor='white',
                           alpha=0.5)

    @pytest.mark.requires_matplotlib
    def test_probplot_pltkwargs(self, close_figures):
        self.prbplt.probplot(ax=self.ax, line=self.line,
                             marker='d',
                             markerfacecolor='cornflowerblue',
                             markeredgecolor='white',
                             alpha=0.5)


class TestProbPlotLongely(BaseProbplotMixin):
    def setup(self):
        np.random.seed(5)
        self.data = sm.datasets.longley.load(as_pandas=False)
        self.data.exog = sm.add_constant(self.data.exog, prepend=False)
        self.mod_fit = sm.OLS(self.data.endog, self.data.exog).fit()
        self.prbplt = sm.ProbPlot(self.mod_fit.resid, stats.t, distargs=(4,))
        self.line = 'r'
        super(TestProbPlotLongely, self).setup()


class TestProbPlotRandomNormalMinimal(BaseProbplotMixin):
    def setup(self):
        np.random.seed(5)
        self.data = np.random.normal(loc=8.25, scale=3.25, size=37)
        self.prbplt = sm.ProbPlot(self.data)
        self.line = None
        super(TestProbPlotRandomNormalMinimal, self).setup()


class TestProbPlotRandomNormalWithFit(BaseProbplotMixin):
    def setup(self):
        np.random.seed(5)
        self.data = np.random.normal(loc=8.25, scale=3.25, size=37)
        self.prbplt = sm.ProbPlot(self.data, fit=True)
        self.line = 'q'
        super(TestProbPlotRandomNormalWithFit, self).setup()


class TestProbPlotRandomNormalLocScale(BaseProbplotMixin):
    def setup(self):
        np.random.seed(5)
        self.data = np.random.normal(loc=8.25, scale=3.25, size=37)
        self.prbplt = sm.ProbPlot(self.data, loc=8.25, scale=3.25)
        self.line = '45'
        super(TestProbPlotRandomNormalLocScale, self).setup()


class TestTopLevel(object):
    def setup(self):
        self.data = sm.datasets.longley.load(as_pandas=False)
        self.data.exog = sm.add_constant(self.data.exog, prepend=False)
        self.mod_fit = sm.OLS(self.data.endog, self.data.exog).fit()
        self.res = self.mod_fit.resid
        self.prbplt = sm.ProbPlot(self.mod_fit.resid, stats.t, distargs=(4,))
        self.other_array = np.random.normal(size=self.prbplt.data.shape)
        self.other_prbplot = sm.ProbPlot(self.other_array)

    @pytest.mark.requires_matplotlib
    def test_qqplot(self, close_figures):
        sm.qqplot(self.res, line='r')

    @pytest.mark.requires_matplotlib
    def test_qqplot_pltkwargs(self, close_figures):
        sm.qqplot(self.res, line='r', marker='d',
                  markerfacecolor='cornflowerblue',
                  markeredgecolor='white',
                  alpha=0.5)

    @pytest.mark.requires_matplotlib
    def test_qqplot_2samples_ProbPlotObjects(self, close_figures):
        # also tests all values for line
        for line in ['r', 'q', '45', 's']:
            # test with `ProbPlot` instances
            sm.qqplot_2samples(self.prbplt, self.other_prbplot,
                               line=line)


    @pytest.mark.requires_matplotlib
    def test_qqplot_2samples_arrays(self, close_figures):
        # also tests all values for line
        for line in ['r', 'q', '45', 's']:
            # test with arrays
            sm.qqplot_2samples(self.res, self.other_array, line=line)
