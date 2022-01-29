import constants

def parseOutput(attributes):
    for attribute in constants.TO_DELETE:
        del attributes[attribute] 
    return attributes