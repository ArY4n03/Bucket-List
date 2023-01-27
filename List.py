#Importing Modules
import tkinter as tk 
from tkinter import messagebox as msg
from tkinter import ttk
import pickle
import os

class List(): #List Class
    def __init__(self,master):
        self.master = master
        master.geometry("1050x610")
        master.title("List")
        master.resizable(False,False)
        self.lists = []
        self.current_list = None
        self.current_list_data = None
        self.Font = (None,15)
        self.width = 40
        self.theme = tk.StringVar()
        self.bgcolor = "lightblue"
        self.tab_control = ttk.Notebook(master)
        
        #adding tabs
        self.Lists_tab = tk.Frame(self.tab_control,bg="lightblue")
        self.tab_control.add(self.Lists_tab,text="Lists")
        self.Add_list_tab = tk.Frame(self.tab_control,bg="lightblue")
        self.tab_control.add(self.Add_list_tab,text="Add List")
        self.help_tab = tk.Frame(self.tab_control,bg="lightblue")
        self.tab_control.add(self.help_tab,text="Help")
        self.tab_control.pack(expand=1,fill="both")

        #Adding widgets in lists tab

        #List tab content
        self.Frame1 = tk.Frame(self.Lists_tab,bg="lightblue")
        self.Frame1.grid(column=0,rowspan=50)
        
        self.Label = tk.Label(self.Frame1,text="List : ",font=self.Font,bg="lightblue").pack()
        self.lists_combobox = ttk.Combobox(self.Frame1,width=self.width,state="readonly",font=self.Font)
        self.lists_combobox.pack(padx=5,pady=10)

        self.scrollBar = tk.Scrollbar(self.Frame1)
        self.scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        self.listbox_data = tk.Listbox(self.Frame1,width=50,height=20,font=self.Font)
        self.listbox_data.pack(padx=5,pady=10)
        self.listbox_data.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.listbox_data.yview)
        
        self.Frame2 = tk.Frame(self.Lists_tab,bg="light blue")
        self.Frame2.grid(column=1,row=0)
        
        self.AddListDataEntry = tk.Entry(self.Frame2,width=self.width,font=self.Font)
        self.AddListDataEntry.pack(padx=15,pady=10)
        self.AddListDataButton = tk.Button(self.Frame2,text="Add list Data",font=self.Font,command=self.add_list_data).pack(padx=15,pady=10,fill=tk.X)
        self.DeleteListDataButton = tk.Button(self.Frame2,text="Delete List Data",font=self.Font,command=self.delete_list_data).pack(padx=15,pady=10,fill=tk.X)
        self.LoadListDataButton = tk.Button(self.Frame2,text="Load List Data",font=self.Font,command=self.load_list_data).pack(padx=15,pady=10,fill=tk.X)
        self.SaveListDataButton = tk.Button(self.Frame2,text="Save List Data",font=self.Font,command=self.save_list_data).pack(padx=15,pady=10,fill=tk.X)
        self.RefreshButton = tk.Button(self.Frame2,text="Refresh",font=self.Font,command=self.load_list_data).pack(padx=15,pady=10,fill=tk.X)
        self.DeleteListButton = tk.Button(self.Frame2,text="Delete List",font=self.Font,command=self.delete_list).pack(padx=15,pady=10,fill=tk.X)

        #Add list tab content
        self.ListNameLabel = tk.Label(self.Add_list_tab,text="List Name : ",font=self.Font,bg="lightblue").grid(column=0,row=0,padx=5,pady=10,sticky=tk.W)
        self.ListName = tk.Entry(self.Add_list_tab,width=self.width,font=self.Font)
        self.ListName.grid(column=1,row=0,pady=10)
        self.createListButton = tk.Button(self.Add_list_tab,text="Create List",font=self.Font,command=self.create_list).grid(columnspan=5,row=1,padx=50,pady=50)

        #help tab content
        self.shortcut_keys = tk.Text(self.help_tab,bg="lightblue",width=25,height=10,font=self.Font)
        self.shortcut_keys.insert(1.0,"Ctrl + S to save list items")
        self.shortcut_keys.insert(1.0,"Ctrl + Q to load list items \n")
        self.shortcut_keys.insert(1.0,"Ctrl + D to delete list item \n")
        self.shortcut_keys.insert(1.0,"Ctrl + A to add list item \n")
        self.shortcut_keys.insert(1.0," \n")
        self.shortcut_keys.insert(1.0,"Shortcut keys \n")
        self.shortcut_keys.config(state="disabled")
        self.shortcut_keys.grid(row=0,column=0,padx=20,pady=10)
        
        #binding shortcut keys
        self.bind_shortcutKeys()
        
        #loading lists
        self.load_lists()
        if len(self.lists) >= 1:
            self.lists_combobox.current(0)
        self.load_list_data() #loading list datas
        self.update_lists() #updating lists
        
    def update_lists(self):
        List = []
        try:
            for list_name in self.lists: #checking every value in the list (which are list file names)
                if os.path.exists(f"Lists\{list_name}.list"):
                    List.append(str(list_name)) # adding every one of them to new list
                else:
                    pass
                
        except Exception as e:
            msg.showerror(title="error",message=f" error : {e} ")
        self.lists = List # putting the value of list into another list which contains the list file names
        self.save_lists() #saving lists
        self.load_lists() #loading lists
        if len(self.lists) >= 1:
            self.lists_combobox.current(0)
        self.load_list_data() #loading list datas
        
    def load_lists(self):
        try:
            file = open("list name.file","rb")
            self.lists = pickle.load(file)
            file.close()
        except Exception as e:
            print(e)
        self.lists_combobox['values'] = self.lists
        
    def save_lists(self):
        try:
            file = open("list name.file","wb")
            pickle.dump(self.lists,file)
            file.close()
        except Exception as e:
            print(e)
    
    def add_list_data(self,*args):
        print(tk.END)
        #adding data to listbox
        list_data = self.AddListDataEntry.get()
        if list_data != "":
            self.listbox_data.insert(tk.END,list_data)
        else:
            msg.showwarning(title="Warning",message="You must enter a data")
        self.AddListDataEntry.delete(0,tk.END)

    def delete_list_data(self,*args):
        try:
            selected_list_data = self.listbox_data.curselection()[0]
            print(str(selected_list_data))
            self.listbox_data.delete(selected_list_data)
        except:
            msg.showwarning(title="Warning",message="You must select a data")

    def load_list_data(self,*args):
        try:
            list_name = self.lists_combobox.get()
            if list_name != "":
                list_file = open(f"Lists\{list_name}.list","rb")
                list_data = pickle.load(list_file)
                list_file.close()
                self.listbox_data.delete(0,tk.END)
                for data in list_data:
                    self.listbox_data.insert(tk.END,data)
                
        except Exception as e:
            print(e)
            
    def save_list_data(self,*args):
        list_name = self.lists_combobox.get()
        try:
            list_file = open(f"Lists\{list_name}.list","wb")
            listbox_content = self.listbox_data.get(0,tk.END)
            pickle.dump(listbox_content,list_file)
            list_file.close()
            
        except Exception as e:
            print(e)

    def create_list(self):
        try:
            list_name = self.ListName.get()
            if list_name != "":
                list_data = []
                file = open(f"Lists\{list_name}.list","wb")
                pickle.dump(list_data,file)
                file.close()
                self.lists.append(list_name)
                self.save_lists()
                self.load_lists()

                self.ListName.delete(0,tk.END)
            else:
                msg.showwarning(title="warning",message="You Must enter list name and list data file name")
        except:
            msg.showwarning(title="warning",message="something is wrong")

    def delete_list(self):
        list_name = self.lists_combobox.get()
        delete = msg.askyesnocancel(title="Delete list",message="Are you sure you want to delete this list")
        if delete:
            try:
                if os.path.exists(f"Lists\{list_name}.list"):
                    os.remove(f"Lists\{list_name}.list")
                    self.update_lists()
            except Exception as e:
                print(e)
        else:
            pass
      
    def bind_shortcutKeys(self):
        #control + A to add list data
        #control + D to delete list data
        #control + Q to load list data
        #control + S to save list data
        self.master.bind('<Control-a>',self.add_list_data)
        self.master.bind('<Control-d>',self.delete_list_data)
        self.master.bind('<Control-q>',self.load_list_data)
        self.master.bind('<Control-s>',self.save_list_data)
    
if __name__ == "__main__":
    master = tk.Tk()
    list_ = List(master)
    master.mainloop()
