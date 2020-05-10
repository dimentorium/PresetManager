class ChoiceDialog(simpledialog.Dialog):
    """ChoiceDialog.

    Dialog for selecting an item from a list of possible choices.
    Class is derived from simpledialog.Dialog

    Methods
    -------
        init: init class and set properties
        body: build user interface
        validate: check if input is ok
        apply: update return values

    Properties
    ----------
        selection: selected item
        items: list of items from which can be selected
        text: title of dialog
        message: label to show text message
        tree: tree from which the item is selected
    """

    def __init__(self, parent, title: str, text: str, items: list):
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            parent: parent frame calling dialog
            title: title of dialog
            text: message for user
            items: list for selection
        """
        #init properties
        self.selection = None
        self._items = items
        self._text = text

        #call parent function from tkinter
        super().__init__(parent, title=title)

    def body(self, parent) -> Treeview:
        """Body.

        Builds user interface
        
        Parameters
        ----------
            parent: dialog root
            
        Returns:
        -------
            tree: tree for selection
        """
        #configure message label
        self._message = Label(parent, text=self._text)
        self._message.pack(expand=1, fill=BOTH, padx=5, pady=5)

        #configure treeview
        self._tree = Treeview(parent)
        self._tree.pack(expand=1, fill=BOTH, side=TOP, padx=5, pady=5)
        for item in self._items:
            self._tree.insert("", END, text=self._items[item].preset_name)
        return self._tree

    def validate(self) -> int:
        """Validate.

        Function validating user data
            
        Returns:
        -------
            int: 1 for OK, 0 for not ok
        """
        #if no item is selected, than result is not valid
        if len(self._tree.selection()) == 0:
            return 0
        return 1

    def apply(self):
        """apply.

        Store selected data in selection.
        """
        self.selection = self._tree.item(self._tree.focus())