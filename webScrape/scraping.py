import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import json


class RedditPost:
	"""
	Class structure defining a reddit post.
	"""
	def __init__(self, post_date, sub, title, link, flair,\
				       author, comment_count, score, rank,\
				       post_type, timestamp):
		self.date = post_date.strip()
		self.rank = int(rank.strip())
		self.sub = sub.strip()
		self.title = title.strip()
		self.link = link.strip()
		self.author = author.strip()
		self.flair = flair.strip()
		self.comment_count = int(comment_count.strip())
		self.score = int(score.strip())
		self.post_type = post_type.strip()
		self.timestamp = int(timestamp.strip())
	
	def __str__(self):
		return("Date: {}\n".format(self.date) +
			   "Rank: {}\n".format(self.rank) +
			   "Sub: {}\n".format(self.sub) +
			   "Title: {}\n".format(self.title) +
			   "Link: {}\n".format(self.link) +
			   "Flair: {}\n".format(self.flair) +
			   "Author: {}\n".format(self.author) +
			   "Comment Count: {}\n".format(self.comment_count) +
			   "Score: {}\n".format(self.score) +
			   "Post Type: {}\n".format(self.post_type) +
			   "Timestamp: {}".format(self.timestamp))		


def getFormattedPost(post):
	"""
	Parses a given post, returning it as a formatted RedditPost object
	"""
	flair_regex = re.compile("(linkflair-.*)")
	title_regex = re.compile('(title may-blank.*)')
	today_date = date.today().strftime("%m-%d-%Y")

	post_desc = post.find("a",{'class': title_regex})
	
	post_author = post.get('data-author')
	post_link = post.get('data-permalink')
	post_comment_count = post.get('data-comments-count')
	post_title = post_desc.text
	post_score = post.get('data-score')
	post_rank = post.get('data-rank')
	post_type = post.get('data-type')
	post_timestamp = post.get('data-timestamp')
	post_flair = list(filter(flair_regex.match, post.get('class')))
	if len(post_flair) == 0:
		post_flair = ["linkflair-none"]
	post_flair = post_flair[0][len("linkflair-"):]
	post_date = today_date
	post_sub = "/r/wow"

	currPost = RedditPost(post_date, post_sub,\
							post_title, post_link, post_flair,\
							post_author, post_comment_count, post_score,\
							post_rank, post_type, post_timestamp)

	return currPost


def getTodaysTop25WoWPosts():
	"""
	Scrapes reddit wow top posts of the day for top 25 posts.
	"""
	urls = ['https://old.reddit.com/r/wow/top/?sort=top&t=day']
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 \
				Safari/537.36"}
	todays_top_25_posts = []

	for url in urls:
		request_text = requests.get(url, headers=headers).text
		soup = BeautifulSoup(request_text,'lxml')
		post_regex = re.compile('(thing id.*)')

		post_table = soup.find_all('div',{'class': post_regex})

		for post in post_table:
			if 'promoted' in post.get('class'):
				# Advertisement, skip!
				continue

			currPost = getFormattedPost(post)
			todays_top_25_posts.append(currPost)

	return todays_top_25_posts


def flushToDisk(post_list):
	"""
	Takes as input a list of each subreddits top 25 posts (list of list),
	then dumps the list onto a json file.

	Input: post_list - A list of list where each sublist contains the top 25 posts
	"""
	today_date = date.today().strftime("%m-%d-%Y")
	file_name = "./data/" + today_date + ".json"

	json_list = []
	for curr_list in post_list:
		for post in curr_list:
		    json_list.append(post.__dict__)

	mewDict = {"posts": json_list}

	with open(file_name, 'w', newline='') as fp:
		json.dump(mewDict, fp, indent=4)


def main():
	todays_top_25_posts = getTodaysTop25WoWPosts()
	flushToDisk([todays_top_25_posts])


if __name__ == "__main__":
    main()
