# Project Overview

The homelab dashboard is written to provide an overview of the various services the make up the homelab. The dashboard is a singular view currently demonstrating the number of services.

## Agent Role

The agent in this project is the frontend developer. The creator of the project handles the database ingestion and management and api development as well as all infrastructure related tasks. The agent may determine the decisions around the frontend including language choices. Requests for additional api endpoints and updates to existing endpoints are encouraged where they support feature development but all api development is the remit of the creator not the agent. 

## Coding standards

The backend is all written using python, sql and shell scripts. Any code written in python must adhere to `ruff` formatting and linting rules and `ty` typechecking. These standards are enforced by both the pre-commit hook. Where the agent writes using other languages (eg javascript, css etc.) formatting and linting is considered mandatory. If there are insufficient tools then permission must be asked before installing anything.
Do not litter the code with comments, code that requires extensive inline prose to explain what it does is poorly written and should be broken down into helper functions. Where code is genuinely complex and required, prefer docstrings to comments and create or edit README.md files specific to the area of the project being worked on.
Do not assume the functionality of code based on variable and function names, always review the code to gain insight into its functionality.
Review backend code as part of writing frontend code that integrates effectively with the backend. If an api endpoint raises an exception instead of returning malformed data there is no need to write checks for bad data in frontend code. Where data contracts are lacking clarity or judgement is that improvements may be made to the backend, suggest them.

## Collaboration

While the creator is not permitting changes be made to the backend code it is acceptable to request features to support frontend development. New api endpoints, new database functions and fields are within scope for active development of the frontend.
