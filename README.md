# ansible-role-module-cfn-lookup

Role / Module for looking up CloudFormation outputs

This can be used as either a role or a module.

If used as a role, run the role with the **cfn_lookup_stack_name** parameter:

```yaml
roles:
  - role: cfn_lookup
    cfn_lookup_stacks:
      - stack_name: "some_stack"
        fact_name: "some_fact"
```

This will look up the stack outputs for stack "some_stack" and place them in the fact "some_fact".

If used as a module, just run the role first with no parameters, then run the module as a task:

```yaml
- name: Look up stack outputs by stack name
  cfn_lookup:
    stack_name: "some_stack"
    fact_name: "some_fact"
  register: stack_outputs
```
