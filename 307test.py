# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 23:02:30 2019

@author: kbuzz
"""

import DatabaseLibrary as d
import time

#d.newUser("kbuzza", "password", "Kyle", "kbuzza@purdue.edu", "4129134625", "6/13/1999", "This is my description.")
#d.newUser("testuser1", "pass1", "User1", "test1@test.net", "1111111111", "1/1/2019", "desc1")
#d.newUser("testuser2", "pass2", "User2", "test2@test.net", "2222222222", "2/2/2019", "desc2")


#print(d.validateLogin('kbuzza', 'password'))
#print(d.validateLogin('testuser1', 'pass1'))
#print(d.validateLogin('kbuzza', 'notpassword'))


#d.updatePassword(1, 'newpass')
#print(d.validateLogin('kbuzza', 'password'))
#print(d.validateLogin('kbuzza', 'newpass'))


#print(d.validateEmail("kbuzza@purdue.edu"))
#print(d.validateEmail("email-not-in-database@email.com"))


#print(d.validateUsername("kbuzza"))
#print(d.validateUsername("username-not-in-database"))


#print(d.getUserId("kbuzza@purdue.edu"))


#d.updateCommonName(1, "New Kyle")


#d.updateDescription(1, "new description")


#print(d.getUser(1))

#d.newUserTopic(1, "Sports")
#d.newUserTopic(1, "Gaming")
#d.newUserTopic(1, "News")
#d.newUserTopic(1, "Entertainment")
#d.newUserTopic(2, "Sports")
#d.newUserTopic(2, "Gaming")
#d.newUserTopic(2, "News")
#d.newUserTopic(2, "Entertainment")
#d.newUserTopic(3, "Sports")
#d.newUserTopic(3, "Gaming")
#d.newUserTopic(3, "News")
#d.newUserTopic(3, "Entertainment")


#print(d.getUserTopics(1))


#d.newPost(1, "Post 1", "Gaming")
#d.newPost(1, "Post 2", "Sports,News")
#d.newPost(1, "Post 3", "Gaming,Entertainment")
#d.newPost(2, "Post 4", "Gaming")
#d.newPost(2, "Title", "Post 5", "Sports,News")
#d.newPost(2, "Post 6", "Gaming,Entertainment")
#d.newPost(3, "Sample Title", "Post 7", "Gaming")
#d.newPost(3, "Post 8", "Sports,News")
#d.newPost(3, "Post 9", "Gaming,Entertainment")
#d.newPost(1, "Post 10", "")


#print(d.getAllPosts())


#print(d.getAllTopicPosts("Sports"))


#print(d.getUserPosts(1))


#d.newFollow(1, 2, "Gaming")
#d.newFollow(1, 3, "News")
#print(d.getUserTimeline(1))

#d.newFollow(2, 3, "All")
#print(d.getUserTimeline(2))


#d.unfollowUser(2, 3)


#d.newFollow(2, 3, "All")
#items = ["Sports","Gaming","Entertainment"]
#d.updateFollow(2, 3, items)


#d.deletePost(4)
#d.deleteUser(3)


#d.like(1,1)
#d.unlike(1,1)


#d.retweet(1,11)
#d.unretweet(1,11)
#d.retweet(2,1)


#print(d.getUserPosts(1))
#print(d.getAllPosts())
#print(d.getAllTopicPosts("News"))
#print(d.getUserTimeline(1))


#d.newDM(1,2,'message1')
#time.sleep(1.5)
#d.newDM(2,1,'message2')
#time.sleep(1.5)
#d.newDM(1,2,'message3')
#time.sleep(1.5)
#d.newDM(2,1,'message4')
#time.sleep(1.5)
#d.newDM(1,2,'message5')
#time.sleep(1.5)
#d.newDM(2,1,'message6')

#d.newDM(1,3,'message7')
#d.newDM(1,3,'message8')


#d.deleteDMs(1,2)
#d.deleteDMs(2,1)


#print(d.getDMConvo(1,2))


#print(d.getDMList(1))