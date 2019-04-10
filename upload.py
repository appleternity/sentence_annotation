import boto3
from pprint import pprint
import json

def get_key():
    with open("/home/appleternity/workspace/lab/rootkey.csv", "r") as infile:
        data = [line.strip().split("=")[1] for line in infile]
        access_key = data[0]
        secret_key = data[1]
    return access_key, secret_key

def get_client():
    region_name = 'us-east-1'
    aws_access_key_id, aws_secret_access_key = get_key()
    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

    # Uncomment this line to use in production
    #endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

    client = boto3.client(
      'mturk',
      endpoint_url=endpoint_url,
      region_name=region_name,
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
    )

    # This will return $10,000.00 in the MTurk Developer Sandbox
    print(client.get_account_balance()['AvailableBalance'])
    return client

def send_hit(client):
    with open("setting.xml", 'r') as infile:
        setting = infile.read()

    response = client.create_hit(
        MaxAssignments=3,
        # AutoApprovalDelayInSeconds=10,
        LifetimeInSeconds=60*60*60,
        AssignmentDurationInSeconds=60*60,
        Reward='0.01',
        Title='Difference of the synonyms.',
        Keywords='Synonyms,Difference,Example Sentences',
        Description='We have two example sentences written with two words. These two words are synonym. Do they have the same meaning?',
        Question=setting,
        # QualificationRequirements=[
        #     {
        #         'QualificationTypeId': 'string',
        #         'Comparator': 'LessThan'|'LessThanOrEqualTo'|'GreaterThan'|'GreaterThanOrEqualTo'|'EqualTo'|'NotEqualTo'|'Exists'|'DoesNotExist'|'In'|'NotIn',
        #         'IntegerValues': [
        #             123,
        #         ],
        #         'RequiredToPreview': True|False,
        #         'ActionsGuarded': 'Accept'|'PreviewAndAccept'|'DiscoverPreviewAndAccept'
        #     },
        # ],
        # HITLayoutParameters=[
        #     {
        #         'Name': 'string',
        #         'Value': 'string'
        #     },
        # ]
    )
    pprint(response)

def list_hit(client):
    response = client.list_reviewable_hits(
        # HITTypeId='string',
        # Status='Reviewable'|'Reviewing',
        # NextToken='string',
        # MaxResults=123
    )
    print(response)

def list_assignment(client, hit_id):
    response = client.list_assignments_for_hit(
        HITId=hit_id,
        # NextToken='string',
        # MaxResults=123,
        AssignmentStatuses=[
            'Submitted',
        ]
    )
    print(response)

def approve_assignment(client, assignment_id):
    print("approving {}".format(assignment_id))
    response = client.approve_assignment(
        AssignmentId=assignment_id,
        # RequesterFeedback='string',
        # OverrideRejection=True|False
    )

def get_all_assignment(client, hit_id):
    response = client.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=[
            'Submitted',
        ]
    )
    # print(response["Assignments"])

    for r in response["Assignments"]:
        r["SubmitTime"] = str(r["SubmitTime"])
        r["AcceptTime"] = str(r["AcceptTime"])
        r["AutoApprovalTime"] = str(r["AutoApprovalTime"])

    with open("result.json", 'w', encoding='utf-8') as outfile:
        json.dump(response["Assignments"], outfile, indent=4)

def approve_all_assignment(client, hit_id):
    response = client.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=[
            'Submitted',
        ]
    )
    for r in response["Assignments"]:
        approve_assignment(client, r["AssignmentId"])

def main():
    client = get_client()
    send_hit(client)
    # list_hit(client)
    # list_assignment(client, "3087LXLJ6NP46TKL2FUX3SQEZENF0G")
    # get_all_assignment(client, "3087LXLJ6NP46TKL2FUX3SQEZENF0G")
    #approve_all_assignment(client, "3087LXLJ6NP46TKL2FUX3SQEZENF0G")
    # approve_assignment(client, "3ATPCQ38JAJ9UHXSPAOHJZ2LJD8AYY")

if __name__ == "__main__":
    main()
