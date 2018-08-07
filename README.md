
# README #

  

Python3 API with basic dependencies (Flask, Mongodb, PyMongo).

### How do I get set up? ###

* Import Mongodb database to local (percobaan_db_berita.json, percobaan_db_user.json)
* Install python dependencies (pip install -r requirements.txt)
* Run the API with (python run.py)
 
### Notes ###

* CRUD for collection "berita"
* Some of the mongo crud procedure were moved to model folder and some were not, for example purpose
* Added CRUD for collection "user"
* Added login with JWT
* Added protected access with JWT and app secret key (get single berita)