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
            # print(path)
            # print(seperator)
            df = pd.read_csv(filepath_or_buffer=path, sep=seperator)
            shape = df.shape
            # print(df.head())
            logging.log(20, f"Successfully read file : '{path}' and it contains '{shape[0]} Row(s)' and '{shape[1]} Column(s)")
            return df
        except Exception as e:
            logging.log(40,f"Exception occurred while reading the file : {e}")
            return None

if __name__ == "__main__":
    logging.basicConfig(filename='analysis_app.log', level=logging.DEBUG, filemode='a',
                        format='%(asctime)s %(levelname)s - %(message)s')

    # Create an object of class
    populatio_analysis = Population_Analysis(logging)

    # calling read_csv method of class
    df = populatio_analysis.read_csv("https://ddbj.nig.ac.jp/public/mirror_database/1000genomes/20131219.populations.tsv","\t")
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
    logging.log(20,f"Question 1 - Average of 'Phase1 Samples' : {int(phase_1_sample_avg)}")

    # Check if average was calculated
    assert phase_1_sample_avg != 0, "Failed to calculate average of 'Phase1 Samples'. Check analysis_app.log for exception."

    # calculate the total of
    final_phase_sample_total = df["Final Phase Samples"].sum()
    logging.log(20,f"Question 2 - Total of 'Final Phase Samples' : {final_phase_sample_total}")
    assert final_phase_sample_total != 0, "Failed to calculate Total of 'Final Phase Samples'. Check analysis_app.log for exception."

    # Since there are no description about dataset. I am assuming 1st column is the only field from where I can extract the country details
    df["Countries"] = df["Population Description"].apply(lambda x: str(x).split(' in ')[-1].split(',')[-1])
    df["Countries"] = df["Countries"].apply(lambda x: str(x).strip().lower())
    # most_repeated_countries = df.groupby("Countries").size()
    most_repeated_countries = df["Countries"].value_counts()
    logging.log(20,f"Question 3 - Top 5 Most repeated countries : \n{most_repeated_countries.head(5)}")
