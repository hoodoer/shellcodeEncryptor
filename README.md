# Shellcode Encryptor
Python script to take any file and create a C header file with that binary data encoded as a char array. Optionally XOR encrypts the data. 


Simple tool to take an arbitrary binary (DLL, exe, etc.) 
and convert it to a XOR encrypted char array for embedding
in loaders that decrypt the data in memory and do something
useful with it. 

Helpful for writing custom loaders for shellcode. 

Basically a wrapper around xxd.

Note that the generated header file includes the encryption passphrase by default. If you leave this in the binary, many AVs will find that string, decrypt the payload and scan it. Best to use runtime assignment of the decryption key if you're shooting for AV bypass. 
