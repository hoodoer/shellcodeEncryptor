# fileToCharEncoding
Python script to take any file and create a C header file with that binary data encoded as a char array. Optionally XOR encrypts the data. 


Simple tool to take an arbitrary binary (DLL, exe, etc.) 
and convert it to a XOR encrypted char array for embedding
in loaders that decrypt the data in memory and do something
useful with it. 

Basically a wrapper around xxd
