import customtkinter
import tkinter as tk

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("450x400")
root.title("WatorPlus Settings")

# FUNCTION THAT START THE SIMULATION
def start():
    max_characters = 200
    min_gridsize = 100
    max_gridsize = 1000
    import WatorPlus_Simulation as wps
    from WatorPlus_Simulation import run
    if entryGridsize.get() == "" or entrySharks.get() == "" or entryFishes.get() == "" or entryJellys.get() == "":
        tk.messagebox.showwarning(title="Error!", message="All values must be specified!")
    elif int(entryGridsize.get()) < min_gridsize or int(entryGridsize.get()) > max_gridsize:
        tk.messagebox.showwarning(title="Error!", message="Grid size must be between %d and %d!" % (min_gridsize, max_gridsize))
    elif  int(entrySharks.get())>max_characters or int(entryFishes.get())>max_characters or int(entryJellys.get())>max_characters:
        tk.messagebox.showwarning(title="Error!", message="The max number of each character must be below %d!"%(max_characters))
    else:
        wps.grid_size = int(entryGridsize.get())
        wps.n_shark = int(entrySharks.get())
        wps.n_fish = int(entryFishes.get())
        wps.n_jelly = int(entryJellys.get())
        root.destroy()
        run() 

#FUNCTION THAT RESET DEFAULT VALUES 
def reset():
    entrySharks.delete(0, customtkinter.END)
    entrySharks.insert(0, "10")
    entryFishes.delete(0, customtkinter.END)
    entryFishes.insert(0, "100")
    entryJellys.delete(0, customtkinter.END)
    entryJellys.insert(0, "15")
    entryGridsize.delete(0, customtkinter.END)
    entryGridsize.insert(0, "1000")

#FUNCTION THAT VALIDATE IF A NUMBER IS >=1 AND ACCEPT IT 
def validate_number(value):
    # CHECK TO ALLOW TO CANCEL THE VALUE
    if value == "":
        return True
    # CHECK IF THE VALUE IS >=1
    try:
        number = int(value)
        if number >= 1:
            return True
        else:
            return False
    # IF THE VALUE IS NOT A NUMBER THAN IT CAN'T BE USED
    except ValueError:
        return False

# THE FUNCTION VALIDATE_NUMBER IS REGISTERED 
vcmd = (root.register(validate_number), "%P")
#FRAME
frame = customtkinter.CTkFrame(master=root)
frame.place(relx=0.5, rely=0.5, anchor="center")
#CREATING ALL THE DIFFERENT LABELS, ENTRYS AND BUTTONS
labelSharks = customtkinter.CTkLabel(master=frame, text="Number of sharks:")
labelSharks.grid(row=0, column=0, pady=12, padx=10, sticky="w")
entrySharks = customtkinter.CTkEntry(master=frame, placeholder_text="Insert...", validate="key", validatecommand=vcmd)
entrySharks.grid(row=0, column=1, pady=12, padx=10, sticky="w")
entrySharks.insert(0, "10")

labelFishes = customtkinter.CTkLabel(master=frame, text="Number of Fishes:")
labelFishes.grid(row=1, column=0, pady=12, padx=10, sticky="w")
entryFishes = customtkinter.CTkEntry(master=frame, placeholder_text="Insert...)", validate="key", validatecommand=vcmd)
entryFishes.insert(0, "100")
entryFishes.grid(row=1, column=1, pady=12, padx=10, sticky="w")

labelJellys = customtkinter.CTkLabel(master=frame, text="Number of Jellyfishes:")
labelJellys.grid(row=2, column=0, pady=12, padx=10, sticky="w")
entryJellys = customtkinter.CTkEntry(master=frame, placeholder_text="Insert...)", validate="key", validatecommand=vcmd)
entryJellys.insert(0, "15")
entryJellys.grid(row=2, column=1, pady=12, padx=10, sticky="w")

labelGridsize = customtkinter.CTkLabel(master=frame, text="Grid Size:")
labelGridsize.grid(row=4, column=0, pady=12, padx=10, sticky="w")
entryGridsize = customtkinter.CTkEntry(master=frame, placeholder_text="Insert...", validate="key", validatecommand=vcmd)
entryGridsize.insert(0, "1000")
entryGridsize.grid(row=4, column=1, pady=12, padx=10, sticky="w")


buttonConferma = customtkinter.CTkButton(master=frame, text="Start", command=start)
buttonConferma.grid(row=5, column=1, pady=12, padx=10, sticky="se")

buttonReset = customtkinter.CTkButton(master=frame, text="Reset defaul values", command=reset)
buttonReset.grid(row=5, column=0, pady=12, padx=10, sticky="sw")

root.mainloop()