#!/usr/bin/env python

import collections
from ansible import utils, errors
import json
import yaml
import sys
from ansible.module_utils.basic import *

try:
  import boto3
except ImportError:
  raise errors.AnsibleError(
    "Can't LOOKUP(cloudformation): module boto3 is not installed")

def main():
  module = AnsibleModule(
    argument_spec = dict(
      stack_name = dict(required=True, type='str'),
      fact = dict(required=True, type='str'),
      fact_type = dict(required=False, type='str'),
      region = dict(required=False, type='str')
    )
  )

  stack_name = module.params.get('stack_name')
  region = module.params.get('region')

  if region is not None:
    cfn_client = boto3.client('cloudformation', region_name=region)
  else:
    cfn_client = boto3.client('cloudformation')

  outputs_fixed = {}
  stacks = cfn_client.describe_stacks(StackName=stack_name)['Stacks']

  if len(stacks) == 0:
    module.exit_json(
      Changed=False,
      Failed=True,
      msg=('Stack: {0} was not found!'.format(stack_name))
    )

  for output in stacks[0]['Outputs']:
    outputs_fixed[output['OutputKey']] = output['OutputValue']

  result = dict(changed=False, failed=False)
  if module.params.get('fact') is not None:
    if module.params.get('fact_type') == 'yaml':
      result['ansible_facts'] = { module.params.get('fact'): yaml.safe_load(outputs_fixed) }
    elif module.params.get('fact_type') == 'json':
      result['ansible_facts'] = { module.params.get('fact'): json.load(outputs_fixed) }
    else:
      result['ansible_facts'] = { module.params.get('fact'): outputs_fixed }


  module.exit_json(**result)

main()
