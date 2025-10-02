"""
Context building functions for LaunchDarkly.

Best Practice: getContext() - Manage and create contexts dynamically.
Keeping it simple with essential context building functions.
"""
from ldclient import Context
import logging

logger = logging.getLogger(__name__)


def build_demo_context():
    """
    Build a simple demo user context for testing.
    
    Returns:
        Context: Demo user context
    """
    logger.info("📍 FLOW [3/6]: context.build_demo_context() - Building demo user context")
    logger.info("   ↳ User Key: 'example-user-key'")
    logger.info("   ↳ User Name: 'Sandy'")
    logger.info("   ↳ Kind: 'user'")
    
    context = Context.builder('example-user-key')\
        .kind('user')\
        .name('Sandy')\
        .build()
    
    logger.info("✓ Demo context built successfully")
    return context


def build_user_context(user_id, name=None, **attributes):
    """
    Build user context with custom attributes.
    
    Best Practice: getContext() - Create contexts dynamically as needed.
    
    Args:
        user_id: Unique user identifier
        name: User's display name (optional)
        **attributes: Additional custom attributes
        
    Returns:
        Context: LaunchDarkly user context
        
    Example:
        context = build_user_context(
            'user-123',
            name='John Doe',
            email='john@example.com',
            plan='premium'
        )
    """
    logger.info(f"📍 FLOW [3/6]: context.build_user_context() - Building context for user: {user_id}")
    logger.info(f"   ↳ User ID: '{user_id}'")
    if name:
        logger.info(f"   ↳ Name: '{name}'")
    if attributes:
        logger.info(f"   ↳ Attributes: {list(attributes.keys())}")
    
    builder = Context.builder(user_id).kind('user')
    
    if name:
        builder.name(name)
    
    # Add custom attributes
    for key, value in attributes.items():
        builder.set(key, value)
    
    context = builder.build()
    logger.info(f"✓ User context built successfully for: {user_id}")
    
    return context
