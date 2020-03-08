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

from datetime import datetime
from polibeepsync.common import CourseFile, Folder,  GMT1, \
    synclocalwithonline, need_syncing, Course
import pytest
import os


class TestLocalOnlineCompare:
    def test_filenotonline(self):
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})

        local.files.append(a)
        synclocalwithonline(local, online)
        assert local.files == []

    def test_foldernotonline(self):
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})

        sub = Folder({'name': 'sub'})
        sub2 = Folder({'name': 'sub2'})
        local.folders.append(sub)
        local.folders.append(sub2)
        online.folders.append(sub)
        synclocalwithonline(local, online)
        assert local.folders == online.folders

    def test_recursive_filenotonline(self):
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})
        localsub = Folder({'name': 'sub'})
        localsubsub = Folder({'name': 'subsub'})
        localsubsub.files.append(a)
        onlinesub = Folder({'name': 'sub'})
        onlinesubsub = Folder({'name': 'subsub'})

        localsub.folders.append(localsubsub)
        local.folders.append(localsub)
        onlinesub.folders.append(onlinesubsub)
        online.folders.append(onlinesub)
        synclocalwithonline(local, online)
        assert local.folders[0].folders[0].files == []

    def test_recursive_foldernotonline(self):
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})
        localsub = Folder({'name': 'sub'})
        localsubsub = Folder({'name': 'subsub'})
        localsubsub.files.append(a)
        onlinesub = Folder({'name': 'sub'})

        localsub.folders.append(localsubsub)
        local.folders.append(localsub)
        online.folders.append(onlinesub)
        synclocalwithonline(local, online)
        assert local.folders[0].folders == []

    def test_existsonlyonline(self):
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})

        online.files.append(a)
        synclocalwithonline(local, online)
        assert local.files == [a]

    def test_recursiveexistsonlyonline(self):
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})
        b = CourseFile({'title': 'b', 'modifiedDate': 631152060000})
        c = CourseFile({'title': 'c', 'modifiedDate': 631152060000})
        sub = Folder({'name': 'subfolder'})
        subsub = Folder({'name': 'subsubfolder'})

        online.files.append(a)
        sub.files.append(b)
        subsub.files.append(c)
        sub.folders.append(subsub)
        online.folders.append(sub)
        synclocalwithonline(local, online)
        assert local.files == [a]
        assert local.folders == [sub]
        assert local.folders[0].folders == [subsub]
        assert local.folders[0].files == [b]
        assert local.folders[0].folders[0].files == [c]

    def test_neweronline(self):
        gmt1 = GMT1()
        online = Folder({'name': 'online', 'friendlyURL': 'fake'})
        local = Folder({'name': 'local', 'friendlyURL': 'fake'})
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        b = CourseFile({'title': 'b', 'modifiedDate': 631152060000})

        online.files.append(a)
        local.files.append(b)
        synclocalwithonline(local, online)
        assert local.files[0].last_online_edit_time == \
            datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)


class TestNeedSync:
    def test_flat_datenone(self):
        top = '/a/fake/path'
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        docs.files.append(a)

        assert need_syncing(docs, top) == [(a, top)]

    def test_flat_olddate(self):
        """local date older: should update the file (doesn't matter if file
        exists or not"""
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        docs.files.append(a)

        assert need_syncing(docs, top) == [(a, top)]

    def test_flat_newdate(self, tmpdir):
        """local date newer: should not update the file if the file exists"""
        gmt1 = GMT1()
        b = tmpdir.join('a')
        b.write('content')
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})
        a.local_creation_time = datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        docs.files.append(a)

        assert need_syncing(docs, str(tmpdir)) == []

    def test_flat_nofileondisk(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.join('b')
        b.write('content')
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})
        a.local_creation_time = datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        docs.files.append(a)
        assert need_syncing(docs, str(tmpdir)) == [(a, str(tmpdir))]

    def test_flat_nofileondisk2(self, tmpdir):
        """Dates reversed from the previous test"""
        gmt1 = GMT1()
        b = tmpdir.join('b')
        b.write('content')
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        docs.files.append(a)
        assert need_syncing(docs, str(tmpdir)) == [(a, str(tmpdir))]

    def test_recursive_datenone(self):
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        sub = Folder({'name': 'sub', 'friendlyURL': 'fake'})
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, top) == [(a, os.path.join(top, 'sub'))]

    def test_recursive_olddate(self):
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        sub = Folder({'name': 'sub', 'friendlyURL': 'fake'})
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, top) == [(a, os.path.join(top, 'sub'))]

    def test_recursive_newdate(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.mkdir('sub').join('a')
        b.write('content')
        a = CourseFile({'title': 'a', 'modifiedDate': 631152060000})
        a.local_creation_time = datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        sub = Folder({'name': 'sub', 'friendlyURL': 'fake'})
        sub.files.append(a)
        docs.folders.append(sub)

        assert need_syncing(docs, str(tmpdir)) == []

    def test_recursive_nofileondisk(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.mkdir('sub').join('b')
        b.write('content')
        a = CourseFile({'title': 'a.pdf', 'modifiedDate': 662688060000})
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        sub = Folder({'name': 'sub', 'friendlyURL': 'fake'})
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, str(tmpdir)) == [(a, os.path.join(
            str(tmpdir), 'sub'))]

    def test_filenamewithoutextension(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.join('a.pdf')
        b.write('content')
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        docs.files.append(a)
        assert need_syncing(docs, str(tmpdir)) == [(a, str(tmpdir))]

    def test_recursive_filenamewithoutextension(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.mkdir('sub').join('a.pdf')
        b.write('content')
        a = CourseFile({'title': 'a', 'modifiedDate': 662688060000})
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder({'name': 'root', 'friendlyURL': 'fake'})
        sub = Folder({'name': 'sub', 'friendlyURL': 'fake'})
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, str(tmpdir)) == [(a, os.path.join(
            str(tmpdir), 'sub'))]
