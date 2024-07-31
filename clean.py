def clean_data(df):
    """
    Clean the data in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to be cleaned.    
    
    Returns
    -------
    df : pandas.DataFrame
        The cleaned DataFrame.
    """
    df.rename(columns={'State Name': 'State', 'Investment Dollars': 'Investment'}, inplace=True)
    df['Investment'] = df['Investment'].str.replace(',', '').astype(int)
    df.loc[df['City'] == 'City Name Withheld', 'City'] = 'Unknown'
    return df