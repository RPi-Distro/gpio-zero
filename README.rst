========
gpiozero
========

A simple interface to everyday GPIO components used with Raspberry Pi

Latest release: v0.6.0 Public beta

Motivation
==========

The "hello world" program in Java is at least 5 lines long, and contains 11
jargon words which students are taught to ignore.

The "hello world" program in Python is one simple line. However, the "hello
world" of physical computing in Python (flashing an LED) is similar to the Java
program: 6 lines of code to flash an LED.

Young children and beginners shouldn't need to sit and copy out several lines
of text they're told to ignore. They should be able to read their code and
understand what it means.

Install
=======

Install with pip::

    sudo pip install gpiozero
    sudo pip-3.2 install gpiozero

Both Python 3 and Python 2 are supported. Python 3 is recommended!

Usage
=====

Example usage for lighting up an LED::

    from gpiozero import LED

    led = LED(2)
    led.on()

Documentation
=============

Comprehensive documentation is available at `pythonhosted.org/gpiozero`_.

Development
===========

This project is being developed on `GitHub`_. Join in:

* Provide suggestions, report bugs and ask questions as `Issues`_
* Help design the `API`_
* Contribute to the code

Alternatively, email suggestions and feedback to ben@raspberrypi.org or add to
the `Google Doc`_.

Contributors
============

- `Ben Nuttall`_ (project maintainer)
- `Dave Jones`_
- `Martin O'Hanlon`_


.. _pythonhosted.org/gpiozero: http://pythonhosted.org/gpiozero
.. _GitHub: https://github.com/RPi-Distro/python-gpiozero
.. _Issues: https://github.com/RPi-Distro/python-gpiozero/issues
.. _API: https://github.com/RPi-Distro/python-gpiozero/issues/7
.. _Google Doc: https://docs.google.com/document/d/1EbbVjdgXbKVPFlgH_pEEtPZ0zOZVSPHT4sQNW88Am7w/edit?usp=sharing
.. _Ben Nuttall: https://github.com/bennuttall
.. _Dave Jones: https://github.com/waveform80
.. _Martin O'Hanlon: https://github.com/martinohanlon

