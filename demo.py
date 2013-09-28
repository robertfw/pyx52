import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define the X52 labels
LABELS = {
    'axes': [
        'left/right',
        'up/down',
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


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint(object):

    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def output(self, screen, textString):
        textBitmap = self.font.render(textString, True, WHITE)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [1500, 800]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while not any(True for e in pygame.event.get() if e.type == pygame.QUIT):
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.output(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.output(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.output(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.output(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.output(screen, "[{}] {}: {:>6.3f}".format(i, LABELS['axes'][i], axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.output(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.output(
                screen, "[{}] {}: {}".format(i, LABELS['buttons'][i], button))
        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.output(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.output(screen, "[{}] {}: {}".format(i, LABELS['hats'][i], str(hat)))
        textPrint.unindent()

        textPrint.unindent()

        # draw the circular buttons
        SMALL = 10
        MEDIUM = 15
        LARGE = 20

        circle_buttons = (
            (1, SMALL, (1200, 200)),    # fire
            (2, SMALL, (1300, 200)),    # a
            (3, SMALL, (1300, 300)),    # b
            (7, LARGE, (600, 200)),    # E
            (6, SMALL, (600, 300)),    # D
            (29, MEDIUM, (600, 400)),  # info
        )

        for btn_num, radius, pos in circle_buttons:
            width = 0 if joystick.get_button(btn_num) else 2
            pygame.draw.circle(screen, BLUE, pos, radius, width)

        hats = (
            ('btns', (15, 16, 17, 18), (1100, 200)),
            ('btns', (19, 20, 21, 22), (500, 200)),
            ('hat', 0, (1200, 310))
        )

        margin = 10
        length = 20
        width = 8

        for hat_type, hat_map, pos in hats:
            if hat_type == 'btns':
                states = (
                    joystick.get_button(hat_map[0]),
                    joystick.get_button(hat_map[1]),
                    joystick.get_button(hat_map[2]),
                    joystick.get_button(hat_map[3]),
                )
            elif hat_type == 'hat':
                hat_val = joystick.get_hat(hat_map)
                states = (
                    hat_val[1] == 1,
                    hat_val[0] == 1,
                    hat_val[1] == -1,
                    hat_val[0] == -1
                )

            cx, cy = pos

            # entries are in order of up, right, down, left
            # values are ((left, top, width, height), border_width)
            hats = (
                ((cx - (width / 2),
                  cy - margin - length,
                  width,
                  length),
                 0 if states[0] else 1),
                ((cx + margin,
                  cy - (width / 2),
                  length,
                  width),
                 0 if states[1] else 1),
                ((cx - (width / 2),
                  cy + margin,
                  width,
                  length),
                 0 if states[2] else 1),
                ((cx - margin,
                  cy - (width / 2),
                  -length,
                  width),
                 0 if states[3] else 1)
            )

            for rect, border_width in hats:
                pygame.draw.rect(screen, BLUE, rect, border_width)



    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
