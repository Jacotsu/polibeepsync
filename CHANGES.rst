Changelog
=========

0.7.0 (2020-04-13)
------------------
New
~~~
- Added support for MAC OS Catalina [DCDRJ]
- Added more startup options [DCDRJ]

  - `--sync-on-startup`: lets you override your settings file, and sync
    the course files on application startup
  - `--sync-interval`: lets you override your settings file sync frequency
- Added built in backup certificate to mitigate malformed beep ones [DCDRJ]

Fix
~~~
- Added missing dependencies to setup.py [DCDRJ]
- Minor UI improvements [DCDRJ]
- Minor code cleanup [DCDRJ]
- Increased info logging [DCDRJ]
- Fixed bug that hid some logging messages [DCDRJ]
- Added a default file version (0) to manage files that have None [DCDRJ]
- Added exception handling for invalid uuids [DCDRJ]
- Renewed copyright year in documentation [DCDRJ]
- Changed default professor name separator from `/` to `;` [DCDRJ]
- Updated documentation [DCDRJ]

0.6.0 (2020-03-10)
------------------
New
~~~
- Set 8 hours as new default sync time [DCDRJ]
- Added references in about info [DCDRJ]
- Added donate button link [DCDRJ]
- Renewed copyright year and explicitly added license to each file [DCDRJ]

Fix
~~~
- Improved name simplification code [DCDRJ]
- Now course files destination folders contain professor names [DCDRJ]
- Updated tests to match the new simplification algorithm [DCDRJ]
- Minor test code cleanup [DCDRJ]
- Removed some cruft [DCDRJ]
- Removed old icons [DCDRJ]
- Reorganized resources [DCDRJ]

0.5.2 (2019-10-25)
------------------
Fix
~~~
- Reimplemented webscraping as default download method due to BeeP's JSON API deactivation [DCDRJ]

0.5.1 (2019-07-11)
------------------
Fix
~~~
- Signalslot is now fetched from pypi [DCDRJ]
- Included icon in PPA [DCDRJ]
- Modified GUI layout [DCDRJ]
- Made checkboxes bigger [DCDRJ]
- Checkboxes are now more centered [DCDRJ]
- Moved login form and sync button out of the settings tab [DCDRJ]

0.5.0 (2019-07-09)
------------------
New
~~~
- PPA package release [DCDRJ]
- Windows installer release [DCDRJ]
- Automated multiplatform building with Makefile [DCDRJ]

Fix
~~~
- Improved documentation [DCDRJ]

0.4.4 (2019-03-08)
------------------
New
~~~
- The password is now saved in the system keyring instead of the dump file [DCDRJ]

Fix
~~~
- Status bar now shows when sync is finished [DCDRJ]
- Now thread priority is properly set [DCDRJ]
- Removed tests from package [DCDRJ]
- Now password and person code are updated when the input field looses focus [DCDRJ]

0.4.3 (2019-01-22)
------------------
Fix
~~~
- Url encoded filenames are now saved with a proper name [DCDRJ]
- Login doesn't fail when password change prompt is shown [DCDRJ]

0.4.2 (2018-12-27)
------------------
New
~~~
- New icon (thanks to `Davide Depau <https://github.com/Depau>`_) [DCDRJ]

Fix
~~~
- Now the manually inserted root folder path is no longer ignored [DCDRJ]
- Now course names without a year or with accents are supported [DCDRJ]
- Now minimize and restore work properly [DCDRJ]
- Now the tar file includes the new_gui.ui file [DCDRJ]

0.4.1 (2018-12-26)
------------------
Fix
~~~
- Included .ui file in pip package [DCDRJ]

0.4.0 (2018-12-26)
------------------
New
~~~
- Implemented beep's liferay json api (thanks to `davethecipo <https://github.com/davethecipo>`_ and
  `edomora97 <https://github.com/edomora97>`_)[DCDRJ]

Fix
~~~
- Now if the settings file is corrupted the application doesn't crash [DCDRJ]
- Updated docs link in check new version code [DCDRJ]
- Updated tests [DCDRJ]
- Code cleanup [DCDRJ]

0.3.3 (2018-12-14)
------------------
New
~~~
- Set 'info' as default logging level [DCDRJ]
- Logging is now less cluttered [DCDRJ]
- Download size are now shown in human readable format during logging [DCDRJ]
- Terminal logging and console now are synced [DCDRJ]

Fix
~~~
- Code cleanup [DCDRJ]
- Improved QT integration [DCDRJ]
- Reduced number of connection threads, now beep shouldn't drop connections [DCDRJ]


0.3.2 (2018-08-04)
------------------
New
~~~
- Multithread download [DCDRJ]
- Material design theme implemented [DCDRJ]

Fix
~~~
- Increased download code robustness [GV]
- Redesigned interface in qt designer for increased modularity [DCDRJ]
- Regenerated documentation [DCDRJ]

0.3.1 (2018-07-25)
------------------
New
~~~
- PySide2 support added for python3.6 [DCDRJ]

Fix
~~~
- Fixed Gui code where app couldn't find button [DCDRJ]
- Now sync message label works [DCDRJ]
- Fixed login error [DCDRJ]
- Fixed labels typos [DCDRJ]
- Added status label [DCDRJ]
- Fixed sync code [DCDRJ]

0.2.0 (2015-01-02)
------------------

New
~~~

- --hidden option works #6. [Davide Olianas]

Changes
~~~~~~~

- --debug option works #6. [Davide Olianas]

- Addition to readme, remove include directive of changelog. [Davide
  Olianas]

0.1.5 (2015-01-02)
------------------

New
~~~

- Basic working configuration for logging. [Davide Olianas]

Changes
~~~~~~~

- Some other debugging statements. [Davide Olianas]

- Add pypi pins to readme. [Davide Olianas]

- Style fixes. [Davide Olianas]

- Remove unused import. [Davide Olianas]

- No commit message. [Davide Olianas]

  Landscape.io should ignore behave steps definitions.

- Add .ico icon for Windows. [Davide Olianas]

- Git ignore codecov script. [Davide Olianas]

  ...because I should keep the token private

- Chglog generated by gitchangelog. [Davide Olianas]

- Store __version__ in __init__.py and use setuptools. [Davide Olianas]

Fix
~~~

- Bugfix for #4. [Davide Olianas]

  Even though not all errors can be solved, because landscape.io can't
  install PySide and apparently doesn't recognize the *exist* parameter
  of the function os.makedirs.

Other
~~~~~

- Merge branch 'debug-mode' [Davide Olianas]

  A first debug mode is enabled and better installation documentation
  has been written.

- Merge remote-tracking branch 'origin/master' [Davide Olianas]

- Change imports to avoid import * [Davide Olianas]

- Update documentation: linux64 build doesn't work. [Davide Olianas]

- Update docs with quickstart and installation. [Davide Olianas]

  I also customized the Sphinx theme by adding Google Analytics.

- Builder script for windows with cx_freeze. [Davide Olianas]

- Bugfix: always append extension to filename. [Davide Olianas]

- Bugfix: files downloaded to the correct root folder. [Davide Olianas]

  With this fix, after the user changes the root folder, files get
  downloaded to the new selected folder, instead of the old one.

- Remove debug prints. [Davide Olianas]

- Better handling of default save folder. [Davide Olianas]

- Theme qrc file. [Davide Olianas]

- Remove unused file (including complete license text) [Davide Olianas]

- Fix misspelling in license. [Davide Olianas]

- New icons (still ugly) [Davide Olianas]

- Add GPL text. [Davide Olianas]

- Appdirs in requirements.txt. [Davide Olianas]

- Correct development status to beta. [Davide Olianas]

- README in rst for pypi and development stage = alpha. [Davide Olianas]

- Small refactor to allow pbr console script generation. [Davide
  Olianas]

- Change import. [Davide Olianas]

- Timer gets updated when user changes setting. [Davide Olianas]

- Correct import statements. [Davide Olianas]

- Change name of main window. [Davide Olianas]

- Remove notification option. [Davide Olianas]

- Download in separate thread. [Davide Olianas]

- Sync new courses option respected. [Davide Olianas]

- Fix download bug (wrong folder creation) [Davide Olianas]

- Two different courses can't have the same folder name. [Davide
  Olianas]

- Fix typo in filename. [Davide Olianas]

- Test script: test only useful files. [Davide Olianas]

- BUGFIX: correct behaviour when refreshing courses. [Davide Olianas]

  Before this fix, the "ok signal" from loginthread is not disconnected
  from do_refreshcourses; therefore, the next time the user presses "try
  login credentials", the function do_refreshcourses gets called.  The
  function do_refreshcourses should be called only when the ok signal is
  emitted from the loginthread started by refreshcourses.

- Connect ok/error signals to both login status and status textbox.
  [Davide Olianas]

- Remove old comments from LoginThread. [Davide Olianas]

- Use myStream_message function to add text to "status" [Davide Olianas]

- Restore default sys.stdout. [Davide Olianas]

- Bugfix: refresh courses thread now exits when done. [Davide Olianas]

- Refactoring. [Davide Olianas]

  Moved code to MainWindow definition; use threads for login and courses
  synchronization

- New class style for common classes. [Davide Olianas]

- Change in filesettings defaults and updated unit tests. [Davide
  Olianas]

- Function to save a folder recursively +  tweaks. [Davide Olianas]

  The function is not tested yet; other tweaks are  * helper function to
  get the modification date for a local file * new courses created
  default to sync=False * updated docstring for logout()

- Add functionality to GUI. [Davide Olianas]

  * implemented insertRows and removeRows to update the view when new
  courses are available or when some should be removed * load username,
  password, courses list from "data" file * testlogin() ensures that the
  user is logged * refreshcourses() synces the local state of data with
  the remote website * syncfiles() should be able to download files to
  local directories (not tested)

- Default text for login information label. [Davide Olianas]

- Ok button hides window. [Davide Olianas]

- __init__.py re-inserted and renamed polibeepsync to common. [Davide
  Olianas]

  Import statements have been rewritten to accomodate file name change.

- Stdout goes to "status" textbox. [Davide Olianas]

- Change code to use new interface. [Davide Olianas]

- A better resizable window. [Davide Olianas]

- Almost working courses tab. [Davide Olianas]

  Also add icons and some auxiliary script to understand tableview and
  model.

- Get both files and folders. [Davide Olianas]

- PEP-8, complete coverage for filesettings, removed unused code.
  [Davide Olianas]

- Simple functions to load/save settings and files rename. [Davide
  Olianas]

- Start working on GUI. [Davide Olianas]

- It can get all files available online. [Davide Olianas]

- Better documentation and few PEP-8 corrections. [Davide Olianas]

- Function to sync courses, with tests. [Davide Olianas]

- Automatic documentation for polibeepsync package. [Davide Olianas]

- Move sphinx conf.py back to original folder. [Davide Olianas]

  ...and create script to build documentation

- Don't require a real account to test with behave. [Davide Olianas]

  Tests should not rely on an actual connection, or on a real account.
  Only scenarios tagged with "require_login" will get a User instance in
  the scenario context, already logged in.  In order to run such tests,
  a real account is needed. If you have one, you can test them by
  invoking behave like this  $ USERCODE=yourusercode
  PASSWORD=yourpassword\ behave --tags=require_login  Of course, you
  need to replace "yourusercode" and "yourpassword" with, guess what,
  your real usercode and password. Please note that shells usually
  record the typed commands and make them available through the
  "history" command.

- Update available courses avoids adding BeeP channel. [Davide Olianas]

- Use the Courses class in "User" instead of list. [Davide Olianas]

- Some fixes for Course and GenericSet. [Davide Olianas]

  Define __len__ for GenericSet. In Courses, override the init function
  in the correct way (by calling the init function of the parent class
  GenericSet). In Courses, define a property "files" which is a nicer
  name for the "elements" instance attribute.

- Fix typo in readme. [Davide Olianas]

- Update license and readme. [Davide Olianas]

- Updated requirements and test-requirements. [Davide Olianas]

- Move Sphinx configuration file. [Davide Olianas]

- Initial documentation. [Davide Olianas]

- Add shebang to test_all.sh script. [Davide Olianas]

- Change import statements in behave tests. [Davide Olianas]

  This is due to the change in package organization (the subfloder
  polibeepsync now contains everything)

- Coverage settings, script to run all tests, update test-requirements.
  [Davide Olianas]

  Also ignore coverage html reports and coverage internal files

- Unit tests for custom classes. [Davide Olianas]

- Move files to subfolder, including tests. [Davide Olianas]

- Automatically login when page is requested and session has expired.
  [Davide Olianas]

  Also, a handy logout() function is defined. For now, the only needed
  action is clearing session cookies.

- PEP-8 corrections. [Davide Olianas]

- Write helper function to re-login when necessary. [Davide Olianas]

- Login function doesn't require SSL_JSESSIONID cookie. [Davide Olianas]

- Given a valid session, I get the available courses. [Davide Olianas]

- Login with requests only. [Davide Olianas]

- Rewrite environment.py and avoid selenium. [Davide Olianas]

  It's actually possible to use requests exclusively, thus selenium is
  removed. The enviroment.py of behave runs "before_all_scenarios" which
  basically does the login procedure; it's not executed in the scenarios
  tagged with 'login'.

- Update gitignore to ignore common temporary files. [Davide Olianas]

- Module setup with basic script. [Davide Olianas]

- Initial features. [Davide Olianas]

- PySide added to pip requirements. [Davide Olianas]

- Remove additional requirements file. [Davide Olianas]

  If qmake can be found in $PATH, pyside installs without additional
  options; therefore I deleted "custom-requirements.txt" which was
  executed with the additional option --qmake=PATH_TO_QMAKE

- Custom requirements for pyside in separate file. [Davide Olianas]

- PySide added to requirements: fix typo. [Davide Olianas]

- PySide added to requirements. [Davide Olianas]

- Readme links to wiki. [Davide Olianas]

- Initial commit. [Davide Olianas]


