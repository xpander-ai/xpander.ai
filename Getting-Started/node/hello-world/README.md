# Hello World Node.js - Xpander SDK

A Node.js implementation of the Hello World app using the `xpander-sdk` with camelCase conventions and parameter-based function calls.

## Prerequisites

- Node.js 22.0.0 or higher
- npm or yarn package manager
- OpenAI API key
- Xpander API key and Agent ID

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd hello-world-node
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   
   # Note: This will install the xpander-sdk package for Node.js
   # which provides camelCase API methods and parameter-based functions
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Xpander Configuration (already in xpander_config.json)
   # XPANDER_API_KEY=your_xpander_api_key_here
   # XPANDER_ORG_ID=your_organization_id_here
   # AGENT_ID=your_agent_id_here
   ```

4. **Update configuration:**
   The xpander configuration is loaded from `xpander_config.json`. Update it with your actual credentials:
   ```json
   {
     "organization_id": "your_organization_id",
     "api_key": "your_xpander_api_key",
     "agent_id": "your_agent_id"
   }
   ```

## Usage

Run the application:
```bash
npm start
# or
node app.js
```

For development with auto-reload:
```bash
npm run dev
```

## Key Differences from Python Version

This Node.js implementation follows JavaScript/TypeScript conventions and uses the same `xpander-sdk` package name but with different API conventions:

1. **CamelCase Method Names:**
   - `add_task()` → `addTask()`
   - `add_messages()` → `addMessages()`
   - `is_finished()` → `isFinished()`
   - `get_tools()` → `getTools()`
   - `run_tools()` → `runTools()`

2. **Parameter-based Function Calls:**
   - Python: `agent.add_task(input=user_input, thread_id=thread_id)`
   - Node.js: `agent.addTask(userInput, threadId)`

3. **ES Modules:**
   - Uses `import`/`export` syntax instead of Python's import system
   - File extensions required in import statements

4. **Async/Await:**
   - Uses native JavaScript async/await patterns
   - Promise-based readline interface for user input

5. **Package Installation:**
   - Python: `pip install xpander-sdk`
   - Node.js: `npm install xpander-sdk`
   - Both use the same package name but different package managers

## Project Structure

```
hello-world-node/
├── app.js                    # Main application entry point
├── MyAgent.js               # Agent implementation class
├── package.json             # Node.js dependencies and scripts
├── xpander_config.json      # Xpander API configuration
├── agent_instructions.json  # Agent role and instructions
└── README.md               # This file
```

## Features

- Interactive chat interface with the xpander agent
- Token usage tracking and reporting
- Step-by-step execution logging
- Error handling and graceful shutdown
- Memory thread management for conversation continuity

## Commands

- Type `exit` or `quit` to end the conversation
- Press Ctrl+C to force quit the application

## Troubleshooting

1. **Node Version:** Ensure you're using Node.js 22.0.0 or higher
2. **API Keys:** Verify your OpenAI and Xpander API keys are correct
3. **Agent ID:** Confirm your agent ID exists and is accessible
4. **Dependencies:** Run `npm install` to ensure all packages are installed

## License

MIT License - Copyright (c) 2025 Xpander, Inc. 