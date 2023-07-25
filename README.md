## Helix Protocol
Pitchdeck : https://drive.google.com/file/d/1-YteptDq4k9noVn_HU7sNfUdeLzPgWyS/view?usp=sharing
Website : https://helixprotocol.vercel.app/

## why in python?

We first developing our business logic with xrpl python sdk.  
It is easy and fast way to develop our project.

After the program gets stabilized, we will hire some smart contract developers and make the smart contract with xrpl-hooks.

It would not be a problem for us since our team has an experience of making web-assembly based smart contract project called Web3Mon.

## admin

It controls the overall launchpad.

It manages the ICO projects including creating and closing them.

## ico_project

It manages ICO projects.

When first made, new wallet is created for the funding.  
Every User can see the wallet so that people can trust.

Also, people will send xrp to this wallet by "Escrow",  
so that the project team should fulfill conditions to get access to xrp.

Furthermore, the tokens of the project will be globally freezed during the funding period.

## launchpad_user

It represents launchpad users' accounts.

User can search for the projects and fund and also claim their shares.

We didn't care much about the security issues since the purpose is to implement the logics.  
We will make a secure code when implementing smart contracts also getting audits.

## docker

Will dockerize the application so that every people can test regardless of the environments.

## Future plans

-   Make this as a python API and integrate with our websites so the website functions.
-   Implement incomplete functionalities.
-   Review the code and make it secure and readable.
"# helix_protocol" 
