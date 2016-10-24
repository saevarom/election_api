from __future__ import with_statement
from fabric.api import *
from fabric.operations import get
from fabric.contrib.files import exists
from contextlib import contextmanager
import os


env.roledefs = {
    'web': ['web1b.overcast.is', 'web1c.overcast.is'],
    'db': ['web1b.overcast.is'],
}


env.project_name = 'election_api'
env.supervisor_app_name = 'election_api'
env.git_url = 'git@bitbucket.org:overcastsoftware/election_api.git'
env.user = 'ubuntu'
env.apps_path = '/home/ubuntu/'
env.directory = '/home/ubuntu/election_api'
env.activate = 'source /home/ubuntu/.virtualenvs/election_api/bin/activate'
env.do_collectstatic = False
env.django_settings_module = 'election_api.settings.prod'


@contextmanager
@roles('web')
def virtualenv():
    with settings(sudo_user=env.user):
        with cd(env.directory):
            with prefix(env.activate):
                puts('Activated virtualenv')
                yield

@roles('web')
def setup():
    pass
    # run('cd %s && git clone %s %s' % (env.apps_path, env.git_url, env.project_name))
    # run('source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv %s' % env.project_name)
    # sudo('ln -s /home/ubuntu/%(name)s/deploy/supervisorctl.conf /etc/supervisor/conf.d/%(name)s.conf' % {'name': env.project_name})
    # sudo('ln -s /home/ubuntu/%(name)s/deploy/nginx.conf /etc/nginx/sites-enabled/%(name)s.conf' % {'name': env.project_name})
    # sudo('mkdir /var/log/www/%s' % env.project_name)
    # nginx_reload()
    # with cd(env.directory):
    #     if not exists('.env'):
    #         run('echo "DJANGO_SETTINGS_MODULE=%s" > .env' % env.django_settings_module)
    # git_pull()
    # pip_install()
    # sudo('supervisorctl reread')
    # sudo('supervisorctl update')
    # restart_app()


@roles('web')
def with_static():
    env.do_collectstatic = True

@roles('web')
def uptime():
    with virtualenv():
        run('uptime')

@roles('web')
def git_pull():
    with virtualenv():
        run('git pull')

@roles('web')
def pip_install():
    with virtualenv():
        run('pip install -r requirements.txt')

@roles('db')
def syncdb():
    with virtualenv():
        run('python manage.py migrate')

@roles('web')
def collectstatic():
    with virtualenv():
        run('pwd')
        run('python manage.py collectstatic --noinput')

@roles('web')
def restart_app():
    sudo('supervisorctl restart %s' % env.supervisor_app_name)

@roles('web')
def nginx_reload():
    sudo('service nginx reload')

@roles('db')
def dump():
    with virtualenv():
        run('python manage.py dbdump latest.dump')
        get('latest.dump', 'latest.dump')

@roles('db')
def manage(arguments):
    with virtualenv():
        run('python manage.py %s' % arguments)


@roles('web')
def deploy():
    git_pull()
    pip_install()
    syncdb()
    if env.do_collectstatic:
        collectstatic()
    restart_app()

