# IT493
Source code for IT493 Project
## Initial setup
- Install python: https://www.python.org/downloads/
- Install MariaDB: https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.10.2&os=Linux&cpu=x86_64&pkg=tar_gz&i=systemd&m=acorn
- Install the project dependencies in a virtual environment:
```
# Create the virtual environment
python3 -m venv flask

# Activate the virtual environment
## If using Windows
python -m venv C:\path\to\flask_env

## If using Mac or Linux
source /path/to/flask_env/bin/activate

pip install requirements.txt
```
> If ```python``` or ```pip``` are not working, try using ```python3``` or ```pip3```. If none of those work, you have to configure your PATH.

- Install Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

## How to work on this
1. Create a "fork" of the repository so you have your own copy. You can do this within github
2. You will push changes to your forked repository, not the main one.
3. When you want your changes to be merged into the main repository, open a pull request into the "Dev" branch. Everyone, or a designated person should approve this pull request after it is reviewed.
4. If the changes from the pull request aren't breaking anything in the "dev" branch, they will be merged into the "main" branch after testing
5. I will have a pull request template soon

## Running the app
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Run the above command, then open `localhost:5000` in your browser.