'''
copyright bibekghimire99@gmail.com
version 1.1
windows and linux only
'''
VERSION=' BU 1.2'
import os,sys,shelve
try:
    from meta import contact
    import sys
    import glob,shelve,os
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    sys.exit(0)
sys.path.append(os.getcwd())



fields=('Name','Mobile','Home','Office','Email')
update=False
forgot_list=[]
id_list=[]


top=tk.Tk()
frame=tk.Frame(top)
frame.master.maxsize(400,400)
frame.grid()
'''
child widgets
'''
search_entry=tk.Entry(frame)
e1=tk.Entry(frame)
e2=tk.Entry(frame)
e3=tk.Entry(frame)
e4=tk.Entry(frame)
e5=tk.Entry(frame)
entries=[e1,e2,e3,e4,e5]

b1=tk.Button(frame)
b2=tk.Button(frame)
b3=tk.Button(frame)


contact_list=tk.Listbox(frame,font='helbeticaBold 20')
scroll_bar=tk.Scrollbar(frame)

contact_list['yscrollcommand']=scroll_bar.set
scroll_bar['command']=contact_list.yview


def directory():
    if os.name=='nt':
        if os.path.exists(r'c:/Users/'+os.getlogin()+'/BU/pb'):
            path=r'c:/Users/'+os.getlogin()+'/BU/pb/'
        else :
            path=os.makedirs(r'c:/Users/'+os.getlogin()+'/BU/pb/')
    elif os.name=='posix':
        if os.path.exists(r'/home/'+os.getlogin()+'/BU/pb'):
            path=r'/home/'+os.getlogin()+'/BU/pb'
        else:
            path=os.makedirs(r'/home/'+os.getlogin()+'/BU/pb')
    else:
        sys.exit(0)
    return path

def get_ID():
    try:
        db=shelve.open(path+'pb')
        ID=db['Id']
        db.close()
    except KeyError:
        ID=[]
    print('ID:',ID)
    return ID
    
def get_id():
    db=shelve.open(path+'pb')
    try:
        max_id=sorted([eval(k) for k in db.keys() if k!='Id'])[-1]
    except:
        max_id=0
    print('max:',max_id)
    db.close()
    ID=get_ID()
    if ID :
        r=str(ID.pop())
        update_ID(ID)
        print('r:',r)
        return r
    else:
        print('max+1:',str(max_id + 1))
        return str(max_id + 1)


def update_ID(ID):
    db=shelve.open(path+'pb')
    db['Id']=ID
    db.close()
    print('ID:',ID)
    
    
def get_contact():
    db=shelve.open(path+'pb')
    try:
        #ID=db['Id']
        return sorted([db[Id] for Id in db.keys() if Id!='Id'])
    except KeyError:
        return []

def save(entries,c=None):
    def empty():
        for item in entries:
            if item.get():
                return False
        return True
    def create():
        #print(*[entries[i].get() for i in range(len(entries))],_id)
        name,mobile,home,office,email=[entries[i].get() for i in range(len(entries))]
        #name=name or email or mobile or home or office
        c=contact(name=name,mobile=mobile,home=home,office=office,email=email,id_=_id)
        db=shelve.open(path+'pb')
        db[c.id_]=c
        db.close()
        main()
    if empty():
        main()
    else:
        if update:
            _id=c.id_
        else:
            _id=get_id()
        create()
        
    

def delete(c):
    boo=messagebox.askyesno('delete?','are you sure you want to delete?')
    if boo==True:
        ID=get_ID()
#        if ID:
#            ID.append(c.id_)
#        else:
        ID.append(c.id_)
        update_ID(ID)
        db=shelve.open(path+'pb')
        db.pop(c.id_)
        db.close()
        main()
    else:
        pass
def forgot():
    global forgot_list
    for item in forgot_list:
        item.grid_forget()
    forgot_list=[]
def c_grid(w,cnf={},**kw):
    global forgot_list
    forgot_list.append(w)
    w.grid(cnf,**kw)

def b_rename(b,n):
    for i in range(len(b)):
        b[i].config(text=n[i])



def main():
    global id_list
    global update
    update=False
    id_list=[]
    frame.master.maxsize(400,400)
    update=False
    forgot()
    frame.master.title('contacts'+VERSION)
    contact_list.delete(0,'end')
    search_entry.delete(0,'end')
    b1.config(text='Add New')
    c_grid(search_entry,row=0,column=0,columnspan=10,sticky=tk.E+tk.W)
    c_grid(b1,row=0,column=11,columnspan=2)
    c_grid(contact_list,row=1,column=0,columnspan=11,rowspan=12,sticky=tk.E+tk.W+tk.N+tk.S)
    c_grid(scroll_bar,row=1,column=11,rowspan=12,sticky=tk.N+tk.S)

    contact_list.bind('<Double-1>',lambda x:view())
    b1.bind('<ButtonRelease-1>',lambda x: edit())
    search_entry.bind('<KeyRelease>',search)
    
    contacts=get_contact()
    contact_list.insert('end',*contacts)
    for id_ in [item.id_ for item in get_contact()]:
        id_list.append(id_)
    
    

def view():
    global update
    update=True
    frame.master.maxsize(400,400)
    #contacts=get_contact()
    #contacts_name=[item.get['name'] for item in get_contact()]
    #i=contacts_name.index(contact_list.get(contact_list.curselection()))
    try:
        id_=id_list[contact_list.curselection()[0]]
        db=shelve.open(path+'pb')
        c=db[id_]
        db.close()
    except IndexError:
        c=None
    #ct=contacts_name.count(contact_list.get(contact_list.curselection()))
    frame.master.title(c)
    forgot()
    var=('Back','Delete','Edit')
    b_rename((b1,b2,b3),var)
    contact_list.delete(0,'end')
    c_grid(contact_list,row=1,column=0,columnspan=11,rowspan=12)
    c_grid(scroll_bar,row=1,column=11,rowspan=12,sticky=tk.N+tk.S)
    c_grid(b1,row=0,column=0,columnspan=3,sticky=tk.E+tk.W)
    c_grid(b2,row=13,column=0,columnspan=5,sticky=tk.E+tk.W)
    c_grid(b3,row=13,column=5,columnspan=5,sticky=tk.E+tk.W)
    contact_list.unbind('<Double-1>')

    b1.bind('<ButtonRelease-1>',lambda x: main())
    b2.bind('<ButtonRelease-1>',lambda x: delete(c) )
    b3.bind('<ButtonRelease-1>',lambda x: edit(c))

    if c:
        contact_list.insert('end',*[field + '  :  '+c.get[field.lower()] for field in fields])
    else:
        contact_list.insert('end','sorry no fields found')
    
    
    
def edit(c=None):
    frame.master.maxsize(200,200)
    forgot()
    
    global update
    def cancel():
        ask = messagebox.askyesnocancel(title='save on close',message='do yo want to save contact: {0} before closing?'.format(entries[0].get()))
        if ask==True:
            save(entries,c)
        elif ask==False:
            main()
        else:
            pass
        
    frame.master.title('edit window')
    var=('back','save')
    b_rename((b2,b3),var)
    labels=[tk.Label(frame,text=item) for item in fields]
    entries=[tk.Entry(frame,bg='yellow') for item in fields]
    for i,lb,en in zip(tuple(range(len(labels))),labels,entries):
        c_grid(lb,column=0,row=i,columnspan=2,rowspan=1,sticky=tk.E+tk.W)
        c_grid(en,column=2,row=i,columnspan=6,rowspan=1,sticky=tk.E+tk.W)
    c_grid(b2,column=0,row=i+1,columnspan=3)
    c_grid(b3,column=3,row=i+1,columnspan=3)

    b2.bind('<ButtonRelease-1>',lambda x: cancel())
    b3.bind('<ButtonRelease-1>',lambda x: save(entries,c))
    if c:
        for e,f in zip(entries,fields):
            if c.get[f.lower()]:
                e.insert('end',c.get[f.lower()])
        
    else:
        update=False
    
    
def search(event=None):
    global id_list
    id_list=[]
    contact_list.delete(0,'end')
    text=search_entry.get().strip()
    for name,id_ in [[item.get['name'],item.id_] for item in get_contact()]:
        if text in name:
            contact_list.insert('end',name)
            id_list.append(id_)
            
        else:
            pass   


path=directory()
main()
tk.mainloop()
