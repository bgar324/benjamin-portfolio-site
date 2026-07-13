import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from peewee import CharField, DateTimeField, Model, MySQLDatabase, TextField
from playhouse.shortcuts import model_to_dict

from app.portfolio_data import (
    ABOUT_PARAGRAPHS,
    EDUCATION,
    EXPERIENCES,
    HOBBIES,
    LOCATIONS,
    NAV_ITEMS,
    PROFILE,
    PROJECTS,
    SOCIAL_LINKS,
)

load_dotenv()

app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=3306,
)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost])


@app.context_processor
def inject_site_data():
    return {
        "nav_items": NAV_ITEMS,
        "profile": PROFILE,
        "social_links": SOCIAL_LINKS,
        "url": os.getenv("URL"),
    }


@app.route("/benjamin/")
def benjamin():
    return index()


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=PROFILE["title"],
        about_paragraphs=ABOUT_PARAGRAPHS,
        experiences=EXPERIENCES,
        education=EDUCATION,
        hobbies=HOBBIES,
        locations=LOCATIONS,
        projects=PROJECTS,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title="Hobbies",
        hobbies=HOBBIES,
    )


@app.route("/projects")
def projects():
    return render_template(
        "projects.html",
        title="Projects",
        projects=PROJECTS,
    )


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline")


@app.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    timeline_post = TimelinePost.create(
        name=request.form["name"],
        email=request.form["email"],
        content=request.form["content"],
    )

    return model_to_dict(timeline_post), 201


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_posts():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())

    return {
        "timeline_posts": [
            model_to_dict(post)
            for post in posts
        ]
    }


if __name__ == "__main__":
    app.run(debug=True)
