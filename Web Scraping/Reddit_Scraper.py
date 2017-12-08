"""
	Shows the top 10 links in the specified subreddit using BeautifulSoup.
	Tim Coutinho
"""

import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen

MAX_POSTS = 10

def main():
	subreddit = input('Subreddit: ')
	with urlopen(f'https://www.reddit.com/r/{subreddit}/') as url:
		site = BeautifulSoup(url, 'lxml')
	posts = site.find_all('div', onclick='click_thing(this)')	# Only the actual posts in the subreddit
	subreddit = posts[0]['data-subreddit']

	csv_file = open(f'top{MAX_POSTS}{subreddit}.csv', 'w', newline='')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Title', 'Link'])

	print(f"\nCurrent top {MAX_POSTS} posts in {subreddit}:\n")
	i = 0
	for post in posts:	# Can't use enumerate, don't always want to increment i
		if post.find('span', class_='stickied-tagline') is None:	# Is not a stickied post
			title, link = (post.find('p', class_='title').a.text, post['data-url'])
			if '/r/' in link:	# If hosted on reddit, only gives last part of url
				link = 'https://www.reddit.com' + link
			print(title, link)
			csv_writer.writerow([title, link])
			i += 1
			if i == MAX_POSTS:
				return
	if i == 0:	# Somehow all stickied posts
		print('No posts found.')

	csv_file.close()
		
if __name__ == '__main__':
	main()