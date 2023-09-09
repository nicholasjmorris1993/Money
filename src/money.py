import re
import math
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot


def stream(balance: float, income: list, expenses: list, noise: float, periods: int):

    flow = Stream()
    flow.cash_flow(balance, income, expenses, noise, periods)
    flow.simulate()
    flow.savings()
    flow.plots()

    return flow

class Stream:
    def cash_flow(self, balance, income, expenses, noise, periods):
        self.noise = noise
        self.periods = periods

        # expand the cash flow for so many periods
        repeat = math.ceil(self.periods / len(income))
        income = np.tile(income, repeat)[:self.periods]
        income[0] = income[0] + balance
        repeat = math.ceil(self.periods / len(expenses))
        expenses = np.tile(expenses, repeat)[:self.periods]

        self.data = pd.DataFrame({
            "Period": np.arange(self.periods) + 1, 
            "Income": income, 
            "Expenses": expenses,
        })

    def simulate(self):
        # simulate random increases in expenses
        np.random.seed(0)
        increase = np.random.uniform(low=self.noise / 2, high=self.noise, size=self.periods) + 1
        self.data["Expenses"] *= increase

    def savings(self):
        self.data["Savings"] = self.data["Income"] - self.data["Expenses"]
        self.data["Total Savings"] = self.data["Savings"].cumsum()

    def plots(self):
        # plot savings
        self.histogram(
            self.data,
            x="Savings",
            bins=20,
            title="Savings Histogram",
            font_size=16,
        )
        self.line_plot(
            self.data,
            x="Period",
            y="Savings",
            title="Savings Over Time",
            font_size=16,
        )
        self.bar_plot(
            self.data,
            x="Period",
            y="Total Savings",
            title="Total Savings Over Time",
            font_size=16,
        )

    def line_plot(self, df, x, y, color=None, title="Line Plot", font_size=None):
        fig = px.line(df, x=x, y=y, color=color, title=title)
        fig.update_layout(font=dict(size=font_size))
        title = re.sub("[^A-Za-z0-9]+", "", title)
        plot(fig, filename=f"{title}.html")

    def bar_plot(self, df, x, y, color=None, title="Bar Plot", font_size=None):
        fig = px.bar(df, x=x, y=y, color=color, title=title)
        fig.update_layout(font=dict(size=font_size))
        title = re.sub("[^A-Za-z0-9]+", "", title)
        plot(fig, filename=f"{title}.html")

    def histogram(self, df, x, bins=20, vlines=None, title="Histogram", font_size=None):
        bin_size = (df[x].max() - df[x].min()) / bins
        fig = px.histogram(df, x=x, title=title)
        if vlines is not None:
            for line in vlines:
                fig.add_vline(x=line)
        fig.update_traces(xbins=dict( # bins used for histogram
                size=bin_size,
            ))
        fig.update_layout(font=dict(size=font_size))
        title = re.sub("[^A-Za-z0-9]+", "", title)
        plot(fig, filename=f"{title}.html")
