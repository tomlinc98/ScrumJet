from flask import Blueprint, render_template, redirect, url_for, request
from flask_paginate import Pagination, get_page_args
from app.models import User, Announcement, Category, Course

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    announcements = Announcement.query.order_by(Announcement.created_at).all()
    return render_template('index.html',  title='Home', announcements=announcements)

@main.route('/courses', methods=['GET', 'POST'])
@main.route('/courses/<cat>', methods=['GET', 'POST'])
def courses(cat=None):
    page = int(request.args.get('page', 1))
    per_page = 8
    offset = (page - 1) * per_page

    courses = Course.query.order_by(Course.title.asc())
    categories = [cat.name for cat in Category.query.all()]
    if cat is not None:
        courses = [c.courses.order_by(Course.title.asc()) for c in Category.query.filter_by(name=cat)][0]

    courses_for_render = courses.limit(per_page).offset(offset)
    search =False
    q = request.args.get('q')
    if q:
        search=True
    pagination = Pagination(
        page=page, 
        per_page=per_page,
        offset=offset,
        total=courses.count(),
        css_framework='bootstrap3',
        search=search
        )

    return render_template('courses.html', courses=courses_for_render,
    pagination=pagination, categories=categories, title='Courses')

@main.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html',  title='FAQ')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html',  title='Contact')

@main.route('/sitemap', methods=['GET', 'POST'])
def sitemap():
    return render_template('sitemap.html',  title='Sitemap')    

@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html',  title='About')

@main.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html',  title='Blog')

@main.route('/blog-form', methods=['GET', 'POST'])
def blogform():
    return render_template('blog-form.html',  title='Blog Form')

@main.route('/terms', methods=['GET', 'POST'])
def terms():
    return render_template('legal/terms.html',  title='Terms & Conditions')

@main.route('/policy', methods=['GET', 'POST'])
def policy():
    return render_template('legal/policy.html',  title='Privacy Policy')

@main.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html',  title='Admin')

"""@app.route("/courses/<int:course_id>")
def pet_details(pet_id):
    # View function for Showing Details of Each Pet. # 
    pet = next((pet for pet in pets if pet["id"] == pet_id), None) 
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet = pet) """