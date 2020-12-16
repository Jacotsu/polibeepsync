__copyright__ = """Copyright 2020 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele (dcdrj.pub@gmail.com)."""

__license__ = """This f is part of poliBeePsync.
poliBeePsync is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

poliBeePsync is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with poliBeePsync. If not, see <http://www.gnu.org/licenses/>.
"""

from polibeepsync.common import Courses, Course, CourseFile, User, Folder, \
    total_size, folder_total_size
import pytest
import json
import os


class TestCourse:
    def test_multiprofessor(self):
        course = Course({'name': '[2017-18] - FISICA [ GALZERANO / VITTORIO '
                         'MAGNI ]',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})
        assert course.simplify_name(course.name) == "Fisica [Galzerano; "\
            "Vittorio Magni]"

    def test_nobracketsprofessor(self):
        course = Course({'name': '[2017-18] - ANALISI MATEMATICA 1 - E. '
                         'MALUTA',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})
        assert course.simplify_name(course.name) == "Analisi Matematica 1 "\
                "[E. Maluta]"

    def test_simplifynamewithsquarebrackets(self):
        course = Course({'name': '[2014-15] - OTTICA FISICA E TECNOLOGIE '
                         'OTTICHE [ C.I. ] [ INGEGNERIA FISICA ]',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})
        assert course.simplify_name(course.name) == "Ottica Fisica E "\
        "Tecnologie Ottiche [C.I.]"

    def test_simplifysimplename(self):
        course = Course({'name': '[2014-15] - SOME STUFF [ A PROFESSOR ]',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Some Stuff [A Professor]"

    def test_simplifycoursewithoutyear(self):
        course = Course({'name': 'RETI LOGICHE [ FABRIZIO FERRANDI ]',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Reti Logiche [Fabrizio "\
            "Ferrandi]"

    def test_simplifycoursewithaccents(self):
        course = Course({'name': "[2017-18] - PROBABILITÀ E STATISTICA PER "
                         "L'INFORMATICA [ GIUSEPPINA GUATTERI ]",
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Probabilità E Statistica"\
            " Per L'Informatica [Giuseppina Guatteri]"

    def test_simplifycoursewithspecialchars(self):
        course = Course({'name': "[2018-19] - SISTEMI INFORMATIVI (PER IL "
                         "SETTORE DELL'INFORMAZIONE) [ MONICA VITALI ] "
                         "classe-694572",
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Sistemi Informativi "\
            "[Monica Vitali]"

    def test_cannotsimplifyname(self):
        course = Course({'name': 'Metid',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Metid"

    def test_simplify_mems(self):
        course = Course({'name': '[2014-15] - MICRO ELECTRO MECHANICAL '
                         'SYSTEMS (MEMS) [ ALBERTO CORIGLIANO ]',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Micro Electro Mechanical"\
            " Systems [Alberto Corigliano]"

    def test_simplify_name_with_student_number(self):
        course = Course({'name': '[2019-20] -088775 - DYNAMICS OF MECHANICAL '
                         'SYSTEMS [ STEFANO BRUNI ]',
                         'friendlyUrl': 'beep.com',
                         'classPK': 1})

        assert course.simplify_name(course.name) == "Dynamics Of Mechanical "\
            "Systems [Stefano Bruni]"

    def test_size_calculation(self):
        afile = CourseFile({'title': 'a',
                            'groupId': 5,
                            'uuid': '50-ddf-kek',
                            'size': 1000})
        asecondfile = CourseFile({'title': 'a',
                                  'groupId': 5,
                                  'uuid': '50-ddf-kek',
                                  'size': 10001})
        afile.size = 1099776
        asecondfile.size = 752640
        complete_list = [(afile, '/his/path'), (asecondfile, '/another/path')]
        assert total_size(complete_list) == afile.size + asecondfile.size

    def test_folder_size(self):
        COMMON_SIZE = 1099776
        a = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 1000})
        b = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 10001})
        c = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 10001})
        d = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 10001})
        e = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 10001})
        f = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 10001})
        a.size = COMMON_SIZE
        b.size = COMMON_SIZE
        c.size = COMMON_SIZE
        d.size = COMMON_SIZE
        e.size = COMMON_SIZE
        f.size = COMMON_SIZE
        top = Folder({'name': 'top', 'friendlyUrl': 'url'})
        middle = Folder({'name': 'middle', 'friendlyUrl': 'url'})
        bottom = Folder({'name': 'bottom', 'friendlyUrl': 'url'})
        top.files.append(a)
        middle.files.append(b)
        middle.files.append(c)
        bottom.files.append(d)
        bottom.files.append(e)
        bottom.files.append(f)
        middle.folders.append(bottom)
        top.folders.append(middle)
        sizes = []
        assert sum(folder_total_size(top, sizes)) == COMMON_SIZE*6

    def test_ignorebeepcourse(self):
        clean_list = [
            Course({'name': '[2016-17] - ANALISI MATEMATICA 1 [ FEDERICO '
                    'MARIO GIOVANNI VEGNI ]',
                    'friendlyUrl': 'beep.com',
                    'classPK': 122035314}),
            Course({'name': '[2016-17] - GEOMETRIA E ALGEBRA LINEARE '
                    '[ PAOLO DULIO ]',
                    'friendlyUrl': 'beep.com',
                    'classPK': 115041662}),
            Course({'name': '[2017-18] - DISPOSITIVI ELETTRONICI [ ANDREA '
                    'LEONARDO LACAITA ]',
                    'friendlyUrl': 'beep.com',
                    'classPK': 115292440})
                ]
        clean_courses = Courses()
        clean_courses.append(*clean_list)
        # the following file is an exact copy of what you get online.
        # It's a one-line document
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'courses-page.json')
        with open(path) as fake_courses:
            temp_courses = json.load(fake_courses)
            courses = Courses()
            for elem in temp_courses:
                course = Course(elem)
                courses.append(course)
            assert courses == clean_courses

    def test_ignoreotherbadnames(self):
        clean_list = [
            Course({'name': '[2016-17] - ANALISI MATEMATICA 1 [ FEDERICO '
                    'MARIO GIOVANNI VEGNI ]',
                    'friendlyUrl': 'beep.com',
                    'classPK': 122035314}),
            Course({'name': '[2016-17] - GEOMETRIA E ALGEBRA LINEARE [ PAOLO '
                    'DULIO ]',
                    'friendlyUrl': 'beep.com',
                    'classPK': 115041662}),
            Course({'name': '[2017-18] - DISPOSITIVI ELETTRONICI [ ANDREA '
                    'LEONARDO LACAITA ]',
                    'friendlyUrl': 'beep.com',
                    'classPK': 115292440})
        ]
        clean_courses = Courses()
        clean_courses.append(*clean_list)
        # the following html file is like courses-page.html, but prettified
        # i.e has multiple lines, like humans would expect html pages.
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'nicer-courses-page.json')
        with open(path) as fake_courses:
            temp_courses = json.load(fake_courses)
            courses = Courses()
            for elem in temp_courses:
                course = Course(elem)
                courses.append(course)
            assert courses == clean_courses

    def test_difference(self):
        a = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 1990})
        b = CourseFile({'title': 'b',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 111})
        c = CourseFile({'title': 'c',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 111})
        e = CourseFile({'title': '3',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 19})
        offline_metal = Course({'name': 'metalli',
                                'friendlyUrl': 'beep.com',
                                'classPK': 1})
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        offline_metal.append(a, b, c)
        metal.append(a, b, e)
        assert set(metal-offline_metal) == set([e])

    def test_equality(self):
        a = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 1990})
        b = CourseFile({'title': 'b',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 111})
        c = CourseFile({'title': 'c',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 111})

        offline_metal = Course({'name': 'metalli',
                                'friendlyUrl': 'beep.com',
                                'classPK': 1})
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        offline_metal.append(a, b)
        metal.append(a, b, c)
        assert metal == offline_metal

    def test_inequality(self):
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        other = Course({'name': 'mthing',
                        'friendlyUrl': 'beep.com',
                        'classPK': 2})

        assert metal != other

    def test_getitem(self):
        a = CourseFile({'title': 'a',
                        'groupId': 5,
                        'uuid': '50-ddf-kek',
                        'size': 1990})
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        metal.append(a)
        assert metal['a'] == a

    def test_getitem_raises_keyerror(self):
        with pytest.raises(KeyError):
            a = CourseFile({'title': 'a',
                            'groupId': 5,
                            'uuid': '50-ddf-kek',
                            'size': 1990})
            metal = Course({'name': 'metalli',
                            'friendlyUrl': 'beep.com',
                            'classPK': 1})

            metal.append(a)
            metal['b']

    def test__repr__(self):
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        assert repr(metal) == "Course metalli"

    def test__contains__a_file(self):
        onefile = CourseFile({'title': 'a',
                              'groupId': 5,
                              'uuid': '50-ddf-kek',
                              'size': 1990})
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        metal.append(onefile)
        assert onefile in metal

    def test__doesnt_contain__a_file(self):
        onefile = CourseFile({'title': 'a',
                              'groupId': 5,
                              'uuid': '50-ddf-kek',
                              'size': 1990})
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        assert onefile not in metal

    def test__init__(self):
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})

        assert hasattr(metal, 'elements')


class TestCourses:
    def test_difference(self):
        polim = Course({'name': 'polimeri',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        offline_polim = Course({'name': 'polimeri',
                                'friendlyUrl': 'beep.com',
                                'classPK': 1})

        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        offline_metal = Course({'name': 'metalli',
                                'friendlyUrl': 'beep.com',
                                'classPK': 1})

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
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        metalinside = Course({'name': 'metalli',
                              'friendlyUrl': 'beep.com',
                              'classPK': 1})
        other = Course({'name': 'other',
                        'friendlyUrl': 'doesntmatter',
                        'classPK': 2})

        courses = Courses()
        courses.append(metalinside, other)
        assert metal in courses

    def test_notbelonging(self):
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        courseinside = Course({'name': 'polimeri',
                               'friendlyUrl': 'beep.com',
                               'classPK': 1})
        other = Course({'name': 'other',
                        'friendlyUrl': 'doesntmatter',
                        'classPK': 2})

        courses = Courses()
        courses.append(courseinside, other)
        assert metal not in courses

    def test_return_hash(self):
        courses = Courses()
        courses.append(Course({'name': 'metalli',
                               'friendlyUrl': 'beep.com',
                               'classPK': 1}))
        assert hash(courses) is not None

    def test_hash_not_depending_on_order(self):
        oneorder = Courses()
        otherorder = Courses()
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        polim = Course({'name': 'polimeri',
                        'friendlyUrl': 'beep.it',
                        'classPK': 2})

        oneorder.append(metal, polim)
        otherorder.append(polim, metal)
        assert hash(oneorder) == hash(otherorder)

    def test_append(self):
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        other = Course({'name': 'other',
                        'friendlyUrl': 'doesntmatter',
                        'classPK': 2})

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
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        other = Course({'name': 'other',
                        'friendlyUrl': 'doesntmatter',
                        'classPK': 2})
        all.append(metal, other)
        one.append(other)
        all.remove(metal)
        assert all == one

    def test__len__(self):
        courses = Courses()
        courses.append(Course({'name': 'metalli',
                               'friendlyUrl': 'beep.com',
                               'classPK': 1}),
                       Course({'name': 'other',
                               'friendlyUrl': 'beep.com',
                               'classPK': 2}))

        assert len(courses) == 2


class TestCourseFile:
    def test_repr(self):
        a = CourseFile({'title': 'metalli name',
                        'modifiedDate': 100000})
        assert repr(a) == "metalli name"

    def test_notequal(self):
        a = CourseFile({'title': 'metalli',
                        'modifiedDate': 1000000})
        b = CourseFile({'title': 'other',
                        'modifiedDate': 1000000})
        assert a != b


class TestFolder:
    def test_repr(self):
        a = Folder({'name': 'name', 'friendlyUrl': 'fakeurl'})
        assert repr(a) == "name folder"


class TestUser:
    def test_sync_courses_new_course(self):
        guy = User('fakeid', 'fakepwd')
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        other = Course({'name': 'other',
                        'friendlyUrl': 'doesntmatter',
                        'classPK': 2})
        online = Courses()
        online.append(metal, other)
        guy.available_courses.append(metal)
        guy.sync_available_courses(online)
        assert guy.available_courses == online

    def test_sync_courses_remove(self):
        guy = User('fakeid', 'fakepwd')
        metal = Course({'name': 'metalli',
                        'friendlyUrl': 'beep.com',
                        'classPK': 1})
        other = Course({'name': 'other',
                        'friendlyUrl': 'doesntmatter',
                        'classPK': 2})

        online = Courses()
        online.append(metal)
        guy.available_courses.append(metal, other)
        guy.sync_available_courses(online)
        assert guy.available_courses == online
