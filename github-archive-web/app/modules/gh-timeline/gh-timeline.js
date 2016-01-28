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

angular.module('crate.demo.modules.gh-timeline', ['ngRoute', 'chart.js', 'hljs'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/m/gh-timeline', {
    templateUrl: 'modules/gh-timeline/gh-timeline.html',
    controller: 'GHTimelineCtrl'
  });
}])

.controller('GHTimelineCtrl', ["$scope", "Crate", "$timeout", function($scope, Crate, $timeout) {

  var windowEnd = 1357344000000;
  var windowStart = 1356998400000;
  var days = 0;
  var count = 0;
  var windowSize = 1;

  var addDays = function() {
    windowStart = windowEnd;
    windowEnd = windowEnd + 86400000 * days;
  };

  var query = "...";

  var refreshQuery = function() {
    query = `SELECT COUNT(*), type, date_format('%Y-%m-%d', created_at) AS label, (created_at / 1000 / 60 / 60 / 24) - 15706 as days_since_start \nFROM github \nWHERE created_at >= ${windowStart} AND created_at < ${windowEnd} \nGROUP BY 4, 2, 3 \nORDER BY 4, 1 DESC`;
  };
  refreshQuery();

  var currentQuery = null;
  var chart = [];
  var duration = 0;
  var error = {};

  var dataObj = {};

  var data = {
    series: new Set(),
    labels: new Set(),
  };

  var showResults = function(result) {
    if (result.rowcount) {
      var dayCount = result.rows[result.rows.length - 1][3] + 1;

      result.rows.reduce(function(obj, row) {
        var n = row[1];
        var x = row[3];
        var val = [];
        if (n in obj) {
          val = obj[n];
        }
        val = val.concat(new Array(dayCount - val.length).fill(0));

        val[x] = row[0];
        obj[n] = val;
        return obj;
      }, dataObj);

      Object.keys(dataObj).filter(function(k) {
        return dataObj[k].length < dayCount;
      }).forEach(function(k) {
        dataObj[k] = dataObj[k].concat(new Array(dayCount - dataObj[k].length).fill(0));
      });

      result.rows.forEach(function(row) {
        data.labels.add(row[2]);
      });

      Object.keys(dataObj).forEach(function(e)  {
        data.series.add(e);
      });

      duration = result.duration;
      var series = [...data.series];
      chart = [{
        labels: [...data.labels],
        series: series,
        data: series.map(function(s) {
          return dataObj[s];
        })
      }];
    }
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
      .then(refresh)
      .then(function(d) {

        if (count < 5) {
          days += windowSize;
          addDays();
          refreshQuery();
          $timeout(runQuery, 6000);
          count++;
        }
      });

    refresh();
  };

  function refresh() {
    $scope.page = {
      heading: 'GitHub Timeline',
    };

    $scope.query = {
      text: query,
      duration: duration,
      chart: chart,
      running: !!currentQuery,
      error: error,
    };

    $scope.events = {
      runQuery: runQuery
    };
  };
  refresh();
}]);
