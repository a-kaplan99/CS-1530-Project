public class Accounts {

  public boolean register(String username, String email, String password) {
    boolean validUsername = true;

    // access database to ensure username has not been taken

    if (validUsername) {
      return true;
    } else {
      System.out.println("Username is already in use.");
      return false;
    }
  }

  public boolean login(String username, String password) {
    if (usernameExists()) {
      // query database to make sure password and username match
      return true;
    }
    System.out.println("Username does not exist.")
    return false;
  }

  public String username(int id) {
    //SELECT username FROM users WHERE id = 'id';
    return "";
  }

  public String password(int id) {
    //SELECT password FROM users WHERE id = 'id';
    return "";
  }

  public String email(int id) {
    //SELECT email FROM users WHERE id = 'id';
    return "";
  }

  private boolean usernameExists() {
    // search in db for for username
    return true;
  }
}
