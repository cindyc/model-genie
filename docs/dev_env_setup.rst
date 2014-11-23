1. Download the Community Edition Neo4J from neo4j.com/download

2. Install Neo4j: 
   http://neo4j.com/docs/stable/server-installation.html
   it will be installed under /usr/local/Cellar/neo4j/2.1.4/libexec

3. Start Neo4j server: 
   /usr/local/neo4j/bin/neo4j start
   Using additional JVM arguments:  -server -XX:+DisableExplicitGC -Dorg.neo4j.server.properties=conf/neo4j-server.properties -Djava.util.logging.config.file=conf/logging.properties -Dlog4j.configuration=file:conf/log4j.properties -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled
   Starting Neo4j Server...WARNING: not changing user
   process [18440]... waiting for server to be ready..... OK.
   http://localhost:7474/ is ready.

Installing Gremlin (Gremlin is a domain-specific-language for graph databases)
git clone https://github.com/tinkerpop/gremlin.git
cd gremlin
mvn clean install

Gremlin plugin is no longer bundled with Neo4j, to install the plugin: 
http://stackoverflow.com/questions/21637155/no-such-serverplugin-gremlinplugin
https://github.com/thinkaurelius/neo4j-gremlin-plugin

Set JAVA_HOME to work around the following problem: 
http://www.jayway.com/2013/03/08/configuring-maven-to-use-java-7-on-mac-os-x/
http://stackoverflow.com/questions/17824889/how-to-force-maven-3-1-to-use-right-version-of-java-on-mac-os-8-10

echo JAVA_HOME=/usr/libexec/java_home -v 1.8*` | sudo tee -a /etc/mavenrc`
if the above doesn't work, do the following: 
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_67.jdk/Contents/Home"
sudo echo JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_67.jdk/Contents/Home" > /etc/mavenrc

git clone https://github.com/neo4j-contrib/gremlin-plugin.git
mvn clean package
unzip target/neo4j-gremlin-plugin-*-server-plugin.zip -d $NEO4J_HOME/plugins/gremlin-plugin

Add the following line to $NEO4J_HOME/conf/neo4j-server.properties
org.neo4j.server.thirdparty_jaxrs_classes=com.thinkaurelius.neo4j.plugins=/tp

cd $NEO4J_HOME
bin/neo4j restart


Note: to fix this error: 

ValueError: ({'status': '400', 'access-control-allow-origin': '*', 'content-type': 'application/json; charset=UTF-8', 'content-length': '5140', 'server': 'Jetty(9.0.5.v20130815)'}, '{\n  "message" : "javax.script.ScriptException: groovy.lang.MissingMethodException: No signature of method: groovy.lang.MissingMethodException.startTransaction() is applicable for argument types: () values: []",\n  "exception" : "BadInputException",\n  "fullname" : "org.neo4j.server.rest.repr.BadInputException",\n  "stacktrace" : [ "org.neo4j.server.plugin.gremlin.GremlinPlugin.executeScript(GremlinPlugin.java:93)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.plugins.PluginMethod.invoke(PluginMethod.java:61)", "org.neo4j.server.plugins.PluginManager.invoke(PluginManager.java:159)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:312)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:134)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.rest.transactional.TransactionalRequestDispatcher.dispatch(TransactionalRequestDispatcher.java:139)", "java.lang.Thread.run(Thread.java:745)" ],\n  "cause" : {\n    "message" : "javax.script.ScriptException: groovy.lang.MissingMethodException: No signature of method: groovy.lang.MissingMethodException.startTransaction() is applicable for argument types: () values: []",\n    "cause" : {\n      "message" : "groovy.lang.MissingMethodException: No signature of method: groovy.lang.MissingMethodException.startTransaction() is applicable for argument types: () values: []",\n      "cause" : {\n        "message" : "No signature of method: groovy.lang.MissingMethodException.startTransaction() is applicable for argument types: () values: []",\n        "exception" : "MissingMethodException",\n        "stacktrace" : [ "org.codehaus.groovy.runtime.ScriptBytecodeAdapter.unwrap(ScriptBytecodeAdapter.java:55)", "org.codehaus.groovy.runtime.callsite.PojoMetaClassSite.call(PojoMetaClassSite.java:46)", "org.codehaus.groovy.runtime.callsite.AbstractCallSite.call(AbstractCallSite.java:112)", "Script3.run(Script3.groovy:4)", "com.tinkerpop.gremlin.groovy.jsr223.GremlinGroovyScriptEngine.eval(GremlinGroovyScriptEngine.java:219)", "com.tinkerpop.gremlin.groovy.jsr223.GremlinGroovyScriptEngine.eval(GremlinGroovyScriptEngine.java:90)", "javax.script.AbstractScriptEngine.eval(AbstractScriptEngine.java:233)", "org.neo4j.server.plugin.gremlin.GremlinPlugin.executeScript(GremlinPlugin.java:86)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.plugins.PluginMethod.invoke(PluginMethod.java:61)", "org.neo4j.server.plugins.PluginManager.invoke(PluginManager.java:159)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:312)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:134)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.rest.transactional.TransactionalRequestDispatcher.dispatch(TransactionalRequestDispatcher.java:139)", "java.lang.Thread.run(Thread.java:745)" ],\n        "fullname" : "groovy.lang.MissingMethodException"\n      },\n      "exception" : "ScriptException",\n      "stacktrace" : [ "com.tinkerpop.gremlin.groovy.jsr223.GremlinGroovyScriptEngine.eval(GremlinGroovyScriptEngine.java:221)", "com.tinkerpop.gremlin.groovy.jsr223.GremlinGroovyScriptEngine.eval(GremlinGroovyScriptEngine.java:90)", "javax.script.AbstractScriptEngine.eval(AbstractScriptEngine.java:233)", "org.neo4j.server.plugin.gremlin.GremlinPlugin.executeScript(GremlinPlugin.java:86)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.plugins.PluginMethod.invoke(PluginMethod.java:61)", "org.neo4j.server.plugins.PluginManager.invoke(PluginManager.java:159)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:312)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:134)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.rest.transactional.TransactionalRequestDispatcher.dispatch(TransactionalRequestDispatcher.java:139)", "java.lang.Thread.run(Thread.java:745)" ],\n      "fullname" : "javax.script.ScriptException"\n    },\n    "exception" : "ScriptException",\n    "stacktrace" : [ "com.tinkerpop.gremlin.groovy.jsr223.GremlinGroovyScriptEngine.eval(GremlinGroovyScriptEngine.java:94)", "javax.script.AbstractScriptEngine.eval(AbstractScriptEngine.java:233)", "org.neo4j.server.plugin.gremlin.GremlinPlugin.executeScript(GremlinPlugin.java:86)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.plugins.PluginMethod.invoke(PluginMethod.java:61)", "org.neo4j.server.plugins.PluginManager.invoke(PluginManager.java:159)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:312)", "org.neo4j.server.rest.web.ExtensionService.invokeGraphDatabaseExtension(ExtensionService.java:134)", "java.lang.reflect.Method.invoke(Method.java:606)", "org.neo4j.server.rest.transactional.TransactionalRequestDispatcher.dispatch(TransactionalRequestDispatcher.java:139)", "java.lang.Thread.run(Thread.java:745)" ],\n    "fullname" : "javax.script.ScriptException"\n  }\n}')

Use the following workaround:

In [8]: g.scripts.source_file_map
Out[8]: OrderedDict([('/Users/cindy.cao/.virtualenvs/modelgenie/lib/python2.7/site-packages/bulbs/gremlin.groovy', 'gremlin'), ('/Users/cindy.cao/.virtualenvs/modelgenie/lib/python2.7/site-packages/bulbs/neo4jserver/gremlin.groovy', 'gremlin')])

Open /Users/cindy.cao/.virtualenvs/modelgenie/lib/python2.7/site-packages/bulbs/gremlin.groovy 
Delete or comment these 2 methods everywhere: 
  //g.setMaxBufferSize(0)
    //g.startTransaction()

https://groups.google.com/forum/#!msg/gremlin-users/10ppC5b7g6w/xmMpTU5BLggJ
