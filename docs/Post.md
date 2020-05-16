Add new post on WordPress site. Following tasks can be performed:

## New Post
Add new post on WordPress site.

`post_new(title, category=None, tag=None, featured_image=None, excerpt=None, file_path=None)`

### Type
* :type title: str
* :type category: str
* :type tag: str
* :type featured_image: str
* :type excerpt: str
* :type file_path: str

### Description
* :param title: title of the post.
* :param category: category name of the post. (optional)
* :param tag: tag of the post. (optional)
* :param featured_image: name of the Image in media library to set as featured image. (optional)
* :param excerpt: excerpt of the post. (optional)
* :param file_path: path of docx or html file for post content. (optional)

### Example
Post with just a title

`wp.post_new("Post Title")`

Post with title, category, tag, featured image and excerpt

`wp.post_new("Post Title", "Technology", "tech", "featured", "This is excerpt for this post")`

Post with title, category, tag, featured image, excerpt and a file to post from

`wp.post_new("Post Title", "Technology", "tech", "featured", "This is excerpt for this post", "docx/html-file-path")`

***


## Title
Set Post Title.

`post_title(title)`

### Type
* :type title: str

### Description
* :param title: title of the post

### Example
`wp.post_title("Post Title")`

***


## Status
Configure Post Status Settings.

`post_status(visibility='public', password=None, stick_top=False, pending_review=False)`

### Type
* :type visibility: str
* :type password: str
* :type stick_top: bool
* :type pending_review: bool

### Description
* :param visibility: Visibility of Post. Allowed: ['public', 'private, 'password'] (optional)
* :param password: Password for post if visibility set to password protected.
* :param stick_top: True to stick post on top on the blog page. (optional)
* :param pending_review: True to add post in pending

### Example
Public post

`wp.post_status('public', password=None, True, True)`

Private post

`wp.post_status('private')`

Password protected post

`wp.post_status('password', "your-password-here")`

***


## Category
Choose category if category name exists otherwise create new category.

`post_category(category)`

### Type
* :type category: str

### Description
* :param category: Post category name

### Example
`wp.post_category("category-name")`

***


## Tag
Choose tag if tag name exists otherwise create new tag.

`post_tag(tag)`

### Type
* :type tag: str

### Description
* :param tag: tag name of the post

### Example
`wp.post_tag("tag-name")`

***


## Featured Image
Set Featured Image for Post from media library.

`post_image(image_name)`

### Type
* :type image_name: str

### Description
* :param image_name: Name of the Image in media library.

### Example
`wp.post_image("featured-image-name")`

***


## Excerpt
Set Post excerpt.

`post_excerpt(excerpt)`

### Type
* :type excerpt: str

### Description
* :param excerpt: excerpt of the post.

### Example
`wp.post_excerpt("excerpt-text")`

***


## Discussion
Configure Discussion settings for post.

`post_discussion(comments=True, traceback=True)`

### Type
* :type comments: bool
* :type traceback: bool

### Description
* :param comments: False to Disable comments on post. (Default = True)
* :param traceback: False to Disable pingbacks & trackbacks. (Default = True)

### Example
`wp.post_discussion(False, False)`

***


## Format
Set Post Format.

`post_format(formatting='standard')`

### Type
* :type formatting: str

### Description
* :param formatting: Post display format. Allowed: ['standard', 'gallery', 'link', 'quote', 'video', 'audio']

### Example
`wp.post_format('gallery')`

***


## Save Draft
Save Post as Draft.

`post_save_draft()`

### Example
`wp.post_save_draft()`

***


## Publish
Publish Post.

`post_publish()`

### Example
`wp.post_publish()`

***


## Update
Update Post.

`post_update()`

### Example
`wp.post_update()`

***


## Switch to Draft
Switch Post from Published to Draft.

`post_switch_to_draft()`

### Example
`wp.post_switch_to_draft()`

***


## Url
Set Post Url. Applicable after publishing post.

`post_url(url)`

### Type
* :type url: str

### Description
* :param url: title of the post

### Example
`wp.post_url('post-url-here')`

***


## Open Document Setting
Open or switch to DOCUMENT SETTING Panel on the right.

`post_document_setting_open()`

### Example
`wp.post_document_setting_open()`

***