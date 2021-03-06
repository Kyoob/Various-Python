"""
	Shows the top 10 links in the specified subreddit using BeautifulSoup.
	Tim Coutinho
"""

import csv
from urllib.request import urlopen

from bs4 import BeautifulSoup

MAX_POSTS = 10


def get_subreddit():
	subreddit = input('Subreddit: ')
	with urlopen(f'https://www.reddit.com/r/{subreddit}/') as url:
		site = BeautifulSoup(url, 'lxml')
	posts = site.find_all('div', onclick='click_thing(this)')
	subreddit = posts[0]['data-subreddit']
	return (subreddit, posts)


def get_posts(posts, csv_writer):
	i = 0
	for post in posts:  # Can't use enumerate, don't always want to increment
		if post.find('span', class_='stickied-tagline') is None:
			# Is not a stickied post
			title, link = (post.find('p', class_='title').a.text,
						   post['data-url'])
			if '/r/' in link:
				# Only last part of url is given if hosted on Reddit
				link = 'https://www.reddit.com' + link
			print(title, link)
			csv_writer.writerow([title, link])
			i += 1
			if i == MAX_POSTS:
				return
	if i == 0:  # Somehow all stickied posts
		print('No posts found.')
		

def main():
	while True:
		try:
			subreddit, posts = get_subreddit()
			break
		except KeyError as e:
			print('Subreddit does not exist, try again.')

	with open(f'top{MAX_POSTS}{subreddit}.csv', 'w', newline='') as f:
		csv_writer = csv.writer(f)
		csv_writer.writerow(['Title', 'Link'])
		print(f"\nCurrent top {MAX_POSTS} posts in {subreddit}:\n")
		get_posts(posts, csv_writer)


if __name__ == '__main__':
	main()
