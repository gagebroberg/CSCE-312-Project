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