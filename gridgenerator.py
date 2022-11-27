# generategrid
from numpy import random
import pandas as pd
import configfilereader as cfr
class GridGenerator():

    def swap_two_numbers(self, grid):

        foo = random.randint(4) + 1
        bar = random.randint(4) + 1
        for i in range(4):
            for j in range(4):
                if grid[i][j] == foo:
                    grid[i][j] = bar
                elif grid[i][j] == bar:
                    grid[i][j] = foo

    def generate_random_grid(self, isValid):
        
        # SANITY CHECK: if you uncomment the next line then performance drops to 50% as expected
        # isValid = True
        
        # there are three templates:  
        grid1 = [[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]]
        grid2 = [[1,2,3,4],[3,4,1,2],[4,1,2,3],[2,3,4,1]]
        grid3 = [[1,2,3,4],[4,3,1,2],[2,1,4,3],[3,4,2,1]]
        allgrids = [grid1,grid2,grid3]
        foo = random.randint(3)
        grid = allgrids[foo]
 
        if( not isValid):
            # 50% chance of making a totally random mess (every digit still occurs 4 times)
            foo = random.randint(2)
            if( foo == 0):
                grid = [[1,1,2,3],[4,2,3,1],[2,2,4,4],[3,1,3,4]]
            
                
        # swap pairs of digits (grid remains valid if and only if it was already valid)           
        for foo in range(3):
            self.swap_two_numbers(grid)

        # swap two rows covering the same boxes (grid remains valid if and only if it was already valid)   
        for foo in range(5):
            i = random.randint(4)
            j = random.randint(4)
            if( int(i/2) == int(j/2)):
                for k in range(4):
                    temp=grid[i][k];grid[i][k]=grid[j][k];grid[j][k]=temp
        # swap two columns covering the same boxes
        for foo in range(5):
            i = random.randint(4)
            j = random.randint(4)
            if( int(i/2) == int(j/2)):
                for k in range(4):
                    temp=grid[k][i];grid[k][j]=grid[k][j];grid[k][i]=temp

        # if we want a non-valid grid, swap two cells in the same row or column 
        if( not isValid):
            tempcount = 0
            while(tempcount != 1):
                tempcount = 0
                i1 = random.randint(4); i2 = random.randint(4)
                j1 = random.randint(4); j2 = random.randint(4)
                if( i1 == i2):
                    tempcount += 1
                if( j1 == j2):
                    tempcount += 1
            temp=grid[i1][j1];grid[i1][j1]=grid[i2][j2];grid[i2][j2]=temp       
                


        return grid

    def flatten_grid(self, grid):
        result = []
        for i in range(4):
            for j in range(4):
                result.append(grid[i][j])
        return result

    
    def generate_raw_data(self, num_right, num_wrogn, filename):
        mydata = []
        for foo in range(num_right):
            grid = self.generate_random_grid(True)
            row = self.flatten_grid(grid)
            row.append(1)
            mydata.append(row)
        for foo in range(num_wrogn):
            grid = self.generate_random_grid(False)
            row = self.flatten_grid(grid)
            row.append(0)
            mydata.append(row)
           
            
        df = pd.DataFrame(mydata)
        df.to_csv(filename,header=False,index=False)


    
    def print_grid(self, grid):
        for x in grid:
            for y in x:
                print(y,end='')
            print('')





if __name__ == "__main__":
    
    c = cfr.ConfigFileReader()
    parameterdict = c.readfile('configparams.txt')
    print('parameterdict = ', parameterdict)
    
    g = GridGenerator()

    NUMVALID = int(parameterdict['NUMVALID'])
    NUMINVALID = int(parameterdict['NUMINVALID'])
    RAWDATAFILE = parameterdict['RAWDATAFILE']
    g.generate_raw_data(NUMVALID,NUMINVALID,RAWDATAFILE)