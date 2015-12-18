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


angular.module('crate.demo.modules.frontpage', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/hi', {
    templateUrl: 'modules/frontpage/frontpage.html',
    controller: 'FrontpageCtrl'
  });
}])

.controller('FrontpageCtrl', ["$scope", "Crate", function($scope, Crate) {

  var typeQuery = "select type, count(*) from github group by 1 order by 2 desc limit 6";
  var countQuery = "select count(*) from github";

  var currentQuery = null;
  var chart = {};
  var duration = 0;
  var error = {};
  var totalRows = 0;


  var showResults = function(result) {

    var labels = result.rows.map(function(row) {
      return row[0];
    });
    duration = result.duration;
    chart = {
      labels: labels,
      data: result.rows.map(function(row) {
        return row[1];
      })
    };
  };

  var showError = function(result) {
    error = result;
  };

  function runQuery() {
    Crate.query({
        stmt: countQuery
      }).$promise
      .then(function(success) {
        totalRows = success.rows[0][0];
      })
      .then(refresh);

    currentQuery = Crate.query({
        stmt: typeQuery
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
      heading: 'Github Archive Data with Crate',
    };

    $scope.results = {
      rows: totalRows
    };


    $scope.query = {
      text: typeQuery,
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
  runQuery();
}]);
