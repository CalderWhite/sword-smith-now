3. Files
========

This page will go over all the files and their contents.

.. _here: Help.html

If you need help reading these documents, the help document is `here`_.

3 - Contents
------------

File Contents (in alphabetical order):

.. _launcher.py: #id1
.. _launcher>functions: #functions
.. _launcher>classes: #classes
.. _gui: #launcher.gui
.. _runtime.py: #id2
.. _runtime>functions: #id3
.. _runtime.main: #id3
.. _runtime>classes: #id4
.. _guiObjects.py: #id5
.. _guiObjects>classes: #id6

- `launcher.py`_
	- `launcher>functions`_
		- `main`_
	- `launcher>classes`_
		- `gui`_
		- `launcher`_
- `runtime.py`_
	- `runtime>functions`_
		- `runtime.main`_
	- `runtime>classes`_
		- `audio_manager`_
		- `font_collection`_
		- `game_kernel`_
		- `item_manager`_
		- `new_player`_
		- `runtime.gui`_
		- `sword_crafter`_
- `guiObjects.py`_
	- `guiObjects>classes`_
		- `ask_window`_
		- `confirm`_
		- `button`_

3.1 launcher.py
---------------

The ``launcher.py`` file will launch the game.

3.1.1 Functions
~~~~~~~~~~~~~~~

.. function:: main()

	When run, ``main`` will use the options from ``sys.argv`` to run the launcher in a command line fashion. 

	Help with the command line can be found by running 

	**Windows**

	..

		``py launcher.py --help``

	**Other**

	..

		``python3 launcher.py --help``

3.1.2 Classes
~~~~~~~~~~~~~

.. class:: launcher(mode,log_file,info_file,initial_gui=False,run_with_errors=True)

	.. attribute:: mode

		 The mode defines what mode the game is running in. This may allow or block certain features.
	
	.. warning::
		In Alpha 0.3.0 The only supported ``mode`` is ``1``.
	
	..

		+------+------------------------------------------+-----------------+
		| Mode | Description                              | Supported in    |
		+======+==========================================+=================+
		|  0   | Consumer mode                            |  NOT SUPPORTED  |
		+------+------------------------------------------+-----------------+
		|  1   | Developer mode. Certain features enabled.| >= v0.1.0-alpha |
		+------+------------------------------------------+-----------------+
		|  2   | Cheats mode. all dev mode cheats enabled |  NOT SUPPORTED  |
		+------+------------------------------------------+-----------------+

	.. attribute:: log_file

		The launcher will send all the logs to a file with this name. The location of that file will be in the installation location

	.. attribute:: info_file

		The launcher will search the ``ssn`` directory inside the current directory (``./ssn``) for a file with the name of info_file

	.. attribute:: initial_gui

		**True** \: When the launcher is loaded, it will create a gui.

		**False** \: When the launcher is loaded, it will prompt the user in the terminal for a yes or no answer, whether to launch.

	.. attribute:: run_with_errors

		**True** \: The launcher will loop, even after the program has hit a critical error. It will also log information on the error.

		**False** \: The launcher will ``exit`` when it hits a critical error, and it will not log the error that was hit.

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

		Uses python's `logging`_ module to write to a log file, formatted as follows::

			[user][level]:msg

	.. method:: module_checklist()

		Tries to import all the modules in ``requirements.json``, according to the mode. ``"vanilla"`` if the mode is 0 or 2. ``"dev"`` if the mode is 1 (developer mode).

	.. method:: do_checks()

		Executes certain methods according to mode

.. class:: launcher.gui()
	
	Sets up, and contains the tkinter display.

	.. attribute:: tk

		The gui's ``Tk()`` class.

3.2 runtime.py
--------------

The ``runtime.py``  file is the main file of the game. It consists of all the core game classes, and one function : ``main`` .

3.2.1 Functions
~~~~~~~~~~~~~~~

.. function:: main(parent)
	
	main forwards all the options from the parent object to the `game_kernel`_ class, and runs it.

	*parent* \:

		.. _launcher.launcher: #launcher

		Please refer to the `launcher.launcher`_ for a documentation on what this parent object should consist of. The parent must consist of (at least) a log method, mode int and run_with_errors boolean.

3.2.2 Classes
~~~~~~~~~~~~~

.. class:: font_collection()

	Loads and contains fonts.

	.. method:: add(name,filename,size)

		Adds an attribute to itself with the name as :mod:`name`, the font file from :mod:`filename` and the font size from :mod:`size`.

.. class:: audio_manager(parent)

	Contains and manages audio. Requires a parent, which must be in the template of *game_kernel*.

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

		This class contains all of the player's possesion utilities. From minerals to items, it does it. It is initialized as ``possesions`` in the *game_kernel*.

		*minerals* \: A dictionary of all the minerals the player has.
		All the keys are the names, and the values are `item_manager.mineral_counter`_ 's.

		.. method:: give(item_type,obj,quantity)

			The item type tells the method what to do with the information given.

			+-----------+---------------+
			| item_type | Desc.         |
			+===========+===============+
			|     0     | minerals      |
			+-----------+---------------+

			**For minerals:**

			..

				``obj`` \: must be a `item_manager.mineral_counter`_ .

				This method will add to an existing ``mineral_counter`` the quantity or create a ``mineral_counter`` with the quantity provided.

				Example::

					# We're assuming that item_manager is already defined.
					# If you wish to learn about it, it's easy to find its documentation by typing its name into the search bar. (item_manager)
					player.possesions.give(
						0,					# minerals
						item_manager.minerals["mercury"],	# selecting mercury from the item_manager's index
						1					# quantity
					)

		.. method:: take(item_type,obj,quantity)

			Please refer to `new_player.possesions_class.give`_ for information. Instead of adding the quantity, it takes away the quantity. 
			All checks to see if there is in fact an ``obj`` to take away must be done before this method.
			For this method will not check that, and consequently hit a critical ``KeyError`` .
			
	.. method:: give_all(quantity=999)
		
		Gives the player ``quantity`` amount of each mineral. Used for developement only.
		
.. class:: runtime.gui(parent)

	Manages anything to do with the display. To get to the window, you must go through this class
	
	.. attribute:: parent

		Must be a *game_kernel*
	
	.. attribute:: screen

		A pygame surface. Dimensions: (600,600)
	
	.. method:: check_events(keybindings=True)
		
		Checks pygame events, to keep the operating system happy. Additionally,
		if keybindings is ``True``, it will check all the keybindings in ``parent.key_bindings``
		on a ``pygame.KEYDOWN`` event.
		
		It will also check through the gui's custom_events
		property (``dict``). The key is the event, and the value is the callback. For more info
		go to `runtime.gui.add_event`_'s documentation.
		
		Just recently, this method also resizes the display on ``pygame.VIDEORESIZE``
		
	.. method:: load_cursors()
		
		Adds all of the images in ``./images/cursors`` to ``runtime.gui.cursors`` dictionary.
		The key is the name of the file (minus file suffixes) and the value is the ``pygame.image.load``
		object of the image.
	
	.. method:: update()
		
		Blits its screen property to the center of the ACTUAL pygame display.
		This is so the user can resize the pygame display window, and the game's width will remain the same.
		This also allows room of styling outside the game window.
	
	.. method:: set_cursor(name)
		
		Sets the ``runtime.gui.cursor`` to ``runtime.gui.cursors[name]``.
	
	.. method:: add_event(t)
		
		.. attribute:: t

			Must be a ``tuple`` in the format: ``(pygame event, callback)``
		
		.. note:: The callback will be supplied with an event object
		
		Adds event to ``runtime.gui.custom_events``
		
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
	
	.. method:: load_chunks()
		
		.. warning:: 
			This method will only work in developer mode, and does not serve its full
			purpose. Instead it simply loads a predetermined chunk from an image.
		
		Loads chunk file.
	
.. class:: item_manager

	Manages items.
	
	.. _item_manager.load_minerals: #item_manager.load_minerals
	
	.. attribute:: minerals

		dictionary of all minerals, returned by `item_manager.load_minerals`_
	
	.. load_minerals()
		Returns the minerals json file (``minerals.json``).
	
	.. class:: mineral_counter(obj)
		
		Grabs the ``name`` and ``color`` property from ``obj`` , and the adds its own
		``count`` property
		
		.. method::add(quantity)
			Increases the object's ``count`` property by ``quantity``.
			
		.. method::remove(quantity)
			Decreases the object's ``count`` property by ``quantity``.

.. class:: sword_crafter(parent,dimensions)
	
	sword_crafter is an autonomous object that will start when ``sword_crafter.run`` is called.
	Essentially, it takes over the gui display when it's running. The sword crafter is used to 
	edit the user's sword in a friendly environment.
	
	.. warning::
	
		The surface of the sword_crafter cannot be customized. Since it takes a parent argument,
		it feeds all of it's gui output directly to ``parent.screen``.
	
	.. method:: check_mouse(event)
		
		Run a couple of the sword_crafter's children's check_mouse methods.
		
	.. method:: try_save(status)
		
		If status, run `sword_crafter.save_weapon`_ . It should be noted
		that the status parameter is coming from a confirm box.
		
	.. method:: load_popup()
		
		Shows popup window. This is a method for the purpose of being a callback. To some button.
		
	.. method:: ask_loop(question)
		
		Takes over the main loop for a while, to wait for user response of ``question``. 
		This message uses ``guiObjects.ask_window`` .
		
	.. method:: show_conf()
		
		Creates a certain confirm window in the center of the `runtime.gui.screen`_ .
	
	.. method:: exit()
		
		Sets the ``looping`` property to ``False``, therefore ending the
		`sword_crafter.run`_ loop without exiting.
		
	.. method:: run()
		
		The run method is split into two sections: setup and loop.
		
		Though the class already has an ``init`` method, there is still setup that may only be done when the ``run`` method is called.
		After the setup, a loop is run while ``sword_crafter.looping``.
	
	.. method:: save_weapon()
		
		Since Sword Smith Now is having trouble with encryption modules, so we are forced to
		just save the files in the png video format (0 security preveting game hacking...)

.. class:: game_kernel(parent,dev_window=None,mode=0)
	
	.. warning::
		In Alpha 0.3.0 dev mode is the only mode supported. Please refer to `launcher.mode`_.
		
	This class serves as the parent class, and manages all of the other classes, as the name suggests.
	This is also where the main game loop is stored and run.
	
	.. attribute:: parent

		This must fit the critera of `launcher`_. Usually this parameter is supplied by the main function.
	
	
	.. method:: log(msg,level="INFO",user="GAME")
		
		Forwards log input to ``parent.log`` (`launcher.log`_)
	
	.. method:: kill_sound()

		Mutes its audio manager. (`audio_manager.mute`_)

	.. method:: pause(gui=True)

		Sets ``paused`` to ``True``. (Whether gui is ``True`` or ``False``)

		Additionally, if ``gui == True`` it will take over the loop of the game, and run its own while loop. It will display a pause screen, with some buttons.

	.. method:: unpause()

		Sets the ``game_kernel.paused`` to ``False``. As of now nothing special, but there may be additions in regards to resuming processes, in the future.

	.. method:: start_crafter()

		.. _run it: #sword_crafter.run

		.. _player.possesions.minerals: #new_player.possesions_class

		As long as the player has minerals (`player.possesions.minerals`_) it will create a `sword_crafter`_ object and `run it`_ .

	.. method:: toggle_pause()
	
		Inverts the current state of pausing.
		If the game is paused, it calls `game_kernel.unpause`_.
		Vice versa it calls `game_kernel.pause`_ with the **default arguments**.

	.. method:: pause_quit()

		Sets all of the ``game_kernel``'s looping variables to a value that will make the game stop.
		(Essentially this stops the game from looping, without exiting python3)

	.. method:: run()

		.. _mode: #launcher

		Runs different methods to start the game, depending on the game's `mode`_

	.. method:: quit()

		Stops the game from looping, and exits **pygame**, not python.

	.. method:: init_credits()

		Displays the pre-game credits, in a finite (set) amount of time.

	.. method:: run_start()

		Displays the start page. Has its own loop. It will also play the start page music.

	.. method:: realm_explorer_init()

		.. _Developer mode: #launcher

		Sets the current chunk, for starting the game.
		At the moment it only runs in `Developer mode`_, and it doesn't do any processing to set the current chunk.
		It simply selects the first chunk out of ``runtime.gui.chunks``.

	.. method:: run_realm_explorer()

		This is the main game loop. Essentially, this manages the game during gameplay.
		It checks all the events, sound, player movement, etc.

3.2 guiObjects.py
-----------------

.. danger:: 
	
	guiObjects is a very unorganized file that will probably be restructured
	by Beta, so don't count on it being the same then.

guiObjects is a file containing all the window related gui classes/widgets.

3.2.1 Classes
~~~~~~~~~~~~~

.. class:: ask_window(parent,screen,background_img,qtxt)

	.. image:: comp.svg

	ask_window should be used by functions such as `sword_crafter.ask_loop`_, since they will handle the game loop.
	
	When shown, the ask window covers the entire screen, which is why it should have its own loop.

	.. _PIL: https://pillow.readthedocs.io/en/4.0.x/
	
	.. attribute:: parent

		should have the same gui related properties as `sword_crafter`_
	
	.. attribute:: screen

		Should be a pygame surface. (This should probably be `runtime.gui.screen`_)
	
	.. attribute:: background_img

		Should be a pygame surface.  The ask window wil blur this surface using a `PIL`_ filter, and then render it behind the popup window.
	
	.. attribute:: qtxt

		A string that will be rendered by a font, as the question.
	
	.. method:: check_keys(e)
		
		*e* \: pygame.event object, the key kind.
		
		Checks if allowed characters are pressed. If so, append them to ``ask_window.text``.
		
	.. method::	update()
		
		redraw the display.
	
	.. method:: check_events()
		
		A custom version of `runtime.gui.check_events`_, with keypress.
		
	.. method:: draw()
		
		Draw its surface to the main display.

.. class:: confirm(parent,surf,rect,msg,onclick)

	.. image:: incomp.svg
	
	.. Danger::
		THIS CLASS CAN **ONLY** BE USED WITH `sword_crafter`_
		
	Essentially a confirm popup.
	
	.. attribute:: parent

		must be a `sword_crafter`_.
	
	.. attribute:: surf

		The main surface. (should be `runtime.gui.screen`_)
	
	.. attribute::  rect

		Works in regularly compared to pygame and tkinter rectangles. (x,y,width,height)
	
	.. attribute:: msg

		The question that will be asked.
	
	.. attribute:: onclick

		The callback for the user's answer.
	
	.. note:: The onclick callback will be supplied with one parameter : True or False. Depending on the user's descion.
	
	.. method:: clickT()
		
		Calls the callback with ``True`` as the parameter.
		
	.. method:: clickF()
		
		Calls the callback with ``False`` as the parameter.
	
	.. method:: check_click()
		
		Check if the user has clicked on any of the buttons.
		
	.. method:: update()
		
		Redraw to its own surface
	
	.. method:: draw()
		
		Draw the object's surface to the main surface. (``surf``)

.. class:: button(surf,color,onclick,text=None,hover=None,text_align="center",padding=0,right_text=None,outer_offset=None,text_vertical=None)
	
	.. image:: comp.svg
	
	.. attribute:: surf 

		The surface where the button will be drawn.
	
	.. attribute:: color 

		The background color of the button. (Should be in rgb format ``(R,G,B)``).
	
	.. attribute:: onclick

		 The callback run, when the button is clicked.
	
	.. attribute:: text

		If supplied, it should be a ``pygame.font.Font.render`` object. This will be displayed on the button.
	
	.. attribute:: hover

		The color the button turns when hovered over. (RGB format)
	
	.. attribute:: text_align

		options: ``"center"``, ``"left"``. The text will be positioned according to this parameter.
	
	.. attribute:: padding

		The amount of pixels add/subtracted from the text's calculated position.
	
	.. warning:: padding is an unstable feature, and is recommended not to be touched. However, it is not deprecated, and still in use.
	
	.. attribute:: right_text

		Extra text that will be rendered from the right and out. Should be a ``pygame.font.Font.render`` object.
	
	.. attribute:: outer_offset

		The offset surf is from the main surface.
		For Example, if a button was being draw on a surface that is not the main screen,
		it requires an out_offset parameter to tell it **exactly** where it is on the entire page, not just the surface it's being drawn to.
		 
	.. attribute:: text_vertical

		Documentation unavailable.
	
	.. method:: draw()
		
		Draw button to its surface (``surf``)
	
	.. method:: try_hover()
		
		If the mouse is hovering over the button, and there is a hover color for said button,
		change the background color of said button temporarily.
	
	.. method:: get_hover()
		
		Returns ``True`` if the mouse is hovering over the button. If there are issues with this method, refer to `button.outer_offset`_ for a possible reason why.
