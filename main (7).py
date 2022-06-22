import numpy as np
import random


class Assignment8():

    def __init__(self, name="anonymous"):
        self.__name = name
        self.__connections = []
        self.__valid_connection_type = None
        self.__score = 0

    def __str__(self):
        return self.__name

    def add_connection(self, con):
        if type(con) == self.__valid_connection_type:
            self.__connections.append(con)

    def compute_score(self):
        self.__score = 0

    def get_score(self):
        return self.__score

    def get_name(self):
        return self.__name

    def __eq__(self, other):
        return (self.__score) == (other.__score)

    def __ne__(self, other):
        return (self.__score) != (other.__score)

    def __lt__(self, other):
        return (self.__score) > (other.__score)


class Customer(Assignment8):
    def __init__(self, name="anonymous"):
        super().__init__(name)
        self.__connections = []
        self.__valid_connection_type = Restaurant
        self.__score = 0
        self.__visits_list = []
        self.__sum_visits = 0

    def sum_visits(self, entry_table, names_table, name):
        # We find the sum of restaurants a customer has eaten at w:
        self.__sum_visits = 0
        name_index = np.where(names_table == name)[0][0]
        for i in entry_table[name_index]:
            self.__sum_visits += i
        return self.__sum_visits

    def add_connection(self, con):
        if type(con) == self.__valid_connection_type:
            self.__connections.append(con)

    def compute_score(self):
        self.__score = 0
        for i in self.__connections:
            i.compute_score()
            print("score: ", self.__score)
            self.__score += i.get_score()
        self.__score = round(self.__score / len(self.__connections), 1)
        return self.__score

    def get_score(self):
        return self.__score

    def __eq__(self, other):
        return (self.__score) == (other.__score)

    def __ne__(self, other):
        return (self.__score) != (other.__score)

    def __lt__(self, other):
        return (self.__score) > (other.__score)

    class Restaurant(Assignment8):
        def __init__(self, name="anonymous"):
            super().__init__(name)
            self.__connections = []
            self.__valid_connection_type = Customer
            self.__score = 0

        def add_connection(self, con):
            if type(con) == self.__valid_connection_type:
                self.__connections.append(con)

        def compute_score(self):
            self.__score = 0
            for i in self.__connections:
                self.__score += i.sum_visits(entry_table, names_tab, i.get_name())
            return self.__score

        def get_score(self):
            return self.__score

        def __eq__(self, other):
            return (self.__score) == (other.__score)

        def __ne__(self, other):
            return (self.__score) != (other.__score)

        def __lt__(self, other):
            return (self.__score) > (other.__score)

    def connection_worthy(entry_table, names_table, restaurant_table, restaurant, customer):
            #
            roww = np.where(names_table == customer.get_name())[0][0]
            column = np.where(restaurant_table == restaurant.get_name())[0][0]
            if (entry_table[roww][column] == 1):
                return True
            elif (entry_table[roww][column] == 0):
                return False

    # Initialize tables of values and names
    gen_table = np.loadtxt("Customers and Restaurants 2022.text", dtype=str, delimiter=",")
    num_cols = gen_table.shape[1]
    entry_table = np.loadtxt("Customers and Restaurants 2022.text", dtype=int, skiprows=1, usecols=range(1, num_cols), delimiter=",")
    restaurant_tab = np.loadtxt("Customers and Restaurants 2022.text", dtype=str, max_rows=1, usecols=range(1, num_cols), delimiter=",")
    names_tab = np.loadtxt("Customers and Restaurants 2022.text", dtype=str, skiprows=1, usecols=0, delimiter=",")
    list_for_customer = []
    list_for_restaurant = []

    # Create the list of restaurants and customers :
    for i in range(names_tab.shape[0]):
        customer = Customer(names_tab[i])
        list_for_customer.append(customer)

    for i in range(restaurant_tab.shape[0]):
        restaurant = Restaurant(restaurant_tab[i])
        list_for_restaurant.append(restaurant)

    # Create connections :
    for i in range(names_tab.shape[0]):
        for j in range(restaurant_tab.shape[0]):
            if (connection_worthy(entry_table, names_tab, restaurant_tab,
                                  list_for_restaurant[j], list_for_customer[i]) == True):
                list_for_customer[i].add_connection(list_for_restaurant[j])

    for i in range(restaurant_tab.shape[0]):
        for j in range(names_tab.shape[0]):
            if (connection_worthy(entry_table, names_tab, restaurant_tab,
                                  list_for_restaurant[i], list_for_customer[j])==True):
                list_for_restaurant[i].add_connection(list_for_customer[j])


    # CREATE/DISPLAY THE T10

    for i in list_for_customer:
        i.compute_score()

    list_for_customer = sorted(list_for_customer)
    print("TOP 10 CUSTOMERS!")

    for i in range(10):
        print("\n", i + 1, ": ", list_for_customer[i], list_for_customer[i].get_score())


    for i in list_for_restaurant:
        i.compute_score()

    print("\nTHE TOP 10 RESTAURANTS!!!!!!1")
    list_for_restaurant = sorted(list_for_restaurant)
    for i in range(10):
        print("\n", i + 1, ": ", list_for_restaurant[i], list_for_restaurant[i].get_score())






