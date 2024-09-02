import pygame
import math

WIDTH, HEIGHT, border_width = 1000, 800, 10

class Ball:
    def __init__(self, radius, color, x_pos, y_pos, x_velocity, y_velocity, gravity, retention, x_acceleration, y_acceleration):
        self.radius = radius
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.gravity = gravity
        self.friction = 0.98
        self.retention = retention
        self.x_acceleration = x_acceleration
        self.y_acceleration = y_acceleration
        self.bounce_stop = 1.5
        self.circle = None
        self.selected = False

    def handle_movement(self, mouse_position):
        if not self.selected:
            self.x_pos += self.x_velocity
            self.y_pos -= self.y_velocity
        else:
            self.x_pos = mouse_position[0]
            self.y_pos = mouse_position[1]
            self.x_velocity = 0
            self.y_velocity = 0

        # y-axis border collision
        if self.radius + border_width / 2 <= self.y_pos <= HEIGHT - self.radius - border_width / 2:
            self.y_velocity += self.y_acceleration
        else:
            extra_distance = abs(self.y_pos - (HEIGHT - self.radius - border_width / 2))
            # bottom border collision
            if self.y_pos > HEIGHT - self.radius - border_width / 2:
                self.y_pos = HEIGHT - self.radius - border_width / 2
                if abs(self.y_velocity) > self.bounce_stop:
                    self.y_velocity += extra_distance / abs(self.y_velocity)
                    self.y_velocity *= -self.retention
                    self.calculate_friction()
                else:
                    self.y_velocity = 0

            # top border collision
            elif self.y_pos < self.radius + border_width / 2:
                self.y_pos = self.radius + border_width / 2
                self.y_velocity *= -self.retention
                self.calculate_friction()

        # x-axis border collision
        if self.x_pos <= self.radius + border_width / 2 and self.x_velocity < 0:
            self.x_pos = self.radius + border_width / 2
            self.x_velocity *= -1 * self.retention
            self.calculate_friction()
        elif self.x_pos >= WIDTH - self.radius - border_width / 2 and self.x_velocity > 0:
            self.x_pos = WIDTH - self.radius - border_width / 2
            self.x_velocity *= -1 * self.retention
            self.calculate_friction()
        else:
            self.x_velocity += self.x_acceleration


        # print('x_pos: {}, y_pos: {}, x_vel: {}, y_vel: {}'.format(self.x_pos, self.y_pos, self.x_velocity, self.y_velocity))

    def calculate_friction(self):
        self.x_velocity *= self.friction


    def check_select(self, position):
        self.selected = False
        if self.circle:
            if self.circle.collidepoint(position):
                self.selected = True
        return self.selected


    def release(self, mouse_position_log):
        self.selected = False
        if len(mouse_position_log) > 10:
            self.x_velocity = (mouse_position_log[-1][0] - mouse_position_log[-2][0]) / 2 * 0.75
            self.y_velocity = (mouse_position_log[-1][1] - mouse_position_log[-2][1]) / 2 * -0.5

    def check_collisions(self, other):
        dx = self.x_pos - other.x_pos
        dy = self.y_pos - other.y_pos
        distance = math.sqrt(dx**2 + dy**2)
        return distance < (self.radius + other.radius)


    def resolve_collisions(self, other):
        # Calculate the normal vector
        dx = self.x_pos - other.x_pos
        dy = self.y_pos - other.y_pos
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:  # Prevent division by zero
            return

        self.x_velocity -= other.x_velocity
        other.x_velocity += self.x_velocity

        self.y_velocity -= other.y_velocity
        other.y_velocity += self.y_velocity

    def draw_vector(self, screen):
        pygame.draw.line(screen, 'red', (self.x_pos, self.y_pos), (self.x_pos + self.x_velocity * 4, self.y_pos), 4)
        pygame.draw.line(screen, 'green', (self.x_pos, self.y_pos), (self.x_pos, self.y_pos - self.y_velocity * 4),4)

    def draw_self(self, screen):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)