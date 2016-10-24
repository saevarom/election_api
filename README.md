How to install this template
============================

    django-admin startproject --template=https://bitbucket.org/overcastsoftware/overcast-wagtail-projecttemplate/get/master.zip --extension=py,md,html,env,gitignore,js,css PROJECT_NAME
    cd PROJECT_NAME
    pip install -r requirements.txt

create a `election_api/settings/local.py` and setup your DB details

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

And you're good to go!

P.s. If you have trouble installing wagtailfontawesome, upgrade pip