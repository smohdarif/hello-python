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
    return Context.builder('example-user-key')\
        .kind('user')\
        .name('Sandy')\
        .build()


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
    builder = Context.builder(user_id).kind('user')
    
    if name:
        builder.name(name)
    
    # Add custom attributes
    for key, value in attributes.items():
        builder.set(key, value)
    
    context = builder.build()
    logger.debug(f"Built user context for: {user_id}")
    
    return context
