from flask import Flask, render_template, redirect, url_for, flash, make_response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import sqlite3 as sql
import pandas as pd
import requests
from dataclasses import dataclass
import os
import abc
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from dotenv import load_dotenv
from backend_web import functions as func
from backend_web import models as mdls