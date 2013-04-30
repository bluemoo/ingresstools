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

To find these values, log into the intel map, and observe the cookies sent with a rpc request (Ideally, the request to dashboard.getPaginatedPlextsV2). Copy the value
of the ACSID cookie to SESSION_ID, and the value of the csrftoken cookie to CSRF_TOKEN.

You will also need to create an empty file named 'actions.state' in the directory in which you are running the action
logger.

## Run the action logger

Once you've configured everything, actually running the logger is simple. Navigate to the src directory and run:

> python actionlog.py

If properly configured, it will begin logging to the file actions.log, and keep its current state in actions.state.
You can start and stop the logger, and it will pick up where it left off.

## License

Copyright (c) 2013 Noah Jacobson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
