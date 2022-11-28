# Onion: A Minimal Recipe App (Web)

Onion is a Web Recipe App. It uses Python Flask as backend and work with SQL servers.

There exists a SQL Injection for my project Security at INSA CVL Bourges

## Installation

Use Git and package manager pip to install the requirements with the following commands one by one in the command prompt,

```bash
git clone https://github.com/thanhnguyen287/SQL-Vulnerable.git
cd 
.\env\Scripts\activate
pip install -r requirements.txt
```
Then edit the following line in ```init.py``` located in ```Recipe-Web-App/App```
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_USERNAME:DB_PASSWORD@DB_HOST/DB_NAME'

# To use SQLite remove the above code and paste this.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
```

then run ```python run.py``` After running run.py visit 
```
pip install email_validator

your_url.com/install
```
This will install the table's in the Database and add Admin Profile.


## Default Logins

```
Username: admin
Password: admin
```

## Reference
For front-end, modules of [Owl Theme](https://owltheme.com/) has been used

## License
[MIT](https://choosealicense.com/licenses/mit/)

