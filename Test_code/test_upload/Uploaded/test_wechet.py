import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	print(msg.fromUserName)
	print(msg.content)


	return "hello"

itchat.auto_login()
itchat.run()


# import time
# from wxbot import *

# class MyWXBot(WXBot):
#     def handle_msg_all(self, msg):
#         if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
#             self.send_msg_by_uid(u'hi', msg['user']['id'])
#             self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
#             self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

#     def schedule(self):
#         self.send_msg(u'tb', u'schedule')
#         time.sleep(1)

# def main():
#     bot = MyWXBot()
#     bot.DEBUG = True
#     bot.run()

# if __name__ == '__main__':
#     main()