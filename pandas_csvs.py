import pandas as pd

class Csv:
    @staticmethod
    def austria(df):
        max_date = df['Datum'].max()
        df = df[df['Datum'] == max_date]
        total = df[df['Name'] == 'Österreich']['BestaetigteFaelleEMS']
        assert len(total) == 1
        return max_date, int(total)

    @staticmethod
    def italy(df):
        return df.to_json(orient='index'), int(df['totale_positivi'][0])

    @staticmethod
    def malta(df):
        recent_total = list(df[df['Date'] == df['Date'].max()]['Total Cases'])
        recent_total = [str(cases) for cases in recent_total]
        return ' '.join(recent_total), int(df['Total Cases'].max())

    @staticmethod
    def netherlands(df):
        return df['Date_of_report'].max(), int(df['Total_reported'].sum())

    @staticmethod
    def slovakia(df):
        total = \
            df[
                df['Datum'] == df['Datum'].max()
            ]['Pocet.potvrdenych.PCR.testami'].sum()
        return df['Datum'].max(), int(total)
