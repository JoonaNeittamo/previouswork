# Your final assignment is about creating a register / login functionality to your app.
# You need to also associate each todo item created in the database with the corresponding logged-in user.
# For storing and retrieving the users you ARE REQUIRED TO USE SQLAlchemy. if not using SQLAlchemy, then the whole assignment will give you a direct fail (0 points).

# What you need to do:
# First, create table for holding users. Class model should be called 'User' and name of the table should be 'users'.
#   The users table should have at least the fields userId, username and password.
#   Make sure that you also have foreign key relationship between the items and users tables and relationship created from both tables into each another.
# Before your main application launches, it should ask the user if they want to REGISTER or LOGIN
#   If user wants to REGISTER, the application should then ask the user for the username and password combination
#      If user with this username already exists in the table users, app should notify about that and not create the new user
#      If this username did not exist, create account for the user in the table users
#   If user wants to LOGIN, then you need to ask user the username and password
#      If the given username and password combination does not exist in the table users, then inform user about this and do not allow user into the system
#      If this username and password combination exists in the table users, then allow the user in the system and store the user that logged in
# Finally, you will also need to associate each item created with the logged-in user. This way each logged-in user will have their own todo items.

from collections import UserDict
import sys
import os

from attr import asdict
from database import session, User, Item, UserItem


# Main app function
def main():
  while True:
    
      print(f"\nWhat do you want to do today?")
      print("1: View todo items")
      print("2: Create new todo item")
      print("3: Remove item")
      print("4: Exit\n")
      selection = input(": ")
      if selection == '1': 
        showItems()
      elif selection == '2': 
        createItem()
      elif selection == '3': 
        removeItem()
      elif selection == '4': 
        sys.exit("Goodbye!")

    

# Login to the system
def login():
  register_or_login = input("Do you want to register or login? : ").lower()
  if register_or_login == 'register':
    cls()
    register()
  elif register_or_login == 'login':
    print("Enter your Username and Password to login!\n")
    global login_username
    login_username = input("Username: ")

    if session.query(User).filter(User.username==login_username).first() == None:
      loop_again = True
      while loop_again:
        account_creation_input = input(f"User '{login_username}' does not exist, want to register? : ").lower()
        if account_creation_input == 'yes':
          loop_again = False
          cls()
          register()
        elif account_creation_input == 'no':
          cls()
          login()
        else:
          cls()
    else:
      login_password = input("Password: ")
      logged_in_user = session.query(User).filter(User.username==login_username) #
      for user in logged_in_user: # Extremely stupid way of checking if given password matches username accounts password
        if user.password != login_password:
          cls()
          print("Username does not match the password")        
          login()
        else:
          cls()
          print("Welcome user!")
          main()

  else:
    cls()
    login()




# Register if user does not exist
def register():
  print("To register you need to write a username, password and e-mail, 'BACK' to go back.")
  register_username = input("Username: ")
  if session.query(User).filter(User.username==register_username).first() != None:   
    cls()
    print("Username already exists, choose a name that does not exist")
    register()
  elif register_username == 'BACK':
    cls()
    login()
  else:
    register_password = input("Password: ")
    not_valid_email = True
    while not_valid_email:
      register_email = input("E-Mail: ")
      if '@' and '.' not in register_email: # Really minimal version of checking of valid email
        cls()
        print("Not a valid E-Mail, try 'xxx@xxx.xxx'\n")
      else:
        not_valid_email = False
        cls()

  session.add( 
    User(
      username=register_username,
      password=register_password,
      email=register_email
    )
  )
  session.commit()

  login()

# Lists all todo items
def showItems():
  print("\nYour todo lists:")
  print("---")

  current_user_show = session.query(User).filter(User.username==login_username)
  for user in current_user_show:
    useritemtodo = session.query(UserItem).filter(UserItem.userId==user.userId)
    for itemtodo in useritemtodo:
      allItems = session.query(Item).filter(Item.itemId==itemtodo.itemId)
      for item in allItems:
        print(f"{item.itemId} : {item.name} : {item.description}")
      


  input("---\nPress ENTER to continue")

# Creates new todo item
def createItem():
  item_name = input("Create a name for the To-Do: ")
  item_description = input("Create a description for the To-Do: ")
  

  current_user_create = session.query(User).filter(User.username==login_username).first()
  current_user_create.items.append(
    Item(
      name=item_name,
      description=item_description
    )
  )
  session.commit()

  # THIS IS USED FOR CHECKING ALL TODOS
  #useritemsids = session.query(UserItem)
  #for useritemids in useritemsids:
  #  todoname = session.query(Item).filter(Item.itemId==useritemids.itemId)
  #  for name_of_todo in todoname:
  #    print(useritemids.userId, useritemids.itemId, name_of_todo.name)

  input("Press ENTER to continue")
  cls()
  main()

# Removes todo item with ID
def removeItem():
  cls()
  print("--- List of your To-Do's")
  current_user_show = session.query(User).filter(User.username==login_username)
  for user in current_user_show:
    useritemtodo = session.query(UserItem).filter(UserItem.userId==user.userId)
    for itemtodo in useritemtodo:
      allItems = session.query(Item).filter(Item.itemId==itemtodo.itemId)
      for item in allItems:
        print(f"{item.itemId} : {item.name} : {item.description}")
  print("---\n")

  itemid_list = []
  itemid_list.clear()
  
  current_user_show = session.query(User).filter(User.username==login_username)
  for user in current_user_show:
    useritemtodo = session.query(UserItem).filter(UserItem.userId==user.userId)
    for itemtodo in useritemtodo:
      allItems = session.query(Item).filter(Item.itemId==itemtodo.itemId)
      for item in allItems:
        itemid_list.append(str(item.itemId))

  print("CHOOSE THE ID ON THE LEFT")
  user_remove_choice = input("Which do you want to remove? 'back' to go back : ")
  if user_remove_choice in itemid_list:
    session.query(Item).filter(Item.itemId==user_remove_choice).delete()
    session.commit()
  elif user_remove_choice == 'back':
    cls()
    main()
  else:
    print("That To-Do is not in your list! Check your To-Do's from the list shown.")
    input("Press ENTER to continue")
    removeItem()

  input("Press ENTER to continue")

# Clear screen
def cls():
  os.system("cls")

# Start the app
print("Welcome to TOD-O LIST O-MAKER Version 5123.524")
login()