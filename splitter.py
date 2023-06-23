from tkinter import Label, Button, Tk, Spinbox, filedialog
import os
from PyPDF2 import PdfWriter, PdfReader

pdf = None


def browse_files():
    succes_message.config(text="")
    file_path = filedialog.askopenfilename(
        title="Open a file", filetypes=[("pdf file", "*.pdf")]
    )
    if file_path:
        global file
        file = open(file_path, "rb")
        selected_file_name.config(text="Selected file: " + os.path.basename(file_path))
        button_split["state"] = "normal"
        global pdf
        pdf = PdfReader(file)
        global file_length
        file_length = len(pdf.pages)
        spinbox.config(to=file_length)


def split_files():
    pages_per_file = spinbox.get()
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        page_count = file_length
        current_page = 0
        current_file = 1
        while current_page < page_count:
            writer = PdfWriter()
            for i in range(int(pages_per_file)):
                if current_page < page_count:
                    outputFileName = (
                        selected_directory
                        + "/"
                        + str(current_file)
                        + os.path.basename(file.name)
                    )
                    writer.addPage(pdf.getPage(current_page))
                    current_page += 1
            with open(outputFileName, "wb") as out:
                writer.write(out)
            current_file += 1
        succes_message.config(
            text="Congratulations Jagoda! You split the pdf! Good job!"
        )


def validate(value):
    if pdf:
        return value.isdigit() and int(value) <= file_length
    return value.isdigit()


root = Tk()
root.title("PDF Splitter")
root.geometry("600x400")
root.tk_setPalette(background="white")

input_file_label = Label(
    root, text="Select PDF file to split:", font=("Calibri", 14, "bold")
)
input_file_label.pack(pady=(20, 0))

button_explore = Button(
    root, text="Browse Files", command=browse_files, font=("Calibri", 10)
)
button_explore.pack(pady=(5, 0))

selected_file_name = Label(root, font=("Calibri", 10, "italic"))
selected_file_name.pack()

page_count_label = Label(
    root, text="How many pages per file:", font=("Calibri", 14, "bold")
)
page_count_label.pack(pady=(20, 0))

spinbox = Spinbox(
    root,
    from_=1,
    to=100,
    width=6,
    font=("Calibri", 10),
    validate="key",
    vcmd=(root.register(validate), "%P"),
)
spinbox.pack(pady=(5, 0))

button_split = Button(
    root,
    text="Split",
    command=split_files,
    state="disabled",
    font=("Calibri", 10),
)
button_split.pack(pady=(30, 0))

succes_message = Label(
    root,
    font=("Calibri", 14, "bold"),
    fg="#f00",
)
succes_message.pack(pady=(30, 0))

root.mainloop()
