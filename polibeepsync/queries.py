# -------------------------- [PRAGMAS INITIALIZATION] -------------------------

INIT_PRAGMAS = '''
    -- These pragmas enhance performance
    PRAGMA journal_mode = WAL;
    PRAGMA threads = 4;
'''
# ---------------------------- [TABLES CREATION] ------------------------------

CREATE_FILES_DATA_TABLE = '''
    CREATE TABLE IF NOT EXISTS course_files (
        fileInternalId INTEGER PRIMARY KEY AUTOINCREMENT,
        extension TEXT NOT NULL,
        version INTEGER DEFAULT 0,
        fileEntryId INTEGER UNIQUE,
        parentFolderId INTEGER,
        groupId INTEGER NOT NULL,
        title TEXT NOT NULL,
        modifiedDate INTEGER DEFAULT 0 CHECK(modifiedDate >= 0),
        localCreationTime INTEGER CHECK(localCreationTime >= 0),
        sync INTEGER CHECK(sync BETWEEN 0 AND 1),


        -- 16 bytes
        uuid BLOB NOT NULL UNIQUE,

        size INTEGER DEFAULT 0 CHECK(size >= 0),
        downloadedSize INTEGER DEFAULT 0 CHECK(downloadedSize >= 0),

        FOREIGN KEY(parentFolderId) REFERENCES course_folders(folderId)
        FOREIGN KEY(groupId) REFERENCES courses(groupId)
    );
'''

# folder_id == -1 means that the folder doesn't exist on BeeP
CREATE_FOLDERS_DATA_TABLE = '''
    CREATE TABLE IF NOT EXISTS course_folders (
        folderInternalId INTEGER PRIMARY KEY AUTOINCREMENT,
        folderId INTEGER NOT NULL UNIQUE,
        lastPostDate INTEGER DEFAULT 0 CHECK(lastPostDate >= 0),
        name TEXT NOT NULL,
        parentFolderId INTEGER,
        groupId INTEGER NOT NULL,
        FOREIGN KEY(parentFolderId) REFERENCES course_folders(folderId),
        FOREIGN KEY(groupId) REFERENCES courses(groupId)
    );
'''

CREATE_COURSES_DATA_TABLE = '''
     CREATE TABLE IF NOT EXISTS courses (
        courseInternalId INTEGER PRIMARY KEY AUTOINCREMENT,
        friendlyUrl TEXT,
        name TEXT,
        classPK INTEGER NOT NULL,
        groupId INTEGER NOT NULL,
        folderId INTEGER,
        saveFolderName TEXT,
        -- boolean
        ManuallyAdded INTEGER DEFAULT 0 CHECK(ManuallyAdded BETWEEN 0 AND 1),
        sync INTEGER DEFAULT 0 CHECK(sync BETWEEN 0 AND 1),
        size INTEGER DEFAULT 0 CHECK(size >= 0),
        downloadedSize INTEGER DEFAULT 0 CHECK(downloadedSize >= 0)
    );
'''

CREATE_KEYS_TABLE = '''
    CREATE TABLE IF NOT EXISTS user_keys (
        key TEXT PRIMARY KEY,
        value TEXT
    ) WITHOUT ROWID;
'''

# ---------------------------- [INDEXES CREATIONS] ----------------------------

CREATE_FILES_DATA_INDEX = '''
    CREATE UNIQUE INDEX IF NOT EXISTS files_parent_folder_id_idx
    ON course_files(parentFolderId, groupId);
'''

CREATE_FOLDERS_DATA_INDEX = '''
    CREATE UNIQUE INDEX IF NOT EXISTS folder_ids_idx
    ON course_folders(folderId);
'''

# ------------------------------ [DATA GET/STORE] -----------------------------

STORE_FILE_DATA = '''
    REPLACE INTO course_files(
        extension,
        version,
        fileEntryId,
        title,
        groupId,
        modifiedDate,
        uuid,
        size,
        downloadedSize,
        parentFolderId
        )
    VALUES (
        :extension,
        :version,
        :fileEntryId,
        :title,
        :groupId,
        :uuid,
        :modifiedDate,
        :localCreationTime
        :sync
        :downloadedSize,
        :size,
        :parentFolderId);
'''

STORE_FOLDER_DATA = '''
    REPLACE INTO course_folders(
        folderId,
        lastPostDate,
        name,
        groupId,
        parentFolderId)
    VALUES (
        :folderId,
        :lastPostDate,
        :name,
        :groupId,
        :parentFolderId);
'''

STORE_COURSE_DATA = '''
    REPLACE INTO courses(
        friendlyUrl,
        name,
        classPK,
        groupId,
        folderId,
        saveFolderName,
        ManuallyAdded,
        sync,
        downloadedSize,
        size)
    VALUES (
        :friendlyUrl,
        :name,
        :classPK,
        :groupId,
        :saveFolderName,
        :folderId,
        :ManuallyAdded,
        :sync,
        :size,
        :downloadedSize);
'''

GET_ALL_COURSES = '''
    SELECT *
    FROM courses;
'''

GET_COURSE_ROOT_FOLDERS = '''
    SELECT *
    FROM course_folders
    WHERE classPK = :classPK AND NOT parentFolderId;
'''

GET_COURSE_ROOT_FILES = '''
    SELECT *
    FROM course_files
    WHERE classPK = :classPK AND NOT parentFolderId;
'''

GET_FOLDER_CHILD_FILES = '''
    SELECT *
    FROM course_files
    WHERE parentFolderId = :folderId
'''

GET_FOLDER_CHILD_FOLDERS = '''
    SELECT *
    FROM course_folders
    WHERE parentFolderId = :folderId
'''

SET_KEY = 'REPLACE INTO user_keys(key, value) VALUES (:key, :value);'

GET_KEY = 'SELECT value FROM user_keys WHERE key = ?;'

GET_DB_VERSION = 'PRAGMA user_version;'

SET_DB_VERSION = 'PRAGMA user_version = {};'
