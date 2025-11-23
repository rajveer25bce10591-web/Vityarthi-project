# Farming Advisor  
import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime

# ---- Crops ----
crops = {
    "wheat":{"n":"Wheat","min":15,"max":25,"icon":"🌾"},
    "rice":{"n":"Rice","min":20,"max":35,"icon":"🌾"},
    "corn":{"n":"Corn","min":18,"max":32,"icon":"🌽"},
    "tomato":{"n":"Tomato","min":18,"max":29,"icon":"🍅"},
    "potato":{"n":"Potato","min":15,"max":22,"icon":"🥔"}
}

# ---- Fake Weather ----
def wdata():
    w={}
    w["t"]=round(15+random.random()*20,1)
    w["h"]=round(40+random.random()*50,1)
    w["rain"]=random.random()>0.6
    w["soil"]=round(20+random.random()*60,1)
    w["wind"]=round(5+random.random()*25,1)
    w["cond"]=random.choice(["Sunny","Cloudy","Rainy"])
    days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    today=datetime.today().weekday()
    w["f"]=[]
    for i in range(7):
        w["f"].append({"d":days[(today+i)%7],"t":round(15+random.random()*20),"r":random.random()>0.6})
    return w

# ---- Advisories ----
def advs(sel,w):
    a=[]
    for c in sel:
        cp=crops[c]
        if w["t"]<cp["min"]-5: a.append(f"{cp['n']} 🔴 VERY COLD {w['t']}C")
        elif w["t"]>cp["max"]+5: a.append(f"{cp['n']} 🔴 TOO HOT {w['t']}C")
        if w["soil"]<25: a.append(f"{cp['n']} 🔴 Soil low {w['soil']}%, water now!")
        elif w["soil"]<40 and not w["rain"]: a.append(f"{cp['n']} 🟡 Soil kinda low, maybe water")
        if w["wind"]>20: a.append(f"{cp['n']} 🟡 Wind strong {w['wind']} km/h")
    return a

# ---- GUI ----
class App:
    def __init__(self,r):
        self.r=r
        r.title("Farm Adviser 😅")
        r.geometry("700x600")
        self.w=wdata()
        self.sel=[]
        self.vars={}
        # weather text
        self.wtxt=tk.Text(r,height=8)
        self.wtxt.pack(fill="x",padx=10,pady=5)
        # forecast
        self.ftxt=tk.Text(r,height=4)
        self.ftxt.pack(fill="x",padx=10,pady=5)
        # crops
        for k in crops:
            v=tk.IntVar()
            self.vars[k]=v
            cb=tk.Checkbutton(r,text=f"{crops[k]['icon']} {crops[k]['n']}",variable=v,command=self.upd)
            cb.pack(anchor="w",padx=20)
        # buttons
        tk.Button(r,text="Refresh Weather",command=self.ref).pack(pady=5)
        tk.Button(r,text="Show Advisories",command=self.show).pack(pady=5)
        # adv display
        self.atxt=tk.Text(r,height=15)
        self.atxt.pack(fill="both",padx=10,pady=5,expand=True)
        # init
        self.upd_w()

    def upd(self):
        self.sel=[k for k,v in self.vars.items() if v.get()==1]

    def upd_w(self):
        self.wtxt.delete(1.0,tk.END)
        w=self.w
        self.wtxt.insert(1.0,f"Cond:{w['cond']}\nTemp:{w['t']}C\nHum:{w['h']}%\nSoil:{w['soil']}%\nWind:{w['wind']} km/h")
        self.ftxt.delete(1.0,tk.END)
        s=""
        for d in w["f"]:
            s+=f"{d['d']}:{d['t']}C {'🌧️' if d['r'] else '☀️'}  "
        self.ftxt.insert(1.0,s)

    def ref(self):
        self.w=wdata()
        self.upd_w()
        messagebox.showinfo("Ok","Weather refreshed!")

    def show(self):
        self.atxt.delete(1.0,tk.END)
        if len(self.sel)==0:
            self.atxt.insert(1.0,"Select crops first! ⚠️")
            return
        a=advs(self.sel,self.w)
        if len(a)==0:
            self.atxt.insert(1.0,"No alerts! ✅")
        else:
            for x in a:
                self.atxt.insert(tk.END,x+"\n")

# ---- run ----
root=tk.Tk()
app=App(root)
root.mainloop()

