
# Username Utilities

  

This repository contains two Python scripts:

  

1.  **Username Availability Checker** - A tool to check the availability of usernames across multiple platforms.

2.  **Unicode Variations Generator** - A tool to generate variations of a word using homoglyphs (visually similar Unicode characters).

  

---

  

## Username Availability Checker

  

A Python script to check username availability across various platforms using Playwright or HTTP requests.


### Requirements

  

- Python 3+

- Required Python packages (install with pip):
  

### Usage

  

1.  **Clone the repository:**

```bash
git clone https://github.com/affectioned/username_utilities.git

cd username_utilities
```
or download the repository directly from github

  

2.  **Install dependencies:**

```bash
pip install -r requirements.txt
```

  

3.  **Run the script:**

```bash
python main.py
```

### Configuration



-  **Platforms**: Edit the `platforms_config.py` file to add or modify platform checks.

  

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
  

### Usage

  

1.  **Run the script:**

```bash
python generator.py
```

  

2.  **Enter a word when prompted:**

```plaintext
Enter a word: example
```
  

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

## License

  

This project is licensed under the MIT License.
