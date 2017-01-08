1. Installation
===============

Before attempting to install, see if your platform is supported.

1.1 Platform Support
--------------------

1.1.1 Supported Installer Platforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These platforms all have a designated installer binary that installs the game on the computer.
The installer and game (once installed) require no external programs or libraries (yay!). 

.. _Windows: #windows-installer

+------------+---------------+--------------+
| Platform   |   Versions    | Instructions |
+============+===============+==============+
|  Windows   | v0.1.0-alpha+ |  `Windows`_  |
+------------+---------------+--------------+

1.1.2 Supported Source Platforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the raw code. You'll need python 3 and all of the required libraries (modules). The tricky part is retriving all the libraries for different platforms, so there is a setup link attached to each operating system for how to setup the source before running it.

+------------+---------------+-------+
| Platform   |   Versions    | Setup |
+============+===============+=======+
| Windows 7+ | v0.1.0-alpha+ | None  |
+------------+---------------+-------+
|Ubuntu 16.04| v0.1.0-alpha+ | None  |
+------------+---------------+-------+


1.2 Instructions
----------------

1.2.1 Windows - Installer
~~~~~~~~~~~~~~~~~~~~~~~~~

1.2.1.1 - Downloading
^^^^^^^^^^^^^^^^^^^^^

Download the installer executable, which is currently only available to developers.

1.2.1.2 - Installing
^^^^^^^^^^^^^^^^^^^^

Run the executable. Eventually, it should give the option of installation, and selecting a directory. The default directory is your %appdata% directory.

1.2.1.3 - Running
^^^^^^^^^^^^^^^^^

The actual game launcher will be stored in the current user's "Saved Games" folder. Now you're done! Since you can only launch the game in dev mode, start the game by running:

.. highlight:: batch

Enter games directory::
	
	cd "C:/users/%USERNAME%/Saved Games"

Run the game in dev mode::

	launcher.exe -d
