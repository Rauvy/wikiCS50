import re
import markdown2

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content, edit=False):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"

    if not edit and default_storage.exists(filename):
        raise FileExistsError("Entry Already Exists")
    
    if edit and default_storage.exists(filename):
        default_storage.delete(filename)

    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        with open(f"entries/{title}.md", 'r') as file:
            return file.read()  
    except FileNotFoundError:
        return None


def get_raw_entry(title):
    """
    Retrieves the raw Markdown content of an encyclopedia entry by its title.
    If no such entry exists, the function returns None.
    """

    try:
        with default_storage.open(f"entries/{title}.md") as file:
            return file.read()
    except FileNotFoundError:
        return None