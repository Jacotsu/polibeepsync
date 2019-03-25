init_db = '''
CREATE TABLE IF NOT EXISTS course_files(
    file_entry_id INT PRIMARY KEY,
    folder_id INT,
    group_id INT,
    uuid TEXT,
    modified_date INT,
    to_sync INT DEFAULT 1,
    title TEXT,
    downloaded_bytes INT DEFAULT 0,
    size INT,
    relative_path TEXT,
    friendly_url TEXT,
    version TEXT
);

CREATE TABLE IF NOT EXISTS course_folders(
    folder_id INT PRIMARY KEY,
    parent_folder_id INT,
    group_id INT,
    uuid TEXT,
    name TEXT,
    modified_date INT,
    to_sync INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS courses(
    class_pk INT PRIMARY KEY,
    group_id INT,
    parent_group_id INT,
    friendly_url TEXT,
    name TEXT,
    to_sync INT DEFAULT 1,
    site INT,
    type INT
);

CREATE TRIGGER IF NOT EXISTS folder_deletion_propagation BEFORE DELETE
ON course_folders
BEGIN
    DELETE FROM course_files
    WHERE course_files.folder_id = course_folders.folder_id;
END;

CREATE TRIGGER IF NOT EXISTS course_deletion_propagation BEFORE DELETE
ON courses
BEGIN
    DELETE FROM course_folders WHERE course.group_id = course_folders.group_id
END;
'''
