import boto3
import xmltodict
import sys
import os
import json

from utils import get_mturk_client

from sender import send_json, remove_json, create_mongo_client, get_collection

def get_hits(group_id):
   active_hits = list(get_collection('sandbox', 'active_hits').find({'group_id': group_id}))

   return active_hits

def process_hits(mturk, active_hits):
   results = []

   for hit in active_hits:
      hit_id = hit['id']
      result = get_result(mturk,hit_id)
      if result!=[]:
         data = { 
             'id': hit['id'],
             'group_id': hit['group_id'],
             'url': hit['url'],
             'value': json.loads(result)
         }

         results.append(data)
         send_json(data, 'sandbox', 'completed_hits') 
         
   return_value = {
       'active_hits': results
   }
   return return_value

def clean_up(hits_not_submitted):
   os.remove("active_hits")

   with open("active_hits", "a") as active_hits:
      for line in hits_not_submitted:
         active_hits.write(line + "\n")

def get_result(mturk, hit_id):
   worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])

   if worker_results['NumResults'] > 0:
      for assignment in worker_results['Assignments']:
         xml_doc = xmltodict.parse(assignment['Answer'])

         if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
            # Multiple fields in HIT layout
            for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
               if answer_field['QuestionIdentifier']=='annotation_data':
                  if answer_field['FreeText']:
                     # Return because this project only has one assignment/HIT
                     return answer_field['FreeText']
         else:
            # One field found in HIT layout
            if xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier']=='annotation_data':
               if xml_doc['QuestionFormAnswers']['Answer']['FreeText']:
                  return xml_doc['QuestionFormAnswers']['Answer']['FreeText']

   print(hit_id + " not ready")
   return []

# Get group_id from post args
postreqdata = json.loads(open(os.environ['req']).read())
group_id = postreqdata['group_id']

# Get list of active hits
mturk = get_mturk_client()
hits = get_hits(group_id)
results = process_hits(mturk,hits)

# Write JSON Response
#return_value = json.dumps(results)
#response = open(os.environ['res'], 'w')
#response.write(return_value)
#response.close()
