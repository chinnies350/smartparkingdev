# def send_topic_push(token, title, body, userId):
#     try:
#         message = messaging.Message(
#             notification=messaging.Notification(
#             title=title,
#             body=body
#             ),
#             token=token
#         )
#         response = messaging.send(message)
#         col.insert_one({
#             'userId': userId,
#             'title': title,
#             'message': message,
#             'messageId': response.results[0].messageId,
#             'multicastId': response.multicastId
#         })
#     except Exception as e:
#         return str(e)

# def getMessageByUserId(userId):
#     data = []
#     res = col.find({"userId": userId}, {'_id':0})
#     for i in res:
#         data.append(i)
#     return {
#         'statusCode':1,
#         'response':data
#     }