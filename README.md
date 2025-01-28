
# Username Utilities

  

This repository contains two Python scripts:

  

1.  **Username Availability Checker** - A tool to check the availability of usernames across multiple platforms.

2.  **Unicode Variations Generator** - A tool to generate variations of a word using homoglyphs (visually similar Unicode characters).

  

---

  

## Username Availability Checker

  

A Python script to check username availability across various platforms using Playwright or HTTP requests.

  

### Features

  

- Supports multiple platforms (e.g., Epic Games, Instagram, Twitter, YouTube, etc.).

- Logs available usernames.

- Utilizes proxy configuration for enhanced privacy.

- Displays a progress bar for tracking checks.

  

### Requirements

  

- Python 3+

- Required Python packages (install with pip):

```bash
pip install -r requirements.txt
```

  

### Usage

  

1.  **Clone the repository:**

```bash
git clone https://github.com/affectioned/username_utilities.git

cd username_utilities
```

  

2.  **Install dependencies:**

```bash
pip install -r requirements.txt
```

  

3.  **Run the script:**

```bash
python main.py
```

  

4.  **Follow the prompts to select a platform and start checking usernames.**

  

### Configuration

  

-  **Platforms**: Edit the `platforms_config.py` file to add or modify platform checks.

-  **Proxy Settings**: Customize proxy configuration in `proxy_manager.py`.

  

### Example Output

  

```plaintext
Choose a platform to check usernames:

[xbox] Xbox

[roblox] Roblox

[telegram] Telegram

[exit] Exit

  

Enter your choice (e.g., xbox, roblox, telegram, or exit to exit): xbox

- Selected platform: Xbox

- Checks to perform: ['https://xbox.com/check']

  

Checking usernames: ████████████████ 100%

[+] Available: username123 on Xbox

[!] Error checking username456: Connection timeout
```

  

---

  

## Unicode Variations Generator

  

A Python script to generate variations of a word by replacing characters with visually similar Unicode characters (e.g., Cyrillic, Greek).

  

### Features

  

- Creates variations of a word using visually similar Unicode characters.

- Generates variations in stages, with each stage having a different number of character replacements.

- Useful for testing Unicode normalization or identifying lookalike text.

  

### Usage

  

1.  **Run the script:**

```bash
python generator.py
```

  

2.  **Enter a word when prompted:**

```plaintext
Enter a word: example
```

  

3.  **View the generated variations:** Variations will be displayed in stages, with each stage representing the number of replaced characters.

  

### Example Output

  

```plaintext
Enter a word: test

  

Variations with 1 character(s) replaced:

[1] Τest

[2] tеst

[3] teѕt

[4] tesΤ

  

Variations with 2 character(s) replaced:

[5] Τеst

[6] Τeѕt

[7] ΤesΤ

[8] tеѕt

[9] tеsΤ

[10] teѕΤ

  

Variations with 3 character(s) replaced:

[11] Τеѕt

[12] ΤеsΤ

[13] ΤeѕΤ

[14] tеѕΤ

  

Variations with 4 character(s) replaced:

[15] ΤеѕΤ
```

  

### Configuration

  

-  **Unicode Map**: The `unicode_map` dictionary defines the character replacements. You can extend or modify it to include additional mappings.

  

---

  

## License

  

This project is licensed under the MIT License.