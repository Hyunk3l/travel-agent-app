# Intent
Right now the different agents are just python files. I want to make them independent agents.

# Scope
In scope:
- Infrastructure changes
- Project structure changes

Out of scope:
- Any business logic
- Changes in the UI

# Functional requirements
- None

# Non functional requirements
- Agents must be deployable using AWS CDK and AWS AgentCore
- The three agents must (flight, hotel and orchestrator) have 3 different directories
- Each agent must have a Dockerfile
- All the code must be tested
- Remember to clean up old files
- Update the README once done
