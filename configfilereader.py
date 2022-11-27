# config file reader
class ConfigFileReader():

    def readfile(self,filename):
    
        mydict = {}
        file = open(filename)
        for line in file:
            pieces = line.split()
            mydict[pieces[0]] = pieces[1]
        return mydict