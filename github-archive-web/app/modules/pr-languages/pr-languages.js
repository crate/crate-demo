// Licensed to CRATE Technology GmbH ("Crate") under one or more contributor
// license agreements.

// See the NOTICE file distributed with this work for
// additional information regarding copyright ownership.  Crate licenses
// this file to you under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.  You may
// obtain a copy of the License at
//  http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
// License for the specific language governing permissions and limitations
// under the License.

// However, if you have executed another commercial license agreement
// with Crate these terms will supersede the license and you may use the
// software solely pursuant to the terms of the relevant commercial agreement.


'use strict';

angular.module('crate.demo.modules.pr-languages', ['ngRoute', 'chart.js', 'hljs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/m/pr-languages', {
    templateUrl: 'modules/pr-languages/pr-languages.html',
    controller: 'PRLanguagesCtrl'
  });
}])

.controller('PRLanguagesCtrl', ["$scope", "Crate", function($scope, Crate) {

  var query = "SELECT payload_pull_request_event['pull_request']['head']['repo']['language'] AS language, \n       COUNT(*) AS num_pull_requests, \n       COUNT(DISTINCT(repo['id'])) AS num_repos \nFROM github \nWHERE type = 'PullRequestEvent' \n  AND  payload_pull_request_event['pull_request']['head']['repo']['language'] IS NOT NULL \n  AND repo['id'] IS NOT NULL \nGROUP BY 1 \nORDER BY 2 DESC \nLIMIT 10";

  var currentQuery = null;
  var chart = {};
  var duration = 0;
  var error = {};

  var showResults = function(result) {

    var labels = result.rows.map(function(row) {
      return row[0];
    });
    duration = result.duration;
    chart = [{
      labels: labels,
      data: result.rows.map(function(row) {
        return row[1];
      })
    }, {
      labels: labels,
      data: [result.rows.map(function(row) {
        return row[2];
      })],
      series: []
    }];
  };
  var showError = function(result) {
    error = result;
  };


  function runQuery() {
    currentQuery = Crate.query({
        stmt: query
      }).$promise
      .then(showResults, showError)
      .then(function() {
        currentQuery = null;
      })
      .then(refresh);

    refresh();
  };

  function refresh() {
    $scope.page = {
      heading: 'Pull Request Languages',
    };

    $scope.query = {
      text: query,
      duration: duration,
      chart: chart,
      running: !!currentQuery,
      error: error
    };

    $scope.events = {
      runQuery: runQuery
    };
  };
  refresh();

}]);
