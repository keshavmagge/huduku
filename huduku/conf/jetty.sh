NO_START=0
VERBOSE=yes
JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:bin/javac::")
JETTY_HOME=/opt/solr
JETTY_USER=solr
JETTY_LOGS=/opt/solr/logs
JETTY_PORT=8080
JETTY_HOST=0.0.0.0
