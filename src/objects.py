import pygame

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
        self.retention = retention
        self.x_acceleration = x_acceleration
        self.y_acceleration = y_acceleration
        self.bounce_stop = 1.5

    def handle_movement(self):
        self.x_pos -= self.x_velocity
        self.y_pos -= self.y_velocity

        if self.y_pos <= HEIGHT - self.radius - border_width / 2:
            self.y_velocity += self.y_acceleration
        else:
            extra_distance = self.y_pos - (HEIGHT - self.radius - border_width / 2)
            self.y_pos = HEIGHT - self.radius - border_width / 2
            if abs(self.y_velocity) > self.bounce_stop:

                self.y_velocity += (extra_distance / abs(self.y_velocity))
                self.y_velocity = self.y_velocity * -1 * self.retention



            else:
                if abs(self.y_velocity) <= self.bounce_stop:
                    self.y_velocity = 0
                    self.y_pos = HEIGHT - self.radius - border_width / 2

        if self.x_pos > self.radius + border_width / 2 and self.x_pos < WIDTH - self.radius - border_width / 2:
            self.x_velocity += self.x_acceleration
        else:
            self.x_velocity *= -1


        self.x_velocity += self.x_acceleration




    def draw_self(self, screen):
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)