import praw
import re
import os

reddit = praw.Reddit(private info)

submission = reddit.submission(url='https://www.reddit.com/r/BotTestingPlace/comments/avnv6z/bot_testing_submission_2/')
submission = reddit.submission(url='https://www.reddit.com/r/bottestingplace/comments/awc40x/testing_place_3/')

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = [post for post in f.read.split('\n') if post is not None]

cache = ""


def stob(str=''):
    binstr = ""
    for c in str:
        i = ord(c)
        for counter in range(8):
            if (i >= 128):  # if even
                binstr = binstr + '1'
            else:
                binstr = binstr + '0'
            i = i << 1  # left shift i
            if i > 255:
                i -= 256
        binstr = binstr + ' '
    return binstr


def btos(binstr='', startInd=0):
    output_str = ""

    index = startInd
    while index < len(binstr):
        num = 0
        for bitno in range(8):
            num += (128 / 2 ** bitno) * (ord(binstr[index + bitno]) - 48)

        output_str += chr(int(num))
        index += 8
        if not index < len(binstr):
            break
        if binstr[index] == ' ':
            index += 1

    return output_str


def parseBin(binstr=""):
    index = 0
    noData = True
    startInd = 0
    while index < len(binstr):
        if not (binstr[index + 0] == '0' or binstr[index + 0] == '1'):  # if neither 1 nor 0
            index += 1
        else:  # if yes 1 or 0
            if len(binstr) - index >= 8:  # if remaining chars can form a byte
                for charno in range(8):
                    if not (binstr[index + charno] == '0' or binstr[
                        index + charno] == '1'):  # if neither 0 nor 1, for each char
                        index += charno + 1  # shift index right by bit number
                        break
                    if charno == 7:
                        startInd = index
                        noData = False
                        break

            else:  # only if remaining chars cannot form byte
                break
    if noData:
        return -1
    else:
        return startInd


while 1:
    print("in mentions:\n")
    for comment in reddit.inbox.unread(mark_read=1, limit=None):
        author = comment.author
        if comment.body != "[deleted]":
            print("in subreddit r/", comment.subreddit)
            print("by u/", author.name)
            print("comment body:\n ", comment.body)
            print("\n")
            if comment.id not in posts_replied_to and "asciicodecbot" not in author.name:
                if re.search("u/asciicodecbot info", comment.body, re.IGNORECASE) and comment.id not in cache:
                    comment.reply('You\'ve mentioned ASCIICodecBot!\n\nHere are your options for using my services:\n\n'
                                  '   "u/asciicodecbot info": Display list of functions offered.\n'
                                  '   "u/asciicodecbot decode": Decodes ascii characters from binary numbers in the parent comment. E.g., "01100001 01100010 011000111 01100100 01100101" would yield "abcde".\n'
                                  '   "u/asciicodecbot encode": Encodes ascii characters from parent comment into binary. Like the above function, but backwards.\n'
                                  '   "u/asciicodecbot decode this: [some_string]": Decodes ascii characters from binary numbers following "this:"\n'
                                  '   "u/asciicodecbot encode this: [some_string]": Encodes ascii characters from parent comment into binary.\n\n"'
                                  '**NOTE:** So far, only the "encode" and "decode" functions are working. We\'re working on implementing the other features!\n'
                                  'asciicodecbot ver. 0.3')
                    cache += comment.id
                    posts_replied_to.append(comment.id)
                    print("reply sent: info message.")

                if re.search("u/asciicodecbot decode", comment.body, re.IGNORECASE) and comment.id not in cache:
                    if comment.parent_id == "t3_" + submission.id:
                        comment.reply(
                            "Decoded ASCII text:\n\n" + btos(submission.selftext, parseBin(submission.selftext)))
                        cache += comment.id
                        posts_replied_to.append(comment.id)
                        print("reply sent: text\n")
                    else:
                        parentComment = comment.parent()
                        comment.reply(
                            "Decoded ASCII text:\n\n" + btos(parentComment.body, parseBin(parentComment.body)))
                        cache += comment.id
                        posts_replied_to.append(comment.id)
                        print("Reply sent: text\n")

                if re.search("u/asciicodecbot encode", comment.body, re.IGNORECASE) and comment.id not in cache:
                    if comment.parent_id == "t3_" + submission.id:
                        comment.reply("Encoded ASCII binary:\n\n" + stob(submission.selftext))
                        cache += comment.id
                        posts_replied_to.append(comment.id)
                        print("reply sent: binary\n")
                    else:
                        parentComment = comment.parent()
                        cache += comment.id
                        posts_replied_to.append(comment.id)
                        print("Reply sent: binary\n")

                if re.search("u/asciicodecbot decode this:", comment.body, re.IGNORECASE) and comment.id not in cache:
                    cache += comment.id
                    posts_replied_to.append(comment.id)
                    print("reply sent: none")

                if re.search("u/asciicodecbot encode this:", comment.body, re.IGNORECASE) and comment.id not in cache:
                    cache += comment.id
                    posts_replied_to.append(comment.id)
                    print("reply sent: none")
    break

# # Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
