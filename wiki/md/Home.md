## Install
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [Automate-WordPress-Post](https://pypi.org/project/automateWordPressPost/0.1/).

```bash
pip install automateWordPressPost
```


## Usage
```python
from automateWordPressPost.wordpress import WordPress
wp = WordPress('mysite.com', 'mysite.com/wp-admin', 'path-to-chromedriver')
wp.wp_login('email', 'password')
```


## Sample
```python
from automateWordPressPost.wordpress import WordPress

# Create instance for WordPress site
wp = WordPress("mysite.com", "mysite.com/wp-admin", "path-to-chromedriver")

# Login
wp.wp_login("email", "password")

# Maximize Window
wp.maximize_window()

# Add new post
wp.post_new("Post Title", "Technology", "tech", "featured", "This is excerpt for this post")

# Add a heading block
wp.post_content_block_heading("Heading 1", "h1", "#1bbafe")

# Add a paragraph block
paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
            "dolore magna aliqua. Diam maecenas sed enim ut. Suspendisse interdum consectetur libero id faucibus " \
            "nisl tincidunt eget. Sagittis orci a scelerisque purus semper eget duis at tellus. Vitae ultricies leo " \
            "integer malesuada nunc. Pharetra magna ac placerat vestibulum lectus mauris ultrices eros. Auctor augue " \
            "mauris augue neque gravida in fermentum et. Orci ac auctor augue mauris augue neque gravida in " \
            "fermentum. Maecenas accumsan lacus vel facilisis volutpat. Enim neque volutpat ac tincidunt vitae " \
            "semper quis lectus nulla. Sed turpis tincidunt id aliquet risus feugiat. Quis risus sed vulputate odio " \
            "ut enim blandit volutpat."
wp.post_content_block_paragraph(paragraph, 'right', None, 10, False, '#1bbafe', '#00a337')

# Add an image block
wp.post_content_block_image("tech", "caption", None, 'center', True, "alt-text", "full", 400, 400, 75)

# Add a list block
wp.post_content_block_list(paragraph)

# Add a html block
html = '<a href="https://example.com/home">Home</a>'
wp.post_content_block_html(html)

# Publish post
wp.post_publish()

# Print errors
print(wp.get_errors)

# Close browser
wp.close()
```
***

# Class WordPress
This class opens a chrome window and use it for automating post on a WordPress site.
Automate WordPress Block Editor. Blocks that can be used are: Heading, Paragraph, Image, List and Custom HTML.
Each block can be customized.
Add post using docx file or html file.

## Constructor
Creates a new instance of chrome for a WordPress site

`class WordPress(site_url, login_url, chrome_driver_path, sleep_time=2, user_agent=False)`
### Type
* :type site_url: str
* :type login_url: str
* :type chrome_driver_path: str
* :type sleep_time: int
* :type user_agent: bool
### Description
* :param site_url: Home address of WordPress site.
* :param login_url: Login address of WordPress site.
* :param chrome_driver_path: Path of chrome webdriver for selenium
* :param sleep_time: Wait time (seconds) between execution of different tasks (default is 2)
* :param user_agent: Use random User-Agent for chrome (default is False)
### Example
wp = WordPress('mysite.com', 'mysite.com/wp-admin', 'path-to-chromedriver', 3, True)
