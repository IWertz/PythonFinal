import sqlite3
import tkinter
from sqlite3 import Error

from final.cutsomer import Customer


def create_connection(db):
    """ Connect to a SQLite database
    :param db: filename of database
    :return connection if no error, otherwise None"""
    try:
        _conn = sqlite3.connect(db)
        return _conn
    except Error as err:
        print(err)
    return None


def create_table(_conn, sql_create_table):
    """ Creates table with give sql statement
    :param _conn: Connection object
    :param sql_create_table: a SQL CREATE TABLE statement
    :return:
    """
    try:
        c = _conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)


def create_tables(database):
    sql_create_item_table = """ CREATE TABLE IF NOT EXISTS item (
                                        id integer PRIMARY KEY,
                                        key text NOT NULL,
                                        value text NOT NULL
                                    ); """
    sql_create_customer_table = """CREATE TABLE IF NOT EXISTS customer (
                                        id integer PRIMARY KEY,
                                        fname text NOT NULL,
                                        lname text NOT NULL,
                                        balance integer NOT NULL
                                    );"""
    # create a database connection
    _conn = create_connection(database)
    if _conn is not None:
        # create item table
        create_table(_conn, sql_create_item_table)
        # create customer table
        create_table(_conn, sql_create_customer_table)
    else:
        print("Unable to connect to " + str(database))


def get_all_items(_conn):
    """Query all rows of item table
    :param _conn: the connection object
    :return:
    """
    cur = _conn.cursor()
    cur.execute("SELECT * FROM item")

    rows = cur.fetchall()
    _items = dict()
    for row in rows:
        print(row)
        key = (row[1])
        value = (row[2])
        _items[key] = value
    return _items


def create_item(_conn, item):
    """Create a new person for table
    :param _conn:
    :param item:
    :return: person id
    """
    sql = ''' INSERT INTO item(key,value)
              VALUES(?,?) '''
    cur = _conn.cursor()  # cursor object
    cur.execute(sql, item)


def add_item(_conn, key, value):
    item = (str(key), str(value))
    create_item(_conn, item)


def print_main_menu(_conn):
    global user
    print()
    print("1: Show items")
    print("2: Show balance")
    print("3: Show cart")
    print("4: Buy Item")
    print("5: Add Item To Sales List")
    print("6: Check Out")
    print("7: Exit Program")
    print()
    i = input("Enter Input: ")
    if i == "1":
        print()
        print("Items:")
        get_all_items(_conn)
        print()
    elif i == "2":
        print("User Balance: $" + str(user.balance))
    elif i == "3":
        show_cart(user)
    elif i == "4":
        user = buy_item(user)
    elif i == "5":
        add_item_menu(_conn)
    elif i == "6":
        user = preorder_details(user)
        user = check_out(user)
        check_out_gui(user)
    elif i == "7":
        global sentinel
        sentinel = 'n'
    else:
        print("Please enter a proper menu item.")
        print_main_menu(_conn)


def preorder_details(_user):
    print()
    _user.cart.tax = float(input("Enter you state's sales tax: "))
    _user.cart.shipping = float(input("Enter the cost of shipping: "))
    _user.cart.coupon = float(input("Enter total coupon value: "))
    print()
    return _user


def check_out(_user):
    _user.check_out()
    print()
    print("Receipt: ")
    print("------")
    print("Subtotal: " + str(_user.cart.subtotal))
    print("Tax: " + str(_user.cart.tax))
    print("Shipping: " + str(_user.cart.shipping))
    print("Coupons: " + str(_user.cart.coupon))
    print("Total: " + str(_user.cart.total))
    print("Remaining Balance: " + str(_user.balance))
    print("------")
    print()
    global sentinel
    sentinel = 'n'
    return _user


def check_out_gui(_user):
    m = tkinter.Tk()
    l1 = tkinter.Label(m, text="Receipt: ")
    l2 = tkinter.Label(m, text="------")
    l3 = tkinter.Label(m, text="Subtotal: " + str(_user.cart.subtotal))
    l4 = tkinter.Label(m, text="Tax: " + str(_user.cart.tax))
    l5 = tkinter.Label(m, text="Shipping: " + str(_user.cart.shipping))
    l6 = tkinter.Label(m, text="Coupons: " + str(_user.cart.coupon))
    l7 = tkinter.Label(m, text="Total: " + str(_user.cart.total))
    l8 = tkinter.Label(m, text="Remaining Balance: " + str(_user.balance))
    l9 = tkinter.Label(m, text="------")
    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    l5.pack()
    l6.pack()
    l7.pack()
    l8.pack()
    l9.pack()
    m.mainloop()


def show_cart(_user):
    for item in _user.cart.items:
        print("Item: " + str(item) + ", Value: $" + str(_user.cart.items[item]))


def add_item_menu(_conn):
    i_1 = input("Enter Item: ")
    i_2 = input("Enter Value: ")
    add_item(_conn, i_1, i_2)
    global items
    items = get_all_items(_conn)


def buy_item(_user):
    i = input("Enter Item To Buy: ")
    try:
        if items[i] is not None:
            _user.cart.add_item(i, items[i])
        else:
            print("That didn't work")
    except KeyError:
        print("That item does not exist. Please try again")
    return _user


def add_user_menu(_conn):
    print("Create User")
    i_1 = input("Enter First Name: ")
    i_2 = input("Enter Last Name: ")
    i_3 = input("Enter User Balance: ")
    _user = Customer(i_1, i_2, i_3)
    create_user(_conn, _user)
    _user.add_cart(SALES_TAX, SHIPPING, COUPON)
    return _user


def create_user(_conn, _user):
    """Create a new person for table
    :param _conn:
    :param _user:
    :return: person id
    """
    sql = ''' INSERT INTO customer(fname,lname,balance)
              VALUES(?,?,?) '''
    cur = _conn.cursor()  # cursor object
    sql_user = (_user.fname, _user.lname, _user.balance)
    cur.execute(sql, sql_user)


def get_all_users(_conn):
    """Query all rows of item table
    :param _conn: the connection object
    :return:
    """
    cur = _conn.cursor()
    cur.execute("SELECT * FROM customer")

    rows = cur.fetchall()
    _users = []
    for row in rows:
        print(row)
        fname = (row[1])
        lname = (row[2])
        balance = (row[3])
        _user = Customer(fname, lname, balance)
        _users.append(_user)
    return _users


def user_menu(_conn):
    global user
    print()
    print("1: Select User")
    print("2: Create User")
    print()
    i = input("Enter Input: ")
    if i == "1":
        users = get_all_users(_conn)
        user_num = int(input("Enter User Number: "))
        user_num -= 1
        if 0 <= user_num < users.__len__():
            user = users[user_num]
            user.add_cart(SALES_TAX, SHIPPING, COUPON)
        else:
            print("please enter a proper user number.")
            user_menu(_conn)
    elif i == "2":
        user = add_user_menu(_conn)
    else:
        print("Please enter a proper menu item.")
        user_menu(_conn)


if __name__ == '__main__':
    # Initialize global constants
    SALES_TAX = 0
    SHIPPING = 0
    COUPON = 0
    user = None

    # Connect to database
    conn = create_connection("pythonsqlite.db")
    with conn:
        create_tables("pythonsqlite.db")
        user_menu(conn)
        print()
        print("Items:")
        items = get_all_items(conn)
        print()
        sentinel = 'y'
        while sentinel != 'n':
            print_main_menu(conn)
