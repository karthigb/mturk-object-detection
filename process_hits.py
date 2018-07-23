import boto3
import xmltodict
import sys
import os

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
   aws_access_key_id = "",
   aws_secret_access_key = "",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

def get_hits(active_hits_file):
   active_hits = []
   with open(active_hits_file, "r") as hits_file:
      for line in hits_file:
         active_hits.append(line.strip())
   return active_hits

def process_hits(active_hits):

   not_ready = []

   for line in active_hits:
      hit_id, url = line.split(',')
      result = get_result(hit_id)
      if result==[]:
         not_ready.append(line)
      else:
         with open("output", "a") as output_file:
            output_file.write(line + "," + result + "\n")

   clean_up(not_ready)

def clean_up(hits_not_submitted):
   os.remove("active_hits")

   with open("active_hits", "a") as active_hits:
      for line in hits_not_submitted:
         active_hits.write(line + "\n")

def get_result(hit_id):
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

   print hit_id + " not ready"
   return []

if __name__ == "__main__":
   active_hits_file = sys.argv[1]
   hits = get_hits(active_hits_file)
   process_hits(hits)