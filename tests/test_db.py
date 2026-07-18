import os
import unittest

from peewee import SqliteDatabase

os.environ["TESTING"] = "true"

from app import TimelinePost


MODELS = [TimelinePost]


class TimelinePostDatabaseTests(unittest.TestCase):
    """Exercise Peewee model reads and writes against an isolated database."""

    def setUp(self):
        self.test_db = SqliteDatabase(":memory:")
        self.original_database = TimelinePost._meta.database
        self.test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        self.test_db.connect()
        self.test_db.create_tables(MODELS)

    def tearDown(self):
        self.test_db.drop_tables(MODELS)
        self.test_db.close()
        TimelinePost._meta.set_database(self.original_database)

    def test_timeline_posts_are_saved_and_retrieved(self):
        first_post = TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello world, I'm John!",
        )
        second_post = TimelinePost.create(
            name="Jane Doe",
            email="jane@example.com",
            content="Hello world, I'm Jane!",
        )

        posts = list(TimelinePost.select().order_by(TimelinePost.id))

        self.assertEqual([post.id for post in posts], [first_post.id, second_post.id])
        self.assertEqual([post.name for post in posts], ["John Doe", "Jane Doe"])
        self.assertEqual(posts[1].content, "Hello world, I'm Jane!")
