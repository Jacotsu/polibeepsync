from behave import *

@when('I ask for the courses')
def step_impl(context):
    context.user.update_available_courses()


@then('I get the courses list')
def step_impl(context):
    assert len(context.user.available_courses) > 0

@when('I select a course')
def step_impl(context):
    context.user.update_available_courses()
    selected_course = context.user.available_courses[0]
    assert selected_course is not None

@when('I ask for files')
def step_impl(context):
    assert True

@then('I get files')
def step_impl(context):
    assert True