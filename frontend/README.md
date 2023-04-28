# The Front-End

This frontend folder contains the nessiary components to host a frontend for your applictions. 


## Development
To develop on the frontend you will need the following technolgies installed on your device:
- [node.js](https://nodejs.org/en/download/)
- [npm](https://www.npmjs.com/)

When working in the develoment enviroment you will need to modify the dev varible. To do this open /src/stores/servers.js. Change the const dev (line 5) to true. Remember to switch it to false when moving to the docker version.

To use the development server:
1. Run dockercompose to bring up all the other servers
   - `docker compose -f "dockercompose.yaml" up -d --build`
   - Or if you are using the VS Code extension right click the dockercompose file and select up
   - It is important that the other servers so that the front-end can interact with your back-end
1. Open the terminal
2. 
