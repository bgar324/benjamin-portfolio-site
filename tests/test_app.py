import os
import unittest

os.environ["TESTING"] = "true"

from app import TimelinePost, app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        TimelinePost.delete().execute()

    def test_home_page_renders_profile_and_navigation(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Benjamin Garcia", html)
        self.assertIn('href="/timeline"', html)
        self.assertIn("Selected Projects", html)

    def test_timeline_api_creates_and_returns_posts(self):
        created = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "content": "Built a timeline today.",
            },
        )

        self.assertEqual(created.status_code, 201)
        self.assertTrue(created.is_json)
        self.assertEqual(created.get_json()["name"], "Ada Lovelace")

        response = self.client.get("/api/timeline_post")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        posts = response.get_json()["timeline_posts"]
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["content"], "Built a timeline today.")

    def test_timeline_page_includes_composer_and_post_feed(self):
        response = self.client.get("/timeline")

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('id="timeline-form"', html)
        self.assertIn('action="/api/timeline_post"', html)
        self.assertIn('id="timeline-posts"', html)

    def test_malformed_timeline_posts_return_helpful_errors(self):
        invalid_posts = (
            (
                {"email": "john@example.com", "content": "Hello world, I'm John!"},
                b"Invalid name",
            ),
            (
                {"name": "John Doe", "email": "john@example.com", "content": ""},
                b"Invalid content",
            ),
            (
                {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"},
                b"Invalid email",
            ),
        )

        for post_data, error_message in invalid_posts:
            with self.subTest(post_data=post_data):
                response = self.client.post("/api/timeline_post", data=post_data)

                self.assertEqual(response.status_code, 400)
                self.assertIn(error_message, response.data)
                self.assertEqual(TimelinePost.select().count(), 0)
