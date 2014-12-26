from behave import *
from polibeepsync.common import User, Course, Courses, CourseFile

@when('I ask for the courses')
def step_impl(context):
    guy= User('fakeid', 'fakepwd')
    course_a = Course('a', 'alink')
    course_b = Course('b', 'blink')
    guy.available_courses.append(course_a, course_b)
    context.courses = guy.available_courses


@then('I get the courses list')
def step_impl(context):
    # not a great test
    assert len(context.courses) > 0

@when('I select a course')
def step_impl(context):
    fake_course = Course('fakename', 'fakelink')
    file_a = CourseFile('filea', '03/11/14 12.33')
    file_b = CourseFile('fileb', '06/09/14 11.25')
    fake_course.append(file_a, file_b)
    context.selected_course = fake_course

@when('I ask for files')
def step_impl(context):
    context.files = context.selected_course.files
    # chiamare metodo che riceve i file per un corso
    #context.files = context.selected_course.files

@then('I get files')
def step_impl(context):
    # not a great test
    assert len(context.files) == 2

@when('a new course is available')
def step_impl(context):
    new_course = Course('newcourse', 'fakelink')
    common_course = Course('common', 'commonlink')
    guy = User('fakeid', 'fakepwd')
    guy.available_courses.append(common_course)
    context.guy = guy
    online_courses = Courses()
    online_courses.append(new_course, common_course)
    context.online_courses = online_courses

@then('it should be added to the local copy')
def step_impl(context):
    context.guy.sync_available_courses(context.online_courses)
    assert context.guy.available_courses == context.online_courses

@when('a course is no more available')
def step_impl(context):
    new_course = Course('newcourse', 'fakelink')
    common_course = Course('common', 'commonlink')
    guy = User('fakeid', 'fakepwd')
    guy.available_courses.append(new_course, common_course)
    context.guy = guy
    online_courses = Courses()
    online_courses.append(common_course)
    context.online_courses = online_courses

@then('it should be removed from the local copy')
def step_impl(context):
    context.guy.sync_available_courses(context.online_courses)
    assert context.guy.available_courses == context.online_courses