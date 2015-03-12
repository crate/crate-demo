#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy import func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from crate.client.sqlalchemy.types import Object


hosts = ['localhost:4200']
engine = sa.create_engine('crate://', connect_args={'servers': hosts})
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()


class Tweet(Base):
    __tablename__ = 'tweets'

    id = sa.Column(sa.String, primary_key=True)
    created_at = sa.Column(sa.DateTime)
    text = sa.Column(sa.String)
    source = sa.Column(sa.String)
    retweeted = sa.Column(sa.Boolean)
    user = sa.Column(Object)

    def __repr__(self):
        return '<Tweet {0}>'.format(self.user.get('id'))


tweets = session.query(Tweet)
tweets_austria = session.query(Tweet).filter(func.match(Tweet.text, 'Austria'))

group_by_followers_count = session\
    .query(Tweet.user['followers_count'], func.count(Tweet.user['followers_count']))\
    .group_by(Tweet.user['followers_count'])\
    .order_by(desc(func.count(Tweet.user['followers_count'])))


from IPython import embed
embed()
