import sys
import requests
import json

def delete_channel(base_url, headers, channel_url):
  url = f'{base_url}/v3/group_channels/{channel_url}'
  response = requests.request("DELETE", url, headers=headers)
  return response.ok

def remove_members(base_url, headers, channel_url, member_user_ids):
  print(f'Removing {len(member_user_ids)} members from channel {channel_url}')
  url = f'{base_url}/v3/group_channels/{channel_url}/leave'
  payload={'user_ids': member_user_ids}
  response = requests.request("PUT", url, headers=headers, json=payload)
  return response.ok 

def extract_user_ids(members):
  print(f'Extracting user ids for {len(members)} members')
  return list(map(lambda member: member.get('user_id'), members))

def fetch_members(base_url, headers, channel_url, limit, token):
  print(f'Fetching up to {limit} members for channel {channel_url}')
  url = f'{base_url}/v3/group_channels/{channel_url}/members'
  params = {'limit': limit}
  if token:
    params['token'] = token
  response = requests.request("GET", url, headers=headers, params=params)
  response_json = json.loads(response.text)
  pagination_token = response_json.get('next', '')
  members = response_json.get('members', [])
  member_user_ids = extract_user_ids(members)
  return member_user_ids, pagination_token

def remove_all_members(base_url, headers, channel_url, removal_batch_size = 100, pagination_token = None):
  print(f'Removing a batch of up to {removal_batch_size} member from {channel_url}')
  member_user_ids, new_pagination_token = fetch_members(base_url, headers, channel_url, removal_batch_size, pagination_token)
  success = remove_members(base_url, headers, channel_url, member_user_ids)
  print(f'Success: {success}')
  if new_pagination_token and (pagination_token != new_pagination_token):
    remove_all_members(base_url, headers, channel_url, removal_batch_size, new_pagination_token)
  delete_channel(base_url, headers, channel_url)

app_id = sys.argv[1]
api_token = sys.argv[2]
channel_url = sys.argv[3]
removal_batch_size = sys.argv[4]
base_url = f'https://api-{app_id}.sendbird.com'
headers = {
  'Api-Token': api_token,
  'Content-Type': 'application/json'
}
remove_all_members(base_url, headers, channel_url, removal_batch_size)



