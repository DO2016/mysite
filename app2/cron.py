from django.core.management import execute_from_command_line
import subprocess
import os

def my_scheduled_job():
    output = subprocess.check_output(["python", "/Users/dorlov/Projects/test1/mysite/manage.py", "create_10k"])
    print output