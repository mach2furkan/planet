import pygame
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# Set up font
FONT = pygame.font.SysFont("Comic Sans MS", 16)

class Planet:
    AU = 149.6e6 * 1000  # 1 Astronomical Unit (meters)
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU  # Scale factor: 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        """Draws the planet and its orbit on the screen."""
        x = int(self.x * self.SCALE + WIDTH / 2)
        y = int(self.y * self.SCALE + HEIGHT / 2)

        # Draw orbit path
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = int(px * self.SCALE + WIDTH / 2)
                py = int(py * self.SCALE + HEIGHT / 2)
                updated_points.append((px, py))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw planet
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # Display distance from the sun
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)} km", True, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() // 2, y - distance_text.get_height() // 2))

    def attraction(self, other):
        """Calculates gravitational force between two planets."""
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        """Updates the planet's velocity and position based on gravitational forces."""
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    """Main function to run the simulation."""
    run = True
    clock = pygame.time.Clock()

    # Create planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)  # Limit FPS to 60
        WIN.fill((0, 0, 0))  # Clear screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update and draw planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()  # Refresh display

    pygame.quit()

# Run the simulation
if __name__ == "__main__":
    main()
