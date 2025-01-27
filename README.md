
# Username Utilities

This repository contains two powerful tools for working with usernames: **Username Availability Checker** and **Unicode Username Generator**. Each tool serves a distinct purpose and can be used independently or together for advanced username-related tasks.

----------

## 1. **Username Availability Checker** (`name_checker`)

The **Username Availability Checker** is a tool designed to check the availability of usernames across multiple platforms. It supports both static and dynamic content checks, multi-threading for faster processing, and logging of available usernames.

### Features:

-   **Platform Selection**: Choose from a variety of platforms (e.g., Epic Games, Instagram, Twitter, YouTube) to check username availability.
    
-   **Multi-threading**: Concurrent username checks for faster results.
    
-   **Dynamic & Static Checks**: Uses Playwright for dynamic platforms and HTTP requests for static ones.
    
-   **Progress Tracking**: Real-time progress bar for monitoring checks.
    
-   **Error Handling**: Gracefully handles errors during username checks.
    
-   **Logging**: Logs available usernames for easy reference.
    

### Folder Structure:

Copy

name_checker/
├─ cookie_manager.py
├─ hits_filter.py
├─ main.py
├─ platforms_config.py
├─ platform_specific/
│  ├─ discord_checker.py
│  └─ netease_checker.py
├─ proxy_manager.py
├─ request_handler.py
├─ username_utils.py
├─ utils.py
├─ wordlists/
└─ __pycache__/

### Usage:

1.  Navigate to the `name_checker` folder.
    
2.  Run `main.py` to start the username checker.
    
3.  Select a platform and provide a list of usernames to check.
    
4.  View available usernames in real-time.
    

----------

## 2. **Unicode Username Generator** (`username_unicode_generator`)

The **Unicode Username Generator** is a tool that creates visually similar Unicode variations of a given word by replacing specific characters with their Cyrillic or Greek equivalents. This is useful for generating unique usernames that may bypass restrictions or appear distinct while retaining a similar visual style.

### Features:

-   **Unicode Mapping**: Replaces Latin characters with visually similar Cyrillic or Greek characters.
    
-   **Staged Variations**: Generates variations by replacing 1 to N characters in stages.
    
-   **User Input**: Accepts a word as input and outputs all possible variations.
    
-   **Flexible Use**: Ideal for creating creative usernames or testing Unicode-based edge cases.
    

### Folder Structure:

Copy

username_unicode_generator/
└─ generator.py

### Usage:

1.  Navigate to the `username_unicode_generator` folder.
    
2.  Run `generator.py`.
    
3.  Enter a word to generate Unicode variations.
    
4.  View and use the generated variations.