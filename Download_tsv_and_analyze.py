import pandas as pd
import logging

class Population_Analysis():

    def __init__(self,logging):
        self.logging = logging

    def read_csv(self,path : str, seperator : str) -> pd.DataFrame:
        """
        This method read csv from specified path
        This accepts 2 parameters
        1 - Path of the csv/tsv
        2 - the seperator
        :return: After reading the data it will return the pandas DataFrame and in failure it will return None
        """
        try:
            print(path)
            print(seperator)
            df = pd.read_csv(filepath_or_buffer=path, sep=seperator)
            shape = df.shape
            # print(df.head())
            logging.log(20, f"Successfully read file : '{path}' and it contains '{shape[0]} Row(s)' and '{shape[1]} Column(s)")
            return df
        except Exception as e:
            logging.log(40,f"Exception occurred while reading the file : {e}")
            return None

    # def get_average(self, dataframe : pd.DataFrame, list_of_columns : list) -> float:
    #     """
    #     This method calculates the average on series
    #     This method accepts 2 parameters
    #     1 - dataframe
    #     2 - column name of which we need to calculate average
    #     :return: calculated average and in case of failure it will return 0
    #     """
    #     try:
    #         avg = dataframe[list_of_columns].mean()
    #         logging.log(20,f"Successfully calculated average of column(s) : {list_of_columns}")
    #         logging.log(20,f'\n{avg}')
    #         return avg
    #     except Exception as e:
    #         logging.log(40,f"Exception occurred while calculating the average : {e}")
    #         return None

if __name__ == "__main__":
    logging.basicConfig(filename='analysis_app.log', level=logging.DEBUG, filemode='w',
                        format='%(asctime)s %(levelname)s - %(message)s')

    # Create an object of class
    populatio_analyis = Population_Analysis(logging)

    # calling read_csv method of class
    df = populatio_analyis.read_csv("https://ddbj.nig.ac.jp/public/mirror_database/1000genomes/20131219.populations.tsv","\t")
    # Check if dataframe is not null
    assert df is not None, "Failed to read csv, Dataframe should not be None. Check analysis_app.log for exception."

    # Only last 3 rows contains Nan values. Last 2 rows are NaN and 3rd last row is a calculation, which is not an actual data
    df.dropna(how="any", inplace=True)

    # Convert the datatype of few columns
    df["Pilot Samples"] = df["Pilot Samples"].astype('int')
    df["Phase1 Samples"] = df["Phase1 Samples"].astype('int')
    df["Final Phase Samples"] = df["Final Phase Samples"].astype('int')
    df["Total"] = df["Pilot Samples"].astype('int')

    # calculate average of column 'Phase1 Samples'
    phase_1_sample_avg = df["Phase1 Samples"].mean()
    logging.log(20,f"Average of 'Phase1 Samples' : {int(phase_1_sample_avg)}")

    # Check if average was calculated
    assert phase_1_sample_avg != 0, "Failed to calculate average of 'Phase1 Samples'. Check analysis_app.log for exception."

    # calculate the total of
    final_phase_sample_total = df["Final Phase Samples"].sum()
    logging.log(20,f"Total of 'Final Phase Samples' : {final_phase_sample_total}")
    assert final_phase_sample_total != 0, "Failed to calculate Total of 'Final Phase Samples'. Check analysis_app.log for exception."

    #
