from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired,Email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class ContactForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email Address?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        valid_email = 'utoronto'
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
            print(form.email.data)
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        session['name'] = form.name.data
        if valid_email in form.email.data:
            session['email'] = form.email.data
        else:
            session['email'] = 'invalid'
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))
