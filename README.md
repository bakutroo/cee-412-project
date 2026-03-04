# How to:

## Start a Python environment
For ```Mac```, In your terminal, enter these commands:

Initialize the environment 
``` 
python3 -m venv .venv
```
To start the environment (you'll also want to do this when you're working on the project) activate it:
``` 
source .venv/bin/activate
```
install streamlit, this is only done once
``` 
python3 -m pip install streamlit
```


---
For ```Windows```, In your terminal, enter these commands:

Initialize the environment 
```
py -m venv .venv
```

To start the environment (you'll also want to do this when you're working on the project) activate it:
```
.\\.venv\\Scripts\\activate
```

for ```both Mac and Windows``` to shut it down (when you're done for now), just enter this in the terminal
``` 
deactivate
```

## Start up your app
In your terminal, enter this command

``` 
bash ./bash.sh
```

Alternatively, you can just do, where 'main.py' is the name of the file your code is in:

``` 
streamlit run main.py
```


## INIT Setup GitHub for your project (this should only be done once, by one person)
1. Install Git

Download from: https://git-scm.com
Install with default settings.

If you've already got a folder you want to share, go into it and do this:
``` 
git init
```

2. Create a GitHub Account

Go to: https://github.com

Create a New Repository
	•	Give it a name

Click Create Repository

⸻

3. Connect Your Local Project to GitHub

GitHub will show commands. They look like this:
``` bash
git remote add origin https://github.com/yourusername/my-project.git
```

```bash
git branch -M main
```
```
git push -u origin main
```


## Pull/clone the project from GitHub
On the GitHub project page there should be multiple ways to 'clone' the project, you can get the app, which I recommend since it makes it super easy and that's usually what I use, but otherwise you can also just do the commands which usually look something like this:

```
git clone https://github.com/username/project-name.git
cd project-name
```

## Setup branches so there aren't conflicts !!! IMPORTANT !!!

This needs to be done by every team member, and it's important that everyone does it otherwise there's no point.

WHAT is it?  - A branch is a way to seperate individual's code within a project, so if you're making a calculator and two people work on the division part, they can send/share their code to seperate branches, and the team can decide which is better and choose that one, otherwise if both people send their code to the same (MAIN) branch either there's two division methods or one gets overwritten by the other, both suck.

SO, every time you start on a new section or new feature, or whatever, you need to do THIS:
```
git checkout -b new-feature
```

where 'new-feature' more accurately describes what you're doing


## Merge branches

This is done when you've decided a branch is done and can be accepted into the main branch, this should only be done when you're sure it's at least good enough for everyone to work with, and there isn't a ton of stuff to change on whatever was done in this branch

- Switch back to the main branch
```
git checkout main
```

- Merge the branch
```
git merge new-feature
```

- Delete the old branch (it's merged, so no point in keeping it)
```
git branch -d new-feature
```

``` IMPORTANT ``` : After this is done, everyone should do this (and should just do this regularly) so their codebase is up to date:
```
git pull
```

## Push your changes to GitHub for your teammates to see

This adds all changes in every file in your folder to 'changes to send', but generally speaking just use this if everything on your computer is working fine
``` 
git add .
```


If you want to change this, either go to the source control tab and add, remove, or whatever, all the files you want to send over, or instead of the command above, just do:
``` 
git add <filename>
```

After adding the changes you want to share, do this:
```
git commit -m "Comments about what you're sharing"
```
```
git push
```

