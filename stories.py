import os
from sqlite3 import dbapi2 as sqlite3
from settings import db_config
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

app.configure.update(db_config)

