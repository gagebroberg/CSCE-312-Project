#File: Cachesimulator.py
#Author(s): Armando Cruz, Gage Broberg
#Date: 11/23/2021
#Section: 506
#Email(s): armando.cruz22@tamu.edu , gagebroberg@tamu.edu
#Description: In this lab, we wrote a program which simulates a cache memory. It consists of taking an input file for memory,
#and prompting the user for inputs. We then use the inputs for updating, deleting, and printing cache memory.

import math
import random
import sys

# Dictionaries
###########################################################################################
## The ram dictionary stores the ram data with line numbers being keys
# and the hex values at those line numbers as values.
ramdict = {}
## This is the replacement policy dictionary that stores the options for replacement. 
# This allows for easy conversion from the number entered by the user to the string
# representation of the replacement policy.
repl_policy_dict = {1:'random_replacement', 2:'least_recently_used', 3:'least_frequently_used'}
## This is the write hit policy dictionary that stores the options for how to handle write hits.
# This allows for easy conversion from the number entered by the user to the string
# representation of the write hit policy.
write_hit_policy_dict = {1:'write_through',2:'write_back'}
## This is the write miss policy dictionary that stores the options for how to handle write misses.
# This allows for easy conversion from the number entered by the user to the string
# representation of the write miss policy.
write_miss_policy_dict = {1:'write_allocate',2:'no_write_allocate'}
###########################################################################################

# Initializing globals for user input
###########################################################################################
## The size of the cache in bytes. This is configured by the user at runtime.
cache_size = 0
## The size of a block of data. This is configured by the user at runtime.
data_block_size = 0
## The number of lines in a set. This is configured by the user at runtime.
associativity = 0 
## The replacement policy. The user can enter 1, 2, or 3 which correspond to different replacement policies
# These policies are held in the repl_policy_dict.
replacement_policy = 0
## The write hit policy policy. The user can enter 1 or 2 which correspond to different write hit policies
# These policies are held in the write_hit_policy_dict.
write_hit_policy = 0
## The write miss policy policy. The user can enter 1 or 2 which correspond to different write miss policies
# These policies are held in the write_miss_policy_dict.
write_miss_policy = 0
###########################################################################################

# Initializing calculated globals
###########################################################################################
## The number of sets in cache. This is calculated using user input. Specifically, this is
# cache_size / (data_block_size * associativity)
number_of_sets = 0
## The number of memory addresses in ram. This is calculated using the number of lines in the 
# ram input file. For this project that file is input.txt.
max_memory_addresses = 0
## The number of address bits. This is calculated as the log base 2 of max_memory_addresses.
num_address_bits = 0
## The number of tag bits. This is calculated using the formula t = m - (b + s). For this
# project this is num_address_bits = max_memory_addresses - (num_block_offset_bits + num_set_index_bits).
num_tag_bits = 0
## The number of set index bits. This is calculated as the log base 2 of number_of_sets.
num_set_index_bits = 0
## The number of block offset bits. This is calculated as the log base 2 of data_block_size.
num_block_offset_bits = 0
## The number of times we have had a cache hit during runtime. Every time the user makes a read or write
# that results in a cache hit, this number if incremented.
number_of_cache_hits = 0
## The number of times we have had a cache miss during runtime. Every time the user makes a read or write
# that results in a cache miss, this number if incremented.
number_of_cache_misses = 0
## This is a triple nested list that represents our cache data. The first layer is the entire cache, the second
# layer is the sets, and the third layer is each line within each set in the following format:
# ['valid bit', 'dirty bit', 'tag hex bits', 'start of data block', ..., 'end of data block']
cache_data = list(list(list()))
## This is the recently used list that helps calculate which of the lines in cache
# was least recently used should the user enter '2' for the replacement policy.
recently_used = list()
## This is the frequently used triple nested list that helps calculate which of the lines in cache
# was least frequently used should the user enter '3' for the replacement policy.
frequently_used = list(list(list()))
###########################################################################################

# Static global variabels
###########################################################################################
## The number of valid bits. This is always 1. This variable helps with code readability and clarity. 
num_valid_bits = 1
## The number of dirty bits. This is always 1. This variable helps with code readability and clarity. 
num_dirty_bits = 1
## The number of hex pairs to represent a tag in cache. This is always 1. 
# This variable helps with code readability and clarity. 
num_tag_hex_pairs = 1
###########################################################################################

## This is the main function that runs the entire program.  
# It takes a command line argument to obtain the file path to the 
# ram input data. This input data is then used to configure the ram.
# Then user input is used to configure the cache. The user can then 
# request different actions to be performed on the cache.
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
    ###########################################################################################

    #Iterate through data file
    ###########################################################################################
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
    global cache_data
    cache_data = [
                    [
                        ['0' if x < 2 else '00' for x in range(num_valid_bits + num_dirty_bits + num_tag_hex_pairs + data_block_size)
                        ] for y in range(associativity)
                    ] for z in range(number_of_sets)
                ] #fill cache with 00's
    print(cache_data)
    global recently_used
    recently_used = [x for x in range(number_of_sets * associativity)]
    print(recently_used)
    global frequently_used
    frequently_used = [
                        [
                            [ 0       
                            ] for y in range(associativity)
                        ] for z in range(number_of_sets)
                    ] # fill the recently used with 0's
    print(frequently_used)
    
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

## Prints the menu of options that the user is allowed to choose from.
def print_cache_menu():
    print("*** Cache simulator menu ***")
    print("type one command:")
    print("1. cache-read")
    print("2. cache-write")
    print("3. cache-flush")
    print("4. cache-view")#boop bop
    print("5. memory-view")
    print("6. cache-dump")
    print("7. memory-dump")
    print("8. quit")
    print("****************************")
###########################################################################################

## Processes the user input based on the menu option selected.
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
        h_tag = hex(d_tag).split('x')[1]
        d_set = int(binary_set, 2)
        d_offset = int(binary_offset, 2)
        print("set:" + str(d_set))
        print("tag:" + h_tag)
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
                break               #iterative, the next iteration in the loop could suggest that the cache_hit is false, even though it's true
        if(data == '0'):
            cache_hit = False
        is_hit = "No"
        if(cache_hit):
            is_hit = "Yes"
            global number_of_cache_hits
            number_of_cache_hits += 1
            eviction_line = '-1'
        else:
            data = ramdict[decimal_search_address].strip()
            global number_of_cache_misses
            number_of_cache_misses += 1
            eviction_line = '-1'
        print("hit:" + is_hit)
        # If we get a miss, then we need to replace a line in cache using the replacement policy specified
        if (not cache_hit): # cache miss
            # random replacement
            if (replacement_policy == 1):
                print("RR") # Denotes random replacement; remove later
                randset = random.randrange(0, number_of_sets) # set to replace from
                randline = random.randrange(0, associativity) # line in the set to replace from
                eviction_line = int(str(randset) + str(randline), 2) # overall line to replace from
                cache_data[randset][randline][0] = '1' # set the valid bit to 1
                # next four lines make sure that the tag has two hexadecimal digits
                tag_hex = hex(d_tag).split("x")[1]
                while len(tag_hex) != 2:
                    tag_hex = '0' + tag_hex
                cache_data[randset][randline][2] = tag_hex # set the tag to the search address tag
                ram_block = get_ram_block(decimal_search_address, data_block_size)
                counter = 3
                for byte in ram_block:
                    cache_data[randset][randline][counter] = byte
                    counter += 1

            # least recently used
            elif (replacement_policy == 2):
                print("LRU")    
                # Now that we have the line, we can use it to alter the data in line
                global recently_used
                eviction_line = recently_used[0] # overall line to replace from
                bin_rec_used = bin(recently_used[0]).split('b')[1]
                while len(bin_rec_used) != 2:
                    bin_rec_used = '0' + bin_rec_used
                least_rec_set = int(bin_rec_used[0])
                least_rec_line = int(bin_rec_used[1])
                cache_data[least_rec_set][least_rec_line][0] = '1' # set the valid bit to 1
                recently_used = rotate(recently_used) # move the least recently used line to the next smallest line number
                # next four lines make sure that the tag has two hexadecimal digits
                tag_hex = hex(d_tag).split("x")[1]
                while len(tag_hex) != 2:
                    tag_hex = '0' + tag_hex
                cache_data[least_rec_set][least_rec_line][2] = tag_hex # set the tag to the search address tag
                ram_block = get_ram_block(decimal_search_address, data_block_size)
                counter = 3
                for byte in ram_block:
                    cache_data[least_rec_set][least_rec_line][counter] = byte
                    counter += 1
                
            # least frequently used
            else:
                print("LFU")
                # logic to calculate least frequently used line
                least_freq_set = 0
                least_freq_line = 0
                min_frequency = frequently_used[0][0][0]
                for set_count, set in enumerate(frequently_used):
                    for line_count, line in enumerate(set):
                        if frequently_used[set_count][line_count][0] < min_frequency:
                            min_frequency = frequently_used[set_count][line_count][0]
                            least_freq_set = set_count
                            least_freq_line = line_count
                # Now that we have the line, we can use it to alter the data in line
                eviction_line = int(str(least_freq_set) + str(least_freq_line), 2) # overall line to replace from
                cache_data[least_freq_set][least_freq_line][0] = '1' # set the valid bit to 1
                frequently_used[least_freq_set][least_freq_line][0] += 1
                # next four lines make sure that the tag has two hexadecimal digits
                tag_hex = hex(d_tag).split("x")[1]
                while len(tag_hex) != 2:
                    tag_hex = '0' + tag_hex
                cache_data[least_freq_set][least_freq_line][2] = tag_hex # set the tag to the search address tag
                ram_block = get_ram_block(decimal_search_address, data_block_size)
                counter = 3
                for byte in ram_block:
                    cache_data[least_freq_set][least_freq_line][counter] = byte
                    counter += 1
                    
            print(cache_data)
            print(recently_used)
            print(frequently_used)

        else: # cache hit
            eviction_line = -1
        print("eviction_line:" + str(eviction_line))
        print("ram_address:" + "0x" + search_address)
        print("data:" + "0x" + data)
    
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################
    elif("cache-write" in user_cache_prompt):
        #process input
        data = user_cache_prompt.split()[2]
        address = user_cache_prompt.split()[1]
        newaddress = address.split("x")[1]
        dec_address = int(newaddress, 16)
        bin_address = bin(dec_address)
        bin_address = bin_address[2:]
        bin_string = str(bin_address)
        bin_str_len = len(bin_string)
        bin_str_len = 8 - bin_str_len  ################################## SEE LINE 141
        for _ in range(bin_str_len):
            bin_string = '0' + bin_string

        #index for specific bits
        cache_tag = bin_string[ : num_tag_bits]
        cache_set = bin_string[num_tag_bits : num_tag_bits + num_set_index_bits]
        cache_offset = bin_string[num_tag_bits + num_set_index_bits: ]
        d_tag = int(cache_tag, 2)
        d_set = int(cache_set, 2)
        d_offset = int(cache_offset, 2)

        #determine if cache_hit
        cache_hit = False
        retrieved_data = '0'
        for data_line in cache_data[d_set]:        #iterate through cache_data[d_set]
            tag_bits = data_line[2:num_tag_bits+2] #check tag_bits          each data_line is of the form [valid_bit][dirty_bit][tag_bits][data_blocks]
            if(tag_bits == cache_tag and data_line[0] == 1): #CHECK FOR DIRTY BIT?
                cache_hit = True
            if(cache_hit):
                retrieved_data = data_line[num_tag_bits + num_dirty_bits + 1 + d_offset] #retrieve cache_data
                break
        if(retrieved_data == '0'):
            cache_hit = False
        

        #process cache_hit
        write_hit = "yes"
        eviction_line = -1
        dirty_bit = '0' #dirty bit is always intialized to zero, will be changed for cache hit write back
        ram_address = "-1"
        data_line_index = -1

        if(cache_hit): #cache hit
            if(write_hit_policy == 1): #cache hit write through
                ramdict[dec_address] = data #update the data in RAM
                for data_line in cache_data[d_set]:
                    data_line_index += 1
                    tag_bits = data_line[2 : num_tag_bits + 2]
                    if(tag_bits == cache_tag and data_line == 0): #find where the cache hit was
                        cache_data[d_set][data_line_index][num_tag_bits + 2 + d_offset] = data #update the data in cache_data at the hit
            else: #cache hit write back
                for data_line in cache_data[d_set]:
                    data_line_index += 1
                    tag_bits = data_line[2 : num_tag_bits + 2]
                    if(tag_bits == cache_tag and data_line == 0): #find where the cache hit was
                        cache_data[d_set][data_line_index][num_tag_bits + 2 + d_offset] = data #update the data in cache_data at the hit
                        cache_data[d_set][data_line_index][1] = '1' #update the dirty bit to be 1
                        dirty_bit = '1'
        else: #cache miss
            write_hit = "yes"
            ram_address = address
            eviction_line = dec_address / 8 #eviction lines come in terms of 8
            #write the new cache in?
            if(write_miss_policy == 1): #cache miss write allocate
                data = retrieved_data #load the data from RAM
                """
                for data_line in  cache_data[d_set]:
                    data_line_index += 1
                    tag_bits = data_line[2 :num_tag_bits + 2]                            #IF THERE IS NO HIT, IT IS WRITTEN BASED ON REPLACEMENT POLICY?
                    if(tag_bits == cache_tag and data_line[0] == 1):
                        cache_data[d_set][data_line_index][num_tag_bits + 2 + d_offset] = data #update the data in cache_data
                
                """
            else: #cache miss no-write allocate
                ramdict[dec_address] = data #update the data in RAM (do not load in cache)

        #print
        print("set:" + str(d_set))
        print("tag:" + str(d_tag))
        print("write_hit:" + write_hit)
        print("eviction_line:" + str(eviction_line))
        print("ram_address:" + ram_address)
        print("data:" + data)
        print("dirty_bit:" + dirty_bit)


    elif(user_cache_prompt == "cache-flush"):
        print(range(num_valid_bits + num_tag_bits + data_block_size))
        for x in range(number_of_sets):
            for y in range(associativity):
                for z in range(num_valid_bits + num_tag_bits + num_dirty_bits + data_block_size):
                    if(z < 2):
                        cache_data[x][y][z] = '0'
                    else:
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
    
    elif(user_cache_prompt == "memory-dump"):
        ram_file = open("ram.txt", 'w')         #open ram_file
        for i in range(len(ramdict)):           #iterate through memory dictionary
            ram_file.write(ramdict[i])   #write each memory line to ram.txt with a newline
        ram_file.close()                        #close ram_file
    
    elif(user_cache_prompt == "quit"):
        pass                              #Do nothing

    else:
        print("Invalid input. Select one of the following inputs:")
        print_cache_menu()
        user_cache_prompt = input()
        process_user_input(user_cache_prompt)


## This function takes in the search address and returns a list with the 8 byte block in ram surrounding the address
# as well as what the offset will be to access the specified data
# @param[in] dec_ram_address The decimal ram address to pull the ram block from.
# @return An 8-byte block containing the specified ram address.
def get_ram_block(dec_ram_address, data_block_size):
    lower_bound = 0
    while (lower_bound + data_block_size) < dec_ram_address:
        lower_bound = lower_bound + data_block_size
    ram_block = list()
    for i in range(lower_bound, lower_bound + data_block_size):
        ram_block.append(ramdict[i].strip())
    return ram_block

## This function rotates the elements of an array once. For example, [0, 1, 2, 3] -> [1, 2, 3, 0].
# @param[in] list The list to rotate.
# @return The new list that has been rotated.
def rotate(list):
    return list[1:] + list[:1]

if __name__ == "__main__":
    main()
