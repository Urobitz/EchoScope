def get_review_mean(db):
    query = """
    SELECT
        app_id,
        COUNT(*) AS total_reviews,
        AVG(voted_up) * 100 AS recommendation_rate
    FROM reviews
    GROUP BY app_id;
    """

    cursor = db.get_db_cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    return results