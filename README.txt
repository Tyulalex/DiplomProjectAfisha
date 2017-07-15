#to apply db migration execute the following commands:

python manager.py db init
python manager.py db migrate
python manager.py db revision
python manager.py db upgrade
## apply some catalogue, like categories, age categories, place types
python manager.py seed_catalogue
## seeding test data
python manager.py seed


#to run application:
python run.py

#to install libraries
pip install -r requirements.txt

#database models located in database_models.py