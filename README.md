huduku
======

huduku is a django application that facilitates interaction with a SOLR
index of all active products via a REST API 

Install
-------

Postgres 

    sudo apt-get install postgresql postgresql-contrib


Copy CPS data

create database 'cps' and restore the database from a copy of CPS found at
https://s3.amazonaws.com/cobrainabsolem/datadumps/productdb/20140422_qa_cps_backup.sql.gz

    psql cps < /path/to/sql/backup/file.sql

on psql shell

    CREATE USER cobrain WITH PASSWORD 'pickyourpassword';
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cobrain;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cobrain;

Get huduku
create a virtualenv for the project and a directory to hold the src and clone huduku

    git clone https://github.com/cobrain-labs/huduku.git
    source /path/to/virtualenv/bin/activate
    pip install -r requirements.txt
    python setup.py build
    python setup.py install
    export DJANGO_SETTINGS_MODULE=huduku.settings


Configure Solr

    wget http://archive.apache.org/dist/lucene/solr/4.7.2/solr-4.7.2.tgz
    tar zxvf solr-4.7.2.tgz
    sudo mv solr-4.7.2/example/ /opt/solr

    sudo useradd -d /opt/solr -s /bin/bash solr
    sudo chown solr:solr -R /opt/solr
    
    sudo cp /var/apps/huduku/huduku/conf/jetty7.sh /etc/init.d/jetty
    sudo chmod +x /etc/init.d/jetty

    sudo cp /var/apps/huduku/huduku/conf/schema.xml /opt/solr/solr/collection1/conf/schema.xml
    sudo cp /var/apps/huduku/huduku/conf/solrconfig.xml /opt/solr/solr/collection1/conf/solrconfig.xml

    sudo cp /var/apps/huduku/huduku/conf/jetty-ubuntu /etc/default/jetty
    sudo service jetty start


Build SOLR index

    django-admin.py index_cps_data

