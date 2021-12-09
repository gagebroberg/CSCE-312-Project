# CSCE-312-Project

## Compiling
Since this is a python program, there is no compilation necessary. The user needs a python interpreter in order to run the program. It is recommended that python3 is used to run the program.

## Running the program
In order to run the program, navigate to the root of the project directory. 
Then (assuming the user is running the program using python 3) 
the user can simply run the program in terminal with the following command:
```
python3 src/cachesimulator.py input/input.txt
```

## Using the program
There are 3 steps to using the cache simulator:

### Configuring the RAM
To configure the RAM, the user should note that the input.txt file is where the RAM data is pulled from.
When the program is first run, the user will be prompted to "Initialize the RAM:".
The user should do so by entering a command of the following form:
```
ram-init <start> <end>
```
where "start" must be 0x00 and "end" can be any hex pair from 0x00 - 0xFF.
After the user properly enters ram initialization info, the program will let the 
user know that the ram has been successfully initialized.

### Configuring the cache
To configure the cache, the user has a variety of options:
1. Cache size -> This can be a number anywhere from 8 - 256
2. Data block size -> This can be any power of 2
3. Associativity -> This must either be 1, 2, or 4
4. Replacement policy -> This must either by 1, 2, or 3
5. Write hit policy -> This must either by 1 or 2
4. Write miss policy -> This must either by 1 or 2

After entering the following information about the desired cache structure, the user will be notified that
the cache has been successfully configured.

### Interacting with the cache
Now, the user will be presented with a menu of allowed actions. The user should enter the name of the desired option
followed by parameters. The list of allowed action is as follows:
1. cache-read
```
cache-read <hexadecimal search address>
```
This option will return the data located at the requested address along with other information.
2. cache-write
```
cache-write <hexadecimal search address> <hexadecimal entry to write>
```
This option will return the data entered and in which address along with other information.
3. cache-flush
```
cache-flush
```
This option will clear all lines in the cache.
4. cache-view
```
cache-view
```
This option will display the total number of bytes in RAM as well as a visual of what the RAM
contains.
5. memory-view
```
memory-view
```
This option will display the cache options configured earlier by the user as well as the number of
cache misses, cache hits, and a visual representation of the cache.
6. cache-dump
```
cache-dump
```
This option will write the contents of the cache to a file called cache.txt located in the output folder.
7. memory-dump
```
memory-dump
```
This option will write the contents of the cache to a file called ram.txt located in the output folder.
8. quit
```
quit
```
This option ends the program exectution.
