from pathlib import Path

from aws_cdk import CfnOutput, CfnResource, Stack
from aws_cdk import aws_ecr_assets as ecr_assets
from constructs import Construct


class AgentCoreStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        root_dir = Path(__file__).resolve().parents[1]

        flight_image = ecr_assets.DockerImageAsset(
            self,
            "FlightImage",
            directory=str(root_dir),
            file="agents/flight/Dockerfile",
        )
        hotel_image = ecr_assets.DockerImageAsset(
            self,
            "HotelImage",
            directory=str(root_dir),
            file="agents/hotel/Dockerfile",
        )
        orchestrator_image = ecr_assets.DockerImageAsset(
            self,
            "OrchestratorImage",
            directory=str(root_dir),
            file="agents/orchestrator/Dockerfile",
        )

        self._add_agent("FlightAgent", "flight-agent", flight_image.image_uri)
        self._add_agent("HotelAgent", "hotel-agent", hotel_image.image_uri)
        self._add_agent(
            "OrchestratorAgent", "orchestrator-agent", orchestrator_image.image_uri
        )

        CfnOutput(self, "FlightImageUri", value=flight_image.image_uri)
        CfnOutput(self, "HotelImageUri", value=hotel_image.image_uri)
        CfnOutput(self, "OrchestratorImageUri", value=orchestrator_image.image_uri)

    def _add_agent(self, resource_id: str, name: str, image_uri: str) -> None:
        CfnResource(
            self,
            resource_id,
            type="AWS::AgentCore::Agent",
            properties={
                "AgentName": name,
                "ContainerImageUri": image_uri,
            },
        )
