from datetime import datetime
from polibeepsync.common import CourseFile, Folder,  GMT1, \
    synclocalwithonline
import pytest


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