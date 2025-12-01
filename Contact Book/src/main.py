class ContactBook:
    """A simple contact book to manage contacts with name, phone, and email."""
    
    def __init__(self):
        """Initialize an empty contact book."""
        self.contacts = {}

    def add_contact(self, name: str, phone: str, email: str = None):
        """Add a new contact to the book.
        
        Args:
            name: Contact name (must be unique)
            phone: Phone number
            email: Email address (optional)
            
        Raises:
            Exception: If contact already exists
        """
        if name in self.contacts:
            raise (Exception("Contact already exists"))
        self.contacts[name] = {"email": email, "phone": phone}
        print("Contact added successfully")

    def find_contact(self, name: str) -> dict:
        """Find and return contact information by name.
        
        Args:
            name: Contact name to search for
            
        Returns:
            Dictionary containing phone and email
            
        Raises:
            Exception: If contact not found
        """
        if name in self.contacts:
            return self.contacts.get(name)
        raise Exception("No contact found")

    def delete_contact(self, name: str):
        """Delete a contact from the book.
        
        Args:
            name: Contact name to delete
            
        Raises:
            Exception: If contact not found
        """
        if name in self.contacts:
            del self.contacts[name]
            print("Contact deleted successfully")
        else:
            raise Exception("No contact found")

    def edit_contact(self, name: str, phone: str, email: str):
        """Update contact information.
        
        Args:
            name: Contact name to update
            phone: New phone number (if provided)
            email: New email address (if provided)
            
        Raises:
            Exception: If contact not found
        """
        if name not in self.contacts:
            raise Exception("Contact not found")
        if phone:
            self.contacts[name]['phone'] = phone
        if email:
            self.contacts[name]['email'] = email
        print("Contact updated successfully!")

    def __str__(self):
        """Return string representation of the contact book."""
        if not self.contacts:
            return "Contact book is empty"
        return str(self.contacts)


if __name__ == "__main__":

    print("-----> Add a contact")
    try:
        book = ContactBook()
        book.add_contact("Ali", "0912", "email")
        book.add_contact("Joe", "604", "j.z@gmail.com")
        book.add_contact("Ali", "0912", "email")

    except Exception as e:
        print(f"Exception occured \n: {e}")

    print("-----> Delete a contact")

    try:
        book.delete_contact("Ali")

    except Exception as e:
        print(f"Exception occured \n: {e}")

    print("-----> Find a contact")
    try:
        print(f"Ali's contact': {book.find_contact("Ali")}")
        print(f"Joe's contact': {book.find_contact("Joe")}")
    except Exception as e:
        print(f"Exception occured \n: {e}")

    print("-----> Edit a contact")
    try:
        book.edit_contact("Joe", "237", "joe.h@gmail.com")
    except Exception as e:
        print(f"Exception occured \n: {e}")

    print(f"This is the currect contact book: {book}")
