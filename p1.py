from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
import bs4

try:
	location = input("enter location ")
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric" 
	a2 = "&q=" + location
	a3 = "&appid=" + "e381d3fa0d79b42a188ca7c04e99efa8"

	wa = a1 + a2 + a3
	res = requests.get(wa)
	print(res)

	data = res.json()
	main = data['main']

	name = data['name']	
	temp = main['temp']

except Exception as e:
	print("issue ", e)

try:
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	print(res)

	data = bs4.BeautifulSoup(res.text, 'html.parser')
	info = data.find('img', {'class':'p-qotd'})
	msg = info['alt']

except Exception as e:
	print('issue', e)

def f1():
	add_window.deiconify()
	main_window.withdraw()

def f2():
	main_window.deiconify()
	add_window.withdraw()

def f3():
	con = None
	try:
		con = connect('stu.db')
		cursor = con.cursor()
		sql = "insert into student values('%d', '%s', '%d')"
		rno = int(add_window_ent_rno.get()) 
		if rno <= 0:
			raise Exception("rno should have only positive integers")
		rno = int(rno)
		name = add_window_ent_name.get()
		if (len(name) < 2) or (not name.isalpha()):
			raise Exception("name should be in alphabets with min. length 2")
		marks = int(add_window_ent_marks.get())
		if marks < 0 or marks > 100:
			raise Exception("marks should be in range of 0-100")
		marks = int(marks)
		cursor.execute(sql % (rno, name, marks))
		con.commit()
		showinfo('Success', 'record added')
	except ValueError:
		showerror('Failure', 'you need to enter integers only')
	except ValueError as m:
		showerror('Failure', m)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def f4():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0, END)
	info = ""
	con = None
	try:
		con = connect('stu.db')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " rno: " + str(d[0]) + "      name: " + str(d[1]) + "      marks: " + str(d[2]) + "\n\n"
		print(info)
		view_window_st_data.insert(INSERT, info)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def f5():
	main_window.deiconify()
	view_window.withdraw()

def f6(): 
	update_window.deiconify()
	main_window.withdraw()
	
def f7():
	main_window.deiconify()
	update_window.withdraw()

def f8():
	con = None
	try:
		con = connect('stu.db')
		cursor = con.cursor()
		sql = "update student set name='%s', marks='%d' where rno='%d'"
		rno = int(update_window_ent_rno.get())
		if rno <= 0:
			raise Exception("rno should have only positive integers")
		rno = int(rno)
		name = update_window_ent_name.get()
		if (len(name) < 2) or (not name.isalpha()):
			raise Exception("name should be in alphabets with min. length 2")
		marks = int(update_window_ent_marks.get())
		if marks < 0 or marks > 100:
			raise Exception("marks should be in range of 0-100")
		marks = int(marks)
		cursor.execute(sql % (name, marks, rno))
		if cursor.rowcount > 0:
			con.commit()
			showinfo('Success', 'record updated')
	except ValueError:
		showerror('Failure', 'you need to enter integers only')
	except ValueError as m:
		showerror('Failure', m)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def f9():
	delete_window.deiconify()
	main_window.withdraw()

def f10():
	main_window.deiconify()
	delete_window.withdraw()

def f11():
	con = None
	try:
		con = connect('stu.db')
		cursor = con.cursor()
		sql = "delete from student where rno='%d' "
		rno = int(delete_window_ent_rno.get())
		rno = int(rno)
		cursor.execute(sql % (rno))
		if cursor.rowcount > 0:
			con.commit()
			showinfo('Success', 'record deleted')
		else:
			showerror('Failure', 'rno does not exists')	
	except ValueError:
		showerror('Failure', 'alphabets are not allowed')	
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()

def read_from_db():
	cursor.execute('SELECT name, marks FROM student')
	for row in cursor.fetchall():
		print(row)

def f12():
	chart_window.deiconify()
	main_window.withdraw()
	con = connect('stu.db')
	cursor = con.cursor()
	cursor.execute('SELECT name, marks FROM student')
	name = []
	marks = []
	for row in cursor.fetchall():
		name.append(row[0])
		marks.append(row[1])
	plt.bar(name, marks, width=0.8, color=['red','green','blue'])
	plt.title('Batch Information!')
	plt.ylabel('Marks')
	plt.show()
		
def f13():
	main_window.deiconify()
	chart_window.withdraw()

main_window = Tk()
main_window.title("S. M. S")
main_window.geometry=("500x500+400+100")
main_window.configure(bg='honeydew2')

main_window_btn_add = Button(main_window, text = "Add", font=('Calibri', 23, 'bold'), width=10, borderwidth=1, relief='solid', command=f1)
main_window_btn_view = Button(main_window, text = "View", font=('Calibri', 23, 'bold'), width=10, borderwidth=1, relief='solid', command=f4)
main_window_btn_update = Button(main_window, text = "Update", font=('Calibri', 23, 'bold'), width=10, borderwidth=1, relief='solid', command=f6)
main_window_btn_delete = Button(main_window, text = "Delete", font=('Calibri', 23, 'bold'), width=10, borderwidth=1, relief='solid', command=f9)
main_window_btn_chart = Button(main_window, text = "Charts", font=('Calibri', 23, 'bold'), width=10, borderwidth=1, relief='solid', command=f12)
main_window_lbl_loc = Label(main_window, font=('Times New Roman', 22, 'bold'), height=1, borderwidth=2, relief='solid', bg='honeydew2')
main_window_lbl_loc.config(text = "Location: " + str(name)  +  "           Temp: " + str(temp ))
main_window_lbl_qotd = Label(main_window, font=('Times New Roman', 22, 'bold'), height=1, borderwidth=2, relief='solid', bg='honeydew2')
main_window_lbl_qotd.config(text = "QOTD: " + str(msg ))

main_window_btn_add.pack(pady=10)
main_window_btn_view.pack(pady=10)
main_window_btn_update.pack(pady=10)
main_window_btn_delete.pack(pady=10)
main_window_btn_chart.pack(pady=10)
main_window_lbl_loc.pack(pady=10)
main_window_lbl_qotd.pack(pady=10)

add_window = Toplevel(main_window)
add_window.title("Add St. ")
add_window.geometry("500x530+500+500")
add_window.configure(bg='lavender')

add_window_lbl_rno = Label(add_window, text="enter rno:", font=('Cambria', 20, 'bold'), bg='lavender')
add_window_ent_rno = Entry(add_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
add_window_lbl_name = Label(add_window, text="enter name:", font=('Cambria', 20, 'bold'), bg='lavender')
add_window_ent_name = Entry(add_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
add_window_lbl_marks = Label(add_window, text="enter marks:", font=('Cambria', 20, 'bold'), bg='lavender')
add_window_ent_marks = Entry(add_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
add_window_btn_save = Button(add_window, text="Save", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f3)
add_window_btn_back = Button(add_window, text="Back", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f2)

add_window_lbl_rno.pack(pady=10)
add_window_ent_rno.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=10)
add_window_ent_marks.pack(pady=10)
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()

view_window = Toplevel(main_window)
view_window.title("View St. ")
view_window.geometry("500x530+500+500")
view_window.configure(bg='wheat1')

view_window_st_data = ScrolledText(view_window, width=30, height=10, font=('Cambria', 20, 'bold'), bg='wheat1')
view_window_btn_back = Button(view_window, text="Back", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f5)
view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()

update_window = Toplevel(main_window)
update_window.title("Update St. ")
update_window.geometry("500x530+500+500")
update_window.configure(bg='misty rose')

update_window_lbl_rno = Label(update_window, text="enter rno:", font=('Cambria', 20, 'bold'), bg='misty rose')
update_window_ent_rno = Entry(update_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
update_window_lbl_name = Label(update_window, text="enter name:", font=('Cambria', 20, 'bold'), bg='misty rose')
update_window_ent_name = Entry(update_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
update_window_lbl_marks = Label(update_window, text="enter marks:", font=('Cambria', 20, 'bold'), bg='misty rose')
update_window_ent_marks = Entry(update_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
update_window_btn_save = Button(update_window, text="Save", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f8)
update_window_btn_back = Button(update_window, text="Back", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f7)

update_window_lbl_rno.pack(pady=10)
update_window_ent_rno.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_marks.pack(pady=10)
update_window_ent_marks.pack(pady=10)
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()

delete_window = Toplevel(main_window)
delete_window.title("Delete St. ")
delete_window.geometry("500x530+500+500")
delete_window.configure(bg='azure2')

delete_window_lbl_rno = Label(delete_window, text="enter rno:", font=('Cambria', 20, 'bold'), bg='azure2')
delete_window_ent_rno = Entry(delete_window, borderwidth=1, relief='solid', font=('Cambria', 20, 'bold'))
delete_window_btn_save = Button(delete_window, text="Save", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f11)
delete_window_btn_back = Button(delete_window, text="Back", font=('Calibri', 20, 'bold'), width=10, borderwidth=1, relief='solid', command=f10)

delete_window_lbl_rno.pack(pady=10)
delete_window_ent_rno.pack(pady=10)
delete_window_btn_save.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()

chart_window = (main_window)

main_window.mainloop()