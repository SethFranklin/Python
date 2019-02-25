
import praw
import operator
import urllib
import os
import json
import sched
import time

def repost_new():

    json_data = None

    with open("./RedditLogin.json", "r") as json_file:
        json_data = json.load(json_file)

    reddit = praw.Reddit(username = json_data["bots"][0]["username"], password = json_data["bots"][0]["password"], client_id = json_data["bots"][0]["client_id"], client_secret = json_data["bots"][0]["client_secret"], user_agent = json_data["bots"][0]["user_agent"])

    print("Logged in as /u/" + reddit.user.me().name)

    sub_take = json_data["subs"][0]["sub_take"]
    sub_post = json_data["subs"][0]["sub_post"]
    new_depth = json_data["subs"][0]["new_depth"]

    posts = []
    for i in reddit.subreddit(sub_take).new(limit = new_depth):
        posts.append(i)
    posts.sort(key = lambda post: post.score, reverse = True)

    to_submit = None

    for post in posts:
        if (not post.is_video):
            ending = post.url.split(".")[-1]
            if (ending in json_data["imgs"]):
                to_submit = post
                break

    if (to_submit != None):
        file_name = to_submit.url.split("/")[-1]
        urllib.request.urlretrieve(to_submit.url, "./" + file_name)
        try:
            reddit.subreddit(sub_post).submit_image(title = to_submit.title, image_path = "./" + file_name, send_replies = False)
            print("Sucessfuly posted to /r/" + sub_post)
        except praw.exceptions.APIException as e:
            print("Couldn't post to /r/" + sub_post)
            print(str(e))
        os.remove("./" + file_name)
    else:
        print("No available posts from /r/" + sub_post)

hours = 2
s = sched.scheduler(time.time, time.sleep)

def repeat(sc):
    print("Attempting post")
    repost_new()
    s.enter(3600 * hours, 1, repeat, (sc,))

s.enter(3600 * hours, 1, repeat, (s,))
s.run()
