import numpy as np
import pandas as pd
import wikipediaapi

# Call the Wikipedia function through a user_agent and specify the language
# This code creates an instance of the Wikipedia class from the wikipedia-api package, which is used to interact with the Wikipedia API.
string = "SemSearchDemo/2.0 (Jasper B)" # This line creates a string that will be used as the user agent for the Wikipedia API requests. The user agent is a string that the client sends to the server to identify itself. In this case, it identifies the client as "SemSearchDemo/2.0 (Jasper B)".
wiki_wiki = wikipediaapi.Wikipedia(user_agent= string, language= 'en') #  creates an instance of the Wikipedia class. The user_agent parameter is set to the previously defined string, and the language parameter is set to 'en', which means that the instance will interact with the English version of Wikipedia. The instance is stored in the wiki_wiki variable, which can then be used to make requests to the Wikipedia API.


# Function to extract and store Wikipedia page sections
# The extract_wikipedia_sections function takes a Wikipedia page title as an argument and retrieves the title and sections of the corresponding Wikipedia page, if it exists.
def extract_wikipedia_sections(page_title):
    page = wiki_wiki.page(page_title) # uses the wiki_wiki object (which should be an instance of wikipediaapi.Wikipedia) to get the Wikipedia page with the title page_title.
    if page.exists(): # checks if the page exists.
        title = page.title #  If the page exists, this line gets the title of the page.
        sections = [] # This initializes an empty list to store the sections of the page.

        # Extract introduction if available
        introduction = page.summary
        if introduction:
            sections.append(("Introduction", introduction))

        # Extract all sections and subsections recursively
        def recursive_extraction(section):
            section_text = section.text
            if section_text:
                sections.append((section.title, section_text))
            for sub_section in section.sections:
                recursive_extraction(sub_section)

        for section in page.sections:
            if section.title not in redundant_sections:
                recursive_extraction(section)

        return title, sections

    else:
        return None, None

