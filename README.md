
after starting compose, login to splunk (http://localhost:8000/):
- create an index "pyapp"
- create an HEC token Settings > Data Inputs > HTTP Event Collector, set default index to "pyapp"
- add the token it to fluentd.conf