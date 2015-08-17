from flask import Blueprint, jsonify, request
import MySQLdb, dbc, json, string, random

# Set up api Blueprint
api = Blueprint('api', __name__)

# Generate alias and of size "size"
def gen_rand_alias(size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# API Post Route
@api.route('/create', methods=['GET', 'POST'])
def api_create():
    # Get URL and password from POST Request
    URL = request.form.get('url')
    password = request.form.get('password')
    custom = request.form.get('custom')

    if password is None or URL is None:
        return "Something went wrong.<br>password: " + str(password) + "<br>URL: " + str(URL) + "<br>custom: " + str(custom)

    # Check if custom alias is set, if not, generate one
    if custom == '' or custom is None:
        alias = gen_rand_alias(10)
    else:
        alias = custom

    # If password is incorrect, Rick Roll
    if password not in dbc.passwords or password == '':
        errors = { "error" : "Password was not recognized" }
        return json.dumps(errors)

    # Create database connection
    db = MySQLdb.connect(host=dbc.server, user=dbc.user, passwd=dbc.passwd, db=dbc.db)
    cursor = db.cursor()
    
    # Insert Redirect URL and Alias into database
    cursor.execute("INSERT INTO " + dbc.urltbl + " (url, alias) VALUES (\'" + URL + "\', \'" + alias + "\');")
    
    # Commit to database and close connections
    db.commit()
    cursor.close()
    db.close()

    result = { "url" : "http://frst.xyz/" + alias }

    return json.dumps(result)
