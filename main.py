import sqlite3

db = sqlite3.connect('kabelne_tv.db')
c=db.cursor()

c.execute("""
   CREATE TABLE IF NOT EXISTS companys_ovn (
	id_com INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE,
	description TEXT NOT NULL
);""")
db.commit()
c.execute("""CREATE TABLE IF NOT EXISTS channels_list (
	id_ch INTEGER PRIMARY KEY AUTOINCREMENT,
	id_com INTEGER NOT NULL,
	name_ch TEXT NOT NULL UNIQUE,
	description TEXT NOT NULL,
	number_ch INTEGER UNIQUE NOT NULL,
	frequency_ch REAL UNIQUE NOT NULL,
	FOREIGN KEY (id_com)  REFERENCES companys_ovn (id_com)
);""")
db.commit()

c.execute("""CREATE TABLE IF NOT EXISTS customers_list (
	id_cust INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	subscribe INTEGER NOT NULL
);""")
db.commit()





#створити таблицю нового клієнта
def create_cust_tabl():
   customer_ch = input("Введіть ім'я клієнта: ")
   c.execute(f"""
      CREATE TABLE IF NOT EXISTS {customer_ch}(
	  id_ch INTEGER NOT NULL UNIQUE,
	  name_ch TEXT NOT NULL,
	  use INT DEFAULT 0,
	  FOREIGN KEY (id_ch)  REFERENCES channels_list (id_ch),
	  FOREIGN KEY (name_ch)  REFERENCES channels_list (name_ch)
      );""")
   db.commit()
   print("Створено таблицю клієнта: " + customer_ch)

#додати інфу про наявні канали клієнта до таблиці "імя клієнта"
def add_ch_to_cust ():
   name_cus_tabl = c.execute("SELECT name FROM customers_list;", c.fetchall())
   print("Імена клієнтів")
   for name_list in name_cus_tabl:
      print(f"{name_list[0]}")
   name = input("Введіть ім'я клієнта: ")

   id_name_list = c.execute("SELECT id_ch, name_ch FROM channels_list;", c.fetchall())
   for id_name in id_name_list:
      print(f"ID каналу: {id_name[0]}, назва каналу: {id_name[1]}")
   id_ch = input("Виберіть ID каналу: ")

   c.execute(f"SELECT name_ch FROM channels_list WHERE id_ch=={id_ch};")
   name_ch =((c.fetchall())[0])
   name_ch=name_ch[0]

   use = input("Чи має право користуватись даним каналом (0-ні, 1-так): ")

   c.execute(f"INSERT INTO {name} VALUES ({id_ch}, '{name_ch}', {use})")
   db.commit()

#додати канал до таблиці channels_list
def add_ch_to_ch_ls():
   id_com_list = c.execute("SELECT id_com, name FROM companys_ovn;", c.fetchall())
   for id_com in id_com_list:
      print(f"ID каналу: {id_com[0]}, назва каналу: {id_com[1]}")
   id_com=input("id_com: ")
   name_ch=input("name_ch: ")
   description=input("description: ")
   number_ch=input("number_ch: ")
   frequency_ch=float(input("frequency_ch: "))

   c.execute("INSERT INTO channels_list (id_com, name_ch, description, number_ch, frequency_ch) VALUES (?, ?, ?, ?, ? )", (id_com, name_ch, description, number_ch, frequency_ch))
   db.commit()

#додати клієнта до таблиці customers_list
def add_cust_to_cust_ls():
   name = input("ведіть імя клієнта: ")
   subscribe  = input("Чи оплачено послуги(0-ні, 1-так): ")
   c.execute("INSERT INTO customers_list (name, subscribe) VALUES (?, ?)", (name, subscribe))
   db.commit()

#додати компанію до таблиці companys_ovn
def add_com_to_com_ls():
   name=input("name: ")
   description=input("description: ")
   c.execute("INSERT INTO companys_ovn (name, description) VALUES (?, ?)", (name, description))
   db.commit()

#змінити інфу про наявні канали клієнта до таблиці "імя клієнта"
def update_use_in_costom():
   name_cus_tabl = c.execute("SELECT name FROM customers_list;", c.fetchall())
   print("Імена клієнтів")
   for name_list in name_cus_tabl:
      print(f"{name_list[0]}")
   name = input("Введіть ім'я клієнта: ")

   id_name_list = c.execute(f"SELECT channels_list.id_ch, channels_list.name_ch FROM channels_list, {name} WHERE channels_list.name_ch = {name}.name_ch ", c.fetchall())
   for id_name in id_name_list:
      print(f"ID каналу: {id_name[0]}, назва каналу: {id_name[1]}")
   id_ch = input("Виберіть ID каналу: ")

   c.execute(f"SELECT name_ch FROM channels_list WHERE id_ch=={id_ch};")
   name_ch = ((c.fetchall())[0])
   name_ch = name_ch[0]
   use=input("Дозволити доступ до каналу?(0-ні, 1-так): ")

   c.execute(f"UPDATE {name} SET use = {use} WHERE name_ch = '{name_ch}'")
   db.commit()

def del_cust():
   name_cus_tabl = c.execute("SELECT name FROM customers_list;", c.fetchall())
   for name_list in name_cus_tabl:
      print(f"{name_list[0]}")
   name=input("Введіть імя клієнта для видалення: ")
   c.execute(f"DELETE FROM customers_list WHERE name ='{name}'")
   db.commit()
   c.execute(f"DROP TABLE {name}")
   db.commit()

def sh_ch_list():
   channels_list = c.execute("SELECT * FROM channels_list;", c.fetchall())
   print("ID канала | ID компанії | назва | номер канала | робоча частота | опис")
   for ch_list in channels_list:
      print(f"{ch_list[0]} | {ch_list[1]} | {ch_list[2]} | {ch_list[4]} | {ch_list[5]} | {ch_list[3]}")
   db.commit()

def sh_cus_list():
   fil=int(input("Відфільтрувати за оплатою(0-неоплачено, 1-оплачено): "))
   name_ls=c.execute(f"SELECT * FROM customers_list WHERE subscribe = {fil}", c.fetchall())
   if fil == 0:
      print("Список клієнтів, що неоплатили:\n")
   elif fil==1:
      print("Список клієнтів, що оплатили:\n")
   for name in name_ls:
      print(f"ID клієнт: {name[0]}, і'мя клієнта: {name[1]}")
   db.commit()

ex = 0
while ex == 0:
   input("Головне меню(Enter)")
   menu_1_action=int(input("""Виберіть дію:
0 завершити роботу
1 додати до таблиць
2 редагувати доступ користувача до каналу
3 удалити клієнта
4 показати список каналів
5 показати клаєнтів
"""))

   if menu_1_action == 0:
      ex = 5
   elif menu_1_action == 1:
      menu_2_create =int( input ("""Виберіть дію:
0 повернутись в попереднє меню
1 Додати компанію до таблиці компаній
2 Додати канал до таблиці каналів
3 Додати клієнта до таблиці клієнтів
4 Створити таблицю клієнта
5 Додати канали до таблиці клієнта
"""))
      print(menu_2_create)
      if (menu_2_create) == 1:
         add_com_to_com_ls()
      elif menu_2_create == 2:
         add_ch_to_ch_ls()
      elif menu_2_create == 3:
         add_cust_to_cust_ls()
      elif menu_2_create == 4:
         create_cust_tabl()
      elif menu_2_create == 5:
         add_ch_to_cust()
   elif menu_1_action == 2:
      update_use_in_costom()
   elif menu_1_action == 3:
      del_cust()
   elif menu_1_action == 4:
      sh_ch_list()
   elif menu_1_action == 5:
      sh_cus_list()




db.close()
