/**
 * Copyright (c) 2025 Xpander, Inc. All rights reserved.
 */

import { XpanderClient, LLMProvider, MemoryStrategy , Agent} from 'xpander-sdk';
import OpenAI from 'openai';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Provider to use. Default OpenAI
const llmProvider = LLMProvider.OPEN_AI;

export class MyAgent {
    /**
     * A framework agnostic agent implementation leveraging xpander.ai's backend-as-a-service infrastructure.
     * 
     * Handles asynchronous LLM interactions, orchestrates multi-step reasoning, and seamlessly integrates both local and cloud-based tools.
     * 
     * @param {Agent} agent - The xpander.ai Agent instance to operate.
     */
    constructor(agent) {
        this.agent = agent;
        this.llmProvider = llmProvider;
        
        // Set memory strategy using camelCase
        this.agent.memoryStrategy = MemoryStrategy.BUFFERING;
        
        // Load local instructions
        const localInstructions = JSON.parse(
            fs.readFileSync(join(__dirname, 'agent_instructions.json'), 'utf8')
        );
        
        if (localInstructions) {
            this.agent.instructions.role = localInstructions.role;
            this.agent.instructions.goal = localInstructions.goal;
            this.agent.instructions.general = localInstructions.general;
        }
        
        this.agent.selectLLMProvider(llmProvider);
        
        if (llmProvider === LLMProvider.OPEN_AI) {
            this.openaiClient = new OpenAI({
                apiKey: process.env.OPENAI_API_KEY
            });
        }
    }

    /**
     * Public entry point for chat interaction.
     * 
     * Adds a user task to the agent memory and initiates the async reasoning loop.
     * 
     * @param {string} userInput - User's input or instruction.
     * @param {string} [threadId] - Memory thread to append to (if continuing a thread).
     * @returns {Promise<string>} The memory thread ID of the resulting agent run.
     */
    async chat(userInput, threadId = null) {
        if (threadId) {
            console.log(`🧠 Adding task to existing thread: ${threadId}`);
            // Try using object pattern to skip middle parameters
            this.agent.addTask(userInput, threadId);
        } else {
            console.log("🧠 Adding task to a new thread");
            this.agent.addTask(userInput);
        }

        const agentThread = await this._agentLoop();
        console.log("-".repeat(80));
        console.log(`🤖 Agent response: ${agentThread.result}`);
        return agentThread.memoryThreadId;
    }

    /**
     * Internal helper to call the model endpoint.
     * 
     * @returns {Promise<Object>} Model response or error.
     */
    async _callModel() {
        const response = await this.openaiClient.chat.completions.create({
            messages: this.agent.messages,
            temperature: 0.0,
            tools: this.agent.getTools(),
            tool_choice: this.agent.toolChoice,
            model: "gpt-4o"
        });

        return response;
    }

    /**
     * Core async loop coordinating reasoning steps and tool execution.
     * 
     * @returns {Promise<any>} The final agent thread result after loop completion.
     */
    async _agentLoop() {
        let step = 1;
        console.log("🪄 Starting Agent Loop");
        const executionTokens = { worker: { totalTokens: 0, completionTokens: 0, promptTokens: 0 } };
        const executionStartTime = Date.now();

        // Main agentic loop
        while (!this.agent.isFinished()) {
            console.log("-".repeat(80));
            console.log(`🔍 Step ${step}`);

            // Call the AI model with tools and the state of the agent
            const response = await this._callModel();

            // Handle token accounting
            const stepUsage = this._handleTokenAccounting(executionTokens, response);

            // Add llm response to agent memory using camelCase
            const llmResponse = response.toJSON ? response.toJSON() : response;
            this.agent.addMessages(llmResponse);
            
            // Report execution metrics using camelCase
            this.agent.reportExecutionMetrics(
                executionTokens,
                this.openaiClient.model || "gpt-4o"
            );

            // Extract all tool calls from llm response using camelCase
            const toolCalls = XpanderClient.extractToolCalls(llmResponse);

            // Execute cloud tool calls using camelCase
            const cloudToolCallResults = await this.agent.runTools(toolCalls);

            // Log tool call results
            for (const res of cloudToolCallResults) {
                const emoji = res.isSuccess ? "✅" : "❌";
                console.log(`${emoji} ${res.functionName}`);
            }

            console.log(
                `🔢 Step ${step} tokens used: ${stepUsage.total_tokens} ` +
                `(output: ${stepUsage.completion_tokens}, input: ${stepUsage.prompt_tokens})`
            );
            step++;
        }

        console.log(`✨ Execution duration: ${(Date.now() - executionStartTime) / 1000}s`);
        console.log(
            `🔢 Total tokens used: ${executionTokens.worker.totalTokens} ` +
            `(output: ${executionTokens.worker.completionTokens}, ` +
            `input: ${executionTokens.worker.promptTokens})`
        );

        // Return the final agent thread result using camelCase
        return this.agent.retrieveExecutionResult();
    }

    /**
     * Handle token accounting for the response
     * 
     * @param {Object} executionTokens - Token tracking object
     * @param {Object} response - OpenAI response
     * @returns {Object} Step usage information
     */
    _handleTokenAccounting(executionTokens, response) {
        const usage = response.usage || { 
            total_tokens: 0, 
            completion_tokens: 0, 
            prompt_tokens: 0 
        };
        
        executionTokens.worker.totalTokens += usage.total_tokens;
        executionTokens.worker.completionTokens += usage.completion_tokens;
        executionTokens.worker.promptTokens += usage.prompt_tokens;
        
        return usage;
    }
} 