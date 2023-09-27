import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-database.db")
        self.cursor = self.con.cursor()
        self.create_task_table()

    # create the task table
    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks("
                            "id integer PRIMARY KEY AUTOINCREMENT , "
                            "task varchar(150) NOT NULL, "
                            "due_date varchar(50), "
                            "completed BOOLEAN NOT NULL CHECK(completed IN (0,1)))"
                            "")
        self.con.commit()

    # creating the task
    def create_task(self, task, due_date=None):
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?,?,?)", (task, due_date, 0))
        self.con.commit()

        # getting the last entered item so we can add it to the task list
        created_task = self.cursor.execute("SELECT id, task, due_date from tasks where task = ? and completed = 0",
                                           (task,)).fetchall()

        return created_task[-1] # return last created task from selected list .fetchall()

    # getting the task
    def get_task(self):
        """getting all tasks : completed and incompleted"""
        incompleted_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        completed_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        return completed_task, incompleted_task

    # updating the tasks
    def mark_task_as_completed(self, taskid):
        """mark tasks as completed"""
        self.cursor.execute("UPDATE tasks SET completed = 1 where id = ?", (taskid,))
        self.con.commit()

    def mark_task_as_incompleted(self, taskid):
        """mark tasks as incompleted"""
        self.cursor.execute("UPDATE tasks SET completed = 0 where id = ?", (taskid,))
        self.con.commit()

        # return the task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text[0][0]

    # deleting the task
    def delete_task(self, taskid):
        """delete a task"""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit()

    # close the connection
    def close_db_connection(self):
        self.con.close()





























