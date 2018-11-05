import numpy as np

#Renaming errors that appears after atom cross border of grid.
class LeftError(Exception):
    pass
class RightError(Exception):
    pass
class UpError(Exception):
    pass
class DownError(Exception):
    pass

class grid():
    
    def __init__(self, x, y):
        """Creates NxN grid instance on which atoms can be initiated
        INPUT: Size of grid 
        OUTPUT: None"""
        self.grid = np.zeros((x,y))
        self.list_of_atoms=[]
        
    def initiate_atoms_randomly(self,quantitiy):
        """Initiate specified quantity of atoms spread randomly across grid
        INPUT: quantity of atoms
        OUTPUT: None"""
        coords=[]
        for i in range(np.shape(self.grid)[0]):
            for j in range(np.shape(self.grid)[1]):
                coords.append([i,j])
        np.random.shuffle(coords)#shuffles created coords without repetitions
        for i in range(quantitiy-1):
            self.list_of_atoms.append(atom(*(coords[i])))
            self.grid[coords[i][0],coords[i][1]]=1

    def initiate_atoms_in_line(self,quantitiy):
        """Initiate specified quantity of atoms row by row across grid
        INPUT: quantity of atoms
        OUTPUT: None"""
        coords=[]
        for i in range(np.shape(self.grid)[0]):
            for j in range(np.shape(self.grid)[1]):
                coords.append([i,j])
        for i in range(quantitiy-1):
            self.list_of_atoms.append(atom(*(coords[i])))
            self.grid[coords[i][0],coords[i][1]]=1
            
    def simulate_move(self):
        """Calls move method of atom object for every atom on grid
        INPUT: None
        OUTPUT: None"""
        for atom in self.list_of_atoms:
            atom.move(self.grid)        



class atom():

    def __init__(self,x,y):
        """Creates atom instance that can be placed on a grid.
        INPUT:Atom coords.
        Output: None"""
        self.position=[x,y]
        self.position_tracker=[]
        self.dx=0
        self.dy=0
    def check_occupation_and_move(self,grid,position_now,position_to_move):
        """Check if to-move position is not occupied, if not: moves atom to that position,
        if it is occupied makes atom to stay in place. Also track position of atoms on grid.
        INPUT: target grid,actual position, position-to-move
        OUTPUT: None"""
        if grid[tuple(position_to_move)] != 1:
            grid[tuple(position_to_move)]=1
            grid[position_now]=0
            self.position_tracker.append(tuple(position_to_move))
            self.dx+=position_to_move[0]-position_now[0]
            self.dy+=position_to_move[1]-position_now[1]
            #print(position_to_move)
            #print("########")
        else:
            self.position=list(position_now)
            self.position_tracker.append(position_now)
            
    def move(self,grid):
        """Rolls the dice, and prepare atom to move up, down, left or right.
        In case of end-of-grid teleports atom to opposite site of box.
        INPUT: target grid
        OUTPUT: None"""
        old_position=tuple(self.position)
        roll=np.random.rand()
        grid_size=np.shape(grid)
        if roll < 0.25:
            self.position[0] += 1
        elif roll > 0.25 and roll < 0.5:
            self.position[0] -= 1
        elif roll > 0.5 and roll < 0.75:
            self.position[1] += 1
        elif roll > 0.75 :
            self.position[1] -= 1
        try:
            if self.position[0]<0:
                raise LeftError
            if self.position[0]>grid_size[0]-1:
                raise RightError
            if self.position[1]<0:
                raise DownError
            if self.position[1]>grid_size[1]-1:
                raise UpError
            self.check_occupation_and_move(grid,old_position,self.position)
        except LeftError:
            self.position[0]=grid_size[0]-1
            self.check_occupation_and_move(grid,old_position,self.position)
        except RightError:
            self.position[0]=0
            self.check_occupation_and_move(grid,old_position,self.position)
        except DownError:
            self.position[1]=grid_size[1]-1
            self.check_occupation_and_move(grid,old_position,self.position)
        except UpError:
            self.position[1]=0
            self.check_occupation_and_move(grid,old_position,self.position)