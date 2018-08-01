import boto3
import sys
import os
import json

from utils import get_mturk_client
from sender import send_json, remove_json, create_mongo_client, get_collection

HITLayoutId = '37L8ZID2LKFQS3ZWKNUJLKGGB9UDJR'

def get_params(urls, labels):
	image_urls = urls.split(",")

	return image_urls,labels

def run_batch_job(mturk,image_urls, labels,complete_time,expiration_time,reward):
	lines = []

	for url in image_urls:
		new_hit = create_object_detection_hit(mturk,url,labels,complete_time,expiration_time,reward)
		line = new_hit['HIT']['HITId'] + "," + url + "\n"
		lines.append(line)
		print("A new HIT has been created with HITId " + new_hit['HIT']['HITId'])

		# Post this to CosmosDB
		post_data = {
			'id': new_hit['HIT']['HITId'],
            'group_id': new_hit['HIT']['HITGroupId'],
			'url': url
		}
		send_json(post_data, 'sandbox', 'active_hits')



	print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])

def create_object_detection_hit(mturk,image_url, labels,complete_time,expiration_time,reward):

	HITLayoutParameters=[
		{
			'Name': 'image_url',
			'Value': image_url
		},
		{
			'Name': 'objects_to_find',
			'Value': labels
		}
	]

	new_hit = mturk.create_hit(
		HITLayoutId    = HITLayoutId,
		HITLayoutParameters = HITLayoutParameters,
		Title = 'Tag an image',
		Description = 'Identify any of the following items in the picture: ' + labels + '.',
		Keywords = 'image, quick, labeling, tagging',
		Reward = reward,
		MaxAssignments = 1,
		LifetimeInSeconds = expiration_time * 60,
		AssignmentDurationInSeconds = complete_time * 60,
		RequesterAnnotation = labels
	)

	return new_hit
'''
if __name__ == "__main__":
    image_urls,labels = get_params(sys.argv[1],sys.argv[2])
    mturk = get_mturk_client()
    print("Running batch job to label " + labels)
    run_batch_job(mturk,image_urls,labels)
'''

# Run with hardcoded values
postreqdata = json.loads(open(os.environ['req']).read())

# Sample Post Data
'''
postreqdata = {
    "urls": "https://www.charlotteonthecheap.com/lotc-cms/wp-content/uploads/2015/04/mcdonalds-extra-value-meal.png,https://s3-us-west-2.amazonaws.com/cities.directory/compasseous.com/public_html/uploads/place_images/photos/f382487a2168080397c14bce3dc52839.png,https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/08112410/ourfood-category-full-menu-mobile.jpg",
    "labels": "burgers,fries,drink",
    "complete_time": "120",
    "expiration_time": "120",
    "reward": "0.30"
}
'''
urls = postreqdata['urls']
labels = postreqdata['labels']
complete_time = postreqdata['complete_time']
expiration_time = postreqdata['expiration_time']
reward = postreqdata['reward']

image_urls,labels = get_params(urls, labels)
mturk = get_mturk_client()
print("Running batch job to label " + labels)
run_batch_job(mturk,image_urls,labels,int(complete_time),int(expiration_time),reward)