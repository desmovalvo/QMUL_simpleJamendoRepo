#!/usr/bin/python

# global reqs
from sepy.LowLevelKP import *
import eyed3
import os

# settings
LOCAL_PATH = "audio/"
ABSOLUTE_PATH = os.getcwd() + LOCAL_PATH
SEPA_UPDATE_URI = "http://localhost:8000/update"
NS = "http://ns#"
QMUL = "http://eecs.qmul.ac.uk/wot#"
DC = "http://purl.org/dc/elements/1.1/"
AC = "http://audiocommons.org/ns/audiocommons#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
PREFIXES = """PREFIX ns: <%s> 
PREFIX ac: <%s>
PREFIX dc: <%s>
PREFIX qmul: <%s> 
PREFIX rdf: <%s>
""" % (NS, AC, DC, QMUL, RDF)

# templates
SONG_TITLE = " %s dc:title %s . "

# main
if __name__ == "__main__":

    # create a KP
    kp = LowLevelKP()
    
    # cycle over mp3 files in folder
    for f in os.listdir(LOCAL_PATH):
        if f.endswith('.mp3'):

            # initialise a SPARQL update
            upd = PREFIXES + "INSERT DATA { "

            # generate an URI
            songUriClip = NS + f + "_clip"
            songUriFile = NS + f + "_file"
            print("Generated URI for AudioClip: " + songUriClip)
            print("Generated URI for AudioFile: " + songUriFile)
                        
            # load id3 tags
            id3tags = eyed3.load(LOCAL_PATH + f)
            
            # publish every file
            upd += " <%s> rdf:type ac:AudioClip . " % (songUriClip)
            upd += " <%s> dc:title '%s' . " % (songUriClip, id3tags.tag.title)
            upd += " <%s> ac:available_as <%s> . " % (songUriClip, songUriFile)
            upd += " <%s> rdf:type ac:AudioFile . " % (songUriFile)
            upd += " <%s> ns:hasLocation '%s' " % (songUriFile, ABSOLUTE_PATH + f)
            upd += "}"

            # do the update
            kp.update(SEPA_UPDATE_URI, upd)

    # wait until the end, then delete data
    input("Press <ENTER> to quit")

    # cycle over mp3 files in folder
    for f in os.listdir(LOCAL_PATH):
        if f.endswith('.mp3'):

            # initialise a SPARQL update
            upd = PREFIXES + "DELETE DATA { "

            # generate an URI
            songUriClip = NS + f + "_clip"
            songUriFile = NS + f + "_file"
            print("Deleting AudioClip: " + songUriClip)
                        
            # load id3 tags
            id3tags = eyed3.load(LOCAL_PATH + f)
            
            # publish every file
            upd += " <%s> rdf:type ac:AudioClip . " % (songUriClip)
            upd += " <%s> dc:title '%s' . " % (songUriClip, id3tags.tag.title)
            upd += " <%s> ac:available_as <%s> . " % (songUriClip, songUriFile)
            upd += " <%s> rdf:type ac:AudioFile . " % (songUriFile)
            upd += " <%s> ns:hasLocation '%s' " % (songUriFile, ABSOLUTE_PATH + f)
            upd += "}"

            # do the update
            kp.update(SEPA_UPDATE_URI, upd)
    
    print("Bye!")
