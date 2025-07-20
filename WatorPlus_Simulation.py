grid_size = 1000 #1km
n_shark = 1
n_fish = 100
n_jelly = 10
def run():
    import numpy as np
    import matplotlib.pyplot as plt
    import tkinter as tk
    class Character():
        def __init__(self, x, y, stamina):
            self.stamina = stamina
            self.x = x
            self.y = y
            self.pos = [self.x, self.y]
        def death(self):
            del self.x
            del self.y
            del self.pos
            if isinstance(self, Predator):    # if the character is in the instance
                i = sharks.index(self)        # find the index of the character on its list
                sharks.pop(i)                 # and remove the character
            if isinstance(self, Prey):        
                i = fishes.index(self)        
                fishes.pop(i)                 
            if isinstance(self, Food):
                i = kelps.index(self)
                kelps.pop(i)
        def move_to(self, other, speed):
            # Compute the distance between two objects
            dx = other.x - self.x
            dy = other.y - self.y
            if dx > grid_size / 2:
                dx = dx - grid_size
            elif dx < -grid_size / 2:
                dx = dx + grid_size          # Verify if the distance is greater than half of the grid 
            if dy > grid_size / 2:
                dy = dy - grid_size
            elif dy < -grid_size / 2:
                dy = dy + grid_size
            dist = np.sqrt(dx**2 + dy**2) #Euclidian distance
            # Compute the direction
            direction = [dx / dist, dy / dist]
            # Compute the movement depending on the speed
            displacement = [direction[0] * speed, direction[1] * speed]
            # New toroidal coordinates
            new_x = (self.x + displacement[0]) % grid_size
            new_y = (self.y + displacement[1]) % grid_size
            # Update the coordinates of the object
            self.x, self.y = new_x, new_y
            self.pos = [self.x, self.y]
    class Predator(Character):
        x = []
        y = []
    class Prey(Character):
        x = []
        y = []
        kelps_ate = 0
    class Obstacle(Character):
        x = []
        y = []
    class Food(Character):
        x = []
        y = []
    # function to find the closest pairs
    def closest_distances_indices(firsts, seconds):
        min_distances = []
        min_indices = []
        for i, first in enumerate(firsts):
            min_distance = np.inf
            min_second_index = -1
            for j, second in enumerate(seconds):
                # Compute the distance between every possible pair 
                dx = abs(first.x - second.x)
                dy = abs(first.y - second.y)
                dx = min(dx, grid_size - dx)
                dy = min(dy, grid_size - dy)
                dist = np.sqrt(dx**2 + dy**2)    
                # Updating the min distance and the index of second object(The index of first object is the iteration j)
                if dist < min_distance:
                    min_distance = dist
                    min_second_index = j
            # Adding the min distance to the list of all min distances
            min_distances.append(min_distance)
            # Adding the pair of that min distance to the list of all pairs
            min_indices.append((i, min_second_index))
        return min_distances, min_indices
    #FUNCTION TO SHUTDOWN THE EXECUTION 
    def on_close(event):
        plt.close(fig)
        raise SystemExit(0)
    #Let every mob spawn
    #Sharks
    sharks = []
    fishes = []
    jellys = []
    kelps = []
    for i in range(n_shark) :
        shark = Predator(np.random.rand() * grid_size, np.random.rand() * grid_size, 100) 
        sharks.append(shark)
    print("SHARKS POSITIONS:")
    for f in sharks: print(f.pos)
    #Fishes
    for i in range(n_fish): 
        fish = Prey(np.random.rand() * grid_size, np.random.rand() * grid_size, 100)
        fishes.append(fish) 
    print("FISH POSITIONS:")
    for f in fishes: print(f.pos)
    #Jellyfishes
    for i in range(n_jelly): 
        jelly = Obstacle(np.random.rand() * grid_size, np.random.rand() * grid_size, 100)
        jellys.append(jelly)  
    print("JELLY POSITIONS:")
    for f in jellys: print(f.pos)
    # plot
    fig, ax = plt.subplots()
    ax.set_facecolor("deepskyblue")   # set background color
    # set x and y limits (0 to the size of the grid)
    ax.set(xlim=(0, grid_size), xticks=np.arange(0), ylim=(0, grid_size), yticks=np.arange(0))#(tick)If I wanna see the value of the ticks of the grid
    # set the size of the characters
    shark_size = 20000 / grid_size
    fish_size = shark_size * 0.5
    # initializing the firsts characters into scatters
    scat_kelp = ax.scatter([kelp.pos[0] for kelp in kelps], [kelp.pos[1] for kelp in kelps], c='green', edgecolor='black', linewidth=0.5,label='Kelps', marker='s', s=fish_size)
    scat_fish = ax.scatter([fish.pos[0] for fish in fishes], [fish.pos[1] for fish in fishes], c='blue', edgecolor='black', linewidth=0.5,label='Fishes', marker='.', s=fish_size)
    scat_jelly = ax.scatter([jelly.pos[0] for jelly in jellys], [jelly.pos[1] for jelly in jellys], c='pink', edgecolor='black', linewidth=0.5,label='Jellyfishes', marker='o', s=fish_size)
    scat_shark = ax.scatter([shark.pos[0] for shark in sharks], [shark.pos[1] for shark in sharks], c='red', edgecolor='black', linewidth=0.5,label='Sharks', marker='o', s=shark_size)
    # Getting the figure to be zoomed
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    mng.set_window_title("WatorPlus")

    plt.title('WatorPlus')
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1,1), fontsize='small')
    plt.ion()
    plt.show()
    fig.canvas.mpl_connect('close_event', on_close) #SHUTTING THE EXECUTION WITH THE CLOSING OF THE WINDOW
    num_iterations = 0
    max_iterations = 30
    # Stop when all sharks or fishes are dead
    while len(sharks)>0 and len(fishes)>0:
        if num_iterations == max_iterations:
            print("Kelps spawned")
            num_iterations = 0

            num_kelp = np.random.randint(10, 27) #max number of kelp spawning (between 10 and 27)
            adjacent = []   # a list to save the number of kelps in a row
            y_spacing = 6
            x_spacing = 3
            adjacent_min = 1 #min value for a row
            adjacent_max = 6 #max value for a row
            counter = 0  # needed to access the adjacent value of actual row
            current_kelps = 0
            # Spawning the first kelp
            kelp = Food(np.random.rand() * grid_size, np.random.rand() * grid_size, 100)
            kelps.append(kelp)
            current_kelps +=1
            # run this until all the kelps that are spawning all at once reach the value of num_kelp
            while current_kelps <= num_kelp:
                adjacent.append(np.random.randint(adjacent_min, adjacent_max)) 
                direction = np.random.randint(1,2)     # If the value equals 1 than the row spawn to the right, otherwise to the left
                for num in range(adjacent[counter]-1): 
                    if current_kelps > num_kelp:    # to avoid an eventual error
                        break
                    if direction == 1:      # to the right
                        kelp = Food(kelps[-1].x + x_spacing, kelps[-1].y, 100)  #Takes the positions of the previous kelp, adding only X spacing
                        kelps.append(kelp)
                    elif direction == 2:    # to the left
                        kelp = Food(kelps[-1].x - x_spacing, kelps[-1].y, 100)
                        kelps.append(kelp)
                    current_kelps +=1 
                if current_kelps > num_kelp:
                    break
                # after the first row has spawned
                idx = np.random.randint(1, (current_kelps + 1))  #Index of the previous kelp which will be used to take its X position
                kelp = Food(kelps[-idx].x + x_spacing, kelps[-1].y - y_spacing, 100) #Spawning the next first kelp with some Y spacing
                kelps.append(kelp)
                current_kelps += 1
                counter += 1
        # COMPUTING THE PAIRS NEEDED
        # SHARKS TO FISHES
        min_distances_sharks, min_indices_sharks = closest_distances_indices(sharks, fishes)
        # FISHES TO SHARKS
        min_distances_fishes, min_indices_fishes = closest_distances_indices(fishes, sharks)
        # FISH TO KELPS
        min_distances_kelps, min_indices_kelps = closest_distances_indices(fishes, kelps)
        # JELLYS TO SHARKS
        min_distances_jellys, min_indices_jellys = closest_distances_indices(jellys, sharks)

        # MOVEMENT OF FISHES
        i=0
        for (fish_index, shark_index), (_, kelp_index) in zip(min_indices_fishes, min_indices_kelps):
            if min_distances_fishes[i] > 100:
                if min_distances_fishes[i] < min_distances_kelps[i]:
                    fishes[fish_index].move_to(sharks[shark_index], -0.7)
                else:
                    fishes[fish_index].move_to(kelps[kelp_index], 0.7)
            if min_distances_fishes[i] <=100:
                if min_distances_fishes[i] < min_distances_kelps[i]:
                    fishes[fish_index].move_to(sharks[shark_index], -1.2)       #The fish decide either to move into kelps or swim away from sharks
                else:
                    fishes[fish_index].move_to(kelps[kelp_index], 1.2)
            if min_distances_fishes[i] <=20:
                if min_distances_fishes[i] < min_distances_kelps[i]:
                    fishes[fish_index].move_to(sharks[shark_index], -2)
                else:
                    fishes[fish_index].move_to(kelps[kelp_index], 2)
            if min_distances_kelps[i] < 2:
                print("A FISH ATE A KELP")
                kelps[kelp_index].death()                      #Fish eating a kelp
                fishes[fish_index].kelps_ate += 1              #Adding a kelp to the ones eaten by a single fish
                break
            if fishes[fish_index].kelps_ate >= 2:              #Fish gives birth
                print("A FISH IS BORN")
                fishes[fish_index].kelps_ate = 0               #Turning to 0 the kelps eaten by a single fish
                fish = Prey(fishes[fish_index].x-2, fishes[fish_index].y-2, 100) 
                fishes.append(fish)
                break
            i+=1
        # MOVEMENT OF SHARKS
        i=0
        for shark_index, fish_index in min_indices_sharks:
                if min_distances_sharks[i] > 100:
                    sharks[shark_index].move_to(fishes[fish_index], 1.5) 
                    sharks[shark_index].stamina -= 0.2
                if min_distances_sharks[i] <=100:
                    sharks[shark_index].move_to(fishes[fish_index], 2.2) 
                    sharks[shark_index].stamina -= 0.4
                if min_distances_sharks[i] <=20:
                    sharks[shark_index].move_to(fishes[fish_index], 4) 
                    sharks[shark_index].stamina -= 1
                if min_distances_sharks[i] <= 4:
                    print("A FISH HAS BEEN KILLED BY A SHARK", fishes[fish_index])
                    fishes[fish_index].death() 
                    sharks[shark_index].stamina += 10
                    break
                if sharks[shark_index].stamina <= 0:
                    print("A SHARK DIED BY STAMINA")
                    sharks[shark_index].death()
                    break
                if sharks[shark_index].stamina >=150:
                    print("A SHARK IS BORN")
                    sharks[shark_index].stamina -= 80
                    shark = Predator(sharks[shark_index].x-2, sharks[shark_index].y-2, 100) 
                    sharks.append(shark)
                    break
                i += 1
        # MOVEMENT FOR JELLYS
        for jelly in jellys:
                jelly.x += np.random.uniform(-0.6, 0.6)             
                jelly.y += np.random.uniform(-0.6, 0.6)     #Just floating randomly
                jelly.pos = [jelly.x, jelly.y]
        i=0
        for jelly_index, shark_index in min_indices_jellys:
                if min_distances_jellys[i] <= 4:
                    print("A SHARK HAS BEEN KILLED BY A JELLYFISH", sharks[shark_index])
                    sharks[shark_index].death() 
                    # break
                i += 1
        #UPDATING THE PLOTS FOR EACH CHARACTER
        if sharks !=[]:
            scat_shark.set_offsets([shark.pos for shark in sharks])    
        if fishes !=[]:   
            scat_fish.set_offsets([fish.pos for fish in fishes])
        if jellys !=[]:
            scat_jelly.set_offsets([jelly.pos for jelly in jellys]) 
        if kelps !=[]:
            scat_kelp.set_offsets([kelp.pos for kelp in kelps]) 
        plt.pause(0.01667)      #Should be 60 frame-per-second
        num_iterations += 1
        print("Iteration n°:",num_iterations) 
    #SHUTTING DOWN THE SIMULATION 
    if fishes == []:
        tk.messagebox.showinfo(title="Game over", message="All fishes are dead")
        print("All Fishes are dead")
        mng.destroy()
    elif sharks == []:
        tk.messagebox.showinfo(title="Game over", message="All sharks are dead")
        print("All Sharks are dead")
        mng.destroy()


