import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime


def write_tweets_to_parquet(tweets: list, base_dir: str = "data/tweets"):

    if not tweets:
        return

    df= pd.DataFrame(tweets)

    df["timestamp"]= pd.to_datetime(df["timestamp"], errors="coerce")
    df["scraped_at"]= pd.to_datetime(df["scraped_at"], errors="coerce")

    scrape_date= datetime.utcnow().strftime("%Y-%m-%d")
    output_dir= os.path.join(base_dir, f"date={scrape_date}")
    os.makedirs(output_dir, exist_ok=True)

    table= pa.Table.from_pandas(df, preserve_index=False)

    file_path= os.path.join(output_dir, f"tweets_{int(datetime.utcnow().timestamp())}.parquet")

    pq.write_table(table, file_path, compression="snappy")

    print(f"Stored {len(df)} tweets to {file_path}")
