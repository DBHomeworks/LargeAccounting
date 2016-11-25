db.employee_info.aggregate([
                     { $group: { _id : "$workplace.company", salary: { $sum: "$workplace.salary" } } },
                     { $sort: { salary : 1 } }
                   ])