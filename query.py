class Query:

    GET_VIMEO_STATS = """ select * from vimeo_video_stats """

    UPDATE_VIMEO_STATS = """ update vimeo_video_stats set plays = :plays, loads = :loads, downloads = :downloads, finishes = :finishes,
                            likes = :likes, comments = :comments, unique_loads = :unique_loads, mean_seconds = :mean_seconds,
                            mean_percent = :mean_percent, sum_seconds = :sum_seconds, unique_viewers = :unique_viewers
                            where video_id = :video_id and date = :date """