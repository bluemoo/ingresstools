ingresstools
============

## Prerequisites

 * Python 2.7
 * requests module
 * Ingress account

## Setup

Currently, configuration of these tools requires that you be able to monitor traffic from your browser to the ingress
servers and capture particular values of the cookies used for authentication. I recommand using using the Network tab
of the developer toolbar that is built into Chrome.

The action log does not yet have any way to log your account into ingress - it requires that you log into the intel
map first, and then provide it with your session information. Specifically, you need to provide values for the
CSRF_TOKEN and SESSION_ID keys in the settings.py file. The action logger then pretends to be you, and queries the
servers for new broadcasts every (configurable) 20 seconds.

To find these values, log into the intel map, and observe the cookies sent with a rpcservice request. Copy the value
of the ACSID cookie to SESSION_ID, and the value of the csrftoken cookie to CSRF_TOKEN.

You will also need to create an empty file named 'actions.state' in the directory in which you are running the action
logger.

## Run the action logger

Once you've configured everything, actually running the logger is simple. Navigate to the src directory and run:

> python actionlog.py

If properly configured, it will begin logging to the file actions.log, and keep its current state in actions.state.
You can start and stop the logger, and it will pick up where it left off.

