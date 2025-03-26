FROM jboss/wildfly:latest

# Download kie-server.war from Maven repository
RUN curl -L -o /opt/jboss/wildfly/standalone/deployments/kie-server.war \
    https://repo1.maven.org/maven2/org/kie/server/kie-server/7.74.1.Final/kie-server-7.74.1.Final-webc.war

# Expose ports
EXPOSE 8080 9990

# Start WildFly
CMD ["/opt/jboss/wildfly/bin/standalone.sh", "-b", "0.0.0.0"]
