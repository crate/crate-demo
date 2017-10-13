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

angular.module('crate.demo.modules.pr-latency', ['ngRoute', 'chart.js', 'hljs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/m/pr-latency', {
    templateUrl: 'modules/pr-latency/pr-latency.html',
    controller: 'PRLatencyCtrl'
  });
}])

.controller('PRLatencyCtrl', ["$scope", "Crate", function($scope, Crate) {

  var query = "SELECT COUNT(*) / 1000 AS cnt,\n cast((payload_pull_request_event['pull_request']['merged_at'] - payload_pull_request_event['pull_request']['created_at']) / 1000.0 / 60.0 / 60.0  AS integer) as hours_to_merge \nFROM github \nWHERE payload_pull_request_event['pull_request']['created_at'] >= '2012-01-01' \n  AND payload_pull_request_event['pull_request']['created_at'] <= '2015-08-31' \n  AND payload_pull_request_event['pull_request']['created_at'] IS NOT NULL \n  AND payload_pull_request_event['pull_request']['merged_at'] IS NOT NULL \nGROUP BY 2 \nORDER BY 2 ASC\nLIMIT 24";

  var currentQuery = null;
  var chart = [];
  var duration = 0;
  var error = {};

  var showResults = function(result) {

    var labels = result.rows.map(function(row) {
      return row[1];
    });
    duration = result.duration;
    chart = [{
      labels: labels,
      data: [result.rows.map(function(row) {
        return row[0];
      })]
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
      heading: 'Pull Request Latency',
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
