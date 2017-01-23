###############
# imports ###
###############

import sys
from fabric.api import cd, env, lcd, put, prompt, local, sudo, settings
from fabric.context_managers import shell_env, prefix
from fabric.contrib.files import exists


##############
# config ###
##############

local_app_dir = './'
local_config_dir = './config'

remote_app_dir = '/home/www'
remote_git_dir = '/home/git'
remote_flask_dir = remote_app_dir + '/word_match'
remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

env.user = 'root'
# env.password = 'blah!'


#############
# tasks ###
#############

def install_requirements():
    """ Install required packages. """
    sudo('export LC_ALL=en_US.UTF-8')
    sudo('echo export LC_ALL=en_US.UTF-8 >> /etc/environment')
    sudo('export word_match_ENV=prod')
    sudo('echo word_match_ENV=prod >> /etc/environment')
    sudo("sh -c 'echo \"deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main\" >> /etc/apt/sources.list.d/pgdg.list'")
    sudo('wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -')
    with settings(warn_only=True):
        sudo('apt-get update')

    sudo('apt-get install -y postgresql postgresql-contrib')
    sudo('apt-get install -y python')
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y gunicorn')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')
    sudo('apt-get install -y nodejs')
    with settings(warn_only=True):
        sudo('apt-get install -y npm')
    sudo('apt-get install -y libpq-dev python-dev libffi-dev ')
    sudo('sudo touch /var/run/supervisor.sock')
    sudo('sudo chmod 777 /var/run/supervisor.sock')
    sudo('sudo service supervisor restart')


def deploy_files():

    if exists(remote_app_dir) is False:
        sudo('mkdir -p ' + remote_app_dir)
    if exists(remote_flask_dir) is False:
        sudo('mkdir -p ' + remote_flask_dir)
    with lcd(local_app_dir):
        with cd(remote_app_dir):
            sudo('virtualenv venv')
            sudo('mkdir -p logs')
        with cd(remote_flask_dir):
            put('app', './', use_sudo=True)
            put('manage.py', './', use_sudo=True)
            put('wsgi.py', './', use_sudo=True)
            put('requirements', './', use_sudo=True)


def install_flask():
    """
    Install flask dependencies
    """
    with cd(remote_flask_dir):
        sudo('pip install --upgrade pip')
        sudo('pip install -r requirements/prod.txt')


def configure_database():
    """
    Configures postgres and flask database
    """

    with settings(warn_only=True):
        sudo('psql -c \"CREATE ROLE root WITH SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN\";', user='postgres')
        sudo('psql -c \"ALTER ROLE postgres WITH PASSWORD \'postgres\';\"', user='postgres')
        sudo('psql -c \"CREATE DATABASE root;\"', user='postgres')
        sudo('psql -c \"CREATE DATABASE wordapp OWNER root;\"', user='postgres')

    with settings(warn_only=True):
        with cd(remote_flask_dir):
            with shell_env(word_match_ENV='prod'):
                sudo('python manage.py db init')
                sudo('python manage.py db migrate')
                sudo('python manage.py db upgrade')


def configure_nginx():
    """
    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    sudo('touch /etc/nginx/sites-available/word_match')

    with settings(warn_only=True):
        sudo('ln -s /etc/nginx/sites-available/word_match' +
             ' /etc/nginx/sites-enabled/word_match')
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put('./word_match', './', use_sudo=True)
    sudo('/etc/init.d/nginx restart')

def configure_ssl():
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put('./word_match.ssl', './word_match', use_sudo=True)
    sudo('/etc/init.d/nginx restart')


def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    #if exists('/etc/supervisor/conf.d/word_match.conf') is False:
    with lcd(local_config_dir):
        with cd(remote_supervisor_dir):
            put('./word_match.conf', '/etc/supervisor/conf.d/', use_sudo=True)
            sudo('supervisorctl reread')
            sudo('supervisorctl update')


def configure_git():
    """
    1. Setup bare Git repo
    2. Create post-receive hook
    """
    sudo('rm -rf {0}'.format(remote_git_dir))
    if exists(remote_git_dir) is False:
        sudo('mkdir -p ' + remote_git_dir)
        with cd(remote_git_dir):
            sudo('mkdir -p word_match.git')
            with cd('word_match.git'):
                sudo('git init --bare')
                with lcd(local_config_dir):
                    with cd('hooks'):
                        put('./post-receive', './', use_sudo=True)
                        sudo('chmod +x post-receive')

def flask_requirements():
    with cd(remote_flask_dir):
        sudo('pip install -r requirements/prod.txt')

def run_app():
    """ Run the app! """
    with cd(remote_flask_dir):
        sudo('supervisorctl start word_match')


def deploy(remote):
    """
    1. Copy new Flask files
    2. Restart gunicorn via supervisor
    """
    if remote not in ['prod']:
        print "please enter a remote name (demo, prod) - ex: fab deploy:prod"
        sys.exit()
    elif remote.lower() == 'prod':
        remote_name = 'wordlive'
        env.hosts = ['word_match.com']
    else:
        print "what?"
        sys.exit()

    node_requirements()

    with lcd(local_app_dir):
        local('git push -f {0} master'.format(remote_name))
        flask_requirements()
        sudo('supervisorctl restart word_match')


def create_indexes():
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON events (host_id, start_time, lat, lng, id);"')
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON accounts (id);"')
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON accountsevents (id);"')
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON accountsevents (events_id, accounts_id, liked, confirmed, confirmed_code);"')
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON eventsinterests (events_id, interests_id);"')
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON accountsinterests (accounts_id, interests_id);"')
    sudo('psql -d wordapp -c "CREATE INDEX CONCURRENTLY ON interests (id, name);"')


def node_requirements():
    with cd(remote_flask_dir):
        with settings(warn_only=True):
            sudo('npm install')
            sudo('npm install -g stylus')


def deploy_db(remote):

    """
    1. Copy new Flask files
    2. Restart gunicorn via supervisor
    """
    if remote not in ['prod']:
        print "please enter a remote name (demo, prod) - ex: fab deploy:prod"
        sys.exit()
    elif remote.lower() == 'prod':
        remote_name = 'wordlive'
        env.hosts = ['word_match.com']
    else:
        print "what?"
        sys.exit()

    node_requirements()

    with lcd(local_app_dir):
        local('git push {0} master'.format(remote_name))
        flask_requirements()

    with settings(warn_only=True):
        with cd(remote_flask_dir):
            with shell_env(word_match_ENV='prod'):
                sudo('supervisorctl stop word_match')
                sudo('service postgresql restart')
                sudo('python manage.py db migrate')
                sudo('python manage.py db upgrade')
                sudo('supervisorctl start word_match')


def rollback():
    """
    1. Quick rollback in case of error
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git revert master  --no-edit')
        local('git push {0} master'.format(remote_name))
        sudo('supervisorctl restart word_match')


def tail_log():
    sudo('tail -f /home/www/word_match/logs/word_match.log')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def restart_gunicorn():
    """restart gunicorn process"""
    sudo('supervisorctl restart word_match')


def create():
    remote_name = 'wordlive'
    env.hosts = ['word_match.com']
    install_requirements()
    deploy_files()
    install_flask()
    configure_database()
    configure_nginx()
    configure_supervisor()
    configure_git()
    sudo('supervisorctl restart word_match')
