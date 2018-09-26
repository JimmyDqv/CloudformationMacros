# Macro CommonTags
  
What is the problem that we try to solve with this macro?  
It's really common that you want to add the same tag to all of your resources, it could be for cost allocation or similar.  
Adding the same tag value over and over again produce a lot of boiler plate code. This macro will add specified common tags to all resources supporting tags.  

## The Macro

This Macro will add tags specified in the parameter section to all resources that support tags.  
The macro is intended to be run on the entire template and should be put in the "Transform" section.  
If a tag-key is already present on a resources this macro will not modify the value. That mean that you can override the default values.  

## Parameters

The parameters should be the tags to be added as a key:value pair.  

```yaml
  Parameters:
    'MyKey' : 'MyValue'
    'MyKey2' : 'MyValue2'
```  

You can override the default value of a key by just specifying it on your resource as well.  

```yaml
  Bucket1:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-super-duper-testing-bucket
      Tags:
        - Key: 'MyKey'
          Value: 'this overrides the default value for MyKey in the macro parameters'
```  

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
    --stack-name cfn-macro-common-tags\
    --capabilities CAPABILITY_NAMED_IAM
 ```  
  
## Example usage

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: CommonTags macro example template
Transform:
  Name: CommonTags
  Parameters:
    'Name' : 'MySuperCoolApp'
    'CreatedBy' : 'Me'
    'CostAllocation' : 'MySuperCoolApp'

Resources:
  Bucket1:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-super-duper-cool-app-bucket
      Tags:
        - Key: CostAllocation
          Value: override
  
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      ImageId: ami-123456789
      SubnetId: subnet-123456789
      SecurityGroupIds:
        - sg-123456789
      Monitoring: False
```  