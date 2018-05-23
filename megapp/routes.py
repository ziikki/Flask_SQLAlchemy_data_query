# urls
from megapp import app, db
from flask import render_template, flash, redirect, url_for, request
from megapp.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from megapp.models import User, CancerData
from flask import request
from werkzeug.urls import url_parse
from sqlalchemy import and_

@app.route('/')
@app.route('/index')
def index():

    counts = db.session.query(CancerData).count()
    
    return render_template('index.html', title='Home', user=current_user, counts=counts)    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#########################################################
# access with form
@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        if not request.form['age'] or not request.form['menopause']:
            new_entry = CancerData(Class = request.form['Class'],
                                   age = request.form['age'],
                                   menopause = request.form['menopause'],
                                   tumor_size =request.form['tumor_size'])
            print(new_entry.to_str())
            db.session.add(new_entry)
            db.session.flush()
            # de.session.new #view objects in the session
            flash('new entry created. id: {}'.format(new_entry.id))
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/add_json', methods = ['GET','POST'])
def add_json():
    if request.method == 'POST':
        flash('We got that json file!')
        return "Nothing"
    return redirect(url_for('index'))
    

@app.route('/delete/<int:id>', methods = ['GET'])
def delete(id):
    if CancerData.query.filter_by(id=id).first():
        
        flash('id {} deleted'.format(id))
    else:
        flash('invalid id: {}, failed to delete'.format(id))
    return redirect(url_for('index'))
                            
#########################################################

@app.route('/firstnrows/<int:rows>',methods=['GET'])
def get_rows(rows):
    if rows > 0:
        entries = CancerData.query.limit(rows).all()
    return render_template('data.html', title='First {} rows of data'.format(rows), query_result=entries)

@app.route('/id/<int:id>',methods=['GET'])
def find_id(id):
    entry = CancerData.query.filter_by(id=id).all()
    return render_template('data.html', title='Query result by id', query_result=entry)


@app.route('/filter/<string:column>/<value>')
def find_value(column,value):
    if column in ['id','Class','age','menopause','tumor_size','inv_nodes','node_caps','deg_malig','breast','breast_quad','irradiat']:
        keyword = dict({column: value})
        entries = CancerData.query.filter_by(**keyword).all()
    else:
        flash('The feature does not exist!')
        entries = []
    return render_template('data.html', title='Query result by {}'.format(column), query_result=entries)
        

@app.route('/neverseenbefore/',methods=['POST'])
def find_new():
    args = request.get_json()
    #filtercolumn = args['filtercolumn'] #id for now
    frange = args['filter_range']
    target_column = args['target_column']

    existing_values = to_list(
        db.session.query(getattr(CancerData, target_column))
        .filter( CancerData.id < frange[0])
        .distinct().all()
    )
    recent_values = to_list(
        db.session.query(getattr(CancerData, target_column))
        .filter(and_(CancerData.id >= frange[0], CancerData.id < frange[1]))
        .distinct().all()
    )
    new_values = [value for value in recent_values if value not in existing_values]
    result = {
        "range":frange,
        "target":target_column,
        "new_values":new_values,
        "existing_values":to_str(existing_values)
        #"recent_values":to_str(recent_values)
    }
    return render_template("update.html", title="UpdateValue", result=result)
    
def to_list(values):
    return [value[0] for value in values]

def to_str(values, _for='values'):
    #TODO: newline
    return ' '.join(values)
    
