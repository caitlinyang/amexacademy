from flask import Flask, render_template, url_for, flash, redirect, request
from academy import app, db, bcrypt
from academy.models import User, Location, Item, UserClass, Skill
from academy.forms import RegistrationForm, LoginForm,  LocationForm, ItemForm, CategorySearch, ItemSearch, SkillForm
from academy.models import User, Location, Item, UserClass
from academy.forms import RegistrationForm, LoginForm, LocationForm, ItemForm, CategorySearch, ItemSearch
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def welcome():
    return redirect(url_for('login'))
    return render_template("welcome.html")

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template("login.html", form=form)


@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in.','success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('category_search'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    items = Item.query.filter_by(user_id=current_user.id).all()

    attend = UserClass.query.filter_by(user_id=current_user.id).all()
    attends = []

    for user in attend: 
        item = Item.query.get_or_404(user.item_id)
        if item not in attends: 
            attends.append(item)

    return render_template('account.html', title="Account", items=items, skills=skills, attends=attends)

@app.route('/account/add_skill', methods=["GET","POST"])
@login_required
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill(name=form.name.data, description=form.description.data, category=form.category.data, user_id=current_user.id)
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('add_skill.html', title="Add Skill", form=form, legend="Add Skill")

@app.route('/skill/<int:skill_id>')
@login_required
def skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    user = User.query.get_or_404(skill.user_id)
    return render_template('skill.html', title=skill.name, skill=skill, location=location, user=user)

@app.route('/skill/<int:skill_id>/update_skill', methods=["GET","POST"])
@login_required
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    form = SkillForm()
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.description = form.description.data
        skill.category = form.category.data
        db.session.commit()
        return redirect(url_for('skill', skill_id=skill.id))
    elif request.method == 'GET':
        form.name.data = skill.name
        form.description.data = skill.description
        form.category.data = skill.category
    return render_template('add_skill.html', title="Update Skill", form=form, location=location, legend="Update Skill")

@app.route('/skill/<int:skill_id>/delete_skill', methods=["POST"])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    # location = Location.query.get_or_404(skill.location_id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('account'))

@app.route('/locations')
@login_required
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/<int:location_id>')
@login_required
def location(location_id):
    location = Location.query.get_or_404(location_id)
    items = Item.query.filter_by(location_id=location.id).all()
    return render_template('location.html', title=location.name, location=location, items=items)

@app.route('/locations/new', methods=["GET","POST"])
@login_required
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(name=form.name.data, lat=form.lat.data, long=form.long.data,
        address=form.address.data, city=form.city.data, state=form.state.data, zip=form.zip.data,
        type=form.type.data, phone=form.phone.data, website=form.website.data)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('create_location.html', title="New Location", form=form)

@app.route('/location/<int:location_id>/add_item', methods=["GET","POST"])
@login_required
def add_item(location_id):
    location = Location.query.get_or_404(location_id)
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data, category=form.category.data, date=form.date.data, startTime=form.startTime.data, endTime=form.endTime.data, location_id=location_id, user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('location', location_id=location.id))
    return render_template('add_item.html', title="Create Class", form=form, location=location, legend="Create Class")

@app.route('/item/<int:item_id>/update_item', methods=["GET","POST"])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    location = Location.query.get_or_404(item.location_id)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category = form.category.data
        item.date = form.date.data
        item.startTime = form.startTime.data
        item.endTime = form.endTime.data
        db.session.commit()
        return redirect(url_for('item', item_id=item.id))
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.category.data = item.category
        form.date.data = item.date
        form.startTime.data = item.startTime
        form.endTime.data = item.endTime
    return render_template('add_item.html', title="Update Item", form=form, location=location, legend="Update Item")

@app.route('/item/<int:item_id>/delete_item', methods=["POST"])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    location = Location.query.get_or_404(item.location_id)
    db.session.delete(item)

    all_users = UserClass.query.filter_by(item_id=item_id).all()
    for x in all_users: 
        db.session.delete(x)

    db.session.commit()
    return redirect(url_for('location', location_id=location.id))

@app.route('/item/<int:item_id>/join_item', methods=["GET","POST"])
@login_required
def join_item(item_id):
    item = Item.query.get_or_404(item_id)
    location = Location.query.get_or_404(item.location_id)
    attend = UserClass(user_id = current_user.id, item_id=item.id)
    db.session.add(attend)
    db.session.commit()
    return redirect(url_for('item', item_id=item_id))

@app.route('/item/<int:item_id>')
@login_required
def item(item_id):
    item = Item.query.get_or_404(item_id)
    user = User.query.get_or_404(item.user_id)
    location = Location.query.get_or_404(item.location_id)

    all_users = UserClass.query.filter_by(item_id=item_id).all()
    attendees = []
    for userClass in all_users: 
        username = User.query.get_or_404(userClass.user_id).username
        attendees.append(username)
    return render_template('item.html', title=item.name, item=item, location=location, user=user, attendees=attendees)

@app.route('/dashboard/category_search', methods=["GET","POST"])
@login_required
def category_search():
    form = CategorySearch()
    items = []
    skills = []
    if form.validate_on_submit():
        skills = Skill.query.filter_by(category=form.category.data).all()
        if form.locations.data == 'all':
            items = Item.query.filter_by(category=form.category.data).all()
        else:
            location = Location.query.get(int(form.locations.data))
            items = []
            for item in location.items:
                if item.category == form.category.data:
                    items.append(item)
    return render_template('category_search.html', title='Dashboard',form=form, items=items, skills=skills)

@app.route('/dashboard/item_search', methods=["GET","POST"])
@login_required
def item_search():
    form = ItemSearch()
    items = []
    if form.validate_on_submit():
        if form.locations.data == 'all':
            items = Item.query.filter_by(name=form.name.data).all()
        else:
            location = Location.query.get(int(form.locations.data))
            items = []
            for item in location.items:
                if item.name == form.name.data:
                    items.append(item)
    return render_template('item_search.html', title='Dashboard', form=form, items=items)
