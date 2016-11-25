function map(){
	for(var i in this.interests) {
		emit(this.interests[i], 1);
	}
}

function reduce(key, values) {
	var sum = 0;
	for(var i in values) {
		sum += values[i];
	}
	return sum;
}
db.employee_info.mapReduce(map, reduce, { out : "interests" })