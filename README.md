
## DevSecOps Golden Pipeline

This artifact sets up a ready-to-use development environment integrated with a CI pipeline with security and DevOps best practices. Upon successful deployment, you will have:

- an AWS CodeCommit Git repository (with a Future option to integrate an existing Gitlab repository)
- a multi-stage, multi-account CI pipeline integrated with the code repository  
- pipeline integration with [Bandit](https://github.com/PyCQA/bandit) for finding common security issues in Python code 
- pipeline integration with [Snyk](https://snyk.io/) for continuously monitoring for vulnerabilities in your dependencies
- pipeline integration with [CFN NAG](https://github.com/stelligent/cfn_nag) to look for patterns in 
  CloudFormation templates that may indicate insecure infrastructure
- pipeline integration with [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) that enables you define and
  enforce policies on infrastructure resources at development time
- (Future) pipeline integration with cfn-policy-validator, a tool that dynamically checks for security issues in CloudFormation policies
- (Future) A configuration file that allows for customization of how the tools should execute
- (Future) An output summary of the tools executed by the pipeline.
- (Future) pipeline integration to ensure that a valid LICENSE file is present in your repository.

![validate](./assets/validate.png)

### Install

Create a Cloud9 instance and clone this repository using:
```
git clone <Repo URL here>
```

Create and activate your Python virtual environment, then install the dependencies.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# TODO - Automatically update `cdk.json` with account number and region values to be used for golden pipeline deployment.
```

### Bootstrap

Make sure you have credentials for the toolchain account in a profile named `golden-pipeline-profile`.

Bootstrap the golden pipeline account:
```
AWS_REGION=$(aws configure get region)
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
cdk bootstrap \
  --profile golden-pipeline-profile \
  --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
  aws://$AWS_ACCOUNT/$AWS_REGION
```

Bootstrap the target accounts. You only need to do this one time per environment where you want
to deploy CDK applications.

### Deploy
#### Snyk
For Snyk integration, you need to provide authentication token with a Snyk profile account. You can sign up for a
free Snyk account [here](https://app.snyk.io/login?cta=sign-up&loc=body&page=try-snyk). After sign up, you can get
your Auth Token from the Account Settings section in your profile.

Using the retrieved authentication token, use secret helper tool to securely store the authentication token 
in AWS Secret Manager in the toolchain account to share it with the deployment pipeline:
```
$ ./create_secret_helper.sh snyk-auth-token <snyk-auth-token-value>
```

#### CDK Deployment
```
cdk deploy --all
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
