# NC Commons Import Bot

This Python script is designed to facilitate the import of files from NC Commons to Wikipedia. It automates the process of fetching files from NC Commons, uploading them to Wikipedia, and updating the relevant templates.

1. **Get Languages List from User Page**:
   - The bot retrieves a list of languages from the page titled "User:Mr. Ibrahem/import bot".
   - It parses the content of this page to extract the list of languages represented as language codes.

2. **Retrieve Pages with Template:NC for Each Language**:
   - For each language obtained from the user page, the bot proceeds to fetch pages that contain the template "Template:NC".
   - This is done by making API calls to Wikipedia using the language code to retrieve relevant pages.

3. **Extract Templates with Name "Template:NC"**:
   - Upon accessing each page containing the "Template:NC" template, the bot identifies and extracts all instances of this template.
   - It utilizes a parsing library to parse the wikitext of the page and identify occurrences of the specified template.

4. **Process Each Template**:
   - For each extracted template, the bot retrieves relevant information such as file name and caption.
   - It may also fetch additional details related to the file, such as its content or metadata, from NC Commons.

5. **Upload File to Wikipedia**:
   - Once the necessary information is gathered, the bot proceeds to upload the file to Wikipedia.
   - This involves using the Wikimedia API to perform the upload operation.
   - If the file already exists on Wikipedia, the bot may handle duplicates according to predefined logic.
   - If the file is fetched from NC Commons, it is uploaded to Wikipedia with appropriate attribution and metadata.

6. **Update Template in Page**:
   - After successfully uploading the file, the bot updates the relevant template on the Wikipedia page.
   - It replaces the existing template with the newly uploaded file's information.
   - This ensures that the Wikipedia page reflects the latest changes made by the bot.

7. **Repeat for All Pages and Languages**:
   - The bot iterates through all pages containing "Template:NC" for each language obtained.
   - It repeats the process of extracting templates, uploading files, and updating templates for each page.
   - This ensures comprehensive coverage of files across multiple languages on Wikipedia.