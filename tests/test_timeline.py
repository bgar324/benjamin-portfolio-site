import importlib
import unittest
from unittest.mock import patch

import peewee


class InMemoryMySQLDatabase(peewee.SqliteDatabase):
    """SQLite-backed stand-in that keeps tests isolated from local MySQL."""

    def __init__(self, database, **kwargs):
        super().__init__(":memory:")


with patch.object(peewee, "MySQLDatabase", InMemoryMySQLDatabase):
    application = importlib.import_module("app")


class TimelinePageTests(unittest.TestCase):
    def setUp(self):
        application.app.config.update(TESTING=True)
        self.client = application.app.test_client()
        application.TimelinePost.delete().execute()

    def test_timeline_page_includes_form_and_post_container(self):
        response = self.client.get("/timeline")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="timeline-form"', response.data)
        self.assertIn(b'action="/api/timeline_post"', response.data)
        self.assertIn(b'id="timeline-posts"', response.data)

    def test_post_is_created_and_returned_by_api(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "content": "Built a timeline today.",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Ada Lovelace")
        self.assertEqual(application.TimelinePost.select().count(), 1)

    def test_get_returns_posts_in_descending_order(self):
        older = application.TimelinePost.create(
            name="Older",
            email="older@example.com",
            content="First post",
            created_at="2026-01-01 09:00:00",
        )
        newer = application.TimelinePost.create(
            name="Newer",
            email="newer@example.com",
            content="Second post",
            created_at="2026-01-02 09:00:00",
        )

        response = self.client.get("/api/timeline_post")
        posts = response.get_json()["timeline_posts"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual([post["id"] for post in posts], [newer.id, older.id])


if __name__ == "__main__":
    unittest.main()
