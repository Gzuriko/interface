#!/usr/bin/env python3
import sys
import pickle
import pika
import datetime
import time
import threading
import msvcrt
import npyscreen
import curses

class ChatApp(npyscreen.NPSAppManaged):
        def onStart(self):
                self.addForm("MAIN", MainForm, name="Chat", color="IMPORTANT",)

                self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                        host='hub.zaikin.su',
                        credentials=pika.PlainCredentials('guest', 'surgu2019')))
                self.channel = self.connection.channel()

                #self.nickname = ''

                # self.channel.queue_declare(queue=self.nickname)
                # self.channel.queue_bind(exchange='amq.fanout', queue=self.nickname)

        def onCleanExit(self):
                npyscreen.notify_wait("Goodbye!")
                self.connection.close()

class MessageBox(npyscreen.BoxTitle):
        _contained_widget = npyscreen.TitleMultiLine

class ConnectionButton(npyscreen.ButtonPress):
        def whenPressed(self):
                #self.parent.parentApp.nickname = self.parent.nickname.value
                self.parent.parentApp.channel.queue_declare(queue=self.parent.nickname.value)
                self.parent.parentApp.channel.queue_bind(exchange='amq.fanout', queue=self.parent.nickname.value)
                self.parent.thread.start()

class MainForm(npyscreen.ActionForm):
        def Call(self):
                self.parentApp.channel.basic_qos(prefetch_count=100)
                self.parentApp.channel.basic_consume(queue=self.nickname.value, on_message_callback=self.callback)
                self.parentApp.channel.start_consuming()

        def callback(self, ch, method, properties, body):
                self.messageBox.values += ('InputMessage:',body.decode('utf-8'))
                self.messageBox.display()

        def create(self):
                self.nickname = self.add(npyscreen.TitleText, name = "Nickname:", value= "")
                self.connectionButton = self.add(ConnectionButton, name = "Connect", relx=16, rely=4)
                self.sentfield = self.add(npyscreen.TitleText, name = "Send:", value="",rely=6)
                self.messageBox = self.add(MessageBox, name = "Message", editable = False, max_height=-1, rely=8, scroll_exit=True)

                self.thread = threading.Thread(target=self.Call, name='Thread')

        def on_ok(self):
                message = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')+" "+self.nickname.value+": "+self.sentfield.value
                self.parentApp.channel.basic_publish(
                        exchange='amq.fanout',
                        routing_key='',
                        body=message,
                        properties=pika.BasicProperties(
                        delivery_mode=2,)
                        )

        def on_cancel(self):
                self.parentApp.switchForm(None)

if __name__ == '__main__':
        ChatApp().run()
