import urwid
import logging
import asyncio


logging.basicConfig(filename='example.log', encoding='utf-8',
                    level=logging.DEBUG)


class Timer(urwid.Edit):
    def __init__(self, timer=60, align='left'):
        self.timer = timer
        self.time_count = timer
        super().__init__(caption='Timer:', edit_text=str(self.timer),
                         align=align)

    def set_timer(self):
        try:
            self.time_count = int(super().get_edit_text())
        except TypeError:
            raise TypeError("can't transform from str to int.")

    async def start_timer(self):
        self.timer = self.time_count

        while True:
            if self.timer == 0:
                return

            self.timer -= 1
            super().set_edit_text(f'{self.timer}')
            await asyncio.sleep(1)

    def reset_timer(self):
        super().set_edit_text(f'{self.time_count}')

    def get_time_passed(self):
        return (self.time_count - self.timer)

    def valid_char(self, ch):
        if len(super().get_edit_text()) < 3:
            return(len(ch) == 1 and ch in "0123456789")
        else:
            return(False)
