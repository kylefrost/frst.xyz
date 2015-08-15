from flask import Flask, render_template, request, redirect
import MySQLdb, string, random, dbc, time

app = Flask(__name__)

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
    custom = request.form.get('custom')
    password = request.form.get('password')

    if custom is None:
        alias = gen_rand_alias(10)
    else:
        alias = custom
    
    # If password is incorrect, Rick Roll
    if password not in dbc.passwords or password is None:
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

@app.route('/<alias>', methods=['GET', 'POST'])
def alias(alias):
    # Create database connection
    db = MySQLdb.connect(host=dbc.server, user=dbc.user, passwd=dbc.passwd, db=dbc.db)
    cursor = db.cursor()
    
    # Insert Redirect URL and Alias into database
    cursor.execute("SELECT url FROM " + dbc.urltbl + " WHERE alias = \"" + alias + "\"")

    result = cursor.fetchone()
    
    if result is None:
        return render_template("sorry.html", message="Sorry, that URL alias wasn't found.")
    
    url = result[0]

    cursor.execute("INSERT INTO " + dbc.cltbl + " (ip, alias, dateClicked, userAgent, browser, platform) VALUES (\"" + str(request.remote_addr) + "\", \"" + alias + "\", \"" + time.strftime('%Y-%m-%d %H:%M:%S') + "\", \"" + str(request.headers.get('User-Agent')) + "\", \"" + str(request.user_agent.browser) +  "\", \"" + str(request.user_agent.platform) + "\")")

    # Close connections
    db.commit()
    cursor.close()
    db.close()

    return redirect(str(result[0]), code=302)

# Run Flask app on load
if __name__ == "__main__":
    app.run(host='0.0.0.0')
