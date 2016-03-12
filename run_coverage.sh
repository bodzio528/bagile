#!/bin/sh

coverage run manage.py test --settings=bagile.test_settings scrumboard
coverage report