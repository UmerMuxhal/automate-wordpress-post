## Html File
Read html file and return the code.

`read_html(html_path, full=False)`

### Type
* :type html_path: str
* :type full: bool

### Description
* :param html_path: html file path.
* :param full: True to get full code, otherwise code in body tag. (optional)

### Return
* :rtype: str
* :return: html code of the file.

### Example
`wp.read_html("C\\Path\\To\\File.html")`

***


## Docx File
Convert docx file to html code.

`docx_to_html(docx_path)`

### Type
* :type docx_path: str

### Description
* :param docx_path: Path of docx file.

### Return
* :rtype: str
* :return: html code of the file.

### Example
`wp.docx_to_html("C\\Path\\To\\File.docx")`

***