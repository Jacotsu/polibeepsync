from behave import *

@when('a file is not available locally')
def step_impl(context):
    assert False

@then('I should get a local copy')
def step_impl(context):
    assert False

@when('a file on BeeP is newer than the local copy')
def step_impl(context):
    assert False

@then('I should get the updated file')
def step_impl(context):
    assert False

@when('a local file doesn\'t exist on BeeP')
def step_impl(context):
    assert False

@then('nothing should happen')
def step_impl(context):
    assert False