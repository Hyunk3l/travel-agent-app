from aws_cdk import App

from infra.agentcore_stack import AgentCoreStack


app = App()
AgentCoreStack(app, "TravelAgentAgentCore")
app.synth()
