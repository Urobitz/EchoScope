import requests
import math
from math import ceil
from validators import verify_Json


def fetch_website(url, params):
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()

        response = r.json()
        verify_Json(response)

        return response

    except requests.exceptions.RequestException as e:
        print("Failed to fetch website due to the following error: \n e")


def get_reviews(url, instance, database):  # Temporal prototype
    total_reviews_obtained = 0
    reviews_per_page = instance.get_num_per_page()
    next_page_cursor = ""

    for page_number in range(
        math.ceil(instance.get_review_limit() / reviews_per_page)
    ):
        remaining = instance.get_review_limit() - total_reviews_obtained

        instance.get_params()["num_per_page"] = min(
            instance.get_params()["num_per_page"], remaining
        )

        reviews_data = fetch_website(url, instance.get_params())

        next_page_cursor = reviews_data["response"]["cursor"]

        total_reviews_obtained += reviews_data["response"]["query_summary"]["num_reviews"]

        reviews = [
            (
                review["recommendationid"],
                instance.get_appID(),
                review["review"],
                review["voted_up"],
                review["author"]["playtime_at_review"],
                review["author"]["playtime_forever"],
                review["received_for_free"],
            )
            for review in reviews_data["response"]["reviews"]
        ]

        database.get_db_cursor().executemany(
            """
            INSERT INTO reviews (
                review_id,
                app_id,
                review_text,
                voted_up,
                playtime_at_review,
                playtime_forever,
                received_for_free
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(review_id) DO NOTHING
            """,
            reviews,
        )

        instance.set_cursor(next_page_cursor)

    database.get_db_connection().commit()