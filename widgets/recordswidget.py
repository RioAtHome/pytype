import urwid

PATH = "./user_records.json"


class RecordsPile(urwid.Pile):
    def __init__(self, user_records=None):
        widget_title = urwid.Text("User Previous Records:")
        num, wpm, acc, timer, date = urwid.Text("Number"), urwid.Text("WPM"),
        urwid.Text("ACC"), urwid.Text("TIMER"), urwid.Text("DATE")

        information_col = urwid.Columns([num, wpm, acc, timer, date])
        divider = urwid.Divider('-')
        components = [widget_title, divider, information_col, divider]
        super().__init__(components)

        if not user_records:
            no_records = urwid.Text("No Previous Records")
            super().widget_list.append(no_records)
            return

        for entry, index in zip(user_records, range(len(user_records))):
            num = urwid.Text(f"- {index+1}")
            wpm = urwid.Text(f'{entry["Word Per Min"]}')
            acc = urwid.Text(f'{entry["Accuracy"]}')
            timer = urwid.Text(f'{entry["Timer"]}')
            date = urwid.Text(f'{entry["Date"]}')
            col = urwid.Columns([num, wpm, acc, timer, date])
            super().widget_list.append(col)
            super().widget_list.append(divider)
