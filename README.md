# Finding the largest number in a given PDF

This Python-based program utilizes the open-source NLP library *SpaCy* and PDF parser *PyPDF* to extract numerical values from a PDF document, intelligently identifying and outputting the largest value in the document. 

## 🚀 Features

- Parses the given PDF page by page
- Uses SpaCy for natural language processing
- Detects and scales monetary values (e.g., millions, billions)
- Returns the largest number found

## How to Use

<pre> python solution.py </pre>

To run on the demo pdf or change the `PDF_URL` global var to run on any PDF in the directory

It will print out the largest number found in the document, like so: ``` Largest number found: 9,600,000,000.0 ```

## ❗Limitations

 - Does not parse numbers from tables or images in the PDF
 - May miss some edge cases in unusual numeric formats
 - Unable to identify scalable keywords beyond "trillion" or "trillions" (e.g., "quintillion" will not be found)
