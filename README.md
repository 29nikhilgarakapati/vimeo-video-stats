
# Vimeo video stats

This automation would fetch the data from the video analytics section and push it to the database.

Click here to download the table structure => [sql table structure](https://github.com/29nikhilgarakapati/vimeo-video-stats/blob/main/db_table/vimeo_video_stats.sql)

## Environment Variables

To run this project, you will need to add the environment variables present in **.sample.env** to your **.env** file.

## Installation

To install the requirements

```bash
  pip install -r requirements.txt
```
## Running Tests

To run tests, run the following command

```bash
  python main.py
```

To pass date arguments
```bash
  python main.py --start_date=yyyy-mm-dd --end_date=yyyy-mm-dd
```

