import pandas as pd


def transform_data(file_path):
    df = pd.DataFrame(file_path)
    df.drop_duplicates(inplace=True)
    return df
    

def main():
    transform_data()
