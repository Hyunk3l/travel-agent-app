from aws_cdk import App
from aws_cdk.assertions import Template

from infra.agentcore_stack import AgentCoreStack


def test_agentcore_stack_has_three_agents():
    app = App()
    stack = AgentCoreStack(app, "TestStack")
    template = Template.from_stack(stack)

    template.resource_count_is("AWS::AgentCore::Agent", 3)
