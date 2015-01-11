from polibeepsync.common import Courses, Course, CourseFile, User, Folder, total_size
import pytest
import os


class TestCourse:
    def test_simplifynamewithsquarebrackets(self):
        course = Course('[2014-15] - OTTICA FISICA E TECNOLOGIE OTTICHE [C.I.] [ INGEGNERIA FISICA ]', 'beep.com')
        assert course.simplify_name(course.name) == "Ottica Fisica E Tecnologie Ottiche"

    def test_simplifysimplename(self):
        course = Course('[2014-15] - SOME STUFF [ A PROFESSOR ]', 'beep.com')
        assert course.simplify_name(course.name) == "Some Stuff"

    def test_cannotsimplifyname(self):
        course = Course('Metid', 'beep.com')
        assert course.simplify_name(course.name) == "Metid"

    def test_simplify_mems(self):
        course = Course('[2014-15] - MICRO ELECTRO MECHANICAL SYSTEMS (MEMS) [ ALBERTO CORIGLIANO ]', 'beep.com')
        assert course.simplify_name(course.name) == "Micro Electro Mechanical Systems"

    def test_size_calculation(self):
        afile = CourseFile('name', 'url', '1000')
        asecondfile = CourseFile('name', 'url', '10001')
        afile.size = 1099776
        asecondfile.size = 752640
        complete_list = [(afile, '/his/path'), (asecondfile, '/another/path')]
        assert total_size(complete_list) == afile.size + asecondfile.size

    def test_ignorebeepcourse(self):
        clean_list = [
            Course('[2014-15] - ADVANCED CHEMISTRY FOR MATERIALS ENGINEERING [ MATERIALS ENGINEERING AND NANOTECHNOLOGY ]', 'beep.com'),
            Course('[2014-15] - DURABILITY OF MATERIALS [ MATERIALS ENGINEERING AND NANOTECHNOLOGY ]', 'beep.com'),
            Course('[2014-15] - FAILURE AND CONTROL OF METALS [ MAURIZIO VEDANI ]', 'beep.com'),
            Course('[2014-15] - MATHEMATICAL METHODS FOR MATERIALS ENGINEERING [ MICHELE DI CRISTO ]', 'beep.com'),
            Course('[2014-15] - MECHANICAL BEHAVIOUR OF MATERIALS [ LAURA VERGANI ]', 'beep.com'),
            Course('[2014-15] - MICRO ELECTRO MECHANICAL SYSTEMS (MEMS) [ ALBERTO CORIGLIANO ]', 'beep.com'),
            Course('[2014-15] - PHYSICAL PROPERTIES OF MOLECULAR MATERIALS [ MATTEO MARIA SAVERIO TOMMASINI ]', 'beep.com'),
            Course('[2014-15] - PHYSICS OF NANOSTRUCTURES [ CARLO S. CASARI ]', 'beep.com'),
            Course('[2014-15] - SOLID STATE PHYSICS [ CARLO ENRICO BOTTANI ]', 'beep.com'),
            Course('[2014-15] - STRUCTURAL CHEMISTRY OF MATERIALS [ GUIDO RAOS ]', 'beep.com'),
            ]
        clean_courses = Courses()
        clean_courses.append(*clean_list)
        # the following file is an exact copy of what you get online.
        # It's a one-line document
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'courses-page.html')
        with open(path) as fake_courses:
            text = fake_courses.read()
            user = User("doesn't matter", 'nope')
            temp_courses = user._courses_scraper(text)
            courses = Courses()
            for elem in temp_courses:
                course = Course(elem[0], elem[1])
                courses.append(course)
            assert courses == clean_courses

    def test_ignoreotherbadnames(self):
        clean_list = [
            Course('[2014-15] - ADVANCED CHEMISTRY FOR MATERIALS ENGINEERING [ MATERIALS ENGINEERING AND NANOTECHNOLOGY ]', 'beep.com'),
            Course('[2014-15] - DURABILITY OF MATERIALS [ MATERIALS ENGINEERING AND NANOTECHNOLOGY ]', 'beep.com'),
            Course('[2014-15] - FAILURE AND CONTROL OF METALS [ MAURIZIO VEDANI ]', 'beep.com'),
            Course('[2014-15] - MATHEMATICAL METHODS FOR MATERIALS ENGINEERING [ MICHELE DI CRISTO ]', 'beep.com'),
            Course('[2014-15] - MECHANICAL BEHAVIOUR OF MATERIALS [ LAURA VERGANI ]', 'beep.com'),
            Course('[2014-15] - MICRO ELECTRO MECHANICAL SYSTEMS (MEMS) [ ALBERTO CORIGLIANO ]', 'beep.com'),
            Course('[2014-15] - PHYSICAL PROPERTIES OF MOLECULAR MATERIALS [ MATTEO MARIA SAVERIO TOMMASINI ]', 'beep.com'),
            Course('[2014-15] - PHYSICS OF NANOSTRUCTURES [ CARLO S. CASARI ]', 'beep.com'),
            Course('[2014-15] - SOLID STATE PHYSICS [ CARLO ENRICO BOTTANI ]', 'beep.com'),
            Course('[2014-15] - STRUCTURAL CHEMISTRY OF MATERIALS [ GUIDO RAOS ]', 'beep.com'),
            ]
        clean_courses = Courses()
        clean_courses.append(*clean_list)
        # the following html file is like courses-page.html, but prettified
        # i.e has multiple lines, like humans would expect html pages.
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'nicer-courses-page.html')
        with open(path) as fake_courses:
            text = fake_courses.read()
            user = User("doesn't matter", 'nope')
            temp_courses = user._courses_scraper(text)
            courses = Courses()
            for elem in temp_courses:
                course = Course(elem[0], elem[1])
                courses.append(course)
            assert courses == clean_courses


    def test_difference(self):
        a = CourseFile('a', 'url', '1990')
        b = CourseFile('b', 'url', '111')
        c = CourseFile('c', 'url', '1111')
        e = CourseFile('e', 'url', '19')
        offline_metal = Course('metalli', 'beep.com')
        metal = Course('metalli', 'beep.com')
        offline_metal.append(a, b, c)
        metal.append(a, b, e)
        assert set(metal-offline_metal) == set([e])

    def test_equality(self):
        a = CourseFile('a', 'url', '1990')
        b = CourseFile('b', 'url', '111')
        c = CourseFile('c', 'url', '1111')
        offline_metal = Course('metalli', 'beep.com')
        metal = Course('metalli', 'beep.com')
        offline_metal.append(a, b)
        metal.append(a, b, c)
        assert metal == offline_metal

    def test_inequality(self):
        other = Course('thing', 'beep.com')
        metal = Course('metalli', 'beep.com')
        assert metal != other

    def test_getitem(self):
        a = CourseFile('a', 'url', '1990')
        metal = Course('metalli', 'beep.com')
        metal.append(a)
        assert metal['a'] == a

    def test_getitem_raises_keyerror(self):
        with pytest.raises(KeyError):
            a = CourseFile('a', 'url', '1990')
            metal = Course('metalli', 'beep.com')
            metal.append(a)
            metal['b']

    def test__repr__(self):
        metal = Course('metalli', 'beep.com')
        assert repr(metal) == "Course metalli"

    def test__contains__a_file(self):
        onefile = CourseFile('a', 'url', '1990')
        metal = Course('metalli', 'beep.com')
        metal.append(onefile)
        assert onefile in metal

    def test__doesnt_contain__a_file(self):
        onefile = CourseFile('a', 'url', '1990')
        metal = Course('metalli', 'beep.com')
        assert onefile not in metal

    def test__init__(self):
        metal = Course('metalli', 'beep.com')
        assert hasattr(metal, 'elements')


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

    def test_remove(self):
        all = Courses()
        one = Courses()
        metal = Course('metalli', 'beep.com')
        other = Course('other', 'doesntmatter')
        all.append(metal, other)
        one.append(other)
        all.remove(metal)
        assert all == one

    def test__len__(self):
        courses = Courses()
        courses.append(Course('metalli', 'beep.com'),
                       Course('other', 'doesntmatter'))
        assert len(courses) == 2


class TestCourseFile:
    def test_repr(self):
        a = CourseFile('nice name', 'beep.com', 'fake time')
        assert repr(a) == "nice name"

    def test_notequal(self):
        a = CourseFile('nice name', 'beep.com', 'fake time')
        b = CourseFile('another file', 'beep.com', 'fake time')
        assert a != b


class TestFolder:
    def test_repr(self):
        a = Folder('name', 'fakeurl')
        assert repr(a) == "name folder"


class TestUser:
    def test_sync_courses_new_course(self):
        guy = User('fakeid', 'fakepwd')
        metal = Course('metalli', 'beep.com')
        other = Course('other', 'doesntmatter')
        online = Courses()
        online.append(metal, other)
        guy.available_courses.append(metal)
        guy.sync_available_courses(online)
        assert guy.available_courses == online

    def test_sync_courses_remove(self):
        guy = User('fakeid', 'fakepwd')
        metal = Course('metalli', 'beep.com')
        other = Course('other', 'doesntmatter')
        online = Courses()
        online.append(metal)
        guy.available_courses.append(metal, other)
        guy.sync_available_courses(online)
        assert guy.available_courses == online
