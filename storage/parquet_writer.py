import os
import pandas as pd
from datetime import datetime

def write_tweets_to_parquet(tweets, output_dir="data/processed"):
    if not tweets:
        print("[WARN] No tweets to store")
        return

    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(tweets)

    if "scraped_at" not in df.columns:
        df["scraped_at"] = datetime.utcnow().isoformat()

    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

    output_path = os.path.join(
        output_dir,
        f"tweets_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.parquet"
    )

    df.to_parquet(output_path, index=False)
    print(f"[INFO] Parquet written to {output_path}")
