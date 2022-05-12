#!/usr/bin/env python3
import os
from aws_cdk import core as cdk

from devsecops_quickstart.opa_scan.opascan import OPAScanStack
from devsecops_quickstart.cfn_nag.cfn_nag import CfnNag
from devsecops_quickstart.pipeline import CICDPipelineStack

app = cdk.App()
config = app.node.try_get_context("config")
general_config = config["general"]

opa_scan = OPAScanStack(
    app,
    id=f"{general_config['repository_name']}-opa-scan",
    general_config=general_config,
    env=cdk.Environment(
        account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
        region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
    ),
)

cfn_nag = CfnNag(
    app,
    id=f"{general_config['repository_name']}-cfn-nag",
    general_config=general_config,
    env=cdk.Environment(
        account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
        region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
    ),
)

developmentPipeline = CICDPipelineStack(
    app,
    id=f"{general_config['repository_name']}-ci-development",
    general_config=general_config,
    is_development_pipeline=True,
    opa_scan_rules_bucket_name=opa_scan.opa_rules_bucket_url,
    opa_scan_lambda_arn=opa_scan.opa_lambda_arn,
    opa_scan_role_arn=opa_scan.opa_role_arn,
    cfn_nag_lambda_arn = cfn_nag.cfn_nag_lambda_arn,
    cfn_nag_role_arn = cfn_nag.cfn_nag_role_arn,
    env=cdk.Environment(
        account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
        region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
    ),
)

app.synth()
