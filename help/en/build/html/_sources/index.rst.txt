.. Automatic Backup documentation master file, created by
   sphinx-quickstart on Fri Jan  3 08:17:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Automatic Backup plugin documentation
=====================================

.. toctree ::
   : maxdepth: 2
   : caption: Contents:

.. index :: Presentation


Presentation
************
|
This plugin allows you to create automatic backups of a Qgis project.

Several options are available to you:

    * Create a backup at an interval specified by the user.
      It will be located in the same directory as that of the project.
    |
    * Save the layers being edited.
    |
    * Save a certain number of backups, in a specific folder, still according to an interval.

.. index :: How it works



How it works
************
    |
    * Check only "Activate automatic backup" to create a backup in the same folder as that of the open project.

      Then define how often you want to make backups with the "Interval" tool.

      The backup will bear the name of the project with the extension "_backup".
    |
    * Checking the option "Save layers while editing" allows you to save your changes in the concerned layers.
    |
    * If you check "Save in a separate file", indicate the location and the maximum quantity of backups you want.

      The backups created will bear the name of the project with an extension indicating their creation / modification date, in the format "Project Name" _backup_Year_month_day_hour_minute.

      Example: "test_backup_2020_01_02_18_48.qgs"

.. image:: _images/MainWindow_en.png
   :width: 411 px
   :align: center
   :height: 403 px


Source code
***********

The source code is available at the following address:

https://github.com/Seboon/AutomaticBackup.git



Indexes and tables
******************
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`