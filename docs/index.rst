=========================================
vendor-connectors Documentation
=========================================

Universal vendor connectors for the jbcom ecosystem, providing standardized access to cloud providers, third-party services, and AI APIs.

Overview
--------

``vendor-connectors`` is a modular Python library designed to simplify interaction with various vendors while maintaining strict security standards. It handles authentication, connection pooling, retries, and rate limiting transparently.

Supported Vendors
-----------------

Cloud Providers
~~~~~~~~~~~~~~~
* **AWS**: Organizations, Identity Center (SSO), S3, Secrets Manager, CodeDeploy.
* **Google Cloud**: Cloud Resource Manager, Billing, IAM, Storage, GKE, and more.

Services
~~~~~~~~
* **GitHub**: Repository management, members, teams, and GraphQL support.
* **Slack**: Messaging, channel management, and directory access.
* **HashiCorp Vault**: Secret management with token and AppRole auth.
* **Zoom**: User and meeting management.

AI APIs
~~~~~~~
* **Anthropic**: Full Claude 3/4 support, token counting, and agent execution.
* **Cursor**: Integration with the Cursor Background Agent API.
* **Meshy AI**: 3D asset generation from text and images, rigging, and animation.
* **Google Jules**: Automated coding agent sessions and PR creation.

Key Features
------------

* **Unified API**: Consistent ``VendorConnectorBase`` class for all integrations.
* **AI Tooling**: Native support for LangChain StructuredTools, CrewAI tools, and AWS Strands.
* **MCP Server**: Built-in Model Context Protocol server for direct LLM integration.
* **CLI Interface**: Powerful command-line tool to list and call any connector method.
* **Transparent Auth**: Automatic credential loading from environment variables, stdin, or config files via ``DirectedInputsClass``.

Quick Start
-----------

Install the package with the extras you need:

.. code-block:: bash

   pip install vendor-connectors[aws,github,ai]

Use the unified CLI:

.. code-block:: bash

   vendor-connectors list
   vendor-connectors call aws get_caller_account_id

Or use it in Python:

.. code-block:: python

   from vendor_connectors import AWSConnectorFull
   
   connector = AWSConnectorFull()
   buckets = connector.list_s3_buckets()

AI Framework Integration
------------------------

Get tools ready for your favorite AI framework:

.. code-block:: python

   from vendor_connectors.meshy.tools import get_tools
   
   # Auto-detects LangChain, CrewAI, or Strands
   tools = get_tools()

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started/installation
   getting-started/quickstart

.. toctree::
   :maxdepth: 2
   :caption: Architecture

   architecture/index

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/building-connector-tools

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing

.. toctree::
   :maxdepth: 1
   :caption: Enterprise

   jbcom Hub <https://jbcom.github.io>
   Agentic Docs <https://agentic.dev>
   Strata Docs <https://strata.game>
   Extended Data <https://extendeddata.dev>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
