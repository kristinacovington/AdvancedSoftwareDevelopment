# cs3240-s17-team01
CS 3240 Project 2017
Lokahi Fintech Crowdfunding

## Heroku server is up!

You can still make changes and run it in local server as normal

To make changes in heroku:

    $ heroku git:remote -a glacial-ridge-29106

    $ git add .
  
    $ git commit -am "insert commit message here"
  
    $ git push heroku master
  
  Then you can access it at: https://glacial-ridge-29106.herokuapp.com/home/
  
  All other commands are mostly the same i.e:
  
    $ heroku run python manage.py migrate
    
    $ heroku run python manage.py createsuperuser
    
    etc...

I set up an super user already:

    username: administrator
    password: administratorpassword
  
Note you do have to push to this github repo and the heroku repo separately (hence why we have 2 .git folders)
The Heroku repo is located under the /MyDjangoApp2/ folder 
