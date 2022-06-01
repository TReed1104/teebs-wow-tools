## Imports
import shutil
import json

## Interface Sync Class
class InterfaceSync:
    def __init__(self, config, mode, target):
        ## Load the config json
        configFile = open(config)
        self.configData = json.load(configFile)
        self.configData = self.configData["ui-sync-config"]
        configFile.close()

        ## Set the class variables
        self.target = target
        self.mode = mode

        ## Copy the config data to the object
        self.accountName = self.configData["account_name"]
        self.installPathWarcraft = self.configData["wow_install_path"]
        self.installPathGoogleDrive = self.configData["google_drive_path"]
        self.directoryUI = self.configData["ui_directory"]
        self.directoryAddons = self.configData["addons_directory"]
        

    ## Pull the target folder
    def __pullFolder(self):
        if self.target.upper() == "ALL":
            ## UI sync
            sourcePath = f"{self.installPathGoogleDrive}{self.accountName}.zip"
            targetPath = f"{self.installPathWarcraft}{self.directoryUI}{self.accountName}"
            print(">> Pull:", sourcePath, "-->", targetPath)
            shutil.unpack_archive(sourcePath, extract_dir=targetPath)
            ## Addon sync
            sourcePath = f"{self.installPathGoogleDrive}Addons.zip"
            targetPath = f"{self.installPathWarcraft}{self.directoryAddons}Addons"
            print(">> Pull:", sourcePath, "-->", targetPath)
            shutil.unpack_archive(sourcePath, extract_dir=targetPath)

            ## Done
            return

        ## User selected the UI to sync
        if self.target.upper() == "UI":
            sourcePath = f"{self.installPathGoogleDrive}{self.accountName}.zip"
            targetPath = f"{self.installPathWarcraft}{self.directoryUI}{self.accountName}"
        ## User selected the Addons folder to sync
        elif self.target.upper() == "ADDONS":
            sourcePath = f"{self.installPathGoogleDrive}Addons.zip"
            targetPath = f"{self.installPathWarcraft}{self.directoryAddons}Addons"
        else:
            ## Target is unrecognised
            print(">>> ERROR: Unknown target for Pull request:", self.target)
            return

        ## Console output
        print(">> Pull:", sourcePath, "-->", targetPath)

        ## Unzip the folder from Google drive to the target destination
        shutil.unpack_archive(sourcePath, extract_dir=targetPath)


    ## Push the target folder
    def __pushFolder(self):
        if self.target.upper() == "ALL":
            ## UI sync
            sourcePath = f"{self.installPathWarcraft}{self.directoryUI}{self.accountName}"
            targetPath = f"{self.installPathGoogleDrive}"
            zipOutputName = f"{self.accountName}.zip"
            print(">> Push:", sourcePath, "-->", targetPath)
            createdZip = shutil.make_archive(sourcePath, "zip", sourcePath)
            shutil.move(createdZip, targetPath + zipOutputName)

            ## Addon sync
            sourcePath = f"{self.installPathWarcraft}{self.directoryAddons}Addons"
            targetPath = f"{self.installPathGoogleDrive}"
            zipOutputName = f"Addons.zip"
            print(">> Push:", sourcePath, "-->", targetPath)
            createdZip = shutil.make_archive(sourcePath, "zip", sourcePath)
            shutil.move(createdZip, targetPath + zipOutputName)

            ## Done
            return

        ## User selected the UI to sync
        if self.target.upper() == "UI":
            sourcePath = f"{self.installPathWarcraft}{self.directoryUI}{self.accountName}"
            targetPath = f"{self.installPathGoogleDrive}"
            zipOutputName = f"{self.accountName}.zip"
        ## User selected the Addons folder to sync
        elif self.target.upper() == "ADDONS":
            sourcePath = f"{self.installPathWarcraft}{self.directoryAddons}Addons"
            targetPath = f"{self.installPathGoogleDrive}"
            zipOutputName = f"Addons.zip"
        else:
            ## Target is unrecognised
            print(">>> ERROR: Unknown target for Push request:", self.target)
            return

        ## Console output
        print(">> Push:", sourcePath, "-->", targetPath)

        ## Zip the local folder and push it to Google drive
        createdZip = shutil.make_archive(sourcePath, "zip", sourcePath)
        ## make_archive creates the zip in the same directory, so copy the output zip to the target location
        shutil.move(createdZip, targetPath + zipOutputName)


    ## Execution of the App
    def run(self):
        ## Check the Sync mode - Pull/Push
        if self.mode.upper() == "PULL":
            ## Update the local files
            self.__pullFolder()
        elif self.mode.upper() == "PUSH":
            ## Update the Google drive files
            self.__pushFolder()
