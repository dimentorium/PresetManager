from tkinter import *
from tkinter.ttk import *

class ScrollableFrame(Frame):
    """Scrollable frame widget

    Arguments:
        Frame {Frame} -- Base class from TKinter
    """
    def __init__(self, container, *args, **kwargs):
        """Initialize scrollable frame widget

        Arguments:
            container {unknown} -- parent widget where frame is placed in
        """
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")