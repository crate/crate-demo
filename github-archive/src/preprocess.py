#!/usr/bin/python

import os
import argparse
import gzip
import json
import shutil
import re
from dateutil import parser
import time


def utf8len(s):
    return len(s.encode('utf-8'))

def split_json(lines, delimiter='}{'):
  records = lines.split(delimiter);
  new_items = ['{{{0}}}'.format(x) for x in records]
  return new_items[1:-1]

def get_timestamp(t):
    dt = parser.parse(t)
    return int(time.mktime(dt.timetuple()) * 1000)

def preprocess_timefields(time_field):
    created_at = time_field.get('created_at', None)
    merged_at = time_field.get('merged_at', None)
    updated_at = time_field.get('updated_at', None)
    closed_at = time_field.get('closed_at', None)
    if created_at:
        time_field['created_at'] = get_timestamp(created_at)
    if merged_at:
        time_field['merged_at'] = get_timestamp(merged_at)
    if updated_at:
        time_field['updated_at'] = get_timestamp(updated_at)
    if closed_at:
        time_field['closed_at'] = get_timestamp(closed_at)

def preprocess_push_payload(payload):
    push_event = {}
    _commits = []
    commits = payload.get('commits', None)

    if commits:
        for commit in commits:
            _commit = {}
            message = commit.get('message', '')
            if message and utf8len(message) > 32765:
                _commit['message'] = message[:32765]
            else:
                _commit['message'] = message
            timestamp = commit.get('timestamp', None)
            if timestamp:
                _commit['timestamp'] = get_timestamp(timestamp)
            _commit['url'] = commit.get('url', None)
            _commit['id'] = commit.get('id', None)

            author = commit.get('author', None)
            if author:
                _commit['author'] = {'name': author.get('name', None), \
                    'email': author.get('email', None), \
                    'username': author.get('username', None)}
            _commits.append(_commit)
    push_event['commits'] = _commits
    push_event['size'] = payload.get('size', None)
    push_event['ref'] = payload.get('ref', None)
    push_event['distinct_size'] = payload.get('distinct_size', None)

    return push_event


def preprocess_pull_request_payload(payload):
    pull_request_event = {}
    pull_request_event['action'] = payload.get('action', None)
    pull_request_event['number'] = payload.get('number', None)
    pr = {}

    pull_request = payload.get('pull_request', None)
    if pull_request:
        pr['url'] = pull_request.get('url', None)
        pr['id'] = pull_request.get('id', None)

        body = pull_request.get('body', '')
        if body and utf8len(body) > 32765:
            pr['body'] = body[:32765]
        else:
            pr['body'] = body

        title = pull_request.get('title', '')
        if title and utf8len(title) > 32765:
            pr['title'] = title[:32765]
        else:
            pr['title'] = title

        pr['created_at'] = pull_request.get('created_at', None)
        pr['updated_at'] = pull_request.get('updated_at', None)
        pr['merged_at'] = pull_request.get('merged_at', None)
        pr['closed_at'] = pull_request.get('closed_at', None)
        preprocess_timefields(pr)
        head = pull_request.get('head', None)
        if head:
            pr['head'] = {}
            pr['head']['label'] = head.get('label', None)
            repo = head.get('repo', None)
            _repo = {}
            if repo:
                _repo['id'] = repo.get('id', None)
                _repo['name'] = repo.get('name', None)
                _repo['full_name'] = repo.get('full_name', None)
                _repo['language'] = repo.get('language', None)
                _repo['description'] = repo.get('description', None)
                _repo['created_at'] = repo.get('created_at', None)
                _repo['updated_at'] = repo.get('updated_at', None)
                _repo['merged_at'] = repo.get('merged_at', None)
                preprocess_timefields(_repo)
            pr['head']['repo'] = _repo
    pull_request_event['pull_request'] = pr
    return pull_request_event

def preprocess_repo(json_record):
    _repo = {}
    repo = json_record.get('repo', None)
    repository = json_record.get('repository', None)
    if repo:
        if repo and repo.get('id', None):
            _repo['id'] = int(repo.get('id'))
        else:
            _repo['id'] = None
        _repo['name'] = repo.get('name', None)
        _repo['url'] = repo.get('url', None)
    elif repository:
        if repository and repository.get('id', None):
            _repo['id'] = int(repository.get('id'))
        else:
            _repo['id'] = None

        description = repository.get('description', '')
        if description and utf8len(description) > 32765:
            _repo['description'] = title[:32765]
        else:
            _repo['description'] = description

        created_at = repository.get('created_at', None)
        if created_at:
            _repo['created_at'] = get_timestamp(created_at)

        pushed_at = repository.get('pushed_at', None)
        if pushed_at:
            _repo['pushed_at'] = get_timestamp(pushed_at)

        _repo['homepage']  = repository.get('homepage', None)
        _repo['language'] = repository.get('language', None)
        _repo['master_branch'] = repository.get('master_branch', None)
        _repo['name'] = repository.get('name', None)
        _repo['organization'] = repository.get('organization', None)
        _repo['owner'] = repository.get('owner', None)
        _repo['size'] = repository.get('size', None)
        _repo['stargazers'] = repository.get('stargazers', None)
        _repo['url'] = repository.get('url', None)
    return _repo

def preprocess_actor(json_record):
    actor = json_record.get('actor', None)
    actor_attributes = json_record.get('actor_attributes', None)
    _actor = {}
    if actor and isinstance(actor, str):
        _actor['login'] = actor
    elif actor:
        actor_id = actor.get('id', None)
        if actor_id:
            _actor['id'] = int(actor_id)
        else:
            _actor['id'] = None
        _actor['login'] = actor.get('login', None)
        _actor['gravatar_id'] = actor.get('gravatar_id', None)
        _actor['avatar_url'] = actor.get('avatar_url', None)
        _actor['url'] = actor.get('url', None)
    if actor_attributes:
        _actor['login'] = actor_attributes.get('login', None)
        _actor['gravatar_id'] = actor_attributes.get('gravatar_id', None)
        _actor['blog'] = actor_attributes.get('blog', None)
        _actor['company'] = actor_attributes.get('company', None)
        _actor['email'] = actor_attributes.get('email', None)
        _actor['location'] = actor_attributes.get('location', None)
        _actor['name'] = actor_attributes.get('name', None)
        _actor['type'] = actor_attributes.get('type', None)
    return _actor

def preprocess_org(json_record):
    org = json_record.get('org', None)
    _org = {}
    if org:
        org_id = org.get('id', None)
        if org_id:
            _org['id'] = int(org_id)
        else:
            _org['id'] = None
        _org['login'] = org.get('login', None)
        _org['gravatar_id'] = org.get('gravatar_id', None)
        _org['avatar_url'] = org.get('avatar_url', None)
        _org['url'] = org.get('url', None)
    return _org

def get_values_from_dict(src, v):
    if isinstance(src, dict):
        for key, value in src.items():
            get_values_from_dict(value, v)
    elif isinstance(src, list):
        for s in src:
            get_values_from_dict(s, v)
    else:
        v.append(str(src))

def process_record(record):
    json_record = json.loads(record)

    payload_type = json_record.get('type', None)
    payload = json_record.get('payload', '')

    ft = []
    get_values_from_dict(json_record, ft)
    json_record['record_ft'] = ' '.join(ft)
    json_record['repo'] = preprocess_repo(json_record)
    json_record['actor'] = preprocess_actor(json_record)
    json_record['org'] = preprocess_org(json_record)
    created_at = json_record.get('created_at', None)
    if created_at:
        json_record['created_at'] = get_timestamp(created_at)

    json_record.pop('repository', None)
    json_record.pop('actor_attributes', None)

    if  isinstance(payload, dict):
        if payload_type == 'PushEvent':
            json_record['payload_push_event'] = preprocess_push_payload(payload)

        if payload_type == 'PullRequestEvent':
            json_record['payload_pull_request_event'] = preprocess_pull_request_payload(payload)

    return json.dumps(json_record) + '\n'


def wcl(file_name):
    with gzip.open(file_name, 'rb') as f:
        return sum(1 for line in f)

def process_file(in_file):
    out_file = '_' + in_file

    number_lines = wcl(in_file)
    with gzip.open(in_file, 'rb') as fr, gzip.open(out_file, "a+b") as fw:
        if number_lines > 1:
            for record in fr:
                try:
                    record = record.decode("utf-8")
                    fw.write(bytes(process_record(record), 'utf-8'))
                except Exception as e:
                    print('Can\'t parse the record {}'.format(e))
        else:
            for line in fr:
                try:
                    line = line.decode("utf-8")
                    for record in split_json(line):
                        try:
                            fw.write(bytes(process_record(record), 'utf-8'))
                        except Exception as e:
                            print('Can\'t parse the record {}'.format(e))
                except Exception as e:
                    print('Can\'t parse the record line {}'.format(e))
    shutil.move(out_file, in_file)
