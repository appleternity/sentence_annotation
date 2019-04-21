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

def send_hit_batch(client):
    with open("template_setting.xml", 'r') as infile:
        template_setting = infile.read()
    for i in range(0, 100):
        setting = "https://appleternity.github.io/sentence_annotation/html/{:0>4}.html".format(i)
        send_hit(client, template_setting.format(setting))
        print(setting)

def send_hit(client, setting=None):
    if setting is None:
        with open("setting.xml", 'r') as infile:
            setting = infile.read()

    response = client.create_hit(
        MaxAssignments=5,
        LifetimeInSeconds=60*60*60,
        AssignmentDurationInSeconds=60*10,
        Reward='0.08',
        Title='Difference of the synonyms!!!',
        Keywords='Synonyms,Difference,Example Sentences',
        Description= "Given two example sentences, you need to consider if they have the same meaning or not?",
        Question=setting,
        QualificationRequirements=[
            {
                'QualificationTypeId': '00000000000000000071',
                'Comparator': 'In',
                'LocaleValues': [
                    {
                        'Country': 'US',
                    },
                ],
                'ActionsGuarded': 'Accept'
            },
            #{
            #    "QualificationTypeId": "00000000000000000040",
            #    "Comparator": "GreaterThanOrEqualTo",
            #    "IntegerValues": [
            #        3000
            #    ],
            #    "ActionsGuarded": "Accept"
            #},
            {
                "QualificationTypeId": "000000000000000000L0",
                "Comparator": "GreaterThanOrEqualTo",
                "IntegerValues": [
                    98
                ],
                "ActionsGuarded": "Accept"
            },
            {
                "QualificationTypeId": "00000000000000000060",
                "Comparator": "EqualTo",
                "IntegerValues": [
                    1
                ],
                "ActionsGuarded": "Accept"
            }
        ],
        # HITLayoutParameters=[
        #     {
        #         'Name': 'string',
        #         'Value': 'string'
        #     },
        # ]
    )
    #pprint(response)

def list_hit(client):
    response = client.list_reviewable_hits(
        # HITTypeId='string',
        #Status='Reviewable',
        # NextToken='string',
        MaxResults=100
    )
    response = client.list_hits(MaxResults=100)
    return response

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

def get_all_assignment(client, hit_id, filename=None):
    response = client.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=[
            'Submitted',
            #'Approved',
        ]
    )
    #print(response["Assignments"])
    #print(response)

    for r in response["Assignments"]:
        r["SubmitTime"] = str(r["SubmitTime"])
        r["AcceptTime"] = str(r["AcceptTime"])
        r["AutoApprovalTime"] = str(r["AutoApprovalTime"])
        #r["ApprovalTime"] = str(r["ApprovalTime"])

    if filename is None: filename = "result.json"
    with open(filename, 'w', encoding='utf-8') as outfile:
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

def approve_all_hit(client):
    res = list_hit(client)
    print(len(res["HITs"]))
    for i, r in enumerate(res["HITs"]):
        print(i)
        hit_id = r["HITId"]
        approve_all_assignment(client, hit_id)

def get_all_hit(client):
    res = list_hit(client)
    print(len(res["HITs"]))
    for i, r in enumerate(res["HITs"]):
        print(i)
        hit_id = r["HITId"]
        get_all_assignment(client, hit_id, filename="my_result/result_{:0>4}.json".format(i))

def main():
    client = get_client()
    #approve_all_hit(client)
    get_all_hit(client)
    #send_hit_batch(client)
    # send_hit(client)
    # list_hit(client)
    # list_assignment(client, "3087LXLJ6NP46TKL2FUX3SQEZENF0G")
    #get_all_assignment(client, "31JUPBOOROD8OAZKJUAB5GZEE4A8LJ")
    # approve_all_assignment(client, "3087LXLJ6NP46TKL2FUX3SQEZENF0G")
    # approve_assignment(client, "3ATPCQ38JAJ9UHXSPAOHJZ2LJD8AYY")

if __name__ == "__main__":
    main()
