# Clients Documentation

This repo contains the detailed JSON files specifying client libraries. It is used for generating contect for the [clients documentation page](https://valkey.io/clients/)

## JSON Fields
Each JSON file includes general fields as well as boolean feature fields, specifying whether the client supports them or not.

### General Fields 

1. **`description`** - a short despcription of the library, mostly taken from their repos. 
2. **`repo`** - the url to the library's repo.
3. **`installation`** - an installation command from the most used package manager in the respective language.  
4. **`language`** - the programming language in which the library is written.
5. **`package_size`** - the library's unpacked package size, including dependencies. 

### Feature Fields - 
See [Advanced client features](advanced_client_features.md) for detailed explanation about each feature.
 