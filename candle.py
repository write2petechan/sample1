import asyncio
import platform
import pygame
import random

# Initialize Pygame
def setup():
    global screen, WIDTH, HEIGHT, candle, particles
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Animated Candle with Dancing Flame")
    
    # Candle properties
    candle = {
        'x': WIDTH // 2,
        'y': HEIGHT // 2 + 150,
        'width': 50,
        'height': 120,
        'color': (220, 220, 220)  # Light gray for wax
    }
    
    # Particle list for flame
    particles = []

# Particle class for flame effect
class FlameParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(6, 12)
        self.speed_y = random.uniform(-2.5, -1.5)
        self.speed_x = random.uniform(-0.7, 0.7)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(0, 50))  # Yellow-orange-red
        self.lifetime = random.randint(20, 50)  # Frames to live
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size *= 0.97  # Shrink over time
    
    def draw(self):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Update game loop
def update_loop():
    global particles
    screen.fill((20, 20, 20))  # Dark background for contrast
    
    # Draw candle
    pygame.draw.rect(screen, candle['color'], 
                    (candle['x'] - candle['width'] // 2, 
                     candle['y'] - candle['height'], 
                     candle['width'], 
                     candle['height']))
    
    # Draw wick
    wick_width = 5
    wick_height = 25
    pygame.draw.rect(screen, (40, 40, 40), 
                    (candle['x'] - wick_width // 2, 
                     candle['y'] - candle['height'] - wick_height, 
                     wick_width, 
                     wick_height))
    
    # Update and draw flame particles
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.lifetime <= 0:
            particles.remove(particle)
    
    # Add new flame particles
    if random.random() < 0.6:  # 60% chance per frame for lively flame
        particles.append(FlameParticle(candle['x'], candle['y'] - candle['height'] - 15))
    
    pygame.display.flip()

# Main async loop for Pyodide compatibility
async def main():
    setup()
    clock = pygame.time.Clock()
    FPS = 60
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        update_loop()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

# Pyodide compatibility check
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())