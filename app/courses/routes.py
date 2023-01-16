from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.courses.forms import AddCourseForm, EditCourseForm, ReviewForm, CategoryForm, EditCategoryForm
from app.models import Course, Category, Review
from app.funcs import save_picture
from app import db
from sqlalchemy.sql import func, or_
from flask_login import current_user, login_user, logout_user, login_required

courses = Blueprint('courses', __name__)

@courses.route('/all_courses')
def all_courses():
    return 'All courses page'

@courses.route('/new_course', methods=['GET', 'POST'])
@login_required
def new_course():
    form = AddCourseForm()
    form.category_id.choices = [(c.id, c.name.title()) for c in Category.query.all()]
    if form.validate_on_submit():
        image_file = 'default.jpg'
        if form.image.data:
            image_file = save_picture(form.image.data)
  
        course = Course(
            title=form.title.data,
            summary=form.summary.data,
            image=image_file,
            price=form.price.data,
            category_id=form.category_id.data
        )
        db.session.add(course)
        db.session.flush()
        new_id = course.id
        db.session.commit()
        flash('Course was added successfully', 'success')
        return redirect(url_for('courses.course', id=new_id))
    return render_template('courses/new_course.html', title='Add course', form=form)

@courses.route('/course/<id>', methods=['GET', 'POST'])
def course(id):
    course = Course.query.get(id)
    form = ReviewForm()
    temp = db.session.query(func.avg(Review.rating).label('average')).filter(Review.course_id == id)
    if temp[0].average:
        avg = round(temp[0].average, 2) 
    else: 
        avg = 0

    if form.validate_on_submit():
        rev = Review.query.filter_by(course_id=id, user_id=current_user.get_id()).count()
        if rev != 0:
            flash("Can't review a course twice. Please edit/update your previous review", "warning")
        else:
            review = Review(
                rating = round(form.rating.data, 2),
                text = form.text.data,
                user_id = current_user.get_id(),
                course_id = id
            )
            flash("Review has been added", "success")
            db.session.add(review)
            db.session.commit()
        return redirect(url_for('courses.course', id=id))
    return render_template('courses/course.html', title=course.title.title(), course=course, form=form, average=avg)

@courses.route('/course/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    course = Course.query.get(id)
    form = EditCourseForm(obj=course)
    form.category_id.choices = [(c.id, c.name.title()) for c in Category.query.all()]
    if request.method == 'GET':
        form.populate_obj(course)
    elif request.method == 'POST':
        if form.update.data and form.validate_on_submit():
            course.title = form.title.data
            course.summary = form.summary.data
            if form.image.data:
                course.image = save_picture(form.image.data)
            course.price = form.price.data
            course.category_id = form.category_id.data

            db.session.commit()
            flash ('Update was successful', 'success')
            return redirect(url_for('courses.course', id=id))
        if form.cancel.data:
            return redirect(url_for('courses.course', id=id))
    return render_template('courses/edit_course.html', title='Edit course', form=form)

@courses.route('/course/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_course(id):
    if Course.query.filter_by(id=id).delete():
        db.session.commit()
        flash ('Course has been deleted', 'success')
        return redirect(url_for('main.courses'))
    return redirect(url_for('courses.course', id=id))  

@courses.route('/course/<id>/edit_review', methods=['GET', 'POST'])
@login_required
def edit_review(id):
    review = Review.query.filter_by(course_id=id, user_id=current_user.get_id())[0]
    form = ReviewForm()
    if request.method == 'GET':
        form.text.data = review.text 
    if form.validate_on_submit() and request.method == 'POST':
        review.rating = round(form.rating.data, 2)
        review.text = form.text.data
        db.session.commit()
        return redirect(url_for('courses.course', id=id))
    return render_template('courses/edit_review.html', title="Edit review", form=form, id=id)

@courses.route('/course/<id1>/delete_review/<id2>', methods=['GET', 'POST'])
@login_required
def delete_review(id1, id2):
    if Review.query.filter_by(id=id2).delete():
        db.session.commit()
        flash ('Review has been deleted', 'success')
        return redirect(url_for('courses.course', id=id1))
    return redirect(url_for('courses.course', id=id1))

@courses.route('/search', methods=['GET', 'POST'])
def search():
    courses = None
    target_string = request.form['search']

    courses = Course.query.filter(
        or_(
            Course.title.contains(target_string)
            )
        ).all()

    if target_string == '':
        search_msg = 'No record(s) found - displaying all records'
        color = 'danger'
    else:
        search_msg = f'{len(courses)} course(s) found'
        color = 'success'
    return render_template('courses/search.html', 
        title='Search result', courses=courses, 
        search_msg=search_msg, color=color
    )

@courses.route('/category', methods=['GET', 'POST'])
def category():
    form = CategoryForm()
    categories = Category.query.order_by(Category.name.asc())
    if form.validate_on_submit():
        cat = Category(name = form.name.data)

        db.session.add(cat)
        db.session.commit()
        flash(f'{form.name.data} was added successfully', 'success')
        return redirect(url_for('courses.category'))

    return render_template(
        'courses/categories.html', 
        title='Categories', 
        categories=categories,
        form=form
    )

@courses.route('/edit_category/<id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get(id)
    form = EditCategoryForm(obj=category)
    form.populate_obj(category)
    if request.method == 'POST':
       if form.update.data and form.validate_on_submit():
           category.name = form.name.data 
           db.session.commit()
           flash ('Update was successful', 'success')
           return redirect(url_for('courses.category'))
    if form.cancel.data:
        return redirect(url_for('courses.category'))
    return render_template('courses/edit_category.html', title='Edit Category', form=form)

@courses.route('/delete_category/<id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    if Category.query.filter_by(id=id).delete():
        db.session.commit()
        flash ('Category has been deleted', 'success')
        return redirect(url_for('courses.category'))
    return redirect(url_for('courses.category'))