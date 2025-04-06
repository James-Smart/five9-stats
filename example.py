"""
Example script demonstrating how to use the Five9 Statistics API client library.

This script shows how to use both the Interval Statistics API and the Real-time Stats Snapshot API.
"""

import asyncio
import logging
from datetime import datetime

from five9_stats.api.interval import IntervalStatsClient
from five9_stats.api.snapshot import SnapshotStatsClient


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configure specific loggers
logging.getLogger("five9_stats.api.client").setLevel(logging.DEBUG)
logging.getLogger("aiohttp").setLevel(logging.INFO)

# Note: The client now uses OAuth 2.0 Bearer Token authentication
# The authentication flow is handled automatically when you use the client as an async context manager
# 1. When you create a client instance, it stores your username and password
# 2. When you use the client in an async context manager, it authenticates and obtains a token
# 3. The token is automatically refreshed when needed
# 4. All API requests include the Bearer token in the Authorization header

async def interval_stats_example(username, password, domain_id):
    """Example using the Interval Statistics API."""
    
    logger.info("Starting Interval Statistics API example")
    
    # Initialize the client
    # The base URL depends on your Five9 domain region
    # Options include:
    # - US: https://api.prod.us.five9.net
    # - Canada: https://api.prod.ca.five9.net
    # - EU: https://api.prod.eu.five9.net
    # - UK: https://api.prod.uk.five9.net
    # - India: https://api.prod.in.five9.net
    base_url = "https://api.prod.us.five9.net"  # Default to US region
    
    logger.info(f"Initializing Interval Stats client with base URL: {base_url}")
    client = IntervalStatsClient(
        username=username,
        password=password,
        base_url=base_url,
        timeout=60,  # Increase timeout
        max_retries=5  # Increase retries
    )
    
    # Use the client as an async context manager
    # This will automatically handle authentication and token management
    async with client:
        try:
            # Get statistics metadata
            logger.info("Getting statistics metadata")
            metadata = await client.get_statistics_metadata(domain_id=domain_id)
            logger.info(f"Available statistics types: {[m.statistics_type for m in metadata.items]}")
            
            # Get agent statistics
            logger.info("Getting agent statistics")
            agent_stats = await client.get_agent_statistics(
                domain_id=domain_id,
                media_types="VOICE,CHAT,EMAIL",
                time_period="LAST_15_MINUTES"
            )
            
            # Print agent statistics
            logger.info(f"Retrieved {len(agent_stats.data)} agent statistics")
            for agent in agent_stats.data:
                logger.info(f"Agent ID: {agent.id}")
                logger.info(f"Total calls handled: {agent.total_calls_handled}")
                logger.info(f"Total chats handled: {agent.total_chats_handled}")
                logger.info(f"Total emails handled: {agent.total_emails_handled}")
                logger.info("---")
            
            # Get campaign statistics
            logger.info("Getting campaign statistics")
            campaign_stats = await client.get_campaign_statistics(
                domain_id=domain_id,
                campaign_type="INBOUND",
                media_types="VOICE,CHAT,EMAIL",
                time_period="LAST_15_MINUTES"
            )
            
            # Print campaign statistics
            logger.info(f"Retrieved {len(campaign_stats.data)} campaign statistics")
            for campaign in campaign_stats.data:
                logger.info(f"Campaign ID: {campaign.id}")
                logger.info(f"Total calls handled: {campaign.total_calls_handled}")
                logger.info(f"Total chats handled: {campaign.total_chats_handled}")
                logger.info(f"Total emails handled: {campaign.total_emails_handled}")
                logger.info("---")
            
        except Exception as e:
            logger.error(f"Error in interval stats example: {str(e)}")
            # Print exception type and traceback for debugging
            import traceback
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Traceback: {traceback.format_exc()}")


async def snapshot_stats_example(username, password, domain_id):
    """Example using the Real-time Stats Snapshot API."""
    
    logger.info("Starting Real-time Stats Snapshot API example")
    
    # Initialize the client
    # Using the same base URL as for the interval stats client
    logger.info(f"Initializing Snapshot Stats client with base URL: {base_url}")
    client = SnapshotStatsClient(
        username=username,
        password=password,
        base_url=base_url,
        timeout=60,  # Increase timeout
        max_retries=5  # Increase retries
    )
    
    # Use the client as an async context manager
    # This will automatically handle authentication and token management
    async with client:
        try:
            # Get ACD status
            logger.info("Getting ACD status")
            acd_status = await client.get_acd_status(
                domain_id=domain_id,
                media_types="VOICE,CHAT,EMAIL"
            )
            
            # Print ACD status
            logger.info(f"Retrieved {len(acd_status.data)} ACD status entries")
            for skill in acd_status.data:
                logger.info(f"Skill ID: {skill.id}")
                logger.info(f"Active calls: {skill.active_calls}")
                logger.info(f"Agents active: {skill.agents_active}")
                logger.info(f"Agents on call: {skill.agents_on_call}")
                logger.info(f"Calls in queue: {skill.calls_in_queue}")
                logger.info(f"Chats in queue: {skill.chats_in_queue}")
                logger.info("---")
            
            # Get agent state
            logger.info("Getting agent state")
            agent_state = await client.get_agent_state(
                domain_id=domain_id,
                media_types="VOICE,CHAT,EMAIL"
            )
            
            # Print agent state
            logger.info(f"Retrieved {len(agent_state.data)} agent state entries")
            for agent in agent_state.data:
                logger.info(f"Agent ID: {agent.id}")
                logger.info(f"Presence state: {agent.presence_state}")
                logger.info(f"Voice interaction state: {agent.voice_interaction_state}")
                logger.info(f"Chat interaction state: {agent.chat_interaction_state}")
                logger.info(f"Email interaction state: {agent.email_interaction_state}")
                logger.info("---")
            
        except Exception as e:
            logger.error(f"Error in snapshot stats example: {str(e)}")
            # Print exception type and traceback for debugging
            import traceback
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Traceback: {traceback.format_exc()}")


async def main():
    """Main function to run the examples."""
    
    # Credentials
    username = "usernme"
    password = "password"
    domain_id = "doamain_id"
    # Note: Replace with your actual credentials and domain ID - suggest using environment variables or a secure vault
    # For security reasons, do not hardcode credentials in production code
    
    # Define available regions
    regions = {
        "us": "https://api.prod.us.five9.net",
        "ca": "https://api.prod.ca.five9.net",
        "eu": "https://api.prod.eu.five9.net",
        "uk": "https://api.prod.uk.five9.net",
        "in": "https://api.prod.in.five9.net",
    }
    
    # Set the region to test - change this to try different regions
    region = "us"  # Options: us, ca, eu, uk, in
    global base_url
    base_url = regions[region]
    
    logger.info(f"Testing with {region.upper()} region: {base_url}")
    
    # Run the interval stats example
    logger.info("=" * 50)
    logger.info("RUNNING INTERVAL STATS EXAMPLE")
    logger.info("=" * 50)
    await interval_stats_example(username, password, domain_id)
    
    # Run the snapshot stats example
    logger.info("=" * 50)
    logger.info("RUNNING SNAPSHOT STATS EXAMPLE")
    logger.info("=" * 50)
    await snapshot_stats_example(username, password, domain_id)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())