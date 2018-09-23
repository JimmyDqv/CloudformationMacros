# Macro Ec2KeyPair
  
What is the problem that we try to solve with this macro?  
When creating a EC2 instance we need to create a key pair to be able to ssh into it.  
The creation of that key pair today either have to be done manually or via the cli since there is no support in CloudFormation.
There is also a need to be able to rotate the keys in an easy way.  
There is always a need to make the entire process automatic, since all manual steps are always a potential place where errors can occure.

## The Macro
This Macro will create or rotate the key pair and store it in S3 for users to download.  
The Macro will then return the key pair name for the EC2 to use, thereby completing the template.

## Parameters
The Macro accepts 4 different parameters:  
 * __Operation:__  
   * CREATE: This will create the key pair if it doesn't exists, otherwise the already existing key pair will be used.  
   * ROTATE: This operatin will rotate key pair if it exists otherwise it will be created. 
 * __S3Bucket:__  
 The S3 bucket to store the key pair in
 * __S3Key:__  
 The s3 key to store the key pair under
 * __Keyname:__  
 The name of the key pair  

## Deploying the Macro
The macro is deployed by deploying the CloudFormation template macro.yaml  
Below is an example on how to do that.

```bash
#!/bin/bash

DEPLOYMENT_BUCKET_NAME=my-temporary-deploy-bucket

echo "creating package ..."
aws cloudformation package \
    --template-file macro.yaml \
    --s3-bucket ${DEPLOYMENT_BUCKET_NAME} \
    --output-template-file packaged-template.yaml

echo "deploying package ..."
aws cloudformation deploy \
    --template-file packaged-template.yaml \
    --stack-name macro-ec2-key-pair \
    --capabilities CAPABILITY_NAMED_IAM
 ```  
  

## Example usage
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Ec2KeyPair macro example template

Resources:
  BastionEC2Instance:
  # The bastion Host.
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      ImageId: <ami id>
      SubnetId: <your subnet id>
      KeyName: 
        Fn::Transform: 
          Name: "Ec2KeyPair"
          Parameters:
            'Operation' : 'CREATE'
            'S3Bucket' : '<bucket name>'
            'S3Key' : 'keypairtest.pem'
            'Keyname' : '<key name>'
      SecurityGroupIds: 
        - <security group>
      Monitoring: False
``` 