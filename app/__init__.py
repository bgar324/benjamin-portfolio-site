import os
from flask import Flask, render_template
from dotenv import load_dotenv
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


@app.context_processor
def inject_site_data():
    return {
        "nav_items": NAV_ITEMS,
        "profile": PROFILE,
        "social_links": SOCIAL_LINKS,
        "url": os.getenv("URL"),
    }


@app.route('/')
@app.route('/benjamin/')
def index():
    return render_template(
        'index.html',
        title=PROFILE["title"],
        about_paragraphs=ABOUT_PARAGRAPHS,
        experiences=EXPERIENCES,
        education=EDUCATION,
        hobbies=HOBBIES,
        locations=LOCATIONS,
        projects=PROJECTS,
    )


@app.route('/hobbies')
def hobbies():
    return render_template(
        'hobbies.html',
        title="Hobbies",
        hobbies=HOBBIES,
    )


@app.route('/projects')
def projects():
    return render_template(
        'projects.html',
        title="Projects",
        projects=PROJECTS,
    )
