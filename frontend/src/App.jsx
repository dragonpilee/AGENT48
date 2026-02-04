import React, { useState, useEffect, useRef } from 'react';

function App() {
    const [prompt, setPrompt] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim() || isLoading) return;

        const userMessage = { role: 'user', content: prompt };
        setMessages(prev => [...prev, userMessage]);
        setPrompt('');
        setIsLoading(true);

        try {
            const response = await fetch('/api/agent/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to execute agent');
            }

            const trajectory = data.trajectory || [];
            const agentMessages = trajectory.map(step => {
                if (step.agent) {
                    return { role: 'agent', content: step.agent };
                }
                if (step.tool) {
                    return {
                        role: 'system',
                        content: `Ran ${step.tool}`,
                        isTool: true,
                        output: step.output
                    };
                }
                return null;
            }).filter(Boolean);


            // Only add final_answer if it's different from the last agent message
            const lastAgentMessage = agentMessages[agentMessages.length - 1];
            const shouldAddFinalAnswer = data.final_answer &&
                (!lastAgentMessage || lastAgentMessage.content !== data.final_answer);

            const newMessages = shouldAddFinalAnswer
                ? [...agentMessages, { role: 'agent', content: data.final_answer }]
                : agentMessages;

            setMessages(prev => [...prev, ...newMessages]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'system', content: `Error: ${error.message}`, isError: true }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            <div className="terminal-header">
                AGENT48 TERMINAL v1.0.4 [GPU: RTX 2050] [MODEL: GRANITE-4.0-NANO]
            </div>

            <div className="messages">
                {messages.length === 0 && (
                    <div className="welcome">
                        <h2>SYSTEM READY.</h2>
                        <p>Awaiting commands... (Type to interact with AGENT48)</p>
                    </div>
                )}
                {messages.map((msg, i) => (
                    <div key={i} className={`message ${msg.role} ${msg.isTool ? 'tool' : ''}`}>
                        <span className="content">{msg.content}</span>
                        {msg.isTool && (
                            <pre className="tool-output">{msg.output}</pre>
                        )}
                    </div>
                ))}
                {isLoading && <div className="message agent">...THINKING...<span className="cursor"></span></div>}
                <div ref={messagesEndRef} />
            </div>

            <form className="input-line" onSubmit={handleSubmit}>
                <span className="prompt">USER@AGENT48:~$</span>
                <input
                    type="text"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    autoFocus
                    disabled={isLoading}
                />
                {!isLoading && <span className="cursor"></span>}
            </form>
        </div>
    );
}

export default App;
