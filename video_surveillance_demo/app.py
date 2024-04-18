import sys
sys.path.append('../')

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image
import cv2
import time
import sqlite3
import threading
import tkinter.messagebox as tmsg

from engine.header import *

database_file = "user.db"
MATCH_THRESHOLD = 0.82

def create_db():
	try:
		conn = sqlite3.connect(database_file)
		cursor = conn.cursor()
		create_table_sql = 'CREATE TABLE IF NOT EXISTS People (ID INTEGER PRIMARY KEY, Name TEXT, Template BLOB, Image BLOB)'
		cursor.execute(create_table_sql)
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		print(f"Database error: {e}")
		return False

def add_user(name, template, image_binary):
	if not os.path.exists(database_file):
		create_db()

	try:
		conn = sqlite3.connect(database_file)
		cursor=conn.cursor()
		cursor.execute('INSERT INTO People (Name, Template, Image) VALUES (?, ?, ?)', (name, template, sqlite3.Binary(image_binary)))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		print(f"Database error: {e}")
		return False

def load_users():
	if not os.path.exists(database_file):
		create_db()

	try:
		conn = sqlite3.connect(database_file)
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM People')
		rows = cursor.fetchall()
		users = []
		for row in rows:
			user_id, name, template_bytes, image_binary = row
			# Convert bytes back to the appropriate types
			template = list(template_bytes)
			try:
				image = Image.frombytes('RGB', (250,250), image_binary)
				user = {'id': user_id, 'name': name, 'template': template, 'image': image}
				users.append(user)
			except Exception as e:
				print(f"Error loading image for user {user_id}: {e}")
		conn.close()
		return users
	except sqlite3.Error as e:
		print(f"Database error: {e}")
		return []

def delete_db():
	if os.path.exists(database_file):
		os.remove(database_file)

class RegisterWindow:
	def __init__(self, parent_window):
		self.parent_window = parent_window 
		self.window = None

	def show_window(self):
		self.face_image = None
		self.face_template = None
		self.window = Toplevel()
		self.window.geometry('720x720')
		self.window.minsize(720,720)
		self.window.maxsize(720,720)
		self.window.title("Face Identification System")

		title = Label(self.window, text="Face Identification System",font=("bold", 20),anchor=CENTER,bg="#386184",fg="white")
		title.place(x=0,y=0, width=720)

		window_title = Label(self.window, text="Registration Form",font=("bold", 16),bg="#180020",fg='white')
		window_title.place(x=0,y=42, width=720)

		select_btn=Button(self.window, text="Select Image File",command=self.select_file)
		select_btn.place(x=300,y=120, width=120, height=40)
	
		image=Image.open("icons/image_border.jpg")
		photo=ImageTk.PhotoImage(image)
		photo_label=Label(self.window, image=photo)
		photo_label.place(x=235,y=250, width=250,height=250)
		photo_label.image = photo

		user_name=StringVar()
		name_lbl = Label(self.window, text="Name :",width=20,font=("bold", 12))
		name_lbl.place(x=120,y=550)
		name_input = Entry(self.window,width=40,textvar=user_name)
		name_input.place(x=260,y=550)
   
		register_btn = Button(self.window, text='Register',width=15,font=("bold",10),bg='brown',height=2,fg='white',command=lambda: self.register(user_name.get()))
		register_btn.place(x=300,y=600, width=120, height=40)

		self.window.protocol("WM_DELETE_WINDOW", self.delete_window)
		self.parent_window.withdraw()

	def delete_window(self):
		self.parent_window.deiconify()
		self.window.destroy()
		
	def select_file(self):
		file_path=filedialog.askopenfilename()
		image = cv2.imread(file_path)
		ret, face_result = detect_face(image, 1, ENGINE_MODE.M_ENROLL.value)
		if ret > 0:	
			pil_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			pil_image = Image.fromarray(pil_image)
			self.face_image = pil_image.crop((face_result[0].x1, face_result[0].y1, face_result[0].x2, face_result[0].y2))
			self.face_image = self.face_image.resize((250,250))
			self.face_template = face_result[0].feature
			photo=ImageTk.PhotoImage(self.face_image)
			photo_label=Label(self.window, image=photo,width=250,height=250)
			photo_label.place(x=235,y=250, width=250,height=250)
			photo_label.image = photo

			file_path_lbl = Label(self.window, text=file_path,width=70,font=("bold", 8),anchor=CENTER)
			file_path_lbl.place(x=0,y=180, width=720)
		else:
			tmsg.showinfo("Warning","Cannot detect face in selected image!")


	def register(self, user_name):
		if(user_name!="" and self.face_image!= None and self.face_template!= None):
			ret = add_user(user_name, bytes(self.face_template), self.face_image.tobytes())
			if ret:
				tmsg.showinfo("Success","New Face Recorded Successfully")
			else:
				tmsg.showinfo("Warning","Failed to Record New Face")
			self.delete_window()
		else:
			tmsg.showinfo("Warning","Please enter all (*) marked details")


class UserListWindow:
	def __init__(self, parent_window):
		self.parent_window = parent_window 
		self.window = None
		
	def show_window(self):
		self.appname="Face Identification System"
		self.window=Toplevel()
		self.window.geometry('720x720')
		self.window.minsize(720,720)
		self.window.maxsize(720,720)
		self.window.title(self.appname)
		self.window["bg"]='#382273'
		
		title = Label(self.window, text="Face Identification System",font=("bold", 20),anchor=CENTER,bg="#386184",fg="white")
		title.place(x=0,y=0, width=720)

		window_title = Label(self.window, text="User List",font=("bold", 16),bg="#180020",fg='white')
		window_title.place(x=0,y=42, width=720)
		
		self.tree= ttk.Treeview(self.window, columns=("NAME"),selectmode='browse')
		self.tree.heading("#0", text="IMAGE", anchor='center')
		self.tree.heading("NAME", text="NAME", anchor='center')
		self.tree.column("#0", minwidth=0, width=100, stretch=NO, anchor='center')
		self.tree.column("NAME", minwidth=0, width=200, stretch=NO, anchor='center')
		ttk.Style().configure("Treeview.Heading",font=('Calibri', 13,'bold'), foreground="red", relief="flat")
		ttk.Style().configure("Treeview", rowheight=100)
		self.tree.place(x=(720-300)//2, y=120, height=500)

		delete_btn=Button(self.window, text="Delete All Users",command=self.delete_users)
		delete_btn.place(x=300,y=650, width=120, height=40)

		self.enrolled_users = load_users()
		self.show_users()

		self.window.protocol("WM_DELETE_WINDOW", self.delete_window)
		self.parent_window.withdraw()
		
	def delete_window(self):
		self.parent_window.deiconify()
		self.window.destroy()

	def show_users(self):
		photo_list = []
		for user in self.enrolled_users:
			image = user['image']
			image = image.resize((70,70))
			tk_image = ImageTk.PhotoImage(image)

			self.tree.insert("", 'end', image=tk_image, values=(user['name']))
			photo_list.append(tk_image)
		self.tree.photo_list = photo_list

	def delete_users(self):
		value=tmsg.askquestion("WARNING !","Are you sure you want to delete all users?")
		if value=="yes":
			delete_db()
			for i in self.tree.get_children():
				self.tree.delete(i)

			tmsg.showinfo("Success","All users are removed.")

class PhotoMatchWindow:
	def __init__(self, parent_window):
		self.parent_window = parent_window 
		self.window = None

	def show_window(self):
		self.appname="Face Identification System"
		self.window=Toplevel()
		self.window.geometry('1280x720')
		self.window.minsize(1280,720)
		self.window.maxsize(1280,720)
		self.window.title(self.appname)
		
		title = Label(self.window, text="Face Identification System",font=("bold", 20),anchor=CENTER,bg="#386184",fg="white")
		title.place(x=0,y=0, width=1280)

		window_title = Label(self.window, text="Photo Match",font=("bold", 16),bg="#180020",fg='white')
		window_title.place(x=0,y=40, width=1280, height=40)

		select_btn=Button(self.window, text="Select Image File",command=self.select_file)
		select_btn.place(x=370,y=100, width=120, height=40)
		
		self.photo_label=Label(self.window)
		self.photo_label.place(x=0,y=170, width=860,height=550)

		self.tree= ttk.Treeview(self.window, columns=("NAME", "SCORE"),selectmode='browse')
		self.tree.heading("#0", text="IMAGE", anchor='center')
		self.tree.heading("NAME", text="NAME", anchor='center')
		self.tree.heading("SCORE", text="MATCHING %", anchor='center')

		self.tree.column("#0", minwidth=0, width=100, stretch=NO, anchor='center')
		self.tree.column("NAME", minwidth=0, width=200, stretch=NO, anchor='center')
		self.tree.column("SCORE", minwidth=0, width=120, stretch=NO, anchor='center')
		ttk.Style().configure("Treeview.Heading",font=('Calibri', 13,'bold'), foreground="red", relief="flat")
		ttk.Style().configure("Treeview", rowheight=80)
		self.tree.place(x=860, y=80, height=640)

		self.enrolled_users = load_users()

		self.window.protocol("WM_DELETE_WINDOW", self.delete_window)
		self.parent_window.withdraw()

	def select_file(self):
		file_path = filedialog.askopenfilename()
		file_path_lbl = Label(self.window, text=file_path,width=70,font=("bold", 8),anchor=CENTER)
		file_path_lbl.place(x=100,y=150, width=600)
		image = cv2.imread(file_path)
		if image is None or image.size == 0:
			tmsg.showinfo("Warning","Cannot read image file")
			return
		ret, face_result = detect_face(image, 10, ENGINE_MODE.M_IDENTIFY.value)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(image)
		
		height, width, _ = image.shape
		photo_label_width = self.photo_label.winfo_width()
		photo_label_height = self.photo_label.winfo_height()
		ratio = 1.0
		if width > photo_label_width or height > photo_label_height:
			ratio_xy = width / height
			if width / photo_label_width > height / photo_label_height:
				image = cv2.resize(image, (photo_label_width, int(photo_label_width/ratio_xy)))
				ratio = photo_label_width / width
			else:
				image = cv2.resize(image, (int(photo_label_height * ratio_xy), photo_label_height))
				ratio = photo_label_height / height

		self.clear_tree()
		if ret > 0:	
			font=cv2.FONT_HERSHEY_SIMPLEX
			photo_list = []
			for i in range(ret):
				face = face_result[i]
				if face.liveness == LIVENESS_CODE.L_REAL.value:
					color = (0,0,225)
				else:
					color = (255,0,0)
				name = 'unknown'
				max_similarity_score = 0
				max_similarity_person = None
				for user in self.enrolled_users:
					similarity_score = get_similarity(face.feature, (ctypes.c_ubyte * 2056)(*user["template"]))
					if similarity_score > MATCH_THRESHOLD:
						if similarity_score > max_similarity_score:
							max_similarity_score = similarity_score
							max_similarity_person = user

				if max_similarity_person is not None:
					name = max_similarity_person['name']
					face_image = pil_image.crop((face.x1, face.y1, face.x2, face.y2))
					face_image = face_image.resize((70,70))
					tk_image = ImageTk.PhotoImage(face_image)
					confidence=str(round(max_similarity_score*100,2))+"%"
					self.tree.insert("", 'end', image=tk_image, values=(name, confidence))
					photo_list.append(tk_image)
				
				x1 = int(face.x1 * ratio)
				y1 = int(face.y1 * ratio)
				x2 = int(face.x2 * ratio)
				y2 = int(face.y2 * ratio)
				cv2.rectangle(image,(x1, y1),(x2, y2),color,2)
				text_size, _ = cv2.getTextSize(name, font, 0.5, 1)
				cv2.rectangle(image,(x1, y1-text_size[1]),(x1+text_size[0], y1),color,cv2.FILLED)
				cv2.putText(image,name,(x1,y1),font,0.5,(225,225,225),1)

			self.tree.photo_list = photo_list

		photo = ImageTk.PhotoImage(Image.fromarray(image))
		self.photo_label.config(image=photo)
		self.photo_label.image = photo

	def clear_tree(self):
		for i in self.tree.get_children():
			self.tree.delete(i)

	def delete_window(self):
		self.parent_window.deiconify()
		if self.window is not None:
			self.clear_tree()
			self.window.destroy()
			self.window = None

class SurveillanceWindow:
	def __init__(self, parent_window):
		self.parent_window = parent_window 
		self.browser_window = None
		self.window = None

	def select_file(self):
		file_path=filedialog.askopenfilename()
		self.video_string.set(file_path)

	def show_video_browser(self):
		self.appname="Face Identification System"
		self.browser_window=Toplevel()
		self.browser_window.geometry('800x500')
		self.browser_window.minsize(800,500)
		self.browser_window.maxsize(800,500)
		self.browser_window.title(self.appname)
		self.browser_window["bg"]='#382273'
		
		self.label=Label(self.browser_window,text=self.appname,font=("bold",20),bg='blue',fg='white').pack(side=TOP,fill=BOTH)

		guide_lbl = Label(self.browser_window, text="Input video file path or RTSP URL",anchor=CENTER,font=("bold", 12), bg='#382273', fg='white')
		guide_lbl.place(x=0,y=120, width=800)
		self.video_string = StringVar()
		self.video_input = Entry(self.browser_window,textvar=self.video_string)
		self.video_input.place(x=100,y=160, width=400, height=40)
		select_btn=Button(self.browser_window, text="Select Video File",command=self.select_file)
		select_btn.place(x=510,y=160, width=100, height=40)
		start_btn = Button(self.browser_window, text='Start',width=15,font=("bold",10),bg='brown',height=2,fg='white',command=lambda: self.start_surveillance(self.video_string.get(), False))
		start_btn.place(x=620,y=160, width=100, height=40)

		webcam_lbl = Label(self.browser_window, text="Web CAM ID",anchor=CENTER,font=("bold", 12), bg='#382273', fg='white')
		webcam_lbl.place(x=0,y=270, width=800)
		webcam_id = StringVar()
		webcam_input = Entry(self.browser_window,textvar=webcam_id)
		webcam_input.place(x=300,y=310, width=100, height=40)
		webcam_start_btn = Button(self.browser_window, text='Use WebCam',width=15,font=("bold",10),bg='brown',height=2,fg='white',command=lambda: self.start_surveillance(webcam_id.get(), True))
		webcam_start_btn.place(x=410,y=310, width=100, height=40)

		self.browser_window.protocol("WM_DELETE_WINDOW", self.delete_browser_window)
		self.parent_window.withdraw()

	def start_surveillance(self, video_source, use_webcam=False):
		if video_source == '':
			tmsg.showinfo("Warning","Please select video input")
			return 

		if use_webcam:
			video_source = int(video_source)
			self.delay = 5
		else:
			if video_source.endswith((".mp4", ".avi", ".mov")):
				self.delay = 15 # modify based on video fps
			else:
				self.delay = 5

		self.vid = myvideocapture(video_source)
		vid_opened = self.vid.open()
		if vid_opened is False:
			tmsg.showinfo("Warning","Cannot open video input")
			return 

		self.height = 700
		self.ratio = self.height / self.vid.height
		self.width = int(self.ratio * self.vid.width)
		self.delete_browser_window(goto_main=False)

		self.cur_frame = None
		self.face_result = []
		self.detected_user = dict()
		self.lock = threading.Lock()
		self.update_history = False
		self.running = False

		self.appname="Face Identification System"
		self.window=Toplevel()
		self.window.title(self.appname)
		self.window["bg"]='#382273'
		
		self.label=Label(self.window,text=self.appname,font=("bold",20),bg='blue',fg='white').pack(side=TOP,fill=BOTH)

		self.canvas=Canvas(self.window,height=self.height,width=self.width,bg='#382273')
		self.canvas.pack(side=LEFT,fill=BOTH)

		self.tree= ttk.Treeview(self.window, columns=("NAME", "SCORE"),selectmode='browse')
		self.tree.heading("#0", text="IMAGE", anchor='center')
		self.tree.heading("NAME", text="NAME", anchor='center')
		self.tree.heading("SCORE", text="MATCHING %", anchor='center')
		self.tree.column("#0", minwidth=0, width=100, stretch=NO, anchor='center')
		self.tree.column("NAME", minwidth=0, width=200, stretch=NO, anchor='center')
		self.tree.column("SCORE", minwidth=0, width=120, stretch=NO, anchor='center')
		ttk.Style().configure("Treeview.Heading",font=('Calibri', 13,'bold'), foreground="red", relief="flat")
		ttk.Style().configure("Treeview", rowheight=80)
		self.tree.pack(side=RIGHT,fill=BOTH)

		self.window.protocol("WM_DELETE_WINDOW", self.delete_window)

		self.enrolled_users = load_users()

		self.engine_thread = threading.Thread(target=self.detect_face)
		self.engine_thread.start()
		self.update()

		
	def delete_browser_window(self, goto_main=True):
		if goto_main == True:
			self.parent_window.deiconify()
		if self.browser_window is not None:
			self.video_string.set('')
			self.browser_window.destroy()	
			self.browser_window = None

	def delete_window(self):
		self.parent_window.deiconify()
		if self.window is not None:
			for i in self.tree.get_children():
				self.tree.delete(i)
			
			self.window.destroy()
			self.window = None
		self.running = False


	def detect_face(self):
		self.running = True
		while self.running:
			start_time = time.time()
			with self.lock:
				if self.cur_frame is None:
					continue
				frame = self.cur_frame
			
			ret, face_result = detect_face(frame, 10, ENGINE_MODE.M_IDENTIFY.value)
			self.face_result = []
			if ret > 0:
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				pil_image = Image.fromarray(frame)
				for i in range(ret):
					face = face_result[i]
					name = 'unknown'
					max_similarity_score = 0
					max_similarity_person = None
					for user in self.enrolled_users:
						similarity_score = get_similarity(face.feature, (ctypes.c_ubyte * 2056)(*user["template"]))
						if similarity_score > MATCH_THRESHOLD:
							if similarity_score > max_similarity_score:
								max_similarity_score = similarity_score
								max_similarity_person = user

					if max_similarity_person is not None:
						name = max_similarity_person['name']
						face_image = pil_image.crop((face.x1, face.y1, face.x2, face.y2))
						face_image = face_image.resize((70,70))
						user = {'name': max_similarity_person['name'],'enrolled_image': max_similarity_person['image'], 'score':max_similarity_score, 'capture':face_image}
						self.detected_user[max_similarity_person['id']] = user
						self.update_history = True

					self.face_result.append({'name': name, 'detection': face})
				end_time = time.time()

	def update(self):
		isTrue,frame=self.vid.getframe()
		if isTrue:
			frame = cv2.resize(frame,(self.width, self.height))
			self.ratio = 1

			with self.lock:
				self.cur_frame = frame.copy()
			
			# frame = cv2.resize(frame,(self.width, self.height))
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			for face in self.face_result:
				x1 = int(face['detection'].x1 * self.ratio)
				y1 = int(face['detection'].y1 * self.ratio)
				x2 = int(face['detection'].x2 * self.ratio)
				y2 = int(face['detection'].y2 * self.ratio)

				if face['detection'].liveness == LIVENESS_CODE.L_REAL.value:
					color = (0,0,225)
				else:
					color = (255,0,0)
				cv2.rectangle(frame,(x1, y1),(x2, y2),color,2)
				font=cv2.FONT_HERSHEY_SIMPLEX
				text_size, _ = cv2.getTextSize(face['name'], font, 0.5, 1)
				cv2.rectangle(frame,(x1, y1-text_size[1]),(x1+text_size[0], y1),color,cv2.FILLED)
				cv2.putText(frame,face['name'],(x1,y1),font,0.5,(225,225,225),1)
			
			self.photo=ImageTk.PhotoImage(image=Image.fromarray(frame))
			self.canvas.create_image(0,0,image=self.photo,anchor=NW)		

			if self.update_history:
				self.update_history = False
				for i in self.tree.get_children():
					self.tree.delete(i)

				photo_list = []
				for id in self.detected_user.keys():
					confidence=str(round(self.detected_user[id]["score"]*100,2))+"%"
					tk_image = ImageTk.PhotoImage(self.detected_user[id]["capture"])
					self.tree.insert("", 'end', image=tk_image, values=(self.detected_user[id]['name'], confidence))
					photo_list.append(tk_image)
				self.tree.photo_list = photo_list

			self.window.after(self.delay,self.update)
		else:
			self.delete_window()

class myvideocapture:
	def __init__(self,video_source):
		self.video_source = video_source

	def open(self):
		self.vid=cv2.VideoCapture(self.video_source)
		if not self.vid.isOpened():
			print("unable to open", self.video_source)
			return False

		self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
		print(f"original frame size: {self.width}x{self.height}")
		return True

	def getframe(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			if ret:
				return (ret, frame)
			else:
				return (ret, None)
		else:
			return (False, None)

	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

class ApplicationWindow:
	def __init__(self):
		self.window = None

	def show_window(self):
		self.window = Tk()
		self.window.geometry('800x600')
		self.window.minsize(800,600)
		self.window.maxsize(800,600)

		self.window.title("Face Identification System")
		self.window.configure(bg="#382273")

		register_window = RegisterWindow(self.window)
		userlist_window = UserListWindow(self.window)
		surveillance_window = SurveillanceWindow(self.window)
		photomatch_window = PhotoMatchWindow(self.window)

		image=Image.open("icons/banner.jpg")
		photo=ImageTk.PhotoImage(image)
		photo_label=Label(image=photo,width=800,height=0,bg='white').place(x=0,y=0)
		photo_label

		title_lbl = Label(self.window, text="Face Identification System",width=50,font=("bold", 20),anchor=CENTER,bg="#386184",fg="white")
		title_lbl.place(x=0,y=100)

		Button(self.window, text='REGISTER PERSON',width=35,height=3,bg='blue',fg='white',font=("bold", 11),command=register_window.show_window).place(x=250,y=180)
		Button(self.window, text='USER LIST',width=35,height=3,bg='blue',fg='white',font=("bold", 11),command=userlist_window.show_window).place(x=250,y=260)
		Button(self.window, text='PHOTO MATCH',width=35,height=3,bg='blue',fg='white',font=("bold", 11),command=photomatch_window.show_window).place(x=250,y=340)
		Button(self.window, text='VIDEO SURVEILLANCE',width=35,height=3,bg='red',fg='white',font=("bold", 11),command=surveillance_window.show_video_browser).place(x=250,y=420)
		self.window.mainloop()

if __name__ == "__main__":
	ret = init_sdk()
	if ret != 0:
		exit(-1)
	application = ApplicationWindow()
	application.show_window()