from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)
