Files
=====

This page will go over all the files and their contents.

Numbered as follows, ``<File>`` . ``<Class>`` . ``<attribute>``

.. _Calder White: mailto:calderwhite1%40gmail.com

If there is any further help required, contact `Calder White`_ (Head Developer)

1. launcher.py
--------------

The ``launcher.py`` file will launch the game.

1.1 Functions
~~~~~~~~~~~~~

.. function:: main()

	When run, ``main`` will use the options from ``sys.argv`` to run the launcher in a command line fashion. 

	Help with the command line can be found by running 

	**Windows**

	..

		``py launcher.py --help``

	**Other**

	..

		``python3 launcher.py --help``

1.2 Classes
~~~~~~~~~~~

.. class:: launcher(mode,log_file,info_file,initial_gui=False,run_with_errors=True)

	*mode* The mode defines what mode the game is running in.

		+------+------------------------------------------+
		| Mode | Description                              |
		+======+==========================================+
		|  0   | Consumer mode                            |
		+------+------------------------------------------+
		|  1   | Developer mode. Certain features enabled.|
		+------+------------------------------------------+
		|  2   | Cheats mode. all dev mode cheats enabled |
		+------+------------------------------------------+

	*log_file* The launcher will send all the logs to a file with this name. The location of that file will be in the installation location

	*info_file* The launcher will search the ``ssn`` directory inside the current directory (`./ssn`) for a file with the name of info_file

	*initial_gui*

	..

		**True** \: When the launcher is loaded, it will create a gui.

		**False** \: When the launcher is loaded, it will prompt the user in the terminal for a yes or no answer, whether to launch.

	*run_with_errors*

	..

		**True** \: The launcher will loop, even after the program has hit a critical error. It will also log information on the error.

		**False** \: The launcher will ``exit`` when it hits a critical error, and it will not log the error that was hit.

	.. _runtime.main : #id1

	.. method:: launcher.try_launch()

		reloads the import of the runtime module, and attempts to call the `runtime.main`_ method.

	.. method:: launcher.load()

		If ``launcher.initial_gui``, it runs the launcher gui, and executes different methods according to ``launcher.mode``

		Else, (``launcher.initial_gui`` is False) it asks the user if it would like to launch, through the terminal/command prompt. Afterwards, it executes the same methods as if ``launcher.initial_gui`` was True, accroding to ``launcher.mode``

	.. method:: launcher.waiting_loop()

		Runs the tkinter mainloop.

	.. method:: launcher.get_game_file()

		Searchs ``./ssn`` for ``self.info_file`` and lods it into memory.

	.. _logging : https://docs.python.org/3.5/library/logging.html

	.. method:: log(msg,level="INFO",user="LAUNCHER")

		Uses `logging`_ module to write to a log file, formatted as follows::

			[user][level]:msg

	.. method:: module_checklist()

		Tries to import all the modules in ``requirements.json``, according to the mode. ``"vanilla"`` if the mode is 0 or 2. ``"dev"`` if the mode is 1 (developer mode).

	.. method:: do_checks()

		Executes certain methods according to mode

.. class:: gui()
	
	Sets up, and contains the tkinter display.

	*tk* : The gui's ``Tk()`` class.

2. runtime.py
-------------

The ``runtime.py``  file is the main file of the game. It consists of all the core game classes, and one function : ``main`` .

2.1 Functions
~~~~~~~~~~~~~

.. function:: main(parent)

	*parent*

		.. _launcher.launcher: #launcher

		Please refer to the `launcher.launcher`_ for a documentation on what this parent object should consist of. The parent must consist of (at least) a log method, mode int and run_with_errors boolean.

1.2 Classes
~~~~~~~~~~~~~~~~~~~~~~~

.. class:: font_collection()

	Loads and contains fonts.

	.. method:: add(name,filename,size)

		Adds an attribute to itself with the name as :mod:`name`, the font file from :mod:`filename` and the font size from :mod:`size`.

.. class:: audio_manager(parent)

	Contains and manages audio. Requires a parent, which must be in the template of `game_kernel`.

	.. method:: log(msg,level="INFO",user="AUDIO")

		Forwards input to the parent's log method.

	.. method:: mute()

		Stops all music and sets ``audio_manager.mute`` to ``True``.

	.. method:: unmute()

		Sets ``audio_manager.mute`` to ``True``. **IT DOES NOT RESUME ANY MUSIC THAT WAS PLAYING WHEN LAST MUTED**

	.. method:: play_and_load_music(filename,loops=0)

		If not muted, it loads ``filename`` from the current directory, and the plays it for ``loops`` amount of loops (-1 loops to play infinitly)

	.. method:: load_audio()

		Does nothing, currently.

.. class:: new_player(name,parent)

	The player manages its own collisions, possesions and movement.

	.. method:: check_movement()

		Checks if the movement keys are pressed. If so, it then proceeds to check if the attempted movement has any collisions. If everything checks out, it adds the movement to the player's current xy coordinates.

	.. method:: check_collision(xoff,yoff)

		checks if the player's current coordinates added with the xoff and yoff collide either into the edge of the chunk, or the edge of a chunk_object. If so, it returns the position the player will **stop at**, if not, it returns the new position of the player.

	.. class:: possesions_class()

		This class contains all of the player's possesion utilities. From minerals to items, it does it. It is initialized as ``possesions`` in the `game_kernel`.

		*minerals* : A dictionary of all the minerals the player has. All the keys are the names, and the values are `item_manager.mineral_counter` 's.

		.. method:: give(item_type,obj,quantity)

			The item type tells the method what to do with the information given.

			+-----------+---------------+
			| item_type | Desc.         |
			+===========+===============+
			|     0     | minerals      |
			+-----------+---------------+

			**For minerals:**

			..

				``obj`` must be a `item_manager.mineral_counter` .

				This method will add to an existing `mineral_counter` the quantity or create a `mineral_counter` with the quantity provided.

				Example::

					# We're assuming that item_manager is already defined.
					# If you wish to learn about it, it's easy to find its documentation by typing its name into the search bar. (item_manager)
					player.possesions.give(
						0,					# minerals
						item_manager.minerals["mercury"],	# selecting mercury from the item_manager's index
						1					# quantity
					)

		.. method:: take(item_type,obj,quantity)

			.. _take : #new_player.possesions_class.give

			Please refer to `take`_ for information. Instead of adding the quantity, it takes away the quantity. 
			All checks to see if there is in fact an ``obj`` to take away must be done before this method.
			For this method will not check that, and consequently hit a critical ``KeyError`` .
	.. method:: give_all(quantity=999)
		
		Gives the player ``quantity`` amount of each mineral. Used for developement only.
		
.. class:: gui(parent)

	Manages anything to do with the display. To get to the window, you must go through this class
	
	*parent* : Must be a *game_kernel*
	
	.. method:: check_events(keybindings=True)
		
		Checks pygame events, to keep the operating system happy. Additionally,
		if keybindings is ``True``, it will check all the keybindings in ``parent.key_bindings``
		on a ``pygame.KEYDOWN`` event.
		
		It will also check through the gui's custom_events
		property (``dict``). The key is the event, and the value is the callback. For more info
		go to `add_event`'s documentation.
		
		Just recently, this method also resizes the display on ``pygame.VIDEORESIZE``
		
	.. method:: load_cursors()
		
		Adds all of the images in ``./images/cursors`` to ``gui.cursors`` dictionary.
		The key is the name of the file (minus file suffixes) and the value is the ``pygame.image.load``
		object of the image.
	
	.. method:: update()
		
		Blits its screen property to the center of the ACTUAL pygame display.
		This is so the user can resize the pygame display window, and the game's width will remain the same.
		This also allows room of styling outside the game window.
	
	.. method:: set_cursor(name)
		
		Sets the ``gui.cursor`` to ``gui.cursors[name]``.
	
	.. method:: add_event(t)
		
		*t* : Must be a ``tuple`` in the format: ``(pygame event, callback)``
		
		.. note:: The callback will be supplied with an event object
		
		Adds event to ``gui.custom_events``
		
		Example::
		
			def check_mouse(event):
				if event.button == 5 or event.button == 4:
					print("Scrolled!")
				pass
			gui.add_event(
				(
				pygame.MOUSEBUTTONDOWN,
				check_mouse
				)
			)
	
