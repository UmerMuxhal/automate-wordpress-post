## Open Block Setting
Open or switch to BLOCK SETTING Panel on the right.

`post_content_block_setting_open()`

### Example
`wp.post_content_block_setting_open()`

***


## Heading
Select Heading style. Available styles are: h1, h2, h3, h4, h5, h6

`post_content_block_setting_heading(style)`

### Type
* :type style: str

### Description
* :param style: Style of heading tag. Allowed: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

### Example
`wp.post_content_block_setting_heading('h1')`

***


## Color
Set color of text and background.

`post_content_block_setting_color(text_color=None, bg_color=None)`

### Type
* :type text_color: str
* :type bg_color: str

### Description
* :param text_color: hex color code. (optional)
* :param bg_color: hex color code. (optional)

### Example
`wp.post_content_block_setting_color('#1bbafe', '#ffffff')`

***


## Image
Set image block style.

`post_content_block_setting_image(alt_text=None, size=None, width=None, height=None, percentage=None)`

### Type
* :type alt_text: str
* :type size: str
* :type width: int
* :type height: int
* :type percentage: int

### Description
:param alt_text: Alt text for image (optional)
:param size: Select size of Image from editor. Allowed: ['thumbnail', 'medium', 'large', 'full'] (optional)
:param width: Width of image (optional)
:param height: Height of image (optional)
:param percentage: Percentage of image. Allowed: [25, 50, 75, 100] (optional)

### Example
`wp.post_content_block_setting_image("Image 1", "full", 500, 500, 75%)`


## Image Align
Set Image Border's style.

`post_content_block_setting_image_align(align="left")`

### Type
* :type align: str

### Description
* :param align: image alignment (default="left"). Allowed: ['left', 'center', 'right']

### Example
`wp.post_content_block_setting_image_align("center")`

***


## Image Border
Set style for Image Border.

`post_content_block_setting_image_border(round_shape=False)`

### Type
* :type round_shape: bool

### Description
* :param round_shape: True, to set round borders. (default=False)

### Example
`wp.post_content_block_setting_image_border(True)`


## List
Customize List block style.

`post_content_block_setting_ordered_list(start=None, reverse=False)`

### Type
* :type start: int
* :type reverse: bool

### Description
* :param start: Number from where to start the list. (optional)
* :param reverse: Reverse the numbering of list. (optional)

### Example
`wp.post_content_block_setting_ordered_list(10, True)`

***


## Text
Set Paragraph block settings.

`post_content_block_setting_text(size=None, custom_size=None, drop_cap=False)`

### Type
* :type size: str
* :type custom_size: int
* :type drop_cap: bool

### Description
* :param size: choose font size from sizes available in the editor: ['default', 'small', 'normal', 'medium', 'large', 'huge'] (optional)
* :param custom_size: font size (optional)
* :param drop_cap: Set first character of paragraph to capital (optional)

### Example
Using editor's font size

`wp.post_content_block_setting_text("normal")`

Using custom font size

`wp.post_content_block_setting_text(None, 54)`

Set First character capital of Text

`wp.post_content_block_setting_text("small", None, True)`

***


## Text Align
Select text alignment.

`post_content_block_setting_text_align(align="left")`

### Type
* :type align: str

### Description
* :param align: text alignment (default="left"). Allowed: ['left', 'center', 'right']

### Example
`wp.post_content_block_setting_text_align("center")`

***