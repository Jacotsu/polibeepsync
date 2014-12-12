from behave import *

@when('I ask for the courses')
def step_impl(context):
    context.courses = context.user.get_available_courses()


@then('I get the courses list')
def step_impl(context):
    assert type(context.courses) == list

@when('I select a course')
def step_impl(context):
    selected_course = context.courses[0]

@when('I ask for files')
def step_impl(context):
    files_dict = context.selected_course.get_files_list()

@then('I get files')
def step_impl(context):
    assert type(context.files_dict) == dict