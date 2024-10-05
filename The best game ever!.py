from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Fullscreen mode
window.fullscreen = True

# Sky
sky = Sky()

# Ground (make it thicker to prevent falling through)
grass = Entity(model='plane', scale=(1000, 1, 1000), texture='grass', collider='box')

# Checkpoint Class
class Checkpoint(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=color.yellow,
            scale=(2, 0.5, 2),
            position=position,
            collider='box'
        )

# Function to create a building with a door
def create_building(x, z):
    building = Entity(
        model='cube',
        scale=(10, random.uniform(10, 30), 10),
        position=(x, random.uniform(5, 15), z),
        color=color.gray,
        collider='box'
    )
    # Window on the building
    Entity(
        parent=building,
        model='cube',
        scale=(2, 2, 0.1),
        position=(0, building.scale_y / 2 + 1, 5),
        color=color.blue,
        collider='box'
    )
    # Door on the building
    Entity(
        parent=building,
        model='cube',
        scale=(2, 4, 0.1),
        position=(0, -building.scale_y / 2 + 2, 5),
        color=color.brown,
        collider='box'
    )
    return building

# Function to create a house with a door
def create_house(x, z, scale=(8, 8, 8)):
    house = Entity(
        model='cube',
        scale=scale,
        position=(x, scale[1] / 2, z),
        color=color.brown,
        collider='box'
    )

    # Define window and door sizes
    window_size = (2, 2, 0.1)
    door_size = (2, 4, 0.1)

    # Create windows
    window_positions = [
        (2, house.scale_y / 2 + 1, -3),  # Front right
        (-2, house.scale_y / 2 + 1, -3), # Front left
        (2, house.scale_y / 2 + 1, 3),   # Back right
        (-2, house.scale_y / 2 + 1, 3)   # Back left
    ]

    for pos in window_positions:
        Entity(
            parent=house,
            model='cube',
            scale=window_size,
            position=pos,
            color=color.blue,
            collider='box'
        )
    
    # Create door
    Entity(
        parent=house,
        model='cube',
        scale=door_size,
        position=(0, -house.scale_y / 2 + 2, -3),
        color=color.dark_gray,
        collider='box'
    )

    return house

# Function to create a tree
def create_tree(x, z):
    trunk = Entity(
        model='cube',
        scale=(1, 4, 1),
        position=(x, 2, z),
        color=color.brown,
        collider='box'
    )
    leaves = Entity(
        model='sphere',
        scale=(3, 3, 3),
        position=(x, 6, z),
        collider='mesh',
        texture='grass'
    )
    return trunk, leaves

# Function to create a car
def create_car(x, z):
    car = Entity(
        model='cube',
        scale=(2, 0.5, 1),
        position=(x, 0.25, z),
        color=color.red,
        collider='box'
    )
    car.speed = random.uniform(0.1, 0.5)  # Random speed for each car
    car.direction = random.choice([-1, 1])  # Random direction
    car.start_x = x
    car.end_x = x + 50 * car.direction  # Move cars along a path
    return car

# Function to create a traffic light
def create_traffic_light(x, z):
    pole = Entity(
        model='cube',
        scale=(0.2, 4, 0.2),
        position=(x, 2, z),
        color=color.gray,
        collider='box'
    )
    light = Entity(
        model='cube',
        scale=(0.5, 0.5, 0.5),
        position=(x, 4, z),
        color=color.red,
        collider='box'
    )
    return pole, light

# Function to create a market
def create_market(x, z):
    for i in range(5):  # Number of market stalls
        Entity(
            model='cube',
            scale=(4, 4, 4),
            position=(x + i * 6, 2, z),
            color=color.orange,
            collider='box'
        )

# Create entities
for i in range(-500, 500, 60):
    for j in range(-500, 500, 60):
        if random.random() > 0.5:
            create_building(i, j)

for i in range(-400, 400, 50):
    for j in range(-400, 400, 50):
        if random.random() > 0.7:
            create_house(i, j)

for i in range(-400, 400, 40):
    for j in range(-400, 400, 40):
        if random.random() > 0.7:
            create_tree(i, j)

cars = []
for i in range(-600, 600, 20):
    for j in range(-600, 600, 20):
        if random.random() > 0.6:
            car = create_car(i, j)
            cars.append(car)

for i in range(-400, 400, 100):
    for j in range(-400, 400, 100):
        if random.random() > 0.8:
            create_traffic_light(i, j)

for i in range(-400, 400, 100):
    for j in range(-400, 400, 100):
        if random.random() > 0.8:
            create_market(i, j)

house_in_sky = create_house(0, 0, scale=(100, 1, 100))
house_in_sky.position = (0, 50, 0)

# Add checkpoints
checkpoints = [
    Checkpoint(position=(0, 0, 0)),
    Checkpoint(position=(50, 0, 50)),
    Checkpoint(position=(-50, 0, -50))
]

# Initialize player's last checkpoint
last_checkpoint = checkpoints[0].position

def update():
    global last_checkpoint
    
    # Check if the player is below ground
    if player.y < -10:
        player.position = last_checkpoint  # Respawn at the last checkpoint
    
    # Update car positions
    for car in cars:
        car.x += car.speed * car.direction
        if car.x < car.start_x - 50 or car.x > car.start_x + 50:
            car.direction *= -1  # Change direction

    # Check if player reaches a checkpoint
    for checkpoint in checkpoints:
        if player.intersects(checkpoint).hit:
            last_checkpoint = checkpoint.position

# FirstPersonController with improved settings
player = FirstPersonController()
player.position = (0, 2, 0)  # Set initial position to be above the ground
player.speed = 5  # Adjust the speed of the player
player.jump_height = 2  # Set jump height if necessary
player.slope_limit = 60  # Adjust slope limit if needed

app.run()
