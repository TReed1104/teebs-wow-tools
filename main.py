## Imports
from argparse import ArgumentParser
from InterfaceSync import InterfaceSync
from AssignmentGenerator import AssignmentGenerator

## App Main
def main():
    ## Setup the command-line arguments
    argParser = ArgumentParser(description="A combined app for all my WoW classic scripts")
    argParser.add_argument("app", choices=[ "angry-assignments", "addons" ], help="Which app are we using")
    argParser.add_argument("-i", "--input", dest="config", help="The config file to use", type=str, default="configs/config.json")
    argParser.add_argument("-m", "--mode", dest="mode", choices=[ "pull", "Pull", "push", "Push" ], help="The sync mode, push or pull", type=str, default="pull")
    argParser.add_argument("-t", "--target", dest="target", choices=[ "UI", "ui", "Addons", "addons", "All", "all" ], help="The folder to sync", type=str, default="UI")
    args = argParser.parse_args()

    ## Execute the Angry assignment App
    if (args.app == "angry-assignments"):
        ## Create the app and run
        print("> Generating AngryAssignments")
        app = AssignmentGenerator(args.config)
        app.run()

    ## Execute the WoW UI Syncer
    if (args.app == "addons"):
        ## Create the app and run
        print("> Syncing WoW Folders")
        app = InterfaceSync(args.config, args.mode, args.target)
        app.run()

## Main thread check
if __name__ == '__main__':
    main()
