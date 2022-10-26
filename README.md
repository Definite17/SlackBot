# SlackBot
In this project, I Created a Slack bot with two-way integration with **[Zenduty](https://www.zenduty.com/)** and **[JIRA](https://www.atlassian.com/software/jira)** to automate **Incident management**.
It can also be used for automating sending of messages, customized the Bot for custom reactions.

### What are Incidents ?
An incident, in the context of information technology, is an event that is not part of normal operations that disrupts operational processes.
An incident may involve the failure of a feature or service that should have been delivered or some other type of operation failure.
Security Incidents are events that indicate that an organization's systems or data may have been compromised.

### Why Do we need a Bot for Incident Management ?
Today, IT services must be available 24/7, but incidents are inevitable. If something goes wrong, the on-call person is called to get the service up and running as soon as possible. During downtime, you lose money every second.

For example: You have an e-commerce website and there is an incident on your cart page, so your customers will not be able to finish their purchase until the incident is resolved. 
In fact, Amazon downtime cost on average $31k per minute in 2008, in 2020 it’s about $220k per minute which represents approximately $13M per hour.

So, whenever a new Incidents occur the problem need to be identified faster and it need t be resolved, by Automating thing we can make certain steps faster and reduce workload, A Bot helps in  automating a lot of things to save time and avoid forgetting any steps. The teams are therefore focused on the incident and not how it should go.

### What is Slack ?
**[Slack](https://slack.com/)** is a messaging app for business that connects people to the information that they need. By bringing people together to work as one unified team, Slack transforms the way that organisations communicate.

### What is Zenduty ? 
**[Zenduty](https://www.zenduty.com/)** is an incident management platform that gives you greater control and automation over the incident management lifecycle.

###  Framework Used
**Python ([Bolt framework](https://slack.dev/bolt-python/concepts) –> slack-bolt):**

Bolt is the swiftest way to start programming with the Slack Platform in JavaScript, Python, or Java.
All flavors of Bolt are equipped to help you build apps.


### What is a Slack-Bot

A Slack-Bot is a type of Slack App designed to interact with users via conversation.

A bot is the same as a regular app: it can access the same range of APIs and do all of the magical things that a Slack App can do.

But when you build a bot for your Slack App, you’re giving that app a face, a name, and a personality, and encouraging users to talk to it.

Your bot can send DMs, it can be mentioned by users, it can post messages or upload files, and it can be invited to channels — or kicked out.

### Requirements

* **Python3**

* **[pip](https://pip.pypa.io/en/stable/)** and **[virtualenv](https://virtualenv.pypa.io/en/stable/)** to handle Python **[application dependencies](https://www.fullstackpython.com/application-dependencies.html)**

* **[Free Slack account](https://slack.com/intl/en-in/)** - you need to be signed in to at least one workspace where you have access to building apps.

* **[Python Slack SDK](https://slack.dev/python-slack-sdk/)** (pip install slack_sdk), **[Slack-Bolt](https://slack.dev/bolt-python/concepts)** (pip install slack-bolt).

### Creating and Installing our App
First thing first, let us create a bot in Slack UI.
* Go to https://api.slack.com/ then "**Create an app**".
* Select ‘From scratch’.
* Provide the bot name you want, I will name my bot  Intern BOT, and the workspace where it will be installed, mine is Slack Bot workspace, and hit ‘**create app**’.
* After this, you will be redirected to another page where you can configure your app. Here we will make some changes.
* Go to ‘**OAuth & Permissions**’. Here we will add the necessary scope and permissions for our bot. For now, we will add ‘**chat:write**’, ‘**groups:read**’, ‘**im:read**’, ‘**mpim:read**’, ‘**channels:manage**’, and ‘**channels:read**’ under ‘**Bot Token Scopes**’.
* Once you have these scopes added, scroll up and click ‘**Install to workspace**’.
* After the app is installed, you will be given a ‘**Bot User OAuth Token**’. Copy and save it somewhere, will come to use.
* Once you are done with all the above steps you can see the bot you created under ‘**Apps**’ in the selected Workspace.


The bot we currently have cannot do anything, we need to add some functionality to it. For this part, we will use only Slack-SDK to send messages and get some basic information about the channel.
