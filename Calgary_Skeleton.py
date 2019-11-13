from datetime import datetime
import re

class Parser:
    def __init__(self):
        self.numberOfDays = 0 # Count number of days passed
        
        self.startDate = datetime.today()
        self.endDate = datetime.today()

        self.totalRequest = 0
        self.dataBytes = 0

        self.ResponseResult = ""
        self.successRate = 0
        self.notModRate = 0
        self.foundRate = 0
        self.unSuccessRate = 0

        self.sourceAddyLocal = 0
        self.sourceAddyRemote = 0

        self.localBytes = 0
        self.remoteBytes = 0
 
        self.FileExt = ""
        self.extValue = ""
        self.HTML = 0
        self.Images = 0
        self.Sound = 0
        self.Video = 0
        self.Formatted = 0
        self.Dynamic = 0
        self.Others = 0

        self.HTMLBytes = 0
        self.ImagesBytes = 0
        self.SoundBytes = 0
        self.VideoBytes = 0
        self.FormatBytes = 0
        self.DynamicBytes = 0
        self.OthersBytes = 0
        
        self.fileTypeDict = {} # Contains file extension - file type information
        self.initializeFileType()
        
    def initializeFileType(self):  # Define file types for each file
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"

    def parse(self, logFile):  # Read each line from the log and process output
        index = 0
        for line in logFile:
            elements = line.split()

            # Skip to the next line if this line has an empty string
            if line is '':continue

            # Skip to the next line if this line contains not equal to 9 - 11 elements
            if not (9 <= len(elements) <= 11):continue

            # Corrects a record with a single "-"
            if (len(elements) == 9 and elements[2] != '-'):
                elements.insert(2, '-')

            sourceAddress = elements[0]
            timeStr = elements[3].replace('[', '')
            requestMethod = elements[5]
            requestFileName = elements[6].replace('"', '')
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]

            ################## From Here, implement your parser ##################
            # Inside the for loop, do simple variable assignments & modifications
            # Please do not add for loop/s
            # Only the successful requests should be used from question 6 onward

            # Prints assigned elements. Please comment print statement.
            #print('{0} , {1} , {2} , {3} , {4} , {5} '.format(sourceAddress,timeStr,requestMethod,requestFileName,responseCode, replySizeInBytes),end="")


            if replySizeInBytes != "-":
                replySizeInBytes = int(replySizeInBytes)
                self.dataBytes += replySizeInBytes

            self.ResponseResult = responseCode
            self.ResponseResult = self.checkResCode(self.ResponseResult)
            if self.ResponseResult == "Successful":
                self.successRate += 1
            elif self.ResponseResult == "Not Modified":
                self.notModRate += 1
            elif self.ResponseResult == "Found":
                self.foundRate += 1
            else:
                self.unSuccessRate += 1

            #Question 6 - Successful local & remote requests AND Question 7
            if sourceAddress == "local":
                if self.ResponseResult == "Successful":
                    self.sourceAddyLocal += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.localBytes += replySizeInBytes
                    
            elif sourceAddress == "remote":
                if self.ResponseResult == "Successful":
                    self.sourceAddyRemote += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.remoteBytes += replySizeInBytes
            else:
                print("Something is wrong.")

            #Question 8 - percentage of file categories
            self.FileExt = re.split('[. ?/]',requestFileName)
            if (self.FileExt[1] in self.fileTypeDict):
                if(self.ResponseResult == "Successful"):
                    self.extValue = self.fileTypeDict[self.FileExt[1]]
            elif (self.FileExt[1] not in self.fileTypeDict):
                if (self.ResponseResult == "Successful"):
                    self.extValue = "Others"

            if self.extValue == "HTML" and (self.ResponseResult == "Successful"):
                self.HTML += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.HTMLBytes += replySizeInBytes

            elif self.extValue == "Images" and (self.ResponseResult == "Successful"):
                self.Images += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.ImagesBytes += replySizeInBytes
                
            elif self.extValue == "Sound" and (self.ResponseResult == "Successful"):
                self.Sound += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.SoundBytes += replySizeInBytes
                    
            elif self.extValue == "Video" and (self.ResponseResult == "Successful"):
                self.Video += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.VideoBytes += replySizeInBytes
                    
            elif self.extValue == "Formatted" and (self.ResponseResult == "Successful"):
                self.Formatted += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.FormatBytes += replySizeInBytes
                    
            elif self.extValue == "Dynamic" and (self.ResponseResult == "Successful"):
                self.Dynamic += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.DynamicBytes += replySizeInBytes
                    
            elif self.extValue == "Others" and (self.ResponseResult == "Successful"):
                self.Others += 1
                if replySizeInBytes != "-":
                    replySizeInBytes = int(replySizeInBytes)
                    self.OthersBytes += replySizeInBytes
            
            # Assigns & prints format type. Please comment print statement.
            fileType = self.getFileType(requestFileName)
            #print(' , {0}'.format(fileType))

            # Q1: Write a condition to identify a start date and an end date.
            self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
            self.endDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")

            self.totalRequest += 1
            
        # Outside the for loop, generate statistics output

        print('total requests = ', self.totalRequest)
        print("total Bytes transfered = ", self.dataBytes)
        print("Response results = ", (self.successRate /724985) * 100, (self.notModRate /724985) * 100, (self.foundRate /724985) * 100, (self.unSuccessRate /724985) * 100)
        print("Local = " ,self.sourceAddyLocal, "Remote = " ,self.sourceAddyRemote)
        print('"""'*30)
        print("Local Bytes Transfered =", self.localBytes, "Remote Bytes Transfered =", self.remoteBytes)
        print('"""'*30)
        print("Number of HTML requests = ",self.HTML, "Number of Images requests = ", self.Images, "Number of Sound requests = ",self.Sound)
        print("Number of Video requests = ", self.Video, "Number of Formatted requests = ",
              self.Formatted, "Number of Dynamic requests = ", self.Dynamic, "Number of Others requests = ",self.Others)
        print('"""'*30)
        print("Success rate = ",self.successRate, "Not Mod rate = ", self.notModRate, "Found rate = ", self.foundRate, "Unsuccess rate =",self.unSuccessRate)
        print('"""'*10)
        print("HTML BYTES = ", self.HTMLBytes, "Image Bytes = ", self.ImagesBytes, "Sound Bytes = ",self.SoundBytes, "Video Bytes = ", self.VideoBytes,
              "Format Bytes = ", self.FormatBytes, "Dynamic Bytes = ", self.DynamicBytes, "Other Bytes = ", self.OthersBytes)

    def getFileType(self, URI):
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'):
            return 'HTML'
        filename = URI.split('/')[-1]
        if '?' in filename:
            return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        return 'Others'

    def checkResCode(self, code):
        if code == '200' : return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'   
        return None

if __name__ == '__main__':
    logfile = open('access_log', 'r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
    pass
