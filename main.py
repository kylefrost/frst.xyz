from flask import Flask, render_template, request, redirect
from jsonapi import api
import MySQLdb, string, random, dbc, time

# Create Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')

# Load Index page
@app.route('/')
def index():
	return render_template("index.html")

# Generate alias and of size "size"
def gen_rand_alias(size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Insert new url and alias into database
@app.route('/create', methods=['GET', 'POST'])
def create():
    # Get URL and password from POST Request
    URL = request.form.get('url')
    password = request.form.get('password')
    custom = request.form.get('custom')
    
    print URL + password + custom

    if password is None or URL is None or custom is None:
        return "Something went wrong."

    # Check if custom alias is set, if not, generate one
    if custom == '':
        alias = gen_rand_alias(10)
    else:
        alias = custom

    # If password is incorrect, Rick Roll
    if password not in dbc.passwords or password == '':
        return render_template("sorry.html", message="Sorry, only Kyle can use this URL shortener.")

    # Create database connection
    db = MySQLdb.connect(host=dbc.server, user=dbc.user, passwd=dbc.passwd, db=dbc.db)
    cursor = db.cursor()
    
    # Insert Redirect URL and Alias into database
    cursor.execute("INSERT INTO " + dbc.urltbl + " (url, alias) VALUES (\'" + URL + "\', \'" + alias + "\');")
    
    # Commit to database and close connections
    db.commit()
    cursor.close()
    db.close()

    return render_template("link.html", url="http://frst.xyz/" + alias)

# Redirect to unshortened URL and log user's info
@app.route('/<alias>', methods=['GET', 'POST'])
def alias(alias):
    # Create database connection
    db = MySQLdb.connect(host=dbc.server, user=dbc.user, passwd=dbc.passwd, db=dbc.db)
    cursor = db.cursor()
    
    # Insert Redirect URL and Alias into database
    cursor.execute("SELECT url FROM " + dbc.urltbl + " WHERE alias = \"" + alias + "\"")

    # Get result
    result = cursor.fetchone()
    
    # If result is None, alias wasn't found, show error
    if result is None:
        return render_template("sorry.html", message="Sorry, that URL alias wasn't found.")
    
    # Set URL
    url = result[0]

    # Log click from user
    cursor.execute("INSERT INTO " + dbc.cltbl + " (ip, alias, dateClicked, userAgent, browser, platform) VALUES (\"" + str(request.remote_addr) + "\", \"" + alias + "\", \"" + time.strftime('%Y-%m-%d %H:%M:%S') + "\", \"" + str(request.headers.get('User-Agent')) + "\", \"" + str(request.user_agent.browser) +  "\", \"" + str(request.user_agent.platform) + "\")")

    # Close connections
    db.commit()
    cursor.close()
    db.close()

    # Redirect to unshortened URL
    return redirect(url, code=302)

# Run Flask app on load
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
