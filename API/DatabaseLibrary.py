# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 22:45:59 2019

@author: kbuzz
"""
import pyodbc
import datetime
import json

############################ USER METHODS #####################################

# INSERTS A NEW USER INTO THE SYSTEM
def newUser(userName, password, commonName, email, description):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
    
    cursor = cnxn.cursor()
    cursor.execute("SELECT MAX(UserId) FROM UserTable")
    
    userId = cursor.fetchone()[0]
    if userId is None: 
        userId = 1
    else:
        userId = userId + 1
        
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO UserTable (UserID, UserName, Password, CommonName, Email, Description)" + 
    " VALUES (" + str(userId) + ",'" + userName + "',ENCRYPTBYPASSPHRASE('team25','" + password + "'),'" + commonName + 
    "','" + email + "','" + description + "')")
    cnxn.commit()
    
    newUserTopic(userId, "All")


#VALIDATES A USERNAME AND PASSWORD
def validateLogin(username, password):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT UserId FROM UserTable WHERE UserName='" + username + "' AND " +
    "CONVERT(varchar(50), DECRYPTBYPASSPHRASE('team25', Password))='" + password + "'")
    
    ret = cursor.fetchone()
    if ret is None:
        return -1
    else:
        return ret[0]
    
   
# UPDATES A USER PROFILE COMMON NAME
def updateCommonName(userId, newCommonName):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("UPDATE UserTable SET CommonName = '" + newCommonName +
                   "' WHERE UserId = '" + str(userId) + "'")
    cnxn.commit()
    

# UPDATES A USER PROFILE DESCRIPTION
def updateDescription(userId, newDescription):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("UPDATE UserTable SET Description = '" + newDescription +
                   "' WHERE UserId = '" + str(userId) + "'")
    cnxn.commit()


# UPDATES A USER PASSWORD
def updatePassword(userId, newPassword):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("UPDATE UserTable SET Password=ENCRYPTBYPASSPHRASE('team25','" + newPassword + "') " +
    "WHERE UserId=" + str(userId))
    cnxn.commit()

    
# ADDS A TOPIC TO THE USERS PROFILE
def newUserTopic(userId, topic):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO TopicTable (UserId, Topic)" +
                   " VALUES ("  + str(userId) + ",'" + topic + "')")
    cnxn.commit()
    

# SHOWS THE TIMELINE FOR A USER
def getUserTimeline(userId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT a.PostId,a.RetweetId,b.UserId,b.UserName,b.CommonName,a.PostText,a.Topics,a.Timestamp," +
	"(SELECT COUNT(*) FROM LikeTable AS c WHERE c.PostId = a.PostId OR c.PostId = a.RetweetId) AS Likes," +
	"(SELECT COUNT(*) FROM PostTable AS d WHERE d.RetweetId = a.PostId OR d.RetweetId = a.RetweetId) AS Retweets," +
	"COALESCE(a.RetweetTimestamp, a.Timestamp) " +
    "FROM PostTable AS a " +
	"LEFT JOIN UserTable AS b ON a.UserId = b.UserId " +
	"LEFT JOIN FollowerTable AS e ON a.UserId = e.FollowingId AND " +
	"(a.Topics LIKE CONCAT(e.Topic, ',%') OR a.Topics LIKE CONCAT('%,', e.Topic) OR a.Topics LIKE CONCAT('%,', e.Topic, ',%') OR a.Topics LIKE e.Topic) " +
    "WHERE e.UserId=" + str(userId) +
    "ORDER BY COALESCE(a.RetweetTimestamp, a.Timestamp) DESC")
    
    return cursor.fetchall()


# GETS ALL POSTS MADE BY A PARTICULAR USER
def getUserPosts(userId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT a.PostId,a.RetweetId,b.UserId,b.UserName,b.CommonName,a.PostText,a.Topics,a.Timestamp," +
    "(SELECT COUNT(*) FROM LikeTable AS c WHERE c.PostId = a.PostId OR c.PostId = a.RetweetId) AS Likes," +
    "(SELECT COUNT(*) FROM PostTable AS d WHERE d.RetweetId = a.PostId OR d.RetweetId = a.RetweetId) AS Retweets " +
    "FROM PostTable AS a LEFT JOIN UserTable AS b ON a.UserId = b.UserId " +
    "WHERE b.UserId=" + str(userId) + " AND NOT EXISTS (SELECT 1 FROM PostTable as e WHERE a.RetweetId = e.PostId)" +
    "ORDER BY COALESCE(a.RetweetTimestamp, a.Timestamp) DESC")
    
    return cursor.fetchall()


# GETS ALL TOPICS FOR A PARTICULAR USER
def getUserTopics(userId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT Topic FROM TopicTable WHERE UserId=" + str(userId))
    
    topics = []
    for topic in cursor.fetchall():
        topics.append(topic[0])

    return topics


# REMOVES A USER AND ALL THEIR DATA FROM THE DATABASE
def deleteUser(userId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
    
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM UserTable WHERE UserId=" + str(userId))
    
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM PostTable WHERE UserId=" + str(userId))
    
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM DMTable WHERE SenderId=" + str(userId) + " OR RecieverId=" + str(userId))
    
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM FollowerTable WHERE UserId=" + str(userId) + " OR FollowingId=" + str(userId))

    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM TopicTable WHERE UserId=" + str(userId))
    
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM LikeTable WHERE UserId=" + str(userId))    

    cnxn.commit()


# GETS USER PROFILE INFORMATION FROM THE DATABASE
def getUser(userId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
    
    cursor = cnxn.cursor()
    cursor.execute("SELECT UserId,UserName,CommonName," +
	   "(SELECT COUNT(*) FROM FollowerTable WHERE UserId=x.UserId) as Following," +
	   "(SELECT COUNT(*) FROM FollowerTable WHERE FollowingId=x.UserId) as Followers," +
	   "(SELECT COUNT(*) FROM PostTable WHERE UserId=x.UserId) as Posts," +
	   "Description " +
       "FROM UserTable as x WHERE UserId=" + str(userId) + " FOR JSON AUTO")

    return json.dumps(eval(cursor.fetchone()[0])[0])
###############################################################################


############################ FOLLOW METHODS ###################################

# ALLOWS A USER TO FOLLOW ANOTHER USER-TOPIC COMBINATION
def newFollow(userId, followingId, topic):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO FollowerTable (UserId, FollowingId, Topic)" +
                   " VALUES ("  + str(userId) + "," + str(followingId) + ",'" + topic + "')")
    cnxn.commit()
    

# ALLOWS A USER TO COMPLETELY UNFOLLOW ANOTHER USER
def unfollowUser(userId, followingId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM FollowerTable WHERE UserId=" + str(userId) +
                   " AND FollowingId=" + str(followingId))
    cnxn.commit()
    

# ALLOWS A USER TO UPDATE TOPICS THEY FOLLOW FOR A PARTICULAR USER
def updateFollow(userId, followingId, topics = []):
    unfollowUser(userId, followingId)
    
    for topic in topics:
        newFollow(userId, followingId, topic)

###############################################################################


############################ GENERAL METHODS ##################################

# VALIDATES NEW EMAILS FOR NEW USERS; RETURNS TRUE IF NOT IN THE DATABASE    
def validateEmail(email):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
    
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 UserId FROM UserTable WHERE Email = '" + email + "'")
    
    if cursor.fetchone() is None:
        return True
    else:
        return False
    
    
def validateUsername(username):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
    
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 UserId FROM UserTable WHERE UserName = '" + username + "'")
    
    if cursor.fetchone() is None:
        return True
    else:
        return False
    

# RETURNS USER ID FROM ACCOUNT EMAIL
def getUserId(email):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
    
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 UserId FROM UserTable WHERE Email = '" + email + "'")
    
    ret = cursor.fetchone()
    if ret is None:
        return -1
    else:
        return ret[0]

###############################################################################


############################ POST METHODS #####################################

# CREATES A NEW POST
def newPost(userId, postTitle, postText, topics):    
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT MAX(PostId) FROM PostTable")
    
    postId = cursor.fetchone()[0]
    if postId is None:
        postId = 1
    else:
        postId = postId + 1
    
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO PostTable (PostId, UserId, PostTitle, PostText, Topics, Timestamp)" +
                   " VALUES (" + str(postId) + "," + str(userId) + ",'" + postTitle + "','" + postText + "','" +
                   topics + ",All','" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "')")
    cnxn.commit()


# GETS ALL POSTS ON THE PLATFORM
def getAllPosts():
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT a.PostId,a.PostTitle, a.RetweetId,b.UserId,b.UserName,b.CommonName,a.PostText,a.Topics,a.Timestamp," +
	"(SELECT COUNT(*) FROM LikeTable AS c WHERE c.PostId = a.PostId OR c.PostId = a.RetweetId) AS Likes," +
	"(SELECT COUNT(*) FROM PostTable AS d WHERE d.RetweetId = a.PostId OR d.RetweetId = a.RetweetId) AS Retweets " +
    "FROM PostTable AS a LEFT JOIN UserTable AS b ON a.UserId = b.UserId " +
    "WHERE a.RetweetId IS NULL " +
    "ORDER BY a.Timestamp DESC FOR JSON AUTO")
    
    ret = cursor.fetchall()[0][0]
    return ret[1 : len(ret) - 1]


# GETS ALL POST ON THE PLATFORM WITH A SPECIFIC TOPIC
def getAllTopicPosts(topic):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT a.PostId,PostTitle,a.RetweetId,b.UserId,b.UserName,b.CommonName,a.PostText,a.Topics,a.Timestamp," +
	"(SELECT COUNT(*) FROM LikeTable AS c WHERE c.PostId = a.PostId OR c.PostId = a.RetweetId) AS Likes," +
	"(SELECT COUNT(*) FROM PostTable AS d WHERE d.RetweetId = a.PostId OR d.RetweetId = a.RetweetId) AS Retweets " +
    "FROM PostTable AS a LEFT JOIN UserTable AS b ON a.UserId = b.UserId " +
    "WHERE a.RetweetId IS NULL AND (Topics LIKE '" + topic + ",%' OR ""Topics LIKE '%," + topic + "' OR ""Topics LIKE '%," + topic + ",%' OR ""Topics LIKE '" + topic + "') " +
    "ORDER BY a.Timestamp DESC FOR JSON AUTO")
    
    ret = cursor.fetchall()[0][0]
    return ret[1 : len(ret) - 1]


# DELETES A POST ON THE PLATFORM
def deletePost(postId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM PostTable WHERE PostId=" + str(postId) + " OR RetweetId=" + str(postId))
    cnxn.commit()


# ADDS A LIKE TO A POST
def like(userId, postId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")

    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO LikeTable (UserId,PostId)" +
                    " VALUES (" + str(userId) + "," + str(postId) + ")")
    cnxn.commit()


# REMOVES A LIKE FROM A POST
def unlike(userId, postId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")

    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM LikeTable WHERE UserId=" + str(userId) +
    " AND PostId=" + str(postId))
    cnxn.commit()


# RETWEETS A POST
def retweet(userId, postId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")

    cursor = cnxn.cursor()
    cursor.execute("SELECT MAX(PostId) FROM PostTable")
    
    newPostId = cursor.fetchone()[0]
    if newPostId is None:
        newPostId = 1
    else:
        newPostId = newPostId + 1

    cursor = cnxn.cursor()
    oldPost = cursor.execute("SELECT * FROM PostTable WHERE PostId=" + str(postId)).fetchone()
    
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO PostTable (PostId,UserId,PostText,Topics,Timestamp,RetweetId,RetweetTimestamp) " +
    "VALUES (" + str(newPostId) + "," + str(userId) + ",'" + oldPost[2] + "','" + oldPost[3] + "','" + str(oldPost[4]) + "'," + str(oldPost[0]) + ",'" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "')")
    cnxn.commit()


# REMOVES A RETWEET FROM A POST
def unretweet(userId, postId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")

    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM PostTable WHERE UserId=" + str(userId) + " AND RetweetId =" + str(postId))
    cnxn.commit()

###############################################################################  
    

############################## DM METHODS #####################################
  
# CREATES A NEW DM MESSAGE  
def newDM(senderId, recieverId, message):    
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO DMTable (SenderId, RecieverId, Message, Timestamp)" +
                   " VALUES (" + str(senderId) + "," + str(recieverId) + ",'" +
                   message + "','" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "')")
    cnxn.commit()


# DELETES DMS FOR A PARTICULAR USER
def deleteDMs(userId, recieverId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("UPDATE DMTable SET SenderDeleted=1 WHERE " +
    "SenderId=" + str(userId) + " AND RecieverId=" + str(recieverId))

    cursor = cnxn.cursor()
    cursor.execute("UPDATE DMTable SET RecieverDeleted=1 WHERE " +
    "SenderId=" + str(recieverId) + " AND RecieverId=" + str(userId))

    cnxn.commit()

    clearDMs()


# WIPES THE DATABASE OF ANY UNUSED DMS
def clearDMs():
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM DMTable WHERE SenderDeleted=1 AND RecieverDeleted=1")
    cnxn.commit()

# GETS A DM CONVERSATION BETWEEN TWO USERS
def getDMConvo(userId, recieverId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT SenderId,RecieverId,Message,TimeStamp FROM DMTable " +
    "WHERE (SenderId=" + str(userId) + " AND RecieverId=" + str(recieverId) + " AND SenderDeleted=0) OR " +
    "(SenderId=" + str(recieverId) + " AND RecieverId=" + str(userId) + " AND RecieverDeleted=0) " +
    "ORDER BY TimeStamp FOR JSON AUTO")

    ret = cursor.fetchall()[0][0]
    return ret[1 : len(ret) - 1]


# GETS LIST OF DM CONVOS FOR A USER
def getDMList(userId):
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" +
                      "Server=tcp:twistter-dns.eastus.cloudapp.azure.com,1401;" +
                      "Database=Twistter-Database;" +
                      "Uid=kbuzza;" +
                      "Pwd=TestTwistter1;" +
                      "Encrypt=no;" +
                      "TrustServerCertificate=no;" +
                      "Connection Timeout=60;")
        
    cursor = cnxn.cursor()
    cursor.execute("SELECT y.UserName,y.CommonName,x.Message,x.TimeStamp,x.OtherUser FROM (" +
	               "SELECT SenderId,RecieverId," +
		           "CASE WHEN SenderId=" + str(userId) + " THEN RecieverId ELSE SenderId END AS OtherUser," +
		           "Message,TimeStamp," +
                   "ROW_NUMBER() OVER (PARTITION BY CASE WHEN SenderId=" + str(userId) + " THEN RecieverId ELSE SenderId END " +
				   "ORDER BY TimeStamp DESC) as part " +
                   "FROM DMTable) as x LEFT JOIN UserTable as y on x.SenderId=y.UserId " +
                   "WHERE x.part=1 AND (x.SenderId=" + str(userId) + " OR x.RecieverId=" + str(userId) + ") AND " +
                   "(EXISTS (SELECT 1 FROM DMTable WHERE SenderId=" + str(userId) + " AND SenderDeleted=0) OR " +
                   "EXISTS (SELECT 1 FROM DMTable WHERE RecieverId=" + str(userId) + " AND RecieverDeleted=0)) " +
                   "ORDER BY TimeStamp DESC FOR JSON AUTO")

    ret = cursor.fetchall()[0][0]
    return ret[1 : len(ret) - 1]

###############################################################################