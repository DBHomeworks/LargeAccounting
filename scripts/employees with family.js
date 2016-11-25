var mapFunction = function() {
                       emit(this.name, this.family);
                   };
                   
var reduceFunction = function(keyId, valuesSalaries) {
                          return Array.sum(valuesSalaries);
                      };
                      
db.employee_info.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Employees with family" }
                   )