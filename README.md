# Floor Cleaning Robot Simulation

> This is a Program that simulates the movement of floor clenaing robots such as the IRobot Roomba in a room
The simulation allows one compare how much time a group of robots will takes to clean the floor of a room using two diffrent strategies. 

## Simulation Components
**1. Room Object**: Rooms are rectangles, divided into square tiles. At the start of the simulation, each tile is covered in some amount of dirt, which is the same across tiles. The Room Parent Object has two subclasses:
* A Standard Room: This is an object which represents an empty without any furniture 
* B Furnished Room: This is a room with some amount of Furniture which must be avoided by the Robots

**2.Robot Object:** Multiple robots can exist in the room. There are two subclasses of Robot objects
* A Standard Robot: The movement strategy for StandardRobot is as follows: in each time-step:
    - Calculate what the new position for the robot would be if it moved straight in its current direction at its given speed.
    - If that is a valid position, move there and then clean the tile corresponding to that position by the robot’s capacity. The position is valid if it is in the room and if it is unfurnished.
    - Otherwise, rotate the robot to be pointing in a random new direction.
* B Faulty Robot: The movement strategy for a FaultyRobot is as follows:
    * Check if the robot is faulty at this timestep.
    * If the robot is faulty,it does not clean the tile it is currently on, and have randomly update its direction.
    * If the robot is not faulty, it would be treated like a StandardRobot - it moves to a new position and clean if it can. If it cannot validly move to the next position, instead changes its direction.

**3 Simulation Starting Conditions:**
* Each robot should start at a random position in the room.
* Each room should start with a uniform amount of dirt on each tile, given by dirt_amount.
* The simulation terminates when a specified fraction of the room tiles have been fully cleaned (i.e., the amount of dirt on those tiles is 0).

### Simulation Visualizytion: To see a Visual version of the cleaning process run gui.py