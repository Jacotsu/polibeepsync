from datetime import datetime
from polibeepsync.common import CourseFile, Folder,  GMT1, \
    synclocalwithonline, need_syncing, Course
import pytest
import os


class TestLocalOnlineCompare:
    def test_filenotonline(self):
        gmt1 = GMT1()
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        local.files.append(a)
        synclocalwithonline(local, online)
        assert local.files == []

    def test_foldernotonline(self):
        gmt1 = GMT1()
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        sub = Folder('sub', 'fake')
        sub2 = Folder('sub2', 'fake')
        local.folders.append(sub)
        local.folders.append(sub2)
        online.folders.append(sub)
        synclocalwithonline(local, online)
        assert local.folders == online.folders

    def test_recursive_filenotonline(self):
        gmt1 = GMT1()
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        localsub = Folder('sub', 'fake')
        localsubsub = Folder('subsub', 'fake')
        localsubsub.files.append(a)
        onlinesub = Folder('sub', 'fake')
        onlinesubsub = Folder('subsub', 'fake')
        localsub.folders.append(localsubsub)
        local.folders.append(localsub)
        onlinesub.folders.append(onlinesubsub)
        online.folders.append(onlinesub)
        synclocalwithonline(local, online)
        assert local.folders[0].folders[0].files == []

    def test_recursive_foldernotonline(self):
        gmt1 = GMT1()
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        localsub = Folder('sub', 'fake')
        localsubsub = Folder('subsub', 'fake')
        localsubsub.files.append(a)
        onlinesub = Folder('sub', 'fake')
        localsub.folders.append(localsubsub)
        local.folders.append(localsub)
        online.folders.append(onlinesub)
        synclocalwithonline(local, online)
        assert local.folders[0].folders == []

    def test_existsonlyonline(self):
        gmt1 = GMT1()
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        online.files.append(a)
        synclocalwithonline(local, online)
        assert local.files == [a]

    def test_recursiveexistsonlyonline(self):
        gmt1 = GMT1()
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        sub = Folder('subfolder', 'fake')
        subsub = Folder('subsubfolder', 'fake')
        b = CourseFile('b', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        c = CourseFile('c', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
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
        online = Folder('online', 'fake')
        local = Folder('local', 'fake')
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        b = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        online.files.append(a)
        local.files.append(b)
        synclocalwithonline(local, online)
        assert local.files[0].last_online_edit_time == \
            datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)


class TestNeedSync:
    def test_flat_datenone(self):
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        docs = Folder('root', 'fake')
        docs.files.append(a)

        assert need_syncing(docs, top, []) == [(a, top)]

    def test_flat_olddate(self):
        """local date older: should update the file (doesn't matter if file
        exists or not"""
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        docs.files.append(a)

        assert need_syncing(docs, top, []) == [(a, top)]

    def test_flat_newdate(self, tmpdir):
        """local date newer: should not update the file if the file exists"""
        gmt1 = GMT1()
        b = tmpdir.join('a')
        b.write('content')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        docs.files.append(a)

        assert need_syncing(docs, str(tmpdir), []) == []

    def test_flat_nofileondisk(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.join('b')
        b.write('content')
        a = CourseFile('a.pdf', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        docs.files.append(a)
        assert need_syncing(docs, str(tmpdir), []) == [(a, str(tmpdir))]

    def test_flat_nofileondisk2(self, tmpdir):
        """Dates reversed from the previous test"""
        gmt1 = GMT1()
        b = tmpdir.join('b')
        b.write('content')
        a = CourseFile('a.pdf', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        docs.files.append(a)
        assert need_syncing(docs, str(tmpdir), []) == [(a, str(tmpdir))]

    def test_recursive_datenone(self):
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        docs = Folder('root', 'fake')
        sub = Folder('sub', 'fake')
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, top, []) == [(a, os.path.join(top, 'sub'))]

    def test_recursive_olddate(self):
        gmt1 = GMT1()
        top = '/a/fake/path'
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        sub = Folder('sub', 'fake')
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, top, []) == [(a, os.path.join(top, 'sub'))]

    def test_recursive_newdate(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.mkdir('sub').join('a')
        b.write('content')
        a = CourseFile('a', 'url', datetime(1990, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1991, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        sub = Folder('sub', 'fake')
        sub.files.append(a)
        docs.folders.append(sub)

        assert need_syncing(docs, str(tmpdir), []) == []

    def test_recursive_nofileondisk(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.mkdir('sub').join('b')
        b.write('content')
        a = CourseFile('a.pdf', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        sub = Folder('sub', 'fake')
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, str(tmpdir), []) == [(a, os.path.join(
            str(tmpdir), 'sub'))]

    def test_filenamewithoutextension(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.join('a.pdf')
        b.write('content')
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        docs.files.append(a)
        assert need_syncing(docs, str(tmpdir), []) == [(a, str(tmpdir))]

    def test_recursive_filenamewithoutextension(self, tmpdir):
        gmt1 = GMT1()
        b = tmpdir.mkdir('sub').join('a.pdf')
        b.write('content')
        a = CourseFile('a', 'url', datetime(1991, 1, 1, 1, 1, tzinfo=gmt1))
        a.local_creation_time = datetime(1990, 1, 1, 1, 1, tzinfo=gmt1)
        docs = Folder('root', 'fake')
        sub = Folder('sub', 'fake')
        sub.files.append(a)
        docs.folders.append(sub)
        assert need_syncing(docs, str(tmpdir), []) == [(a, os.path.join(
            str(tmpdir), 'sub'))]