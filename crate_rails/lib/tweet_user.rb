require 'active_record/attribute_methods/crate_object'

class TweetUser
  attr_accessor :created_at, :description, :followers_count, :friends_count, :id, :location, :statuses_count, :verified

  include CrateObject

  def initialize(opts)
    @user_created_at = opts[:created_at]
    @user_description = opts[:description]
    @user_followers_count = opts[:followers_count]
    @user_friends_count = opts[:friends_count]
    @user_id = opts[:id]
    @user_location = opts[:location]
    @user_statuses_count = opts[:statuses_count]
    @user_verified = opts[:verified]
  end

end
