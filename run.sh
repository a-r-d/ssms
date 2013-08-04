## Python 2.x has issues with unicode running from cron sometimes...
# if you run this from cron, set the default encoding.
export PYTHONIOENCODING=utf-8
python /opt/ssms/server.py
