require 'tweet_user'

class Tweet < ActiveRecord::Base
  serialize :user, TweetUser
end
