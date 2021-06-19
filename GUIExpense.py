# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
# ttk is theme of Tk

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Uncle Engineer')
#GUI.geometry('700x700+50+10')
w = 700
h = 600

ws = GUI.winfo_screenwidth()
hs = GUI.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 20

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI หลัก

#######MENU Bar#######
menubar = Menu(GUI)
GUI.config(menu=menubar)

#file menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Google Sheet')

#Help
def About():
	messagebox.showinfo('About','โปรแกรมนี้เป็นโปรแกรมบันทึกข้อมูล\nสนใจบริจาคติดต่อได้เลย')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

donatmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donat',menu=donatmenu)
#######################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

icon_t1 = PhotoImage(file='Add.png').subsample(15) #  .subsample(2) = ย่อรูป
icon_t2 = PhotoImage(file='list.png').subsample(6)

Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')

F1 = Frame(T1)
#F1.place(x=100,y=50)
F1.pack()

days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัสบดี',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(event=None):
	expense = v_expense.get()
	price = v_price.get()
	quantity = v_quantity.get()

	if expense == '':
		print('No Data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกราคา')
		return
	elif quantity == '':
		quantity = 1

	total = float(price) * float(quantity)
	try:
		total = float(price) * float(quantity)
		# .get() คือดึงค่ามาจาก v_expense = StringVar()
		print('รายการ: {} ราคา: {}'.format(expense,price))
		print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total))
		text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
		text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
		v_result.set(text)
		# clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')

		# บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
		today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
		print(today)
		stamp = datetime.now()
		dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
		transactionid = stamp.strftime('%Y%m%d%H%M%f')
		dt = days[today] + '-' + dt
		with open('savedata.csv','a',encoding='utf-8',newline='') as f:
			# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
			# newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้างฟังชั่นสำหรับเขียนข้อมูล
			data = [transactionid,dt,expense,price,quantity,total]
			fw.writerow(data)

		# ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
		E1.focus()
		resulttable.delete(*resulttable.get_children())
		update_table()
		update_record()
	except:
		print('ERROR')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')

# ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New'
FONT2 = ('Angsana New',16)

#------Image--------
main_icon = PhotoImage(file='Wallet.png').subsample(5)
Mainicon = Label(F1,image=main_icon)
Mainicon.pack()

#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-------------------

#------text2--------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#--------------------

#------text3--------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-------------------

icon_b1 = PhotoImage(file='save.png').subsample(5)

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('--------ผลลัพธ์--------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)
GUI.bind('<Tab>',lambda x: E2.focus())

#Tab2
#L = ttk.Label(T2,text='ตารางแสดงรายการทั้งหมด',font=FONT1).pack()
def read_csv():
	with open('savedata.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data

def update_record():
	getdata = read_csv()
	v_allrecord.set('')
	text = ''
	for d in getdata[1:]:
		text2 = '{}---{}---{}---{}---{}\n'.format(d[0],d[1],d[2],d[3],[4])
		text = text + text2

	v_allrecord.set(text)

v_allrecord = StringVar()
v_allrecord.set('---------All Record-------')
#Allrecord = ttk.Label(T2,textvariable=v_allrecord,font=(FONT2,14),foreground='green')
#Allrecord.pack()

#TREEVIEW
L = ttk.Label(T2,text='ตารางแสดงรายการทั้งหมด',font=FONT1).pack()
header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2, columns=header, show='headings',height=10)
resulttable.pack()

for hd in header:
	resulttable.heading(hd,text=hd)

headerwidth = [120,150,170,80,80,80]
for hd,W in zip(header,headerwidth):
	resulttable.column(hd,width=W)

alltransaction = {}
def UpdateCSV():
	with open('savedata.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f) #เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
		data = list(alltransaction.values())
		fw.writerows(data)
		print('Table was updated')
		
def DeleteRecord(event=None):
	check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
	print('YES/NO:',check)

	if check == True:

		print('delete')
		select = resulttable.selection()
		print(select)
		data = resulttable.item(select)
		data = data['values']
		transactionid = data[0]
		#print(transactionid)
		#print(type(transactionid))
		del alltransaction[str(transactionid)]  # Delete date in dict
		#print(alltransaction)
		UpdateCSV()
		update_table()
	else:
		print('Cancle')

BDelete = ttk.Button(T2,text='Delete',command=DeleteRecord)
BDelete.place(x=50,y=550)

resulttable.bind('<Delete>',DeleteRecord)

def update_table():
	resulttable.delete(*resulttable.get_children())
	try:
		getdata = read_csv()
		for dt in getdata:
			alltransaction[dt[0]] = dt #dt[0] = transectionid
			resulttable.insert('',0,value=dt)
		print(alltransaction)
	except  Exception as e:
		print('No File')

####Right Click Menu#####
def EditRecord():
	POPUP = Toplevel()  #คล้ายๆ Tk() แต่ Tk() ประกาศได้ครั้งเดียว
	POPUP.title('Edit Record')
	#POPUP.geometry('500x400')
	w = 500
	h = 400

	ws = POPUP.winfo_screenwidth()
	hs = POPUP.winfo_screenheight()

	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2) - 20

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

	
	L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
	v_expense = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
	E1.pack()
	#-------------------

	#------text2--------
	L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
	v_price = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
	E2.pack()
	#--------------------

	#------text3--------
	L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
	v_quantity = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
	E3.pack()

	def Edit(even=None):
		#print(transactionid)
		#print(alltransaction)
		olddata = alltransaction[str(transactionid)]
		print('OLD',olddata)
		v1 = v_expense.get()
		v2 = float(v_price.get())
		v3 = float(v_quantity.get())
		total = v2 * v3
		newdata = [olddata[0],olddata[1],v1,v2,v3,total]
		alltransaction[str(transactionid)] = newdata
		UpdateCSV()
		update_table()
		POPUP.destroy() #สั่งปิด popup หลังจากแก้ค่าเสร็จ
	

	icon_b1 = PhotoImage(file='save.png').subsample(5)

	B2 = ttk.Button(POPUP,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Edit)
	B2.pack(ipadx=50,ipady=20,pady=20)

	select = resulttable.selection()
	print(select)
	data = resulttable.item(select)
	data = data['values']
	transactionid = data[0]
	#set ค่าล่าสุดไว้ตรงช่องกรอกค่า
	v_expense.set(data[2])
	v_price.set(data[3])
	v_quantity.set(data[4])


	POPUP.mainloop()
	#-------------------



rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)

def menupopup(event):
	#print(event.x_root,event.y_root)
	rightclick.post(event.x_root,event.y_root)

resulttable.bind('<Button-3>',menupopup)







update_table()

update_record()

GUI.mainloop()
