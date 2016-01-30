angular.module('myApp', ['apiService', 'n3-line-chart'])

.controller('status_controller', function($scope, execute_api_call) {
    
    
    $scope.init = function(status_inquiry_call){
         //reads device status on page loading
        execute_api_call.execute(status_inquiry_call)
    
                .success(function(returned_data) {
                    $scope.current_status =  returned_data;
                });
        
    };
    
    
    //function for button clicks, changes status and then updates status on ui
    $scope.change_status =  function(status_request, status_inquiry_call){
        
        var api_call = status_request;

        execute_api_call.execute(api_call)
    
            .success(function(returned_data) {

                execute_api_call.execute(status_inquiry_call)
    
                    .success(function(returned_data) {
                        $scope.current_status =  returned_data;
                });
                    
                    
          });
    };
    
})


.controller('enterValue', function($scope, execute_api_call) {
    
    $scope.init = function(status_inquiry_call){
         //reads device status on page loading
        execute_api_call.execute(status_inquiry_call)
    
                .success(function(returned_data) {

                    $scope.current_status =  returned_data;
                });
        
    };  
    
    $scope.reset = function(variable, input_data, status_inquiry_call) {
        
       var api_call = variable + "/" + input_data;
       
    
        execute_api_call.execute(api_call)
    
                .success(function(returned_data) {

                    execute_api_call.execute(status_inquiry_call)
    
                        .success(function(returned_data) {
                            $scope.current_status =  returned_data;
                            
                    });
                    
                });
    };
    
});