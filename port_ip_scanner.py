import boto3

# $ aws --profile=cflex-devdemo ec2 describe-addresses --public-ips --query "Addresses[*].[InstanceId,PublicIp,Tags[*]]"
def get_elastic_ips:



if __name__ == "__main__":
    get_elastic_ips()