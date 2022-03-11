import argparse
import os
import pandas as pd
import requests
import sqlalchemy
import warnings

from constants import Constants
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from io import StringIO
from pandas.core.common import SettingWithCopyWarning
from query import Query
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.types import String
from sqlalchemy.sql import text

load_dotenv()
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

parser = argparse.ArgumentParser()

parser.add_argument('--start_date', help='Start Date')
parser.add_argument('--end_date', help='End Date')
args = parser.parse_args()

current_date = datetime.now().strftime('%Y-%m-%d')
next_day_date = str(date.today() + timedelta(days=1))
jwt_token = os.getenv('VIMEO_JWT_TOKEN')

class VimeoAnalytics:

    def __init__(self, start_date, end_date):

        self.start_date = start_date
        self.end_date = end_date

        self.serverdb = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername='mysql+pymysql',
                username=os.getenv('TEST_MYSQL_USER'),
                password=os.getenv('TEST_MYSQL_PASSWORD'),
                database=os.getenv('TEST_MYSQL_DB'),
                host=os.getenv('TEST_MYSQL_HOST'),
                port=os.getenv('TEST_MYSQL_PORT')
                # query={
                #     'unix_socket': '/cloudsql/{}'.format(Constants.cloud_sql_connection_name)
                # }
            ),
        )

    def get_video_stats(self):
    
        try:
            vimeo_url = Constants.VIMEO_STATS_DOWNLOAD_URL.format(jwt_token=jwt_token, \
                start_date=self.start_date ,end_date=self.end_date)
            with requests.Session() as session:
                with session.get(vimeo_url) as response:
                    content = response.text
                    df = pd.read_csv(StringIO(content))
            self.process_data(df)
        except:
            print("Exception/Error has been raised")
        
    def process_data(self, vimeo_df):

        # cleaning and renaming the columns
        vimeo_df = vimeo_df.dropna()
        vimeo_df['date'] = self.start_date
        vimeo_df[['uri','video_id']] = vimeo_df['uri'].str.split('/videos/',expand=True)
        vimeo_df = vimeo_df.rename(columns={
            'created_time': 'video_created_at'
        })
        vimeo_df['identifier'] = vimeo_df['date'].astype(str) + '-' + vimeo_df['video_id'].astype(str)

        # fetch data from the table
        df = pd.read_sql(Query.GET_VIMEO_STATS, self.serverdb)
        df['identifier'] = df['date'].astype(str) + '-' + df['video_id'].astype(str)

        # creating an is_exists col to check whether this identifier exists in db
        vimeo_df = vimeo_df.assign(is_exists=vimeo_df.identifier.isin(df.identifier).astype(int))

        exists_df = vimeo_df[vimeo_df['is_exists'] == 1]
        not_exists_df = vimeo_df[vimeo_df['is_exists'] == 0]

        self.insert_and_update_data(exists_df, not_exists_df)

    def insert_and_update_data(self, exists_df, not_exists_df):

        # update vimeo stats
        with self.serverdb.connect() as conn:
            for index, row in exists_df.iterrows():
                sql = text(Query.UPDATE_VIMEO_STATS).bindparams(bindparam("plays"), bindparam("loads"),
                            bindparam("downloads"), bindparam("finishes"), bindparam("likes"), bindparam("comments"), \
                            bindparam("unique_loads"), bindparam("mean_seconds"), bindparam("mean_percent"), \
                            bindparam("sum_seconds"), bindparam("unique_viewers"), bindparam("video_id", String), \
                            bindparam("date", String))
                
                conn.execute(sql, plays=row['plays'], loads=row['loads'], downloads=row['downloads'], finishes=row['finishes'], \
                    likes=row['likes'], comments=row['comments'], unique_loads=row['unique_loads'], mean_seconds=row['mean_seconds'], \
                    mean_percent=row['mean_percent'], sum_seconds=row['sum_seconds'], unique_viewers=row['unique_viewers'], \
                    video_id=row['video_id'], date=row['date'])

        conn.close()

        # insert vimeo stats
        required_cols = ['date', 'video_id', 'name', 'plays', 'loads', 'downloads', 'finishes', 'likes', 'comments', \
            'unique_loads', 'mean_seconds', 'mean_percent', 'sum_seconds', 'unique_viewers', 'video_created_at']
        not_exists_df[required_cols].to_sql('vimeo_video_stats', con=self.serverdb, if_exists='append', \
            index=False, method='multi')


if __name__ == "__main__":
    vimeo = VimeoAnalytics(
        args.start_date if args.start_date else current_date,
        args.end_date if args.end_date else next_day_date
    )
    vimeo.get_video_stats()