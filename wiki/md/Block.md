## Heading
Add heading block and customize it.

`post_content_block_heading(heading, style='default', align='left', text_color=None)`

### Type
* :type heading: str
* :type style: str
* :type align: str
* :type text_color: str

### Description
* :param heading: Heading text
* :param style: Style of heading tag. Allowed: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
* :param align: Heading alignment (default="left"). Allowed: ['left', 'center', 'right'] (optional)
* :param text_color: hex color code for heading's text color. (optional)

### Example
Simple

`wp.post_content_block_heading("Heading 1")`

Customized

`wp.post_content_block_heading("Heading 1", 'h1', 'center', '#1bbafe')`

***


## Paragraph
Add paragraph block and customize it.

`post_content_block_paragraph(paragraph, align='left', size=None, custom_size=None, drop_cap=False, text_color=None, bg_color=None)`

### Type
* :type paragraph: str
* :type align: str
* :type size: str
* :type custom_size: int
* :type drop_cap: bool
* :type text_color: str
* :type bg_color: str

### Description
* :param paragraph: Paragraph text
* :param align: Paragraph alignment (default="left"). Allowed: ['left', 'center', 'right'] (optional)
* :param size: choose font size from sizes available in the editor: ['default', 'small', 'normal', 'medium', 'large', 'huge'] (optional)
* :param custom_size: font size (optional)
* :param drop_cap: Set first character of paragraph to capital (optional)
* :param text_color: hex color code for paragraph's text color. (optional)
* :param bg_color: hex color code for paragraph's background color. (optional)

### Example
Simple

`wp.post_content_block_paragraph("This is a paragraph.")`

Customized

`wp.post_content_block_paragraph("This is a paragraph.", "center", "normal", None, True, "#1bbafe", "#ffffff")`

***


## Image
Add image block and customize it. 
For Image block, image can be added either from media library or by using url.

`post_content_block_image(image_name=None, caption=None, image_url=None, align='left', round_shape=None, alt_text=None, size=None, width=None, height=None, percentage=None)`

### Type
* :type image_name: str
* :type caption: str
* :type image_url: str
* :type align: str
* :type round_shape: bool
* :type alt_text: str
* :type size: str
* :type width: int
* :type height: int
* :type percentage: int

### Description
* :param image_name: Image name in media library. (Full image name is not necessary) (optional) {Image must be in media of WordPress site, for this to work}
* :param caption: Caption for Image (optional)
* :param image_url: Image url (optional)
* :param align: image alignment (default="left"). Allowed: ['left', 'center', 'right']
* :param round_shape: True, to set round borders. (default=False)
* :param alt_text: Alt text for image (optional)
* :param size: Select size of Image from editor. Allowed: ['thumbnail', 'medium', 'large', 'full'] (optional)
* :param width: Width of image (optional)
* :param height: Height of image (optional)
* :param percentage: Percentage of image. Allowed: [25, 50, 75, 100] (optional)

### Example
Simple

`wp.post_content_block_image("ImageName")`

`wp.post_content_block_image(None, None, "https://www.example.com/image")`

Customized

`wp.post_content_block_image("ImageName", "caption", None, "center", True, "alt-text", "thumbnail", 500, 500, 75)`
***


## List
Add list block and customize it.

`post_content_block_list(list_text, ordered=False, start=None, reverse=False, separator='.')`

### Type
* :type list_text: str
* :type ordered: bool
* :type start: int
* :type reverse: bool
* :type separator: str

### Description
* :param list_text: List
* :param ordered: True, for numbering. (optional)
* :param start: Number from where to start the list. (optional)
* :param reverse: Reverse the numbering of list. (optional)
* :param separator: Separator before new item in the list. (default=".") Example: "Line 1. Line 2" -- Here "." is the separator between list items.

### Example
Un-ordered List

`wp.post_content_block_list("Line 1. Line 2")`

Ordered List

`wp.post_content_block_list("Line 1. Line 2", True, 50, True)`

Using separator

`wp.post_content_block_list("Line 1, Line 2", True, 50, True, ",")`

***


## Html
Add html block.

`post_content_block_html(html)`

### Type
* :type html: str

### Description
* :param html: html code for html block

### Example
`wp.post_content_block_html("<div><h5>Heading</h5></div>")`

***


## Docx/Html File
Add a block using docx or html file.

`post_content_from_file(file_path='', typing_effect=False)`

### Type
* :type file_path: str
* :type typing_effect: bool

### Description
* :param file_path: path to docx or html file on computer.
* :param typing_effect: True if keyboard typing effect is required. (optional) (default=False)

### Example
Docx file

`wp.post_content_from_file("C\\Path\\To\\File.docx")`

Html file with typing effect

`wp.post_content_from_file("C\\Path\\To\\File.html", True)`

***