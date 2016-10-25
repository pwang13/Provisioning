var AWS = require('aws-sdk');
AWS.config.update({region:'us-east-1'});
var ec2 = new AWS.EC2();

var fs = require('fs');

//get public ip
ec2.describeInstances(function(err, result) {
	if (err)
		console.log(err);
	var inst_id = '-';

	//open file descriptor
	fs.writeFile("inventory", "[myServers]", function(err) {
		if(err) {
			return console.log(err);
		}
	}); 

	//iterate through instances
	for (var i = 0; i < result.Reservations.length; i++) {
		var res = result.Reservations[i];
		var instances = res.Instances;


		for (var j = 0; j < instances.length; j++) {
			var public_ip = instances[j].PublicIpAddress;
			console.log(public_ip);
			//write into inverntory
			if (public_ip !== undefined) {

				fs.appendFile("inventory", "\n" + public_ip, function(err) {
				});
				
			}
		}
	}


});