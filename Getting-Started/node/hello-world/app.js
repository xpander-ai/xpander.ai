import fs from 'fs';
import { createInterface } from 'readline';
import { XpanderClient } from 'xpander-sdk';
import { MyAgent } from './MyAgent.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// === Load Configuration ===
// Reads API credentials and organization context from a local JSON file
const xpanderConfig = JSON.parse(
    fs.readFileSync(join(__dirname, 'xpander_config.json'), 'utf8')
);

// Initialize xpander client - using snake_case for parameters like Python version
const xpanderClient = new XpanderClient(xpanderConfig.api_key);
const xpanderAgent = await xpanderClient.agents.get(xpanderConfig.agent_id);

// Create readline interface for user input
const rl = createInterface({
    input: process.stdin,
    output: process.stdout
});

/**
 * Promisified readline question
 * @param {string} question - The question to ask
 * @returns {Promise<string>} User's input
 */
function askQuestion(question) {
    return new Promise((resolve) => {
        rl.question(question, resolve);
    });
}

async function main() {
    try {
        // Initialize agent
        const agent = new MyAgent(xpanderAgent);
        
        // Start the agent
        let thread = await agent.chat("Hi!");
        
        while (true) {
            const userInput = await askQuestion("You: ");
            
            // Exit conditions
            if (userInput.toLowerCase() === 'exit' || userInput.toLowerCase() === 'quit') {
                console.log("Goodbye! 👋");
                break;
            }
            
            thread = await agent.chat(userInput, thread);
        }
    } catch (error) {
        console.error("Error:", error);
    } finally {
        rl.close();
    }
}

// Run the main function
main().catch(console.error); 