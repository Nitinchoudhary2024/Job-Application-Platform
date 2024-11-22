from flask import Flask, render_template, redirect, url_for, request, session, flash
from extensions import db
from models import User, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, PostJobForm, ApplyJobForm
from flask_wtf.csrf import CSRFProtect

# Initialize CSRF protection


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_application.db'
app.config['SECRET_KEY'] = '309b1235271d6cc9c3f52d2dc0f20181'

db.init_app(app)
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

# Candidate and Company Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(
            email=form.email.data,
            password=hashed_password,
            role=form.user_type.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] == 'Candidate':
        jobs = Job.query.all()
        return render_template('candidate_dashboard.html', jobs=jobs)
    elif session['role'] == 'Company':
        jobs = Job.query.filter_by(company_id=session['user_id'])
        return render_template('company_dashboard.html', jobs=jobs)
    return redirect(url_for('index'))

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session or session['role'] != 'Company':
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_job = Job(title=title, description=description, company_id=session['user_id'])
        db.session.add(new_job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('post_job.html')

@app.route('/jobs')
def job_list():
    if 'user_id' not in session or session['role'] != 'Candidate':
        return redirect(url_for('login'))
    jobs = Job.query.all()  # Retrieve all jobs
    return render_template('job_list.html', jobs=jobs)

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'user_id' not in session or session['role'] != 'Candidate':
        return redirect(url_for('login'))

    job = Job.query.get_or_404(job_id)
    application = Application(user_id=session['user_id'], job_id=job.id)
    db.session.add(application)
    db.session.commit()
    flash('Your application has been submitted!', 'success')
    return redirect(url_for('job_list'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if not already present
    app.run(debug=True)
