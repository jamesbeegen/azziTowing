# IT493
Source code for IT493 Project  
  
  
This is built using Flask, a python framework for web development.
## Initial setup
- Install Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- Install python: https://www.python.org/downloads/
- Clone this repository:
```
git clone https://github.com/jamesbeegen/azziTowing.git
```

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

  
- Install MariaDB: https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.10.2&os=Linux&cpu=x86_64&pkg=tar_gz&i=systemd&m=acorn
## How to work on this
1. Create a "fork" of the repository so you have your own copy. You can do this within github
2. You will push changes (commits) to your forked repository, not this one.
3. When you want your changes to be merged into the main (this) repository, open a pull request into the "Dev" branch. Everyone, or a designated person should approve this pull request after it is reviewed.
4. If the changes from the pull request aren't breaking anything in the "dev" branch, they will be merged into the "master" branch after testing
5. I will have a pull request template soon
## How HTML works with Flask
Flask uses a templating engine called ```Jinja2```. The benefit of a templating engine is that rewriting HTML for each page is lessened. There is a "template" named ```base.html``` in the ```templates``` folder. This template acts as the base HTML for any page, which includes a header, footer, and navigation bar. You will see in each individual HTML file other than ```base.html```, there is a line that says
```
{% extends "base.html" %}
```
This line tells the Jinja engine to render all of the HTML from the base template. You will also notice lines like:
```
{% block content %}{% endblock %}
```
The above is found both in the template file and in all of the other HTML files in the ```templates``` folder. This tells the Jinja engine to render HTML found within this block in individual HTML files where the same line is written in the template.  
  
  Any new HTML file will need the following in order to work:
  ![image](https://user-images.githubusercontent.com/77640214/209731462-090f23dc-d09e-4204-84c4-e5e7ccf22249.png)
  
Replace "About" with the title of the page, and replace the HTML in between ```{% block content %}``` and ```{% endblock %}```

## Running the app
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Run the above command, then open `localhost:5000` in your browser.
