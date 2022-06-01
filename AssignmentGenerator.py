## Imports
import os
import json

## Interface Sync Class
class AssignmentGenerator:
    def __init__(self, configFile):
        ## Setup the file directories
        self.inputDirectory = "templates/"
        self.outputDirectory = "bin/"

        ## Load the config json 
        configFile = open(configFile)
        self.configData = json.load(configFile)
        self.configData = self.configData["angry-asignments-config"]
        configFile.close()


    ## Read the file
    def __readFileToString(self, fileName):
        parsedFile = ""
        try:
            ## Open the file, read the contents into a string keeping formatting
            fileContent = open(fileName, "r")
            for line in fileContent:
                parsedFile += line
            fileContent.close()
            return parsedFile

        ## Error Handling
        except (OSError, IOError) as error:
            print(">>> ERROR! - An error occured:", error)
            ## Returns a blank string to prevent execution halt
            return parsedFile


    ## Write the output AAs to file
    def __writeStringToFile(self, fileName, stringToWrite):
        try:
            ## Create a new file, write the string to the file and save it
            outputFile = open(fileName, "w")
            outputFile.write(stringToWrite)
            outputFile.close()

        ## Error Handling
        except (OSError, IOError) as error:
            print(">>> ERROR! - An error occured:", error)


    ## Input the raid member names
    def __parseTemplateFile(self, fileName):
        ## Program flow print - more for debugging than anything
        print(">> Parsing Template:", fileName)

        ## Read in the AA file
        fileData = self.__readFileToString(self.inputDirectory + fileName)

        ## Find and replace assignment tokens e.g. <tank_0>
        for assignmentTag in self.configData["assignments"]:
            ## Replace the placeholder with the raider name, formatted with their class colour
            fileData = fileData.replace(f"<{assignmentTag}>", self.__colourNameByRosterClass(assignmentTag))
        
        ## Find and replace the additional tag tokens e.g. <heroism_alar>
        for additionalTag in self.configData["additional_tags"]:
            ## Replace the placeholder with the additional tag condition
            fileData = fileData.replace(f"<{additionalTag}>", self.__colourAdditionalTagText(additionalTag))

        ## Save the parsed AA to an output file
        self.__writeStringToFile(self.outputDirectory + fileName, fileData)


    ## Get the raider information to replace the placeholder token with
    def __colourNameByRosterClass(self, placeholder):
        ## Get the raider details from the config file
        raiderName = self.configData["assignments"][placeholder]

        ## Check the placeholder has a value to set
        if raiderName == "":
            return "|cRed!!!Not Set!!!|r"

        ## Get the raider's class
        raiderClass = self.configData["roster"][raiderName]

        ## Format the raider name with their class colour in the format WoW uses for colouring text |c<Colour><Text>|r
        formattedRaiderName = f"|c{raiderClass}{raiderName}|r"
        return formattedRaiderName


    ## Format the additional tag content strings for replacing in the text
    def __colourAdditionalTagText(self, placeholder, colour = "Red"):
        ## Get the tag text
        tagText = self.configData["additional_tags"][placeholder]

        ## Check the placeholder has a value to set
        if tagText == "":
            return ""

        ## Format the additional tag by the passed colour param |c<Colour><Text>|r
        formattedTagText = f"|c{colour}{tagText}|r"
        return formattedTagText


    def run(self):
        ## Entry point output, just for context in the command-line
        print("> Generating AngryAssignments")

        ## Create the output directory
        try:
            print(">> Creating the output directory")
            os.makedirs(self.outputDirectory)
        except FileExistsError:
            pass

        ## Iterate through the templates found in the specified directory
        for fileToParse in os.listdir(self.inputDirectory):
            ## Parse the files and replace the values with the assigned raiders
            self.__parseTemplateFile(fileToParse)