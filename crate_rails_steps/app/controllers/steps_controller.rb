class StepsController < ApplicationController

  def index
    @steps = Step.all.limit(100)
    puts YAML::dump(@steps)

    # @steps = Step.where(:username => 'gosinski', :monthly_partition => 201409).limit(1000)

  end

  def show
    @step = Step.find(params[:id])
  end

end
