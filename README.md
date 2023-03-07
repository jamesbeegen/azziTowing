# IT493
Source code for IT493 Project. This is built using Flask, a python framework for web development.
# ***IMPORTANT UPDATES***
**Going forward, you have to add the files in the [azziTowing-secrets](https://github.com/jamesbeegen/azziTowing-secrets) repository in order to run the app. These files contain the API Keys and Access Tokens for Gmail, Stripe, and Twilio APIs. The repository is "private", so it can't be viewed by the public. This repository (the main one), is not private because we need branch protection features that are only available for free on public repositories - hence the need for a separate private repository. Heroku is already confiured with the environment variables found in the new files in the separate repository**  
# ***PLEASE UPDATE DEPENDENCIES AS WELL - I'VE ADDED A LOT***
```
pip3 install -r requirements.txt
```
## Table of Contents
- [Initial setup](#initial-setup)
- [How to work on this](#how-to-work-on-this)
- [Running the app](#running-the-app)
- [View changes to HTML, CSS, etc](#viewing-changes-made-to-html-css-or-anything-else)
- [Updating the repository](#updating-the-repository)
- [Docker](#Docker)
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
### Before doing anything, always run:
```
git pull origin dev
```
1. After cloning the repository and making changes to files, view the status of your changes by running:
      ```
      git status
      ```
    while in the ```azziTowing``` directory. 
2. You will have to "push" your changes back to this repository. To do this, first create a a new "branch" while in the ```azziTowing``` directory:
    ```
    git checkout -b new-branch-name
    ```
    Replace ```new-branch-name``` with a semi-descriptive name.
    
3. Now, you have to stage files to be "committed" to the repository by running:
      ```
      git add .
      ```
      Note the period. This means to add all changes you have made to the "commit" that you will push back to the repository. 
4. Create a "commit" that includes your changes by running:
      ```
      git commit -m "Describe the changes you made here"
      ```
      It's advised to make a commit that encompasses a single change to functionality or design, rather than one commit that encompasses several different adds of functionality, etc.
4. Push the changes/commit to the ` dev ` branch of this repository by running:
      ```
      git push -u origin new-branch-name
      ```
      Again, replace ```new-branch-name``` with the actual name of the branch. 
5. Now we have to "merge" your new branch into the "dev" branch. To do this, we open a pull request from within GitHub. From the main repository page, click on "Pull requests"
6. Then click on "New Pull Request"
7. The base branch should be the ```dev``` branch, and the "compare" branch should be the name of your new branch you just pushed.
8. Click on Create Pull Request
9. Give the pull request a name and a short description, and click "Create Pull Request" again.
10. I will make sure there aren't any merge conflicts and merge your branch into the dev branch. 
11. **IMPORTANT**, after you have ran the ```git push ...``` command, you must switch back to the dev branch locally! Do this by running:
      ```
      git switch dev
      ```
**Always make sure you checkout to a a new branch with ```git checkout``` before running ```git add```**
## Running the app
First, change to the ` azziTowing ` directory:
```
cd azziTowing
```
Then:  
```
python3 app.py
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

## Docker
To build the docker image, navigate to the base directory and run
```
docker build -t azzi .
```
To run the container:
```
docker run --rm -p 5000:5000 -t azzi
```

## Things to look out for
1. I, and others, might have to add another dependency into ` requirements.txt ` in order to add some functionality to the site.  

    If you ever see a change to ` requirements.txt ` , you must run:
    ```
    pip3 install -r requirements.txt
    ```

    This will ensure your flask server doesn't spit out any errors if it doesn't have missing dependencies.

2. We will eventually need to install a database (more than likely ` MySQL` ), so I'll update everybody when we need to do that. We don't need to right now, just focus on making the site functional and looking really nice.
