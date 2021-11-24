#File: Cachesimulator.py
#Author(s): Armando Cruz, Gage Broberg
#Date: 11/23/2021
#Section: 506
#Email(s): armando.cruz22@tamu.edu , gagebroberg@tamu.edu
#Description: In this lab, we wrote a program which simulates a cache memory. It consists of taking an input file for memory,
#and prompting the user for inputs. We then use the inputs for updating, deleting, and printing cache memory.

import numpy
import sys

#dictionaries
ramdict = {} #ram memory dictionary

def main():
    #Initialize Physical memory
    ###########################################################################################
    print("*** Welcome to the cache simulator ***")
    print("initialize the RAM:")
    #open the data file
    path = sys.argv[1] #take input from command line
    data_file = open(path, 'r') #open file
    moredata = True
    memaddress = -1 #memaddress is the address used to access memory from dictionary

    #Iterate through data file
    while(moredata):
        memoryline = data_file.readline() #read in memory line by line
        if not memoryline: #if read unsuccesful, file is at the end, break
            moredata = False
            break
        memaddress += 1 #increment memory address, such that each index is unique
        ramdict[memaddress] = memoryline #store memoryline at memaddress

    print("init-ram 0x00 " + "0x%X" % memaddress) #print the size of ram memory
    print("RAM succesfully initialized!") #print once all data in file has been added to memory dictionary
    ##########################################################################################

    #Configure the cache
    ##########################################################################################
    print("configure the cache:" + "\n")
    cache_size = input("Cache size: ")
    data_block_size = input("data block size: ")
    associativity = input("associativity: ")
    replacement_policy = input("replacement policy: ")
    write_hit_policy = input("write hit policy: ")
    write_miss_policy = input("write miss policy: ")
    #implement inputs, create cache memory (use matrix? array? dictionary?)
    print("cache successfully configured!")
    ##########################################################################################

    #Simulate the cache
    ##########################################################################################
    #print menu
    def print_cache_menu():
        print("*** Cache simulator menu ***")
        print("type one command:")
        print("1. cache-read")
        print("2. cache-write")
        print("3. cache-flush")
        print("4. cache-view")
        print("5. memory-view")
        print("6. cache-dump")
        print("7. memory-dump")
        print("8. quit")
        print("****************************")
    print_cache_menu()

    def process_user_input(user_cache_prompt): #handle each case
        if(user_cache_prompt == "cache-read"):
            print("read")
        elif(user_cache_prompt == "cache-write"):
            print("1")
        elif(user_cache_prompt == "cache-flush"):
            print("2")
        elif(user_cache_prompt == "cache-view"):
            print("3")
        elif(user_cache_prompt == "memory-view"):
            print("4")
        elif(user_cache_prompt == "cache_dump"):
            print("5")
        elif(user_cache_prompt == "memory_dump"):
            print("6")
        elif(user_cache_prompt == "quit"):
            print("0")
        else:
            print("-1")
    
    user_cache_prompt = input()
    process_user_input(user_cache_prompt)
    while(user_cache_prompt != "quit"):
        print_cache_menu()
        user_cache_prompt = input()
        process_user_input(user_cache_prompt)
    ##########################################################################################

main()