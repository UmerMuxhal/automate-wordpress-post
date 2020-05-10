# Automate-WordPress

Automate-WordPress is a Python package for automating WordPress posts.
Automate WordPress Block Editor. Blocks that can be used are: Heading, Paragraph, Image, List and Custom HTML.
Each block can be customized.
Add post using docx file or html file.


**Note:** Tested on WordPress version 5.4

## Prerequisites
Required python modules ad libraries are: 

bs4

time

codecs

mammoth

selenium

pyperclip

random_user_agent

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Automate-WordPress.

```bash
pip install -r requirements.txt
pip install WordPress
```

## Usage

```python
from automateWordPressPost.wordpress import WordPress
wp = WordPress('mysite.com', 'mysite.com/wp-admin', 'path-to-chromedriver')
wp.wp_login('email', 'password')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
