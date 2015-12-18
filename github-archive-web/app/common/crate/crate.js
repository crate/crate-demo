var crateServices = angular.module('crate.demo.services', ['ngResource']);

crateServices.factory('Crate', ['$resource',
  function($resource) {
    return $resource('https://play.crate.io/_sql', {}, {
      query: {
        method: 'POST',
        params: {},
        isArray: false
      }
    });
  }
]);
