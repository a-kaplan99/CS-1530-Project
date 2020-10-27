public class Books {

  public boolean addBook(int book_id, String title, String author, String genre, int rating) {
    // query db to add specified book
    return true;
  }

  public boolean removeBook(String title) {
    // query db to remove specified book
    if (validateBook(title)) {
      return true;
    }
    System.out.println(book)
  }

  public String title(int id) {
    // SELECT title FROM books WHERE id = id
    return "";
  }

  public String author(int id) {
    // SELECT author FROM books WHERE id = id
  }

  public String genre(int id) {
    // SELECT title FROM books WHERE id = id
    return "";
  }

  public int rating(int id) {
    // SELECT author FROM books WHERE id = id
  }

  private validateBook(String title) {
    // check the book db for book
    return true;
  }
}
