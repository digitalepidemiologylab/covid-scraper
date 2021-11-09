import pandas as pd

class Csv:
    @staticmethod
    def malta(df):
        recent_total = list(df[df['Date'] == df['Date'].max()]['Total Cases'])
        recent_total = [str(cases) for cases in recent_total]
        return ' '.join(recent_total), int(df['Total Cases'].max())

    @staticmethod
    def netherlands(df):
        return df['Date_of_report'].max(), int(df['Total_reported'].sum())
