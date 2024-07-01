from tkinter import *
import tkinter.messagebox
import MiniProject_Backend

class Movie:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Movie Ticket Booking System")
        self.root.geometry("1200x700")
        self.root.config(bg="black")
        self.root.resizable(True, True)

        Movie_Name = StringVar()
        Movie_ID = StringVar()
        Release_Date = StringVar()
        Director = StringVar()
        Cast = StringVar()
        Budget = StringVar()
        Duration = StringVar()
        Rating = StringVar()

        # Functions
        def iExit():
            iExit = tkinter.messagebox.askyesno("Online Movie Ticket Booking System", "Are you sure you want to exit?")
            if iExit > 0:
                root.destroy()
            return

        def clcdata():
            self.txtMovie_ID.delete(0, END)
            self.txtMovie_Name.delete(0, END)
            self.txtRelease_Date.delete(0, END)
            self.txtDirector.delete(0, END)
            self.txtCast.delete(0, END)
            self.txtBudget.delete(0, END)
            self.txtRating.delete(0, END)
            self.txtDuration.delete(0, END)

        def adddata():
            if len(Movie_ID.get()) != 0:
                try:
                    MiniProject_Backend.AddMovieRec(Movie_ID.get(), Movie_Name.get(), Release_Date.get(),
                                                    Director.get(), Cast.get(), Budget.get(), Duration.get(), Rating.get())
                    disdata()  # Refresh the listbox after adding a new record
                    tkinter.messagebox.showinfo("Success", "Record has been inserted")
                except sqlite3.IntegrityError:
                    tkinter.messagebox.showerror("Error", "Movie ID must be unique")

        def disdata():
            MovieList.delete(0, END)
            for row in MiniProject_Backend.ViewMovieData():
                movie_details = f"ID: {row[1]}, Name: {row[2]}, Release Date: {row[3]}, Director: {row[4]}, Cast: {row[5]}, Budget: {row[6]}, Duration: {row[7]}, Rating: {row[8]}"
                MovieList.insert(END, movie_details)

        def movierec(event):
            global sd
            searchmovie = MovieList.curselection()[0]
            sd = MovieList.get(searchmovie).split(", ")

            self.txtMovie_ID.delete(0, END)
            self.txtMovie_ID.insert(END, sd[0].split(": ")[1])
            self.txtMovie_Name.delete(0, END)
            self.txtMovie_Name.insert(END, sd[1].split(": ")[1])
            self.txtRelease_Date.delete(0, END)
            self.txtRelease_Date.insert(END, sd[2].split(": ")[1])
            self.txtDirector.delete(0, END)
            self.txtDirector.insert(END, sd[3].split(": ")[1])
            self.txtCast.delete(0, END)
            self.txtCast.insert(END, sd[4].split(": ")[1])
            self.txtBudget.delete(0, END)
            self.txtBudget.insert(END, sd[5].split(": ")[1])
            self.txtDuration.delete(0, END)
            self.txtDuration.insert(END, sd[6].split(": ")[1])
            self.txtRating.delete(0, END)
            self.txtRating.insert(END, sd[7].split(": ")[1])

        def deldata():
            if len(Movie_ID.get()) != 0:
                MiniProject_Backend.DeleteMovieRec(sd[0].split(": ")[1])
                clcdata()
                disdata()
                tkinter.messagebox.showinfo("Success", "Record has been deleted")

        def searchdb():
            MovieList.delete(0, END)
            for row in MiniProject_Backend.SearchMovieData(Movie_ID.get(), Movie_Name.get(), Release_Date.get(),
                                                           Director.get(), Cast.get(), Budget.get(), Duration.get(), Rating.get()):
                movie_details = f"ID: {row[1]}, Name: {row[2]}, Release Date: {row[3]}, Director: {row[4]}, Cast: {row[5]}, Budget: {row[6]}, Duration: {row[7]}, Rating: {row[8]}"
                MovieList.insert(END, movie_details)

        def searchByName():
            MovieList.delete(0, END)
            for row in MiniProject_Backend.SearchMovieByName(Movie_Name.get()):
                movie_details = f"ID: {row[1]}, Name: {row[2]}, Release Date: {row[3]}, Director: {row[4]}, Cast: {row[5]}, Budget: {row[6]}, Duration: {row[7]}, Rating: {row[8]}"
                MovieList.insert(END, movie_details)

        def updata():
            if len(Movie_ID.get()) != 0:
                MiniProject_Backend.DeleteMovieRec(sd[0].split(": ")[1])
            if len(Movie_ID.get()) != 0:
                MiniProject_Backend.AddMovieRec(Movie_ID.get(), Movie_Name.get(), Release_Date.get(),
                                                Director.get(), Cast.get(), Budget.get(), Duration.get(), Rating.get())
                disdata()  # Refresh the listbox after updating the record
                tkinter.messagebox.showinfo("Success", "Record has been updated")

        # Frames
        MainFrame = Frame(self.root, bg="black")
        MainFrame.grid(sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        TFrame = Frame(MainFrame, bg="black", relief=RIDGE)
        TFrame.grid(row=0, column=0, sticky="ew")
        MainFrame.grid_columnconfigure(0, weight=1)

        self.TFrame = Label(TFrame, font=('Arial', 30, 'bold'), text="ONLINE MOVIE TICKET BOOKING SYSTEM", bg="black", fg="orange", wraplength=1100)
        self.TFrame.grid(pady=10)

        BFrame = Frame(MainFrame, bg="black", relief=RIDGE)
        BFrame.grid(row=2, column=0, sticky="ew", pady=10)

        DFrame = Frame(MainFrame, bg="black", relief=RIDGE)
        DFrame.grid(row=1, column=0, sticky="nsew", pady=10)
        MainFrame.grid_rowconfigure(1, weight=1)

        DFrameL = LabelFrame(DFrame, bg="black", relief=RIDGE, font=('Arial', 12, 'bold'), text="Movie Info", fg="white")
        DFrameL.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        DFrame.grid_columnconfigure(0, weight=3)
        DFrame.grid_rowconfigure(0, weight=1)

        DFrameR = LabelFrame(DFrame, bg="black", relief=RIDGE, font=('Arial', 12, 'bold'), text="Movie Details", fg="white")
        DFrameR.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        DFrame.grid_columnconfigure(1, weight=1)

        # Labels & Entry Box
        entry_width = 30

        self.lblMovie_ID = Label(DFrameL, font=('Arial', 12, 'bold'), text="Movie ID:", padx=2, pady=2, bg="black", fg="orange")
        self.lblMovie_ID.grid(row=0, column=0, sticky=W)
        self.txtMovie_ID = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Movie_ID, width=entry_width, bg="black", fg="white")
        self.txtMovie_ID.grid(row=0, column=1)

        self.lblMovie_Name = Label(DFrameL, font=('Arial', 12, 'bold'), text="Movie Name:", padx=2, pady=2, bg="black", fg="orange")
        self.lblMovie_Name.grid(row=1, column=0, sticky=W)
        self.txtMovie_Name = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Movie_Name, width=entry_width, bg="black", fg="white")
        self.txtMovie_Name.grid(row=1, column=1)

        self.lblRelease_Date = Label(DFrameL, font=('Arial', 12, 'bold'), text="Release Date:", padx=2, pady=2, bg="black", fg="orange")
        self.lblRelease_Date.grid(row=2, column=0, sticky=W)
        self.txtRelease_Date = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Release_Date, width=entry_width, bg="black", fg="white")
        self.txtRelease_Date.grid(row=2, column=1)

        self.lblDirector = Label(DFrameL, font=('Arial', 12, 'bold'), text="Director:", padx=2, pady=2, bg="black", fg="orange")
        self.lblDirector.grid(row=3, column=0, sticky=W)
        self.txtDirector = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Director, width=entry_width, bg="black", fg="white")
        self.txtDirector.grid(row=3, column=1)

        self.lblCast = Label(DFrameL, font=('Arial', 12, 'bold'), text="Cast:", padx=2, pady=2, bg="black", fg="orange")
        self.lblCast.grid(row=4, column=0, sticky=W)
        self.txtCast = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Cast, width=entry_width, bg="black", fg="white")
        self.txtCast.grid(row=4, column=1)

        self.lblBudget = Label(DFrameL, font=('Arial', 12, 'bold'), text="Budget:", padx=2, pady=2, bg="black", fg="orange")
        self.lblBudget.grid(row=5, column=0, sticky=W)
        self.txtBudget = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Budget, width=entry_width, bg="black", fg="white")
        self.txtBudget.grid(row=5, column=1)

        self.lblDuration = Label(DFrameL, font=('Arial', 12, 'bold'), text="Duration:", padx=2, pady=2, bg="black", fg="orange")
        self.lblDuration.grid(row=6, column=0, sticky=W)
        self.txtDuration = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Duration, width=entry_width, bg="black", fg="white")
        self.txtDuration.grid(row=6, column=1)

        self.lblRating = Label(DFrameL, font=('Arial', 12, 'bold'), text="Rating:", padx=2, pady=2, bg="black", fg="orange")
        self.lblRating.grid(row=7, column=0, sticky=W)
        self.txtRating = Entry(DFrameL, font=('Arial', 12, 'bold'), textvariable=Rating, width=entry_width, bg="black", fg="white")
        self.txtRating.grid(row=7, column=1)

        # ListBox & ScrollBar
        scrollbar = Scrollbar(DFrameR)
        scrollbar.grid(row=0, column=1, sticky='ns')

        MovieList = Listbox(DFrameR, width=100, height=16, font=('Arial', 12, 'bold'), yscrollcommand=scrollbar.set)
        MovieList.bind('<<ListboxSelect>>', movierec)
        MovieList.grid(row=0, column=0, padx=8)
        scrollbar.config(command=MovieList.yview)

        # Buttons
        btn_bg_color = "orange"
        btn_fg_color = "black"
        btn_font = ('Arial', 12, 'bold')

        self.btnAddNew = Button(BFrame, text="Add New", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=adddata)
        self.btnAddNew.grid(row=0, column=0, padx=5, pady=10)

        self.btnDisplay = Button(BFrame, text="Display", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=disdata)
        self.btnDisplay.grid(row=0, column=1, padx=5, pady=10)

        self.btnClear = Button(BFrame, text="Clear", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=clcdata)
        self.btnClear.grid(row=0, column=2, padx=5, pady=10)

        self.btnDelete = Button(BFrame, text="Delete", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=deldata)
        self.btnDelete.grid(row=0, column=3, padx=5, pady=10)

        self.btnSearch = Button(BFrame, text="Search", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=searchdb)
        self.btnSearch.grid(row=0, column=4, padx=5, pady=10)

        self.btnSearchByName = Button(BFrame, text="Search by Name", font=btn_font, height=1, width=15, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=searchByName)
        self.btnSearchByName.grid(row=0, column=5, padx=5, pady=10)

        self.btnUpdate = Button(BFrame, text="Update", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=updata)
        self.btnUpdate.grid(row=0, column=6, padx=5, pady=10)

        self.btnExit = Button(BFrame, text="Exit", font=btn_font, height=1, width=10, bd=4, bg=btn_bg_color, fg=btn_fg_color, command=iExit)
        self.btnExit.grid(row=0, column=7, padx=5, pady=10)


if __name__ == '__main__':
    root = Tk()
    application = Movie(root)
    root.mainloop()
