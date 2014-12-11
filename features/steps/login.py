from behave import *
from os import environ
from polibeepsync import User
from selenium import webdriver
import requests

@given('I have correct username and password')
def step_impl(context):
    usercode = environ["USERCODE"]
    password = environ["PASSWORD"]
    user = User(usercode, password)
    context.user = user

@given('I\'m logged in')
def step_impl(context):
    assert False

@given('the website is reachable')
def step_impl(context):
    try:
        context.user.visit()
    except (requests.ConnectionError, requests.Timeout):
        assert False
    else:
        assert True

@when('I visit the login page')
def step_impl(context):
    context.user.visit()

@then("I should access the private area")
def step_impl(context):
    context.user.login()
    assert hasattr(context.user, "session")

@given('I have wrong username or password')
def step_impl(context):
    usercode = 99999999
    password = 'abcdef'
    user = User(usercode, password)
    context.user= user

@then('I should get an exception "Invalid username or password"')
def step_impl(context):
    try:
        context.user.login()
    except :
        assert True
    else:
        assert False