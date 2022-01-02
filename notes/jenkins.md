# Jenkins

Get list of plugins:

API token: `https://<url>/me/configure`

```sh
export JENKINS_URL=https://jenkins.common-build.gcp.oreilly.com
export JENKINS_USER_ID=bfrank@oreilly.com
export JENKINS_API_TOKEN=<token>

curl "${JENKINS_URL}/jnlpJars/jenkins-cli.jar" > jenkins-cli.jar

cat << 'EOF' > plugins.groovy
def plugins = jenkins.model.Jenkins.instance.getPluginManager().getPlugins()
plugins.each {println "${it.getShortName()}: ${it.getVersion()}"}
EOF

/usr/local/opt/openjdk/bin/java \
  -jar jenkins-cli.jar groovy = < plugins.groovy > jenkins_plugins.txt
```

Ref: [Jenkins CLI](https://www.jenkins.io/doc/book/managing/cli/)
