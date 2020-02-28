#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
RedditBot
Created by Colin Gallagher
'''

import os
import praw
import pandas
import re

# create args parser instance to capture user options given when running script
parser = argparse.ArgumentParser(description='RedditBot')

# add conditional user arguments
parser.add_argument('-i', '--id', type=str, dest='client_id', default=None,
					help='Client ID from Reddit applications page.')
parser.add_argument('-s', '--secret', type=str, dest='client_secret', default=None,
					help='Client secret API key from Reddit applications page.')
parser.add_argument('-a', '--agent', type=str, dest='user_agent', default=None,
					help='User agent name for Reddit bot application.')
parser.add_argument('-u', '--username', type=str, dest='username', default=None,
					help='Username used to log into Reddit bot account.')
parser.add_argument('-p', '--password', type=str, dest='password', default=None,
					help='Password used to log into Reddit bot account.')
parser.add_argument('-n', '--name', type=str, dest='bot_name', default='RedditBot',
					help='Give your RedditBot a name or identifier.')
parser.add_argument('-r', '--subreddit', type=str, dest='subreddit', nargs='+', action='append', default=None,
					help='Subreddit for Reddit bot to search through relevant posts.')
parser.add_argument('-k', '--keywords', type=str, dest='keywords', nargs='+', action='append', default=None,
					help='Keywords used for filtering relevant posts with Reddit bot.')
parser.add_argument('-l', '--limit', type=int, dest='limit', default=100,
					help='Limit the number of posts returned when searching subreddits.')
parser.add_argument('-t', '--textfile', type=str, dest='textfile', default=None,
					help='Name of text file to export search results to.')
parser.add_argument('-c', '--csvfile', type=str, dest='csvfile', default=None,
					help='Name of CSV file to export search results to.')

# parse args
args = parser.parse_args()
reddit_praw = [args.client_id, args.client_secret, args.user_agent, args.username, args.password]
if None in reddit_praw:
	# check for praw.ini file
	if os.path.exists('praw.ini') is False:
		raise Exception('Pass Reddit login info when calling script or store in "praw.ini" file.')
		sys.exit()
	else:
		reddit = praw.Reddit()
else:
	reddit = praw.Reddit(
		client_id = args.client_id,
		client_secret = args.client_secret,
		user_agent = args.user_agent,
		username = args.username,
		password = args.password
	)

if args.subreddit is None:
	subreddit = reddit.subreddit('popular')
else:
	try:
		subreddit = reddit.subreddit(args.subreddit)
	except:
		raise Exception('Subreddit does not exist or cannot be reached at the moment.')
		sys.exit()

reddit_data = {
	'title':[],
	'score':[],
	'id':[],
	'url':[]
}

limit = int(args.limit)
if args.keywords is not None:
	keywords = list(args.keywords)
else:
	keywords = None

for post in subreddit.top(limit=limit):
	foo = False
	if keywords is None:
		foo = True
	else:
		for key in keywords:
			if re.search(key, post.title. re.IGNORECASE):
				foo = True
				continue
	if foo is True:
		reddit_data['title'].append(post.title)
		reddit_data['score'].append(post.score)
		reddit_data['id'].append(post.id)
		reddit_data['url'].append(post.url)

titles = reddit_data['title']
scores = reddit_data['score']
ids = reddit_data['id']
urls = reddit_data['url']

for i in range(len(titles)):
	print('')
	print('Title: {}'.format(titles[i]))
	print('Score: {}'.format(scores[i]))
	print('ID: {}'.format(ids[i]))
	print('URL: {}'.format(urls[i]))

if args.textfile is not None:
	try:
		with open(args.textfile, 'w') as f:
			for i in range(len(titles)):
				f.write('Title: {}'.format(titles[i]))
				f.write('\nScore: {}'.format(scores[i]))
				f.write('\nID: {}'.format(ids[i]))
				f.write('\nURL: {}'.format(urls[i]))
				f.write('\n\n')
	except:
		print('Unable to export search results from Reddit bot to text file.')

if args.csvfile is not None:
	try:
		df = pandas.DataFrame(reddit_data)
		df.to_csv(args.csvfile, index=False)
	except:
		print('Unable to export search results from Reddit bot to CSV file.')
