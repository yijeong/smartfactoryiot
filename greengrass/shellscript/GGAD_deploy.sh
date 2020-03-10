#!/bin/bash

# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# This bash shell script creates a Keypair and an EC2 Instacne 
# The created EC2 instance will function as a Greengrass Awared Device 
echo GGAD security group :
read ggad_secg

echo GGAD subnet : 
read ggad_subnet

echo 1. Create a keypair

echo Searching for existing keypair named sfworkshop-keypair
keyname=$(aws ec2 describe-key-pairs --key-names sfworkshop-keypair --region us-east-1 --query 'KeyPairs[0].KeyName' --output text)
if  [[ "$keyname" == "sfworkshop-keypair" ]]; then
    echo Keypair sfworkshop-keypair already exists. Please choose another keypair name by editing this script
    exit 1
fi
 
echo Creating a keypair named sfworkshop-keypair. The .pem file will be in your $HOME directory
aws ec2 create-key-pair --key-name sfworkshop-keypair --region us-east-1 --query 'KeyMaterial' --output text > ~/sfworkshop-keypair.pem
if [ $? -gt 0 ]; then
    echo Keypair sfworkshop-keypair could not be created. Please delete the old one. 
    exit $?
fi

chmod 400 ~/sfworkshop-keypair.pem
sleep 10

echo Create an EC2 instance, the Greengrass Awared Device of Greengrass Core Group ...
aws ec2 run-instances --image-id ami-07ebfd5b3428b6f4d --instance-type t3.large --key-name sfworkshop-keypair --security-group-ids $ggad_secg --subnet-id $ggad_subnet --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=SFworkshop-thing}]' --region us-east-1 --output json