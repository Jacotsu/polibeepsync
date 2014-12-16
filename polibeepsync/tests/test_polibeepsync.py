from polibeepsync.polibeepsync import Courses, Course, CourseFile
import pytest


class TestCourse:
    def test_difference(self):
        a = CourseFile('a', '1990')
        b = CourseFile('b', '111')
        c = CourseFile('c', '1111')
        e = CourseFile('e', '19')
        offline_metal = Course('metalli', 'beep.com')
        metal = Course('metalli', 'beep.com')
        offline_metal.append(a, b, c)
        metal.append(a, b, e)
        assert set(metal-offline_metal) == set([e])

    def test_inequality(self):
        a = CourseFile('a', '1990')
        b = CourseFile('b', '111')
        c = CourseFile('c', '1111')
        offline_metal = Course('metalli', 'beep.com')
        metal = Course('metalli', 'beep.com')
        offline_metal.append(a, b)
        metal.append(a, b, c)
        assert metal != offline_metal

    def test_getitem(self):
        a = CourseFile('a', '1990')
        metal = Course('metalli', 'beep.com')
        metal.append(a)
        assert metal['a'] == a

    def test_getitem_raises_keyerror(self):
        with pytest.raises(KeyError):
            a = CourseFile('a', '1990')
            metal = Course('metalli', 'beep.com')
            metal.append(a)
            metal['b']


class TestCourses:
    def test_difference(self):
        offline_metal = Course('metalli', 'beep.com')
        offline_polim = Course('polimeri', 'beep.it')
        metal = Course('metalli', 'beep.com')
        polim = Course('polimeri', 'beep.it')

        offline = Courses()
        offline.append(offline_polim, offline_metal)
        online = Courses()
        online.append(metal, polim)
        for course in online:
            print('online {}'.format(course.name))
        for course in offline:
            print('offline {}'.format(course.name))
        assert online - offline == []

    def test_belonging(self):
        metal = Course('metalli', 'beep.com')
        metalinside = Course('metalli', 'beep.com')
        other = Course('other', 'doesntmatter')
        courses = Courses()
        courses.append(metalinside, other)
        assert metal in courses

    def test_notbelonging(self):
        metal = Course('metalli', 'beep.com')
        courseinside = Course('polimeri', 'beep.com')
        other = Course('other', 'doesntmatter')
        courses = Courses()
        courses.append(courseinside, other)
        assert metal not in courses

    def test_return_hash(self):
        courses = Courses()
        courses.append(Course('metalli', 'beep.com'))
        assert hash(courses) is not None

    def test_hash_not_depending_on_order(self):
        oneorder = Courses()
        otherorder = Courses()
        metal = Course('metalli', 'beep.com')
        polim = Course('polimeri', 'beep.it')
        oneorder.append(metal, polim)
        otherorder.append(polim, metal)
        assert hash(oneorder) == hash(otherorder)

    def test_append(self):
        metal = Course('metalli', 'beep.com')
        other = Course('other', 'doesntmatter')
        oneatatime = Courses()
        # append in two steps
        oneatatime.append(metal)
        oneatatime.append(other)
        twocourses = Courses()
        twocourses.append(other, metal)
        # append in one step
        assert twocourses == oneatatime


class TestCourseFile:
    pass
