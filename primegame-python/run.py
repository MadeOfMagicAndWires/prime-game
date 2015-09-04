#!/usr/bin/env python

from primegame import primegame
from bla import clear
import os
import pickle

#open and print the logo
#with open('/home/joost/GFox/Project Python/primegame/logo.txt', 'r') as logo:
#    for line in logo:
#        print line

highscore_file = '/home/joost/.primegame/highscore'

def print_highscore():
    try:
        with open(highscore_file, 'r+') as highscore:
            highscore_size = os.path.getsize(highscore_file)
            if highscore_size <= 0:
                highscore_dict = {3000: 'Sheppard',\
                9000: 'McKay',\
                6000: 'Zelenka',\
                10000: 'Carter',\
                0: 'Ford'}
                highscore_list = highscore_dict.keys()
                highscore_list.sort(reverse=True)
                print "\nHIGHSCORE:\n"                
                for score in highscore_list:
                    if score <= 9000:
                        print '{0:10}: {1:10}'.format\
                        (highscore_dict[score], score)
                    elif score > 9000:
                        print '{0:10}: {1:10}\t*OVER 9000*'.format\
                        (highscore_dict[score], score)
                    pickle.dump(highscore_dict, highscore)
                highscore.close()

                    #print highscore_size
                    
            elif highscore_size > 0:
                highscore_dict = pickle.load(highscore)
                highscore_list = highscore_dict.keys()
                highscore_list.sort(reverse=True)
                print "\nHIGHSCORE:"
                for score in highscore_list:
                    if score <= 9000:
                        print '{0:10}: {1:10}'.format\
                        (highscore_dict[score], score)
                    elif score > 9000:
                        print '{0:10}: {1:10}\t*OVER 9000*'.format\
                        (highscore_dict[score], score)
                #print highscore_size
                highscore.close()
        print '\n'

    except IOError:
        print "404 Error"

running = True
clear.clear()

def run():
    print "Welcome to the Primegame."
    while running == True:
        prompt = str(raw_input(">"))
        if prompt not in ('highscore', 'high', 'p', 'play', 'run', 'q', 'quit', 'c'\
        , 'clear', 'h', 'help'):
            print "Command not found\n"
            continue
        if prompt in ('highscore', 'high'):
            if os.path.isfile(highscore_file) == True:
                print_highscore()
            elif os.path.isfile(highscore_file) == False:
                newfile = open(highscore_file, 'w')
                newfile.close()
                if newfile.closed == True:
                    print_highscore()
        if prompt in ('p', 'play', 'run'):
            your_score = primegame.play()
            if os.path.isfile(highscore_file) == True:
                with open(highscore_file, 'r+') as highscore:
                    highscore_dict = pickle.load(highscore)
                    highscore_list = highscore_dict.keys()
		    highscore_list.sort(reverse=True)
		    for score in highscore_list:
                        if your_score >= score:
                            print "new highscore!"
                            name = str(raw_input('please enter your name: '))
                            highscore_dict[your_score] = name
                            del highscore_dict[highscore_list[-1]]
                            #print highscore_dict
                            break
			elif your_score <= score:
			    continue
		with open(highscore_file, 'w') as highscore:
                    pickle.dump(highscore_dict, highscore)
                    highscore.close
                    clear.clear()
            print "Goodbye"
            print_highscore()


        if prompt in ('q','quit'):
	    exit()
        if prompt in ('c', 'clear'):
	    clear.clear()
	    print "Welcome to the Primegame."
	    continue
        if prompt in ('h', 'help'):
	    print "What's the matter, need a little help?\n\nTry 'play'."
                

#print_highscore()


if __name__ == "__main__":
    import sys
    run()
