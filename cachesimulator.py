#File: Cachesimulator.py
#Author(s): Armando Cruz, Gage Broberg
#Date: 11/23/2021
#Section: 506
#Email(s): armando.cruz22@tamu.edu , gagebroberg@tamu.edu
#Description: In this lab, we wrote a program which simulates a cache memory. It consists of taking an input file for memory,
#and prompting the user for inputs. We then use the inputs for updating, deleting, and printing cache memory.

import numpy
import math
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
    data_file.close() #close the file

    print("init-ram 0x00 " + "0x%X" % memaddress) #print the size of ram memory
    print("RAM succesfully initialized!") #print once all data in file has been added to memory dictionary
    ##########################################################################################

    #Configure the cache
    ##########################################################################################
    print("configure the cache:" + "\n")
    cache_size = int(input("Cache size: "))                                             #C
    while (cache_size < 8 or cache_size > 256):                                         # Making sure that the requested cache size is in the allowed range
        cache_size = int(input("Cache size must be between 8 and 256 bytes: "))
    data_block_size = int(input("data block size: "))                                   #B
    associativity = int(input("associativity: "))                                       #E
    #implement inputs, create cache memory (use matrix? array? dictionary?)
    number_of_sets = int(cache_size / (data_block_size * associativity))                #S
    max_memory_addresses = len(ramdict)                                                 #M
    num_address_bits = int(math.log(max_memory_addresses, 2))                                #m
    num_block_offset_bits = int(math.log(data_block_size, 2))                                #b
    num_set_index_bits = int(math.log(number_of_sets, 2))                                    #s
    num_tag_bits = num_address_bits - (num_block_offset_bits + num_set_index_bits) #t
    num_valid_bits = 1
    replacement_policy = int(input("replacement policy: "))    #use later
    write_hit_policy = int(input("write hit policy: "))        #use later
    write_miss_policy = int(input("write miss policy: "))      #use later
    cache_data = [[['-1' for col in range(num_valid_bits + num_tag_bits + data_block_size)] for col in range(associativity)] for col in range(number_of_sets)] #fill cache with -1's
    print(cache_data) ################# REMOVE LATER (test that dimensions are correct)
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
        if("cache-read" in user_cache_prompt): # user must enter this command in the form "cache-read 0x___"
            search_address = user_cache_prompt.split()[1].split("x")[1] #grabbing hexadecimal value from search address
            decimal_search_address = int(search_address, 16)
            binary_search_address = bin(decimal_search_address)
            binary_search_address = binary_search_address[2:]
            bs_address_string = str(binary_search_address)
            stringlength = len(bs_address_string)
            stringlength = 8 - stringlength
            for _ in range(0, stringlength): # making sure that the bin search address is at least 8 bits; must start at index 0; convention is to use _ if unused index
                bs_address_string = "0" + bs_address_string
            binary_tag = bs_address_string[:num_tag_bits] # tag bits defined previously
            binary_set = bs_address_string[num_tag_bits:num_tag_bits + num_set_index_bits] # from end of tag bits to end of set bits
            binary_offset = bs_address_string[num_tag_bits + num_set_index_bits:] # from the end of set bets to the end of the address
            d_tag = int(binary_tag, 2)
            d_set = int(binary_set, 2)
            d_offset = int(binary_offset, 2)
            print("set:" + str(d_set))
            print("tag:" + str(d_tag))
            cache_hit = False
            data = -1 #initializing the search address
            for data_line in cache_data[d_set]:
                tag_bits = data_line[1:num_tag_bits+1]
                if (tag_bits == binary_tag):  #check that the tag bits in data_line match
                    cache_hit == True
                if (data_line[0] != 1): #check the valid bit is true
                    cache_hit == False
                if(cache_hit):
                    data = data_line[num_tag_bits + 1 + d_offset]
            if(data == -1):
                cache_hit = False
            is_hit = "No"
            if(cache_hit):
                is_hit = "Yes"
            else:
                data = ramdict[decimal_search_address]
            print("hit:" + is_hit)
            print("ram_address:" + search_address)
            print("data:" + data)
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

if __name__ == "__main__":
    main()
