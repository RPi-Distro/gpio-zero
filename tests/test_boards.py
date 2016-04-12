from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
str = type('')


import sys
import pytest
from time import sleep

from gpiozero.pins.mock import MockPin, MockPWMPin
from gpiozero import *


def setup_function(function):
    import gpiozero.devices
    # dirty, but it does the job
    if function.__name__ in ('test_robot', 'test_ryanteck_robot', 'test_camjam_kit_robot'):
        gpiozero.devices.DefaultPin = MockPWMPin
    else:
        gpiozero.devices.DefaultPin = MockPin

def teardown_function(function):
    MockPin.clear_pins()


def test_composite_output_on_off():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with CompositeOutputDevice(OutputDevice(pin1), OutputDevice(pin2), foo=OutputDevice(pin3)) as device:
        device.on()
        assert all((pin1.state, pin2.state, pin3.state))
        device.off()
        assert not any((pin1.state, pin2.state, pin3.state))

def test_composite_output_toggle():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with CompositeOutputDevice(OutputDevice(pin1), OutputDevice(pin2), foo=OutputDevice(pin3)) as device:
        device.toggle()
        assert all((pin1.state, pin2.state, pin3.state))
        device[0].off()
        device.toggle()
        assert pin1.state
        assert not pin2.state
        assert not pin3.state

def test_composite_output_value():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with CompositeOutputDevice(OutputDevice(pin1), OutputDevice(pin2), foo=OutputDevice(pin3)) as device:
        assert device.value == (0, 0, 0)
        device.toggle()
        assert device.value == (1, 1, 1)
        device.value = (1, 0, 1)
        assert device[0].is_active
        assert not device[1].is_active
        assert device[2].is_active

def test_led_board_on_off():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, pin2, foo=pin3) as board:
        assert isinstance(board[0], LED)
        assert isinstance(board[1], LED)
        assert isinstance(board[2], LED)
        board.on()
        assert all((pin1.state, pin2.state, pin3.state))
        board.off()
        assert not any((pin1.state, pin2.state, pin3.state))
        board[0].on()
        assert board.value == (1, 0, 0)
        assert pin1.state
        assert not pin2.state
        assert not pin3.state
        board.toggle()
        assert board.value == (0, 1, 1)
        assert not pin1.state
        assert pin2.state
        assert pin3.state

def test_led_board_nested():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        assert list(led.pin for led in board.leds) == [pin1, pin2, pin3]
        assert board.value == (0, (0, 0))
        board.value = (1, (0, 1))
        assert pin1.state
        assert not pin2.state
        assert pin3.state

def test_led_board_bad_blink():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        with pytest.raises(ValueError):
            board.blink(fade_in_time=1, fade_out_time=1)
        with pytest.raises(ValueError):
            board.blink(fade_out_time=1)
        with pytest.raises(ValueError):
            board.pulse()

@pytest.mark.skipif(hasattr(sys, 'pypy_version_info'),
                    reason='timing is too random on pypy')
def test_led_board_blink_background():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board.blink(0.1, 0.1, n=2)
        board._blink_thread.join() # naughty, but ensures no arbitrary waits in the test
        test = [
            (0.0, False),
            (0.0, True),
            (0.1, False),
            (0.1, True),
            (0.1, False)
            ]
        pin1.assert_states_and_times(test)
        pin2.assert_states_and_times(test)
        pin3.assert_states_and_times(test)

@pytest.mark.skipif(hasattr(sys, 'pypy_version_info'),
                    reason='timing is too random on pypy')
def test_led_board_blink_foreground():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board.blink(0.1, 0.1, n=2, background=False)
        test = [
            (0.0, False),
            (0.0, True),
            (0.1, False),
            (0.1, True),
            (0.1, False)
            ]
        pin1.assert_states_and_times(test)
        pin2.assert_states_and_times(test)
        pin3.assert_states_and_times(test)

@pytest.mark.skipif(hasattr(sys, 'pypy_version_info'),
                    reason='timing is too random on pypy')
def test_led_board_blink_control():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board.blink(0.1, 0.1, n=2)
        # make sure the blink thread's started
        while not board._blink_leds:
            sleep(0.00001)
        board[1][0].off() # immediately take over the second LED
        board._blink_thread.join() # naughty, but ensures no arbitrary waits in the test
        test = [
            (0.0, False),
            (0.0, True),
            (0.1, False),
            (0.1, True),
            (0.1, False)
            ]
        pin1.assert_states_and_times(test)
        pin3.assert_states_and_times(test)
        print(pin2.states)
        pin2.assert_states_and_times([(0.0, False), (0.0, True), (0.0, False)])

@pytest.mark.skipif(hasattr(sys, 'pypy_version_info'),
                    reason='timing is too random on pypy')
def test_led_board_blink_take_over():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board[1].blink(0.1, 0.1, n=2)
        board.blink(0.1, 0.1, n=2) # immediately take over blinking
        board[1]._blink_thread.join()
        board._blink_thread.join()
        test = [
            (0.0, False),
            (0.0, True),
            (0.1, False),
            (0.1, True),
            (0.1, False)
            ]
        pin1.assert_states_and_times(test)
        pin2.assert_states_and_times(test)
        pin3.assert_states_and_times(test)

@pytest.mark.skipif(hasattr(sys, 'pypy_version_info'),
                    reason='timing is too random on pypy')
def test_led_board_blink_control_all():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board.blink(0.1, 0.1, n=2)
        # make sure the blink thread's started
        while not board._blink_leds:
            sleep(0.00001)
        board[0].off() # immediately take over all LEDs
        board[1][0].off()
        board[1][1].off()
        board._blink_thread.join() # blink should terminate here anyway
        test = [
            (0.0, False),
            (0.0, True),
            (0.0, False),
            ]
        pin1.assert_states_and_times(test)
        pin2.assert_states_and_times(test)
        pin3.assert_states_and_times(test)

def test_led_board_blink_interrupt_on():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board.blink(1, 0.1)
        sleep(0.2)
        board.off() # should interrupt while on
        pin1.assert_states([False, True, False])
        pin2.assert_states([False, True, False])
        pin3.assert_states([False, True, False])

def test_led_board_blink_interrupt_off():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3)) as board:
        board.blink(0.1, 1)
        sleep(0.2)
        board.off() # should interrupt while off
        pin1.assert_states([False, True, False])
        pin2.assert_states([False, True, False])
        pin3.assert_states([False, True, False])

@pytest.mark.skipif(hasattr(sys, 'pypy_version_info'),
                    reason='timing is too random on pypy')
def test_led_board_fade_background():
    pin1 = MockPWMPin(2)
    pin2 = MockPWMPin(3)
    pin3 = MockPWMPin(4)
    with LEDBoard(pin1, LEDBoard(pin2, pin3, pwm=True), pwm=True) as board:
        board.blink(0, 0, 0.2, 0.2, n=2)
        board._blink_thread.join()
        test = [
            (0.0, 0),
            (0.04, 0.2),
            (0.04, 0.4),
            (0.04, 0.6),
            (0.04, 0.8),
            (0.04, 1),
            (0.04, 0.8),
            (0.04, 0.6),
            (0.04, 0.4),
            (0.04, 0.2),
            (0.04, 0),
            (0.04, 0.2),
            (0.04, 0.4),
            (0.04, 0.6),
            (0.04, 0.8),
            (0.04, 1),
            (0.04, 0.8),
            (0.04, 0.6),
            (0.04, 0.4),
            (0.04, 0.2),
            (0.04, 0),
            ]
        pin1.assert_states_and_times(test)
        pin2.assert_states_and_times(test)
        pin3.assert_states_and_times(test)

def test_led_bar_graph_value():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with LEDBarGraph(pin1, pin2, pin3) as graph:
        graph.value = 0
        assert not any((pin1.state, pin2.state, pin3.state))
        graph.value = 1
        assert all((pin1.state, pin2.state, pin3.state))
        graph.value = 1/3
        assert pin1.state and not (pin2.state or pin3.state)
        graph.value = -1/3
        assert pin3.state and not (pin1.state or pin2.state)
        pin1.state = True
        pin2.state = True
        assert graph.value == 1
        pin3.state = False
        assert graph.value == 2/3
        pin3.state = True
        pin1.state = False
        assert graph.value == -2/3

def test_led_bar_graph_pwm_value():
    pin1 = MockPWMPin(2)
    pin2 = MockPWMPin(3)
    pin3 = MockPWMPin(4)
    with LEDBarGraph(pin1, pin2, pin3, pwm=True) as graph:
        graph.value = 0
        assert not any((pin1.state, pin2.state, pin3.state))
        graph.value = 1
        assert all((pin1.state, pin2.state, pin3.state))
        graph.value = 1/3
        assert pin1.state and not (pin2.state or pin3.state)
        graph.value = -1/3
        assert pin3.state and not (pin1.state or pin2.state)
        graph.value = 1/2
        assert (pin1.state, pin2.state, pin3.state) == (1, 0.5, 0)
        pin1.state = 0
        pin3.state = 1
        assert graph.value == -1/2

def test_led_bar_graph_bad_init():
    pin1 = MockPin(2)
    pin2 = MockPin(3)
    pin3 = MockPin(4)
    with pytest.raises(TypeError):
        LEDBarGraph(pin1, pin2, foo=pin3)

def test_pi_liter():
    pins = [MockPin(n) for n in (4, 17, 27, 18, 22, 23, 24, 25)]
    with PiLiter() as board:
        assert [device.pin for device in board] == pins

def test_pi_liter_graph():
    pins = [MockPin(n) for n in (4, 17, 27, 18, 22, 23, 24, 25)]
    with PiLiterBarGraph() as board:
        board.value = 0.5
        assert [pin.state for pin in pins] == [1, 1, 1, 1, 0, 0, 0, 0]
        pins[4].state = 1
        assert board.value == 5/8

def test_traffic_lights():
    red_pin = MockPin(2)
    amber_pin = MockPin(3)
    green_pin = MockPin(4)
    with TrafficLights(red_pin, amber_pin, green_pin) as board:
        board.red.on()
        assert red_pin.state
        assert not amber_pin.state
        assert not green_pin.state

def test_traffic_lights_bad_init():
    with pytest.raises(ValueError):
        TrafficLights()

def test_pi_traffic():
    pins = [MockPin(n) for n in (9, 10, 11)]
    with PiTraffic() as board:
        assert [device.pin for device in board] == pins

def test_snow_pi():
    pins = [MockPin(n) for n in (23, 24, 25, 17, 18, 22, 7, 8, 9)]
    with SnowPi() as board:
        assert [device.pin for device in board.leds] == pins

def test_traffic_lights_buzzer():
    red_pin = MockPin(2)
    amber_pin = MockPin(3)
    green_pin = MockPin(4)
    buzzer_pin = MockPin(5)
    button_pin = MockPin(6)
    with TrafficLightsBuzzer(
            TrafficLights(red_pin, amber_pin, green_pin),
            Buzzer(buzzer_pin),
            Button(button_pin)) as board:
        board.lights.red.on()
        board.buzzer.on()
        assert red_pin.state
        assert not amber_pin.state
        assert not green_pin.state
        assert buzzer_pin.state
        button_pin.drive_low()
        assert board.button.is_active

def test_fish_dish():
    pins = [MockPin(n) for n in (9, 22, 4, 8, 7)]
    with FishDish() as board:
        assert [led.pin for led in board.lights] + [board.buzzer.pin, board.button.pin] == pins

def test_traffic_hat():
    pins = [MockPin(n) for n in (24, 23, 22, 5, 25)]
    with TrafficHat() as board:
        assert [led.pin for led in board.lights] + [board.buzzer.pin, board.button.pin] == pins

def test_robot():
    pins = [MockPWMPin(n) for n in (2, 3, 4, 5)]
    with Robot((2, 3), (4, 5)) as robot:
        assert (
            [device.pin for device in robot.left_motor] +
            [device.pin for device in robot.right_motor]) == pins
        robot.forward()
        assert [pin.state for pin in pins] == [1, 0, 1, 0]
        robot.backward()
        assert [pin.state for pin in pins] == [0, 1, 0, 1]
        robot.forward(0.5)
        assert [pin.state for pin in pins] == [0.5, 0, 0.5, 0]
        robot.left()
        assert [pin.state for pin in pins] == [0, 1, 1, 0]
        robot.right()
        assert [pin.state for pin in pins] == [1, 0, 0, 1]
        robot.reverse()
        assert [pin.state for pin in pins] == [0, 1, 1, 0]
        robot.stop()
        assert [pin.state for pin in pins] == [0, 0, 0, 0]

def test_ryanteck_robot():
    pins = [MockPWMPin(n) for n in (17, 18, 22, 23)]
    with RyanteckRobot() as board:
        assert [device.pin for motor in board for device in motor] == pins

def test_camjam_kit_robot():
    pins = [MockPWMPin(n) for n in (9, 10, 7, 8)]
    with CamJamKitRobot() as board:
        assert [device.pin for motor in board for device in motor] == pins

def test_energenie_bad_init():
    with pytest.raises(ValueError):
        Energenie()
    with pytest.raises(ValueError):
        Energenie(0)

def test_energenie():
    pins = [MockPin(n) for n in (17, 22, 23, 27, 24, 25)]
    with Energenie(1, initial_value=True) as device1, \
            Energenie(2, initial_value=False) as device2:
        assert device1.value
        assert not device2.value
        [pin.clear_states() for pin in pins]
        device1.on()
        assert device1.value
        pins[0].assert_states_and_times([(0.0, False), (0.0, True)])
        pins[1].assert_states_and_times([(0.0, True), (0.0, True)])
        pins[2].assert_states_and_times([(0.0, True), (0.0, True)])
        pins[3].assert_states_and_times([(0.0, False), (0.0, True)])
        pins[4].assert_states_and_times([(0.0, False)])
        pins[5].assert_states_and_times([(0.0, False), (0.1, True), (0.25, False)])
        [pin.clear_states() for pin in pins]
        device2.on()
        assert device2.value
        pins[0].assert_states_and_times([(0.0, True), (0.0, False)])
        pins[1].assert_states_and_times([(0.0, True), (0.0, True)])
        pins[2].assert_states_and_times([(0.0, True), (0.0, True)])
        pins[3].assert_states_and_times([(0.0, True), (0.0, True)])
        pins[4].assert_states_and_times([(0.0, False)])
        pins[5].assert_states_and_times([(0.0, False), (0.1, True), (0.25, False)])

