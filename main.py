#import re
from urllib.request import urlopen
#from bs4 import BeautifulSoup
import json
from collections import defaultdict

def getPostReaction(url,after):

	reaction_type=['LIKE','LOVE','WOW','ANGRY','HAHA','SAD']

	reaction_details =defaultdict(list)

	for reaction in reaction_type:
		fields = "&fields=reactions.type({}).limit(0).summary(total_count)".format(reaction)
		reaction_url = url + fields + after
		reaction_data = json.loads(urlopen(reaction_url).read().decode('utf8'))

		for Data in reaction_data['data']:
			ID=Data['id']
			reaction_num = Data['reactions']['summary']['total_count']
			reaction_details[ID].append(reaction_num)

	return reaction_details


def getpost(url):

	After = ''
	page_num = 1
	while True:
		if page_num>10:
			break
		field = "&fields=message,link,created_time,type,name,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true)"
	
		post_url = url + field + After
		post_data = json.loads(urlopen(post_url).read().decode('utf8'))

		Reaction = getPostReaction(url,After)
		print ('='*100,page_num)

		for i in post_data['data']:
			Id = i['id']
			Name = i['name'] if 'name' in i else Id
			print (Name,Reaction[Id],sum(Reaction[Id]))

		if 'paging' in post_data:
			After = '&after='+post_data['paging']['cursors']['after']
			page_num += 1
		else :
			break

		
		
if __name__ == '__main__' :
	
	
	access_token=your_access_token
	base_url = 'https://graph.facebook.com/v2.9/bbcnews/posts/' + \
			'?limit=100&access_token={}'.format(access_token)

	getpost(base_url)






