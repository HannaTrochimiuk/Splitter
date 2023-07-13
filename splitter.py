from tkinter import Label, Button, Tk, Spinbox, filedialog
import os
from PyPDF2 import PdfWriter, PdfReader


class PdfSplitter:
    def __init__(self):
        self.pdf = None

    def browse_files(self):
        succes_message.config(text="")
        file_path = filedialog.askopenfilename(
            title="Open a file", filetypes=[("pdf file", "*.pdf")]
        )
        if file_path:
            self.file = open(file_path, "rb")
            selected_file_name.config(
                text="Selected file: %s" % os.path.basename(file_path)
            )
            button_split["state"] = "normal"
            self.pdf = PdfReader(self.file)
            self.file_length = len(self.pdf.pages)
            spinbox.config(to=self.file_length)

    def split_files(self):
        pages_per_file = spinbox.get()
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            page_count = self.file_length
            current_page = 0
            current_file = 1
            while current_page < page_count:
                writer = PdfWriter()
                for i in range(int(pages_per_file)):
                    if current_page < page_count:
                        outputFileName = "%s/%s%s" % (
                            selected_directory,
                            str(current_file),
                            os.path.basename(self.file.name),
                        )
                        writer.addPage(self.pdf.getPage(current_page))
                        current_page += 1
                with open(outputFileName, "wb") as out:
                    writer.write(out)
                current_file += 1
            succes_message.config(
                text="Congratulations Jagoda! You split the pdf! Good job!"
            )

    def validate(self, value):
        if self.pdf:
            return value.isdigit() and int(value) <= self.file_length
        return value.isdigit()


root = Tk()
root.title("PDF Splitter")
root.geometry("600x400")
root.tk_setPalette(background="white")

pdfSplitter = PdfSplitter()

input_file_label = Label(
    root, text="Select PDF file to split:", font=("Calibri", 14, "bold")
)
input_file_label.pack(pady=(20, 0))

button_explore = Button(
    root, text="Browse Files", command=pdfSplitter.browse_files, font=("Calibri", 10)
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
    vcmd=(root.register(pdfSplitter.validate), "%P"),
)
spinbox.pack(pady=(5, 0))

button_split = Button(
    root,
    text="Split",
    command=pdfSplitter.split_files,
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
