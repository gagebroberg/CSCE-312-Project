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

# Configuring the RAM
To configure the RAM, the user should note that the input.txt file is where the RAM data is pulled from.
When the program is first run, the user will be prompted to "Initialize the RAM:".
The user should do so by entering a command of the following form:
```
ram-init <start> <end>
```
where "start" must be 0x00 and "end" can be any hex pair from 0x00 - 0xFF.
After the user properly enters ram initialization info, the program will let the 
user know that the ram has been successfully initialized.
