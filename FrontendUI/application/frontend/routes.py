import os
import secrets

import requests

from flask import render_template, flash, redirect, url_for, request, jsonify, session, send_from_directory, current_app
from werkzeug.utils import secure_filename

from . import forms
from . import FE_blueprint

from .. import login_manager
from flask_login import current_user, logout_user
from ..templates import *

from .api.Holder import Holder
from .api.DisplayQR import DisplayQR
from .api.PrintQR import PrintQR


# from FrontendUI.runapp import app


@login_manager.user_loader
def load_user(user_id):
    return None


@FE_blueprint.route('/', methods=['GET', 'POST'])
def index():
    session['user_id'] = None
    return render_template('index.html')


@FE_blueprint.route('/home', methods=['GET', 'POST'])
def home_page():
    if current_user.is_authenticated:
        return render_template('home.html')
    try:
        return render_template('home.html')
    except requests.exceptions.ConnectionError:
        flash('Please check your internet connection.', 'danger')
        return render_template('index.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

MAX_FILE_SIZE = 0.5 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @FE_blueprint.routes('/uploads/<filename>')
# def uploaded_file(filename):
# return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@FE_blueprint.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    upload_img = forms.Upload_Image(request.form)
    if request.method == 'POST':
        if request.files:
            print(request.cookies)
            image = request.files['image']
            if image.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                # image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Image uploaded successfully', 'success')
                return redirect(url_for('FE.register', filename=filename))  # redirect to the register page
            else:
                flash('File type not allowed', 'danger')
                return redirect(request.url)
        else:
            flash('No file selected', 'danger')
            return redirect(request.url)
    return render_template('register/upload.html', title='Upload Image', form=upload_img)


@FE_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm(request.form)  # create a form object
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            holder = Holder.get_username_exists(username)
            if holder:
                flash('Username already exists', 'danger')
                return redirect(request.url)
            else:
                new_holder = Holder.post_create(form)
                if new_holder:
                    flash('User created successfully', 'success')

                    return redirect(url_for('FE.login'))
                else:
                    flash('User creation failed', 'danger')
                    return redirect(request.url)
        else:
            flash('Form validation failed', 'danger')
            return redirect(request.url)
    return render_template('register/register_page.html', title='Register', form=form)


@FE_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # if the user is already logged in
        return redirect(url_for('FE.home_page')) # redirect to the home page
    form = forms.LoginForm(request.form) # create a form object
    if request.method == 'POST': # if the form is submitted
        if form.validate_on_submit(): # if the form is valid
            api_key = Holder.post_login(form) # get the user's api key
            if api_key:

                session['api_key'] = api_key  # store the api_key in the session
                user = Holder.get_users() # get the user's details
                session['user'] = user[:]
                flash('Login successful', 'success')

                current_api_key = session['api_key']  # get the api_key from the session
                if current_api_key:  # if the api_key is not None
                    qrcode = DisplayQR.post_make_qr(current_api_key)  # make a qr code
                    if qrcode:
                        return render_template('home.html', title='QR Code', qrcode=qrcode, user=user)
                    else:
                        flash('QR Code generation failed', 'danger')
                        return redirect(request.url)
                else:
                    flash('API key generation failed', 'danger')

                flash('Welcome: ' + user['username'], 'success')
                return redirect(url_for('FE.home_page', user=user))
            else:
                flash('Login failed', 'danger')
                return render_template('index.html', title='Login', form=form)

        else:
            flash('Form validation failed')
            return render_template('index.html', title='Login', form=form)
    return render_template('login/login_page.html', title='Login', form=form)


@FE_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('FE.index'))


@FE_blueprint.route('/display_qr', methods=['GET', 'POST'])
def display_qr():
    if current_user.is_authenticated:  # if the user is logged in
        cur_api_key = session['api_key']  # get the api_key from the session
        if cur_api_key:  # if the api_key is not None
            qrcode = DisplayQR.retrieve_qr_code(cur_api_key)  # get the qrcode from the database using the api_key
            if qrcode:  # if the qrcode is not None
                return render_template('display_qr/qrcode.html', title='QR Code',
                                       qrcode=qrcode) and send_from_directory("display_serv/application/", qrcode)
            else:
                flash('QR Code generation failed', 'danger')
                return redirect(request.url)
        else:
            flash('API key generation failed', 'danger')
            return redirect(request.url)
    else:
        flash('User is not logged in', 'danger')
        return redirect(url_for('FE.index'))


@FE_blueprint.route('/print', methods=['GET', 'POST'])
def print_qr():
    """
    This function is used to print a qr code
    :return: Prints a qr code
    """

    if current_user.is_authenticated:
        # a qr code is generated and printed
        qr_code = PrintQR.post_print_code()
        if qr_code:
            return render_template('print.html', qr_code=qr_code)
        else:
            flash('Qr code does not exist')
            return redirect(url_for('frontend.home_page'))
    else:
        flash('User is not logged in')
        return redirect(url_for('frontend.index'))
