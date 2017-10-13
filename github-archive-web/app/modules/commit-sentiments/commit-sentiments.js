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

angular.module('crate.demo.modules.commit-sentiments', ['ngRoute', 'chart.js', 'hljs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/m/mentions', {
    templateUrl: 'modules/commit-sentiments/commit-sentiments.html',
    controller: 'CommitSentimentsCtrl'
  });
}])

.controller('CommitSentimentsCtrl', ["$scope", "Crate", function($scope, Crate) {

  var query = [
    "SELECT date_format('%Y-%m', date_trunc('month', created_at)) AS date, \n       count(*) AS \"Tea\" \nFROM github \nWHERE match(record_ft, 'tea') \n  AND TYPE = 'PushEvent' \nGROUP BY date\nORDER BY date ASC",

    "SELECT date_format('%Y-%m', date_trunc('month', created_at)) AS date, \n       count(*) AS  \"Coffee\" \nFROM github \nWHERE match(record_ft, 'coffee') \n  AND TYPE = 'PushEvent' \nGROUP BY date\nORDER BY date ASC"
  ];

  var currentQuery = null;
  var chart = {};
  var duration = 0;
  var error = {};



  var mergeResults = function(results) {

    var labels = results[1].rows.map(function(row) {
      return row[0];
    });

    duration = results.reduce(function(p, c) {
      return p + c.duration;
    }, 0) / results.length;
    chart = {
      labels: labels,
      data: results.map(function(result) {
        return result.rows.map(function(row) {
          return row[1];
        });
      }),
      series: results.map(function(result) {
        return result.cols[1];
      })
    };
  };

  var showError = function(result) {
    error = result;
  };


  function runQuery() {
    currentQuery =
      Crate.query({
        stmt: query[0]
      }).$promise
      .then(function(success0) {
        Crate.query({
            stmt: query[1]
          }).$promise
          .then(function(success1) {
            mergeResults([success0, success1])
          }, showError)
          .then(function() {
            currentQuery = null;
          })
          .then(refresh);

      }, showError)

    refresh();
  };

  function refresh() {
    $scope.page = {
      heading: 'Tea or Coffee?',
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
