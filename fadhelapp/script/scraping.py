import twint
import datetime
def twint_to_pandas(columns):
    return twint.output.panda.Tweets_df[columns]
def scrap(query,awal,akhir,limit):
    # Set up TWINT config
    c = twint.Config()
    c.Search = query + " " + "since:" + awal + " until:" + akhir
    c.Format = "Username: {username} |  Tweet: {tweet}"
    c.Limit = limit
    c.Pandas = True
    print(twint.run.Search(c))
    df_pd = twint_to_pandas(["date", "username", "tweet", "link"])
    return df_pd
