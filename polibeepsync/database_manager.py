import sqlite3
import pickle
import logging
import threading
from uuid import UUID
from appdirs import user_config_dir, user_data_dir
from polibeepsync.queries import *
from polibeepsync.common import Course, Courses, Folder, CourseFile

database_logger = logging.getLogger("polibeepsync.database")


class MultithreadConnectionManager:
    def __init__(self, database_path):
        self._db_path = database_path
        self._conn = {}

    def __enter__(self):
        try:
            return self._conn[threading.get_ident()]
        except KeyError:
            self._conn[threading.get_ident()] = sqlite3.connect(self._db_path)
            self._conn[threading.get_ident()].row_factory = sqlite3.Row
            return self._conn[threading.get_ident()]

    def __exit__(self, type, value, traceback):
        self._conn[threading.get_ident()].commit()
        # self._conn[threading.get_ident()].close()


class DatabaseManager:
    def __init__(self, database_path, import_course_file_path=None):
        self.__database_version = 1
        self.conn_mgr = MultithreadConnectionManager(database_path)

        # check if we have to update the database schema
        if self.version < self.__database_version:
            if self.version < 1:
                self.__init_database()

        try:
            with open(import_course_file_path, 'rb') as f:
                self.__import_serialized_user(pickle.load(f, fix_imports=False))
                database_logger.info("Old database has been imported "
                                     "successfully.")
        except (EOFError, pickle.PickleError):
            database_logger.error('Can\' import old database, it\'s corrupted',
                                  exc_info=True)
        except (TypeError, FileNotFoundError):
            pass

    def __init_database(self):
        pragmas = [
            INIT_PRAGMAS
        ]
        tables_creation = [
            CREATE_FILES_DATA_TABLE,
            CREATE_FOLDERS_DATA_TABLE,
            CREATE_COURSES_DATA_TABLE,
            CREATE_KEYS_TABLE
        ]
        indexes_creation = [
            CREATE_FILES_DATA_INDEX,
            CREATE_FOLDERS_DATA_INDEX
        ]
        with self.conn_mgr as conn:
            for query in pragmas + tables_creation + indexes_creation:
                database_logger.debug(query)
                conn.executescript(query)
        self.version = self.__database_version

    def __import_serialized_user(self, pickled_user):
        for course in pickled_user.available_courses:
            # Make the internal dict representation compatible with the
            # database
            course._course_dict['saveFolderName'] = course.save_folder_name
            course._course_dict['ManuallyAdded'] = course.manually_added
            course._course_dict['sync'] = course.sync
            course._course_dict['size'] = course.size
            course._course_dict['downloadedSize'] = course.downloaded_size

            def update_file_dict(
                fil: 'CourseFile',
                parent_folder: 'Folder'=None
            ):
                fil._file_dict['parentFolderId'] =\
                    parent_folder.id if parent_folder else None
                fil._file_dict['sync'] = fil.sync
                fil._file_dict['downloadedSize'] = fil.downloaded_size
                fil._file_dict['localCreationTime'] = fil.local_creation_time

            def update_folders_dicts(
                folder: 'Folder',
                parent_folder: 'Folder'=None
            ):
                folder._folder_dict['parentFolderId'] =\
                    parent_folder.id if parent_folder else None
                for fil in folder.files:
                    update_file_dict(fil, folder)

                for folder in folder.folders:
                    update_folders_dicts(folder, folder)

            for fold in course.documents.folders:
                update_folders_dicts(fold)

            for fil in course.documents.files:
                update_file_dict(fil)

            self.store_course(course)

    @property
    def version(self) -> int:
        with self.conn_mgr as conn:
            cur = conn.execute(GET_DB_VERSION)
            data = cur.fetchone()
            return data[0]

    @version.setter
    def version(self, new_version: int):
        if new_version > self.version:
            with self.conn_mgr as conn:
                # SQLITE can't bind parameters to pragmas
                # https://stackoverflow.com/questions/39985599/
                # parameter-binding-not-working-for-sqlite-pragma-table-info
                conn.execute(SET_DB_VERSION.format(new_version))
        else:
            raise ValueError('You cannot downgrade the database version')

    def store_course(self, course: 'Course'):
        with self.conn_mgr as conn:
            conn.execute(STORE_COURSE_DATA, course._course_dict)
        for fold in course.documents.folders:
            self.store_folder(fold)
        for fil in course.documents.files:
            self.store_file(fil)

    def store_file(
        self,
        course_file: 'CourseFile',
        parent_folder: 'Folder'=None
    ):
        with self.conn_mgr as conn:
            file_dict = course_file._file_dict
            if parent_folder:
                file_dict['parentFolderId'] = parent_folder\
                    ._folder_dict['folderId']
            conn.execute(STORE_FILE_DATA, course_file._file_dict)

    def store_folder(self, folder: 'Folder', parent_folder: 'Folder'=None):
        with self.conn_mgr as conn:
            folder_dict = folder._folder_dict
            if parent_folder:
                folder_dict['parentFolderId'] = folder_dict['folderId']
            conn.execute(STORE_FOLDER_DATA, folder_dict)

        for fil in folder.files:
            self.store_file(fil)

        for fold in folder.folders:
            self.store_folder(fold, folder)

    def get_courses(self) -> 'Courses':
        with self.conn_mgr as conn:
            courses_data = conn.execute(GET_ALL_COURSES)
            courses = Courses()
            for course_dict in courses_data:
                course = Course(course_dict)
                course.documents.files = self.get_course_root_files(course)
                course.documents.folders = self.get_course_root_folders(course)
                courses.append(course)
            return courses

    def store_courses(self, courses: 'Courses'):
        for course in courses:
            self.store_course(course)

    def get_course_root_files(self, course: 'Course'):
        with self.conn_mgr as conn:
            data = conn.execute(GET_COURSE_ROOT_FILES, course._course_dict)
        return [CourseFile(fil) for fil in data]

    def get_course_root_folders(self, course: 'Course'):
        with self.conn_mgr as conn:
            data = conn.execute(GET_COURSE_ROOT_FOLDERS, course._course_dict)
            folders = []
            for fol in data:
                folder = Folder(fol)
                folder.folders = self.get_child_folders(folder)
                folder.files = self.get_child_files(folder)
        return folders

    def get_child_folders(self, folder: 'Folder'):
        with self.conn_mgr as conn:
            data = conn.execute(GET_FOLDER_CHILD_FOLDERS, folder._folder_dict)
            folder_list = [Folder(folder_dict) for folder_dict in data]
            for folder in folder_list:
                folder.files = self.get_child_files(folder)
                folder.folders = self.get_child_folders(folder)
        return folder_list

    def get_child_files(self, folder: 'Folder'):
        with self.conn_mgr as conn:
            data = conn.execute(GET_FOLDER_CHILD_FILES, folder._folder_dict)
        return [CourseFile(file_dict) for file_dict in data]

    def set_key(self, key, value):
        with self.conn_mgr as conn:
            conn.execute(SET_KEY, {'key': key, 'value': value})

    def get_key(self, key):
        with self.conn_mgr as conn:
            cur = conn.execute(GET_KEY, (key,))
            data = cur.fetchone()
            if data:
                return data[0]
            else:
                raise LookupError(f'Could not find the key "{key}" in the '
                                  'database')
