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
        return df.to_json(orient='records'), int(df['totale_positivi'][0])

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

    # AFRO 8
    @staticmethod
    def chad(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Chad'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def eswatini(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Eswatini'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def lesotho(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Lesotho'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def malawi(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Malawi'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def mali(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Mali'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def mauritius(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Mauritius'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def namibia(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Namibia'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def nigerr(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Niger'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def seychelles(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Seychelles'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def zimbabwe(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Zimbabwe'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def uganda(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Uganda'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])

    @staticmethod
    def botswana(df):
        df.reset_index(inplace=True)
        local = df[df['Name'] == 'Botswana'].iloc[0]
        return ','.join(map(str, local.to_list())), int(local['Cases - cumulative total'])
