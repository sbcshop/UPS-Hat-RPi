from oled_091 import SSD1306
from subprocess import check_output
from time import sleep
from datetime import datetime
from os import path

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf")


class RPiInfo:
    def __init__(self):
        self.IP_cmd = "hostname -I"
        self.CPU_cmd = "top -bn1 | grep load | awk '{print $11}'"
        self.MEM_cmd = "free -m | awk 'FNR==2{print $2, $3}'"
        self.Disk_cmd = "df -h | awk 'FNR==2{print $2, $3}'"

    def output(self, command):
        return check_output(command, shell=True)

    def IP_Info(self):
        IP = self.output(self.IP_cmd)
        IP = str(IP, "UTF8").replace("\n", "")
        return IP

    def CPU_Info(self):
        CPU = self.output(self.CPU_cmd)
        CPU = str(CPU, "UTF8").replace(",", '').replace("\n", "")
        return CPU

    def MEM_Info(self):
        raw_mem = self.output(self.MEM_cmd)
        Mem = str(raw_mem, "UTF8").replace("\n", "")
        Mem = Mem.split()
        return Mem

    def Disk_Info(self):
        raw_disk = self.output(self.Disk_cmd)
        Disk = str(raw_disk, "UTF8").replace("\n", "")
        Disk = Disk.split()
        return Disk


def info_print():
    display = SSD1306()
    info = RPiInfo()
    date = datetime.now().strftime("%d %b %y, %H:%M")

    delay_t = 2

    # display.WhiteDisplay()
    display.DirImage(path.join(DIR_PATH, "Images/SB.png"))
    display.DrawRect()
    display.ShowImage()
    sleep(1)

    while True:
        IP = info.IP_Info()
        display.DirImage(path.join(DIR_PATH, "Images/IP.png"), size=(24,
                                                                      24), cords=(1, 4))
        display.PrintText(IP, cords=(30, 10), FontSize=14)
        display.DrawRect()

        # display.PrintText(date, cords=(60, 1), FontSize=8)
        display.ShowImage()
        sleep(delay_t)

        CPU = info.CPU_Info()
        # display.DirImage("Images/CPU.png", size=(24, 24), cords=(0, 0))
        display.PrintText("CPU Usage: {}".format(CPU), cords=(4, 8), FontSize=14)
        display.DrawRect()
        display.ShowImage()
        sleep(delay_t)

        Mem = info.MEM_Info()
        display.PrintText("Memory- T: {} MB".format(Mem[0]), cords=(1, 2),
                          FontSize=12)
        display.PrintText("U: {} MB".format(Mem[1]),
                          cords=(54, 16), FontSize=12)
        display.DrawRect()
        display.ShowImage()
        sleep(delay_t)

        Disk = info.Disk_Info()
        display.PrintText("Disk- Total: {}".format(Disk[0]),
                          cords=(1, 2), FontSize=12)
        display.PrintText("Used: {}".format(Disk[1]),
                          cords=(34, 16), FontSize=12)
        display.DrawRect()

        display.ShowImage()
        sleep(delay_t)


if __name__ == "__main__":
    info_print()
