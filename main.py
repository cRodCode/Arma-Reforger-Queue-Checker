# Project: QueueChecker
# Author: Carlos Rodriguez
# Date: 8/29/25
# Purpose: Image detection used to check weather a player is in the queue.
# to notify via emailW

import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import customtkinter
from PIL import ImageGrab
import cv2 as cv
import asyncio

from matplotlib import pyplot as plt



class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Queue Checker")
        self.email_text = ""
        self.check_at_0 = True
        self.check_time = 60
        self.check_active = False
        self.check_at_10 = False
        self.check_at_9 = False
        self.check_at_8 = False
        self.check_at_7 = False
        self.check_at_6 = False
        self.check_at_5 = False
        self.check_at_4 = False
        self.check_at_3 = False
        self.check_at_2 = False
        self.check_at_1 = False

        try:
            file = open("settings.txt", "r")
            self.email_text = file.read()
        except Error as e:
            print(e)

        # add widgets to app
        self.button = customtkinter.CTkButton(self, text="Start", command=self.button_click_start)
        self.button_stop = customtkinter.CTkButton(self, text="Stop", command=self.button_click_stop)

        self.button_save = customtkinter.CTkButton(self, text="Save", command=self.button_click_save)
        self.check_option_1 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 1", command=self.check_all_checkboxs)
        self.check_option_2 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 2", command=self.check_all_checkboxs)
        self.check_option_3 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 3", command=self.check_all_checkboxs)
        self.check_option_4 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 4", command=self.check_all_checkboxs)
        self.check_option_5 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 5", command=self.check_all_checkboxs)
        self.check_option_6 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 6", command=self.check_all_checkboxs)
        self.check_option_7 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 7", command=self.check_all_checkboxs)
        self.check_option_8 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 8", command=self.check_all_checkboxs)
        self.check_option_9 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 9", command=self.check_all_checkboxs)
        self.check_option_10 = customtkinter.CTkCheckBox(self, text="Notify at Queue Position 10", command=self.check_all_checkboxs)

        self.email = customtkinter.CTkEntry(self, placeholder_text=self.email_text, width=400)
        self.timer = customtkinter.CTkEntry(self, placeholder_text="60", width=50)
        self.timer.insert(0,(self.check_time))

        self.email.place(x=10,y=10)
        self.timer.place(x=420, y=40)

        self.button.place(x=150, y=400)
        self.button_stop.place(x=300, y=400)

        self.button_save.place(x=420, y=10)
        self.check_option_1.place(x=10, y=60)
        self.check_option_2.place(x=10, y=90)
        self.check_option_3.place(x=10, y=120)
        self.check_option_4.place(x=10, y=150)
        self.check_option_5.place(x=10, y=180)
        self.check_option_6.place(x=10, y=210)
        self.check_option_7.place(x=10, y=240)
        self.check_option_8.place(x=10, y=270)
        self.check_option_9.place(x=10, y=300)
        self.check_option_10.place(x=10, y=330)


    # add methods to app
    def button_click_save(self):
        try:
            file = open("settings.txt", "w")
            file.write(self.email.get())
        except Error as e:
            print(e)

    def check_all_checkboxs(self):
        if self.check_option_1.get() == 1:
            self.check_at_1 = True
        if self.check_option_1.get() == 0:
            self.check_at_1 = False

        if self.check_option_2.get() == 1:
            self.check_at_2 = True
        if self.check_option_2.get() == 0:
            self.check_at_2 = False

        if self.check_option_3.get() == 1:
            self.check_at_3 = True
        if self.check_option_3.get() == 0:
            self.check_at_3 = False

        if self.check_option_4.get() == 1:
            self.check_at_4 = True
        if self.check_option_4.get() == 0:
            self.check_at_4 = False

        if self.check_option_5.get() == 1:
            self.check_at_5 = True
        if self.check_option_5.get() == 0:
            self.check_at_5 = False

        if self.check_option_6.get() == 1:
            self.check_at_6 = True
        if self.check_option_6.get() == 0:
            self.check_at_6 = False

        if self.check_option_7.get() == 1:
            self.check_at_7 = True
        if self.check_option_7.get() == 0:
            self.check_at_7 = False

        if self.check_option_8.get() == 1:
            self.check_at_8 = True
        if self.check_option_8.get() == 0:
            self.check_at_8 = False

        if self.check_option_9.get() == 1:
            self.check_at_9 = True
        if self.check_option_9.get() == 0:
            self.check_at_9 = False

        if self.check_option_10.get() == 1:
            self.check_at_10 = True
        if self.check_option_10.get() == 0:
            self.check_at_10 = False

    def button_click_start(self):
        self.button.configure(state="disabled")
        self.check_active = True
        print("Queue Checker Activated!")
        self.check_time = (int)(self.timer.get())
        self.run_check()  # start loop

    def button_click_stop(self):
        self.check_active = False
        self.button.configure(state="enabled")

    def run_check(self):
        if not self.check_active:
            return

        self.screenshot()
        self.checkscreenshot()
        # schedule next run without blocking
        self.after(int(self.check_time * 1000), self.run_check)


    def screenshot(self):
        # take a screenshot
        screenshot = ImageGrab.grab()
        # save the screenshot
        screenshot.save("assets/game.png")

    def checkscreenshot(self, threshold=0.8):
        if self.check_at_0:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/template.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")
                self.emailservice("😚You're in game!😚")
                check_at_0 = False
                exit(0)


        if self.check_at_1:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_1.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #1!😚")
                self.check_at_1 = False
                self.check_option_1.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_2:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_2.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                #self.emailservice("😚Queue Position #2!😚")
                self.check_at_2 = False
                self.check_option_2.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_3:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_3.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #3!😚")
                self.check_at_3 = False
                self.check_option_3.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")



        if self.check_at_4:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_4.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #4!😚")
                self.check_at_4 = False
                self.check_option_4.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_5:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_5.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #5!😚")
                self.check_at_5 = False
                self.check_option_5.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_6:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_6.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #6!😚")
                self.check_at_6 = False
                self.check_option_6.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_7:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_7.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #7!😚")
                self.check_at_7 = False
                self.check_option_7.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_8:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_8.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #8!😚")
                self.check_at_8 = False
                self.check_option_8.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_9:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_9.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #9!😚")
                self.check_at_9 = False
                self.check_option_9.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

        if self.check_at_10:
            img = cv.imread("assets/game.png", cv.IMREAD_GRAYSCALE)
            assert img is not None, "file could not be read, check your path!"
            template = cv.imread("assets/pos_10.png", cv.IMREAD_GRAYSCALE)
            assert template is not None, "file could not be read, check the path!"
            w, h = template.shape[::-1]

            method = cv.TM_CCOEFF_NORMED  # normalized gives scores between -1 and 1
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Template detected! Confidence: {max_val:.2f}")
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img, top_left, bottom_right, 255, 2)
                self.emailservice("😚Queue Position #10!😚")
                self.check_at_10 = False
                self.check_option_10.deselect()
            else:
                print(f"Template NOT detected (best match: {max_val:.2f})")

    def emailservice(self, body):
        global email_text
        subject = "❗️Queue Alert❗️"

        sender_email = "rebellionair20@inbox.lv"
        sender_password = "?HHoWpTg17"
        receiver_email = self.email_text

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "subject"
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("mail.inbox.lv", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print("✅ Email sent successfully")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")





app = App()
app.mainloop()

