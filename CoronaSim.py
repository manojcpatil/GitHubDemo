from tkinter import *
import random
import time
import numpy as np

tk=Tk()
tk.geometry("700x700")
canvas=Canvas(tk,width=600,height=600,bg="yellow")
tk.title("Corona Simulation")
canvas.pack()

def dist(L1,L2):
	sum=0
	for i in range(4):
		sum+=(L1[i]-L2[i])*(L1[i]-L2[i])
	return np.sqrt(sum)

class Persons:
	def __init__(self):
		posi=np.random.randint(0,600,2)
		self.person=canvas.create_oval(posi[0],posi[1],posi[0]+5,5+posi[1],fill="green")
		self.xshift=random.randint(1,3)
		self.yshift=random.randint(1,3)
		self.corona=0
		self.days=0
		self.death=0
		self.pos=canvas.coords(self.person)

	def movement(self):
		canvas.move(self.person,self.xshift,self.yshift)
		self.pos=canvas.coords(self.person)
		if self.pos[3]>=600 or self.pos[1]<=0:
			self.yshift=-np.random.uniform(0.9,1.1)*self.yshift
		if self.pos[2]>=600 or self.pos[0]<=0:
			self.xshift=-np.random.uniform(0.9,1.1)*self.xshift
frame=Frame(tk).pack(side=BOTTOM)
pop_var=IntVar()
inf_var=IntVar()

L1=Label(frame,text="Population",width=0).pack(side=LEFT)
E1=Entry(frame,textvariable=pop_var,width=3).pack(side=LEFT)
L2=Label(frame,text="Startly Infected",width=0).pack(side=LEFT)
E2=Entry(frame,textvariable=inf_var,width=3).pack(side=LEFT)

Inf_var=IntVar()
Death_var=IntVar()
Cured_var=IntVar()
NotInf_var=IntVar()
Active_var=IntVar()

L4=Label(frame,text="Currently Infected :",width=0).pack(side=LEFT)
E4=Entry(frame,textvariable=Inf_var,width=3).pack(side=LEFT)

L5=Label(frame,text="Deaths :",width=0).pack(side=LEFT)
E5=Entry(frame,textvariable=Death_var,width=3).pack(side=LEFT)

L6=Label(frame,text="Cured :",width=0).pack(side=LEFT)
E6=Entry(frame,textvariable=Cured_var,width=3).pack(side=LEFT)

L7=Label(frame,text="Still Active :",width=0).pack(side=LEFT)
E7=Entry(frame,textvariable=Active_var,width=3).pack(side=LEFT)

L8=Label(frame,text="Not infected :",width=0).pack(side=LEFT)			
E8=Entry(frame,textvariable=NotInf_var,width=3).pack(side=LEFT)

def simulate():
	newperson=[]
	ninfected=inf_var.get()
	pop=pop_var.get()
	ncured=ndeaths=0
	for i in range(pop-ninfected):
		newperson.append(Persons())

	for i in range(ninfected):
		temp=Persons()
		temp.corona=1
		temp.days=1
		canvas.itemconfig(temp.person,fill="red")
		newperson.append(temp)

	while True:
		for i in newperson:
			if i.death<1:
				i.movement()
				for j in newperson:
					if dist(i.pos,j.pos)<=20 and j.death!=1:
						if max(i.corona,j.corona)==1:
							ninfected+=(i.corona==0)
							ninfected+=(j.corona==0)
							canvas.itemconfig(i.person,fill="red")
							canvas.itemconfig(j.person,fill="red")
							i.corona=j.corona=1
				i.days+=(i.corona==1)
				if i.days>=150 and i.corona<2:
					i.death=np.random.binomial(1,0.05+0.15*((ninfected-ndeaths)>=0.3*pop),1)
					if i.death==1:
						canvas.itemconfig(i.person,fill="black")
						ndeaths+=1
					else:
						canvas.itemconfig(i.person,fill="brown")
						ncured+=1	
						i.corona=2
				
			Inf_var.set(ninfected)
			Death_var.set(ndeaths)
			Cured_var.set(ncured)
			Active_var.set(ninfected-ndeaths-ncured)
			NotInf_var.set(pop-ninfected)

		tk.update()
		time.sleep(0.01)


B1=Button(frame,text="Simulate",command=simulate).pack(side=LEFT)
tk.mainloop()



