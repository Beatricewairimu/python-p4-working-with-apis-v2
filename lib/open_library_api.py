import requests
import json
from typing import List, Optional, Dict, Any


class OpenLibraryAPI:
    """
    A class to interact with the Open Library API.
    Provides methods to search for books and retrieve their details.
    """

    BASE_URL = "https://openlibrary.org/search.json"

    def __init__(self, default_fields: List[str] = None, default_limit: int = 1):
        """
        Initialize the API client with default parameters.
        
        Args:
            default_fields: List of fields to include in response (default: title, author_name)
            default_limit: Maximum number of results to return (default: 1)
        """
        self.default_fields = default_fields or ["title", "author_name"]
        self.default_limit = default_limit

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Open Library API with error handling.
        
        Args:
            params: Dictionary of query parameters
            
        Returns:
            Dictionary containing the API response
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            raise

    def search_books(
        self, 
        title: str, 
        fields: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Search for books by title with configurable fields and limit.
        
        Args:
            title: Book title to search for
            fields: List of fields to include in response (uses default if None)
            limit: Maximum number of results (uses default if None)
            
        Returns:
            Dictionary containing the API response
        """
        params = {
            "title": title.replace(" ", "+"),
            "fields": ",".join(fields or self.default_fields),
            "limit": limit or self.default_limit
        }
        return self._make_request(params)

    def format_book_result(self, book_data: Dict[str, Any]) -> str:
        """
        Format book data into a human-readable string.
        
        Args:
            book_data: Dictionary containing book information
            
        Returns:
            Formatted string with book details
        """
        try:
            title = book_data.get("title", "Unknown Title")
            authors = ", ".join(book_data.get("author_name", ["Unknown Author"]))
            return f"Title: {title}\nAuthor(s): {authors}"
        except Exception as e:
            print(f"Error formatting book data: {e}")
            return "Could not format book information"

    def interactive_search(self):
        """
        Run an interactive search prompt that takes user input and displays results.
        """
        print("Open Library Book Search")
        print("-----------------------")
        
        while True:
            try:
                title = input("\nEnter a book title (or 'q' to quit): ").strip()
                if title.lower() == 'q':
                    break
                    
                if not title:
                    print("Please enter a valid book title")
                    continue
                    
                result = self.search_books(title)
                if result.get("docs"):
                    print("\nSearch Result:")
                    print(self.format_book_result(result["docs"][0]))
                else:
                    print("No results found for that title")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    api = OpenLibraryAPI()
    api.interactive_search()
 