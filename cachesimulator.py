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
repl_policy_dict = {1:'random_replacement', 2:'least_recently_used', 3:'least_frequently_used'}
write_hit_policy_dict = {1:'write_through',2:'write_back'}
write_miss_policy_dict = {1:'write_allocate',2:'no_write_allocate'}

# initializing globals for user input
cache_size = 0
data_block_size = 0
associativity = 0 
replacement_policy = 0
write_hit_policy = 0
write_miss_policy = 0
number_of_cache_hits = 0
number_of_cache_misses = 0

#initializing calculated globals
number_of_sets = 0
max_memory_addresses = 0
num_address_bits = 0
num_block_offset_bits = 0
num_set_index_bits = 0
num_tag_bits = 0
num_valid_bits = 1
num_dirty_bits = 1
num_tag_hex_pairs = 1
cache_data = list()

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
    print("configure the cache:")
    global cache_size
    cache_size = int(input("Cache size: "))                                             #C
    while (cache_size < 8 or cache_size > 256):                                         # Making sure that the requested cache size is in the allowed range
        cache_size = int(input("Cache size must be between 8 and 256 bytes: "))
    global data_block_size
    data_block_size = int(input("data block size: "))                                   #B
    global associativity
    associativity = int(input("associativity: "))                                       #E
    global replacement_policy
    replacement_policy = int(input("replacement policy: "))    #use later
    global write_hit_policy
    write_hit_policy = int(input("write hit policy: "))        #use later
    global write_miss_policy
    write_miss_policy = int(input("write miss policy: "))      #use later

    # The following are calculated based on the above user inputs
    global number_of_sets
    number_of_sets = int(cache_size / (data_block_size * associativity))                #S
    global max_memory_addresses
    max_memory_addresses = len(ramdict)                                                 #M
    global num_address_bits
    num_address_bits = int(math.log(max_memory_addresses, 2))                           #m
    global num_block_offset_bits
    num_block_offset_bits = int(math.log(data_block_size, 2))                           #b
    global num_set_index_bits
    num_set_index_bits = int(math.log(number_of_sets, 2))                               #s
    global num_tag_bits
    num_tag_bits = num_address_bits - (num_block_offset_bits + num_set_index_bits)      #t
    print(range(1 + data_block_size))
    global cache_data
    cache_data = [
                    [
                        ['0' if x < 2 else '00' for x in range(num_valid_bits + num_dirty_bits + num_tag_hex_pairs + data_block_size)
                        ] for y in range(associativity)
                        ] for z in range(number_of_sets)
                        ] #fill cache with 00's
    print(cache_data)
    print("cache successfully configured!")                          
    print_cache_menu()
    user_cache_prompt = input()
    process_user_input(user_cache_prompt)    
    while(user_cache_prompt != "quit"):
        print_cache_menu()
        user_cache_prompt = input()
        process_user_input(user_cache_prompt)
    
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
        if(data == '0'):
            cache_hit = False
        is_hit = "No"
        if(cache_hit):
            is_hit = "Yes"
            global number_of_cache_hits
            number_of_cache_hits += 1
            eviction_line = '-1'
        else:
            data = ramdict[decimal_search_address]
            global number_of_cache_misses
            number_of_cache_misses += 1
            eviction_line = '-1'
        print("hit:" + is_hit)
        print("eviction_line:" + eviction_line)
        print("ram_address:" + "0x" + search_address)
        print("data:" + "0x" + data)
    elif(user_cache_prompt == "cache-write"):
        print("1")
    elif(user_cache_prompt == "cache-flush"):
        print(range(num_valid_bits + num_tag_bits + data_block_size))
        for x in range(number_of_sets):
            for y in range(associativity):
                for z in range(num_valid_bits + num_tag_bits + data_block_size):
                    cache_data[x][y][z] = '00'
        print("cache_cleared")

    elif(user_cache_prompt == "cache-view"):
        print("cache_size:" + str(cache_size))
        print("data_block_size:" + str(data_block_size))
        print("associativity:" + str(associativity))
        print("replacement_policy:" + str(repl_policy_dict[replacement_policy]))
        print("write_hit_policy:" + str(write_hit_policy_dict[write_hit_policy]))
        print("write_miss_policy:" + str(write_miss_policy_dict[write_miss_policy]))
        print("number_of_cache_hits:" + str(number_of_cache_hits))
        print("number_of_cache_misses:" + str(number_of_cache_misses))
        print("cache_content:")
        for x in range(number_of_sets):
            for y in range(associativity):
                print(cache_data[x][y][0] + " ", end="") # valid bit
                print(cache_data[x][y][1] + " ", end="") # dirty bit
                print(cache_data[x][y][2] + " ", end="") # tag in hex
                for z in range(num_valid_bits + num_dirty_bits + num_tag_hex_pairs, num_valid_bits + num_dirty_bits + num_tag_hex_pairs + data_block_size):
                    print(cache_data[x][y][z] + " ", end="") # data block
                print()  
          
    elif(user_cache_prompt == "memory-view"): #print all the memory in ramdict in lines of 8
        memory_size = len(ramdict)
        print("memory_size:" + str(memory_size)) #formatting
        print("memory_content:")            
        print("address:data")
        for i in range(0, memory_size, 8):    #traverse the memory 8 blocks of data at a time
            hex_address = hex(i)
            print(hex_address + ":", end="")          #print the address for the line of memory every 8 blocks (in hexadecimal)
            for j in range(0, 8):
                print(ramdict[i+j].strip(), end=" ")#print the memory in nested loop up to 7, so all memory is printed (i + j where j = 8 would just be the next sequence of i)
            print()                          
    
    elif(user_cache_prompt == "cache-dump"):
        cache_file = open("cache.txt", 'w')    #open cache_file
        for x in range(number_of_sets):
            for y in range(associativity):     #for the last loop we only want to write the physical data into cache_file
                for z in range(num_valid_bits + num_dirty_bits + num_tag_hex_pairs, num_valid_bits + num_dirty_bits + num_tag_hex_pairs + data_block_size):
                    cache_file.write(cache_data[x][y][z] + " ")
                cache_file.write("\n")    
        cache_file.close()                     #close cache_file
    
    elif(user_cache_prompt == "memory_dump"):
        ram_file = open("ram.txt", 'w')         #open ram_file
        for i in range(len(ramdict)):           #iterate through memory dictionary
            ram_file.write(ramdict[i] + "\n")   #write each memory line to ram.txt with a newline
        ram_file.close()                        #close ram_file
    
    elif(user_cache_prompt == "quit"):
        print()                           #do nothing
    else:
        print("-1")                       #Error, invalid input

if __name__ == "__main__":
    main()
