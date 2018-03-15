#!/usr/bin/python

# global reqs
from sepy.LowLevelKP import *
import configparser
import urllib
import json

# settings
CONFIG_FILE = "repoSettings.conf"
JAMENDO_TRACKS = "http://api.jamendo.com/v3.0/tracks?client_id="
SEPA_UPDATE_URI = "http://localhost:8000/update"
QMUL = "http://eecs.qmul.ac.uk/wot#"
DC = "http://purl.org/dc/elements/1.1/"
AC = "http://audiocommons.org/ns/audiocommons#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

# main
if __name__ == "__main__":

    # statements
    prefixes = []
    statements = []

    # initialize statements with prefixes
    prefixes.append("PREFIX qmul: <%s> " % QMUL)
    prefixes.append("PREFIX dc: <%s> " % DC)
    prefixes.append("PREFIX ac: <%s> " % AC)
    prefixes.append("PREFIX rdf: <%s> " % RDF)

    # then, put insert data
    
    # create a KP
    kp = LowLevelKP()

    # read config file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    jamendoClientId = config["Jamendo"]["clientId"]
    
    # query Jamendo API
    r = requests.get(JAMENDO_TRACKS + jamendoClientId)
    reply = json.loads(r.text)

    # cycle over results
    for result in reply["results"]:

        # generate triples
        statements.append(" <%s> rdf:type ac:AudioClip . " % result["shorturl"])
        statements.append(" <%s> dc:title '%s' . " % (result["shorturl"], urllib.parse.quote(result["name"])))
        statements.append(" <%s> ac:available_as <%s> . " % (result["shorturl"], result["audiodownload"]))
        statements.append(" <%s> rdf:type ac:AudioFile . " % result["audiodownload"])

    # build the update to insert data
    upd = ' '.join(prefixes) + " INSERT DATA { " + ' '.join(statements) + " }"
    print(upd)
    kp.update(SEPA_UPDATE_URI, upd)

    # wait until the end, then delete data
    input("Press <ENTER> to quit")

    # build the update to delete data
    upd = ' '.join(prefixes) + " DELETE DATA { " + ' '.join(statements) + " }"
    kp.update(SEPA_UPDATE_URI, upd)
    
    # exit
    print("Bye!")
