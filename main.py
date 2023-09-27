from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.list import TwoLineAvatarListItem, ILeftBody, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

# importin the database class from database file
from database import Database

# instantiating the Database class by crating a db object
db = Database()

from datetime import datetime


class DialogContent(MDBoxLayout):
    # the init function for class constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")

    # this function will show the date picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    # this function will get the date and saves in a friendly form
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)


# class for marking and deleting the list item
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):  # pk - primary key, unique identifier for each list item, by default = None
        super().__init__(**kwargs)
        self.pk = pk

    # marking the item as complete or incomplete
    def mark(self, check, the_list_item):
        if check.active:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_completed(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incompleted(the_list_item.pk))

    # deleting the list item
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)


class LeftCheckbox(ILeftBody, MDCheckbox):
    pass


# this is the main App class
class MainApp(MDApp):
    # Flag
    task_list_dialog = None

    # this is the build function for setting the theme
    def build(self):
        self.theme_cls.primary_palette = ("Orange")

    # this is the show task function
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create task",
                type="custom",
                content_cls=DialogContent()
            )
        self.task_list_dialog.open()

    # adding tasks
    def add_task(self, task, task_date):
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)
        # self.root.ids['container'].add_widget(ListItemWithCheckbox(
        #     text = '[b]' + task.text + '[/b]',
        #     secondary_text = task_date))
        self.root.ids['container'].add_widget(ListItemWithCheckbox(
            pk=created_task[0],
            text='[b]' + created_task[1] + '[/b]',
            secondary_text=created_task[2]))
        task.text = ''

    # this is a dialog closing function
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def on_start(self):
        """this is to load the saved tasks and add them to the list widget"""
        completed_tasks, incompleted_tasks = db.get_task()

        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                self.root.ids.container.add_widget(add_task)
        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text="[s]" + task[1] + "[/s]", secondary_text=task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)


if __name__ == "__main__":
    app = MainApp()
    app.run()
# 43:56
