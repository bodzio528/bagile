#!/bin/sh

coverage3 run --source='.' manage.py test scrumboard
coverage3 report
