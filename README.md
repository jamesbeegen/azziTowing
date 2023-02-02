# IT493
Source code for IT493 Project  

This is built using Flask, a python framework for web development.
## Table of Contents
- [Initial setup](#initial-setup)
- [How to work on this](#how-to-work-on-this)
- [Running the app](#running-the-app)
- [View changes to HTML, CSS, etc](#viewing-changes-made-to-html-css-or-anything-else)
- [Updating the repository](#updating-the-repository)
- [Things to look out for](#things-to-look-out-for)
  
## Initial setup
1. Make a GitHub account, and send me your username. I will grant you access to this repository so you can clone it and make changes.
2. Install Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    - Skip this step if using WSL in step 4
    - Set up global username and password
        ```
        git config --global user.name "FIRST_NAME LAST_NAME"
        ```
    - Set up global email
        ```
        git config --global user.email "email@email.com"
        ```
3. Install python: https://www.python.org/downloads/
    - Skip this step if using WSL in step 4
4. (Optional) Install Windows Subsystem for Linux from the Windows Store: https://apps.microsoft.com/store/detail/windows-subsystem-for-linux/9P9TQF7MRM4R
    - Install Ubuntu WSL2 Distro by running these commands after installing WSL:
    ```
    wsl --set-default-version 2
    ```
    then
    ```
    wsl --install Ubuntu
    ```
    From your Ubuntu WSL terminal, run:
    ```
    sudo apt update -y && sudo apt upgrade -y
    ```
5. Clone this repository:
    ```
    git clone https://github.com/jamesbeegen/azziTowing.git
    ```

6. Install the project dependencies:
    ```
    pip3 install -r requirements.txt
    ```
> If ```python``` or ```pip``` are not working, try using ```python3``` or ```pip3```. If none of those work, you have to configure your PATH.  

## How to work on this
1. After cloning the repository and making changes to files, view the status of your changes by running:
      ```
      git status
      ```
    while in the ```azziTowing``` directory. 
2. You will have to "push" your changes back to this repository. First, you have to stage files to be "committed" to the repository by running:
      ```
      git add .
      ```
      Note the period. This means to add all changes you have made to the "commit" that you will push back to the repository. 
3. Create a "commit" that includes your changes by running:
      ```
      git commit -m "Describe the changes you made here"
      ```
      It's advised to make a commit that encompasses a single change to functionality or design, rather than one commit that encompasses several different adds of functionality, etc.
4. Push the changes/commit to the ` dev ` branch of this repository by running:
      ```
      git push -u origin dev
      ```
      I have to grant access to the repository first before you can push changes, but your changes should be visible in the ` dev ` branch after this. 
5. That's it

## Running the app
First, change to the ` azziTowing ` directory:
```
cd azziTowing
```
Then:  

In Windows/CMD/Powershell:
```
set FLASK_APP=app
set FLASK_ENV=development
python3 -m flask run
```
If using WSL:
```
export FLASK_APP=app
export FLASK_ENV=development
python3 -m flask run
```

Run the above command, then open `localhost:5000` in your browser.  

## Viewing Changes made to HTML, CSS or anything else
To view changes, you will have to quit out of the development server in your terminal with ` Ctrl ` + ` C `, save your changes, and then start the development server again with:
```
python3 app.py
```
You can just hit the up arrow in the terminal to enter in the last command that was run.  

It's advised to hold ` Shift ` when clicking refresh on the web page so it clears the cache of the site.

## Updating the repository
You will need to update the repository (to get everyone else's changes) daily. 

You can do this by running:
```
git pull
```

## Things to look out for
1. I, and others, might have to add another dependency into ` requirements.txt ` in order to add some functionality to the site.  

    If you ever see a change to ` requirements.txt ` , you must run:
    ```
    pip3 install -r requirements.txt
    ```

    This will ensure your flask server doesn't spit out any errors if it doesn't have missing dependencies.

2. We will eventually need to install a database (more than likely ` MySQL` ), so I'll update everybody when we need to do that. We don't need to right now, just focus on making the site functional and looking really nice.