#TODO: AxisZone has type checking on its methods which is just begging
# to be converted into a handy util to define valid input combinations.
# Likewise, I bet something interesting could be done to define valid
# values for the objects.
# Essentially, implement a type system...
# How big of a performance hit would it be?
# If it's a big hit, could use it in debug mode and pass through otherwise


class AxisZone(object):
    zone = ([int, float], [int, float])

    def __init__(self, start, end=None):
        '''
        # TODO: find a way to declare this programmatically
        Can be created passing min,max as a tuple or as separate components
        '''
        # TODO: this is nice and succinct, but should it use exceptions?
        assert start in [int, float, tuple]
        if start is not tuple:
            assert end in [int, float]

        if type(start) is tuple:
            zone = start
        else:
            zone = (start, end)

        # we order zone to make the in_zone check simpler
        self.zone = sorted(zone)

    def in_zone(self, position):
        assert position in [int, float]
        return self.zone[0] <= position <= self.zone[1]


class Axis(object):
    deadzone = AxisZone
    maxrange = AxisZone


class Button(object):
    pass


class Hat(object):
    pass


class Joystick(object):
    axes = list
    buttons = list
    hats = list


class X52(object):
    LABELS = {
        'axes': [
            'up/down',
            'left/right',
            'throttle',
            'small dial',
            'top dial',
            'rotate left/right',
            'slider',
            'mouse left/right',
            'mouse up/down'
        ],
        'buttons': [
            # Buttons on the stick
            'trigger',
            'fire',
            'A',
            'B',
            'C',
            'pinky',

            # Buttons on the throttle
            'D',
            'E',

            # The toggle switches on the stick
            'T1',
            'T2',
            'T3',
            'T4',
            'T5',
            'T6',

            # The second stage trigger
            'second trigger',

            # The hat on the top of the stick
            'top hat up',
            'top hat right',
            'top hat down',
            'top hat left',

            # The hat on the throttle
            'throttle hat up',
            'throttle hat right',
            'throttle hat down',
            'throttle hat left',

            # The rotary switch
            'green',
            'orange',
            'red',

            # The MFD buttons
            'function',
            'start/stop',
            'reset',

            # The info button
            'info',

            # The mouse button
            'mouse btn',

            # The scroll wheel - the wheel events seem to be flaky, btn is ok
            'scroll btn',
            'scroll down',
            'scroll up'
        ],
        'hats': [
            # The main hat on the stick
            'central hat'
        ]
    }
