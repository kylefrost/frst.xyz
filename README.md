# frst.xyz
Source code of the frst.xyz URL shortener.

## Install Your Own
- Prerequisites
  - Basic knowledge of web server configuration
  - Flask and Python experience
  - Basic SQL knowledge

- Set up the MySQL Database
```sql
-- Click Logging Table
CREATE TABLE [INSERT_TABLE_NAME] (
  `id`            int(11)      NOT NULL AUTO_INCREMENT,
  `ip`            varchar(50)  DEFAULT NULL,
  `alias`         varchar(20)  DEFAULT NULL,
  `dateClicked`   datetime     DEFAULT NULL,
  `userAgent`     varchar(250) DEFAULT NULL,
  `browser`       varchar(50)  DEFAULT NULL,
  `platform`      varchar(50)  DEFAULT NULL,
  PRIMARY KEY     (`id`)
)

-- URL Table
CREATE TABLE [INSERT_TABLE_NAME] (
  `id`            int(11)      NOT NULL AUTO_INCREMENT,
  `url`           text,
  `alias`         varchar(20)  DEFAULT NULL,
  PRIMARY KEY     (`id`)
)
```

Remember the names you choose for your tables, you'll need those.

- Set up dbc.py

Create a file named dbc.py ("database credentials")<br>This will contain the information for your database as well as some other miscellaneous information
```python
server      =   "mysql host"
user        =   "mysql username"
passwd      =   "mysql password"
db          =   "mysql database"

urltbl      =   "url table name"
cltbl       =   "click logging table name"

passwords   =   ("list of passwords")
```

- Install Requirements

Install requirements from `requirements.txt` with `pip install -r requirements.txt`<br>
Do this from inside of your virtualenv if you plan on running this inside of one.

- Customizing

Inside of [main.py](main.py) you'll find miscellaneous things that are [frst.xyz](http://frst.xyz) specific and user specific to myself (Kyle). These will eventually be moved into the dbc.py file, but for now, these must be changed manually.

- Test

Running `python main.py` from the root directory of the project should now present you with:
```
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
Now, visiting `http://localhost:5000/` in your web browser of choice should present you with a working version

## License
See [LICENSE](LICENSE)
