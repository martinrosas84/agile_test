# agile_test
A cache engine that allows you to search images. The application uses only one framework web capable to do everything, but for the periodic callback to load the images you could use Celery. For that reason all the functionality is inside a single object.
## Install
In order to run the application you need only two libraries:
```
pip install tornado
pip install requests
```
## Run:
To run the application simply use:
```
python app_web.py
```
