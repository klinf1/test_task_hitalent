import csv
import os


class Task():
    '''
    Class for Task objects

    Attributes:
    id
        unique for each Task object
    title: str
        the title of the Task
    description: str
        brief description of the Tast
    category: str
        what category Task belongs to e.g. Study or Work
    due_date: str
        date that the task is due
    prio: str
        Task priority
    status: str
        the status of Taks's completion

    Methods:
    write_csv(): writes the current task to a data.csv file
    in the current directory
    '''

    def __init__(self,
                 id,
                 title: str,
                 description: str,
                 category: str,
                 due_date: str,
                 prio: str,
                 status: str):
        '''
        Parameters:
        id
            unique for each Task object
        title: str
            the title of the Task
        description: str
            brief description of the Tast
        category: str
            what category Task belongs to e.g. Study or Work
        due_date: str
            date that the task is due
        prio: str
            Task priority
        status: str
            the status of Taks's completion
        '''
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.prio = prio
        self.status = status

    def write_csv(self) -> None:
        '''Writes the current task to a data.csv file
           in the current directory
        '''
        to_write = {}
        for attr, value in self.__dict__.items():
            to_write[attr] = value
        with open('data.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=to_write.keys())
            writer.writerow(to_write)


def main():
    if not os.path.isfile('data.csv'):
        with open('data.csv', 'w', newline='') as file:
            fieldnames = ['id',
                          'title',
                          'description',
                          'category',
                          'due_date',
                          'prio',
                          'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    a = Task(3, 'a', 'b', 'c', 'd', 'e', 'f')
    a.write_csv()


if __name__ == "__main__":
    main()
