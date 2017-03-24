========
gpiozero
========

.. image:: https://badge.fury.io/py/gpiozero.svg
    :target: https://badge.fury.io/py/gpiozero
    :alt: Latest Version

.. image:: https://travis-ci.org/RPi-Distro/python-gpiozero.svg?branch=master
    :target: https://travis-ci.org/RPi-Distro/python-gpiozero
    :alt: Build Tests

.. image:: https://img.shields.io/codecov/c/github/RPi-Distro/python-gpiozero/master.svg?maxAge=2592000
    :target: https://codecov.io/github/RPi-Distro/python-gpiozero
    :alt: Code Coverage

A simple interface to GPIO devices with Raspberry Pi.

Created by `Ben Nuttall`_ of the `Raspberry Pi Foundation`_, `Dave Jones`_, and
other contributors.

About
=====

Component interfaces are provided to allow a frictionless way to get started
with physical computing:

.. code:: python

    from gpiozero import LED
    from time import sleep

    led = LED(17)

    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)

With very little code, you can quickly get going connecting your components
together:

.. code:: python

    from gpiozero import LED, Button
    from signal import pause

    led = LED(17)
    button = Button(3)

    button.when_pressed = led.on
    button.when_released = led.off

    pause()

The library includes interfaces to many simple everyday components, as well as
some more complex things like sensors, analogue-to-digital converters, full
colour LEDs, robotics kits and more.

Install
=======

First, update your repositories list::

    sudo apt-get update

Then install the package of your choice. Both Python 3 and Python 2 are
supported. Python 3 is recommended::

    sudo apt-get install python3-gpiozero

or::

    sudo apt-get install python-gpiozero

Take a look at the `changelog <https://gpiozero.readthedocs.io/en/latest/changelog.html>`_
when upgrading from a previous version.

Documentation
=============

Comprehensive documentation is available at https://gpiozero.readthedocs.io/.

Development
===========

This project is being developed on `GitHub`_. Join in:

* Provide suggestions, report bugs and ask questions as `issues`_
* Provide examples we can use as `recipes`_
* `Contribute`_ to the code

Alternatively, email suggestions and feedback to ben@raspberrypi.org

Contributors
============

Core developers:

- `Ben Nuttall`_
- `Dave Jones`_
- `Andrew Scheller`_

Other contributors:

- `Martin O'Hanlon`_
- `Steve Amor`_
- `David Glaude`_
- `Edward Betts`_
- `Alex Chan`_
- `Thijs Triemstra`_
- `Schelto vanDoorn`_
- `Alex Eames`_
- `Barry Byford`_
- `Clare Macrae`_
- `Tim Golden`_
- `Phil Howard`_


.. _Raspberry Pi Foundation: https://www.raspberrypi.org/
.. _GitHub: https://github.com/RPi-Distro/python-gpiozero
.. _issues: https://github.com/RPi-Distro/python-gpiozero/issues
.. _recipes: https://gpiozero.readthedocs.io/en/latest/recipes.html
.. _Contribute: https://gpiozero.readthedocs.io/en/latest/contributing.html
.. _Ben Nuttall: https://github.com/bennuttall
.. _Dave Jones: https://github.com/waveform80
.. _Andrew Scheller: https://github.com/lurch
.. _Martin O'Hanlon: https://github.com/martinohanlon
.. _Steve Amor: https://github.com/SteveAmor
.. _David Glaude: https://github.com/dglaude
.. _Edward Betts: https://github.com/edwardbetts
.. _Alex Chan: https://github.com/alexwlchan
.. _Thijs Triemstra: https://github.com/thijstriemstra
.. _Schelto vanDoorn: https://github.com/goloplo
.. _Alex Eames: https://github.com/raspitv
.. _Barry Byford: https://github.com/ukBaz
.. _Clare Macrae: https://github.com/claremacrae
.. _Tim Golden: https://github.com/tjguk
.. _Phil Howard: https://github.com/Gadgetoid

