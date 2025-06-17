## Valkey Bundle Quick Start Guide

# What is Valkey Bundle

Valkey Bundle is a pre-packaged, containerized version of Valkey that comes preloaded with a collection of supported modules. These modules enable advanced data structures and search capabilities to extend Valkey’s core functionality. The bundle is designed to help developers quickly get started with powerful Valkey features without needing to manually install or configure anything. Some of the modules included in the bundle are:

1. Valkey JSON - Allows users to natively store, query, and modify JSON data structures using the JSONPath query language.
2. Valkey Bloom - Provides space-efficient probabilistic data structures, such as Bloom filters, for adding elements and checking whether they exist in a set.
3. Valkey Search - Enables the creation of indexes and similarity searches through the use of full-text and complex filters. 
4. Valkey LDAP - Handles user authentication against LDAP based identity providers.  

# Quick Start to Using the Bundle

The fastest way to start using Valkey Bundle is by downloading the official image through [Docker Hub](https://hub.docker.com/r/valkey/valkey-extensions/). The following steps will guide you through launching and interacting with your first instance!

1. **Pull the image to get the latest public release**

    ```bash
    docker pull valkey/valkey-extensions
    ```

    This command downloads the most recent stable image of the Valkey Bundle, which includes the Valkey server along with the preloaded modules.

    The Valkey Bundle image also supports multiple tags, allowing you to control the specific version and operating system base. This allows for more control over the environment, whether you’re aiming for a reproducible build (using a version like 8.1-bookworm) or a minimal footprint (alpine variant).

    Check out the [Valkey Bundle Docker Hub Tag](https://hub.docker.com/r/valkey/valkey-extensions/tags) section to view all available tags and example pull commands. 

2. **Start the Valkey server inside a container**

    ```bash
    docker run --name my-valkey-extensions -d -p 6379:6379 valkey/valkey-extensions
    ```

    This command starts the Valkey server in a background container named my-valkey-extensions and maps Valkey’s default port 6379 to your local machine for external access. By default, it uses the latest available image. To run a specific version or variant, append the desired tag to the image name. For example:

    ```bash
    docker run --name my-valkey-extensions -d -p 6379:6379 valkey/valkey-extensions:8.1-bookworm
    ```
 
3. **Connect to the server using valkey-cli**
    
    To interact with the server, use the Valkey command-line interface (valkey-cli). The example below runs the CLI from a separate container on the same Docker network.
     
    ```bash 
    docker run -it --network some-network --rm valkey/valkey-extensions valkey-cli -h my-valkey-extensions
    ```
    
    This approach is ideal when you want to isolate your CLI session or connect from other containers. However, it does require both containers to be connected to the same Docker network.

    Alternatively, you can run the CLI directly inside the server container: 

    ```bash
    docker exec -it my-valkey-extensions valkey-cli
    ```

    This runs the valkey-cli directly inside the server container and connects to the server on localhost. This approach requires no extra setup but only works when the server container is running locally and accessible from your host environment.

4. **Try some commands**

    ```
    # Check Loaded Modules

    MODULE LIST

    # Use the Valkey JSON Module
    JSON.SET test $ ‘{"hello": "world"}’
    JSON.GET test

    # Use the Valkey Bloom Module
    BF.RESERVE test_bloom 0.01 1000
    BF.ADD test_bloom "item1"
    BF.EXISTS test_bloom "item1"

    # Use the Valkey Search Module
    FT.CREATE index ON HASH PREFIX 1 doc: SCHEMA name TEXT
    HSET doc:1 name "valkey bundle"
    FT.SEARCH index "bundle"
    ```

    Make sure to check out the full list of commands for all the bundle components:

    1. [Valkey Commands](https://valkey.io/commands/)
    2. [Valkey JSON Commands](https://valkey.io/commands/#json)
    3. [Valkey Bloom Commands](https://valkey.io/commands/#bloom)
    4. [Valkey Search Commands](https://valkey.io/commands/#search)

Valkey Bundle supports more advanced setup options too including:

1. **Persistent storage**
    
    Persistent storage allows you to save data snapshots locally. The command below is an example of how you can save a snapshot every 60 seconds if at least one write occurred. 
    
    ```
    bash docker run --name my-valkey-extensions -d valkey/valkey-extensions valkey-server --save 60 1 --loglevel warning
    ```
    
2. **Custom Flags with Environment Variable**
    
    This allows you to pass additional Valkey flags at runtime using the VALKEY_EXTRA_FLAGS environment variable. This is a flexible way for customizing behavior without needing to modify the existing image or use a custom configuration file. 
    
    ```
    bash docker run --env VALKEY_EXTRA_FLAGS='--save 60 1 --loglevel warning' valkey/valkey-extensions
    ```
    
3. **Use a Custom Configuration File**
    
    If you need full control over your Valkey settings, you can create a customer configuration file that will be used inside the container. This allows you to override all default settings through the use of your own valkey.conf file.
    
    ```
    docker run -v /myvalkey/conf:/usr/local/etc/valkey --name my-valkey-extensions valkey/valkey-extensions valkey-server /usr/local/etc/valkey/valkey.conf
    ```


# Troubleshooting

Here are some common issues that users may encounter when running the Valkey Bundle, along with ways to resolve them.

1. **The container won’t start**
    
    Possible Causes: 

    - The container name is already in use.
    
    - The host port is already taken by another process.
    
    Solutions:

    - Run docker ps -a to check for existing containers with the same name. If the name already exists, create the Docker container using a different name.
    
    - Make sure no other process is using the same port.
    
2. **Can’t connect using valkey-cli**
    
    Possible Causes: 

    - The CLI container and server container aren’t on the same network.
    
    - The server isn’t running or hasn’t finished starting up.
    
    Solutions:
    
    - Create and use a user-defined Docker network or run the CLI from inside the container.
    
3. **Modules aren’t loaded**
    
    Possible Causes: 

    - You might be using the base valkey image instead of valkey/valkey-bundle.
    
    - The image didn’t load the modules due to an error.
    
    Solutions:

    - Run the command MODULE LIST inside the CLI to confirm loaded modules.
    
    - Make sure you’re using the Valkey Bundle image and not the Valkey image by mistake.
    ```
    bash docker run --name my-valkey-extensions -d valkey/valkey-extensions
    ```
    
# Next Steps

Once you’ve set up the Valkey Bundle, it’s time to start exploring the modules. Check out the documentation for each one to learn what they can do and how to use them effectively.

1. [Valkey JSON Documentation](https://valkey.io/topics/valkey-json/)
2. [Valkey Bloom Documentation](https://valkey.io/topics/bloomfilters/)
3. [Valkey Search Documentation](https://valkey.io/topics/search/)
4. [Valkey LDAP Documentation](https://valkey.io/topics/ldap/)

**Get Involved with the Valkey Community**

1. Join discussions on GitHub issues
2. Contribute improvements to repositories