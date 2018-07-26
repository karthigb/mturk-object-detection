import boto3
import sys

from utils import get_mturk_client
from sender import send_json, remove_json, create_mongo_client, get_collection

HITLayoutId = '37L8ZID2LKFQS3ZWKNUJLKGGB9UDJR'

def get_params(file_of_urls, file_of_labels):
	image_urls = []
	with open(file_of_urls, "r") as urls_file:
	  for url in urls_file:
	    image_urls.append(url.strip())

	labels = ""
	with open(file_of_labels, "r") as labels_file:
		labels = labels_file.readline()

	return image_urls,labels

def run_batch_job(mturk,image_urls, labels):
	lines = []

	for url in image_urls:
		new_hit = create_object_detection_hit(mturk,url,labels)
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

def create_object_detection_hit(mturk,image_url, labels):

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
		Reward = '0.15',
		MaxAssignments = 1,
		LifetimeInSeconds = 7200,
		AssignmentDurationInSeconds = 7200,
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
image_urls,labels = get_params('urls.txt', 'objects_to_find.txt')
mturk = get_mturk_client()
print("Running batch job to label " + labels)
run_batch_job(mturk,image_urls,labels)