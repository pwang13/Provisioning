
var AWS = require('aws-sdk');
AWS.config.update({region:'us-east-1'});

var ec2 = new AWS.EC2();

var params = {
	ImageId: "ami-2d39803a",
	InstanceType: "t2.micro",
	KeyName: "pwangAnsible",
	SecurityGroupIds: ["sg-de178fa4"],
	MinCount: 1, MaxCount: 1
};

//Create the instance
ec2.runInstances(params, function(err, data) {
	if (err) { console.log("Could not create instance", err); return; }

	var instanceId = data.Instances[0].InstanceId;
	console.log("Created instance", instanceId);
  	// Add tags to the instance
  	params = {Resources: [instanceId], Tags: [
  		{Key: 'Name', Value: 'instanceName'}
  		]};
  		ec2.createTags(params, function(err) {
  			console.log("Tagging instance", err ? "failure" : "success");
  		});
  	});


