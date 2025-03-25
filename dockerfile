FROM jboss/wildfly:latest

COPY kie-server.war /opt/jboss/wildfly/standalone/deployements/

# Expose Wildfly ports
EXPOSE 8080 9990

#Start WildFly
CMD ["/opt/jboss/wildfly/bin/standalone.sh", "-b", "0.0.0.0"]
