from os import environ
from polibeepsync.common import User
from behave import *

def before_scenario(context, scenario):
    """Code to run before every scenario, except login tests"""
    if 'require_login' in scenario.tags:
        usercode = environ["USERCODE"]
        password = environ["PASSWORD"]
        context.user = User(usercode, password)
        context.user.visit()
        context.user.login()
