from flask import Blueprint, jsonify, request
import MySQLdb, dbc

# Set up api Blueprint
api = Blueprint('api', __name__)

# API Post Route
@api.route('/create', methods=['GET', 'POST'])
def api_create():
    # Get URL and password from POST Request
    URL = request.form.get('url')
    password = request.form.get('password')
    custom = request.form.get('custom')

    # Check if custom alias is set, if not, generate one
    if custom == '':
        alias = gen_rand_alias(10)
    else:
        alias = custom

    # If password is incorrect, Rick Roll
    if password not in dbc.passwords or password is None:
        return jsonify(error="Password was not recognized.")

    # Create database connection
    db = MySQLdb.connect(host=dbc.server, user=dbc.user, passwd=dbc.passwd, db=dbc.db)
    cursor = db.cursor()
    
    # Insert Redirect URL and Alias into database
    cursor.execute("INSERT INTO " + dbc.urltbl + " (url, alias) VALUES (\'" + URL + "\', \'" + alias + "\');")
    
    # Commit to database and close connections
    db.commit()
    cursor.close()
    db.close()

    return jsonify(url="http://frst.xyz/" + alias)
