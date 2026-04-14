import { useState, useRef, useEffect } from 'react';
import { Send, RefreshCw } from 'lucide-react';
import { Message } from '../lib/types';
import MessageBubble from './MessageBubble';
import LoadingDots from './LoadingDots';
import SuggestedQuestions from './SuggestedQuestions';

const SYSTEM_PROMPT = `You are a helpful assistant specializing in Gaeltacht regions of Ireland.
You help users discover:
- Irish-speaking (Gaeltacht) towns and regions across Ireland
- Local pubs, restaurants, and community spots near Gaeltacht areas
- Heritage sites, ancient monuments, and cultural landmarks
- Volunteering opportunities in Irish-speaking communities
- Irish language words, place names (in Irish and English), and phrases
- Information about specific counties: Galway, Donegal, Mayo, Kerry, Cork, Waterford, Meath

You draw on knowledge of open datasets from Tailte Eireann (Ireland's mapping agency) and OpenStreetMap.
Always be warm, informative, and enthusiastic about Irish culture. When relevant, include a word or phrase in Irish.
Keep responses concise but rich in local detail. Format lists clearly when giving multiple options.`;

const GEMINI_MODELS = ['gemini-2.5-flash-lite', 'gemini-2.5-flash', 'gemini-2.5-pro'];

interface Props {
  onPromptSubmit?: (prompt: string) => void;
}

function extractReplyText(json: any) {
  const parts = json?.candidates?.[0]?.content?.parts;
  if (!Array.isArray(parts)) {
    return '';
  }

  return parts
    .map((part: any) => (typeof part?.text === 'string' ? part.text : ''))
    .join('')
    .trim();
}

function extractGeminiError(json: any, model: string) {
  const promptFeedback = json?.promptFeedback;
  const finishReason = json?.candidates?.[0]?.finishReason;

  if (promptFeedback?.blockReason) {
    return `${model} blocked the prompt: ${promptFeedback.blockReason}`;
  }

  if (finishReason && finishReason !== 'STOP') {
    return `${model} stopped with reason: ${finishReason}`;
  }

  return `${model} returned an empty response.`;
}

export default function ChatInterface({ onPromptSubmit }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [apiKey, setApiKey] = useState(() => sessionStorage.getItem('gemini_api_key') ?? '');
  const [pendingApiKey, setPendingApiKey] = useState(() => sessionStorage.getItem('gemini_api_key') ?? '');
  const [showKeyPrompt, setShowKeyPrompt] = useState(() => !sessionStorage.getItem('gemini_api_key'));
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const adjustTextarea = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 140) + 'px';
  };

  const saveApiKey = () => {
    const trimmed = pendingApiKey.trim();
    if (!trimmed) {
      return;
    }

    setApiKey(trimmed);
    sessionStorage.setItem('gemini_api_key', trimmed);
    setShowKeyPrompt(false);
  };

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const activeApiKey = apiKey.trim();
    if (!activeApiKey) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: 'Please enter your Gemini API key above before starting the chat.',
          created_at: new Date().toISOString(),
        },
      ]);
      return;
    }

    const trimmedText = text.trim();

    setShowSuggestions(false);
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    onPromptSubmit?.(trimmedText);

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmedText,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      history.push({ role: 'user', content: trimmedText });

      const requestBody = {
        system_instruction: {
          parts: [{ text: SYSTEM_PROMPT }],
        },
        contents: history.map((message) => ({
          role: message.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: message.content }],
        })),
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 1024,
        },
      };

      let reply = '';
      let lastError = '';

      for (const model of GEMINI_MODELS) {
        const res = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${activeApiKey}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
          }
        );

        if (!res.ok) {
          let errorText = `${model} failed with HTTP ${res.status}`;
          try {
            const errorJson = await res.json();
            errorText =
              errorJson?.error?.message ||
              errorJson?.message ||
              errorText;
          } catch {
            // Keep the HTTP fallback message when the response body is not JSON.
          }
          lastError = errorText;
          continue;
        }

        const json = await res.json();
        reply = extractReplyText(json);
        if (!reply) {
          lastError = extractGeminiError(json, model);
        }

        if (reply) {
          break;
        }
      }

      if (!reply) {
        reply = lastError
          ? `The AI service returned an error: ${lastError}`
          : 'The AI service returned an error. Please try again.';
      }

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: reply,
          created_at: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      const errMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content:
          error instanceof Error
            ? `Something went wrong connecting to the AI: ${error.message}`
            : 'Something went wrong connecting to the AI. Please try again shortly.',
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const resetChat = () => {
    setMessages([]);
    setShowSuggestions(true);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full">
      {showKeyPrompt && (
        <div className="absolute inset-0 z-20 flex items-center justify-center bg-stone-950/45 p-4 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl border border-emerald-100 bg-white p-5 shadow-2xl">
            <p className="text-xs font-semibold uppercase tracking-wider text-emerald-800">
              Gemini API Key Required
            </p>
            <h3 className="mt-2 text-lg font-semibold text-stone-800">
              Enter your own Gemini API key to start chatting
            </h3>
            <p className="mt-2 text-sm leading-relaxed text-stone-500">
              Your key is stored only in this browser session and is not bundled into the app.
            </p>
            <div className="mt-4 flex gap-2">
              <input
                type="password"
                value={pendingApiKey}
                onChange={(e) => setPendingApiKey(e.target.value)}
                placeholder="Paste your Gemini API key"
                className="flex-1 rounded-xl border border-emerald-200 bg-white px-3 py-2 text-sm text-stone-800 outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
              />
              <button
                type="button"
                onClick={saveApiKey}
                disabled={!pendingApiKey.trim()}
                className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-stone-300"
              >
                Continue
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between px-4 py-3 border-b border-stone-100 bg-white/80 backdrop-blur-sm">
        <div>
          <h2 className="text-sm font-semibold text-stone-800">Gaeltacht Assistant</h2>
          <p className="text-xs text-stone-400">Powered by Gemini AI using your local session key</p>
        </div>
        <button
          onClick={resetChat}
          className="p-2 rounded-lg hover:bg-stone-100 transition-colors text-stone-400 hover:text-stone-600"
          title="New conversation"
        >
          <RefreshCw size={15} />
        </button>
      </div>

      <div className="border-b border-stone-100 bg-emerald-50/70 px-4 py-3">
        <p className="text-[11px] font-semibold uppercase tracking-wider text-emerald-800">
          Gemini API Key
        </p>
        <div className="mt-2 flex gap-2">
          <input
            type="password"
            value={pendingApiKey}
            onChange={(e) => setPendingApiKey(e.target.value)}
            placeholder="Enter your own Gemini API key"
            className="flex-1 rounded-xl border border-emerald-200 bg-white px-3 py-2 text-sm text-stone-800 outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
          />
          <button
            type="button"
            onClick={saveApiKey}
            disabled={!pendingApiKey.trim()}
            className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-stone-300"
          >
            Save Key
          </button>
        </div>
        <p className="mt-1 text-[11px] text-emerald-700/80">
          Stored only in this browser session. Nothing is bundled into the frontend code.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4 scroll-smooth">
        {messages.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-full text-center py-8">
            <div className="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-4">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Flag_of_Ireland.svg/330px-Flag_of_Ireland.svg.png"
                alt="Ireland"
                className="w-8 h-5 object-cover rounded-sm"
              />
            </div>
            <h3 className="text-stone-700 font-semibold text-base mb-1">Dia dhuit!</h3>
            <p className="text-stone-400 text-sm max-w-xs leading-relaxed">
              Ask me anything about Gaeltacht regions, Irish language, local pubs, heritage
              sites, or volunteering opportunities.
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex gap-3 items-start">
            <div className="w-8 h-8 rounded-full bg-stone-100 border border-stone-200 flex items-center justify-center flex-shrink-0">
              <span className="text-emerald-700 text-xs">AI</span>
            </div>
            <div className="bg-white border border-stone-100 rounded-2xl rounded-tl-sm shadow-sm">
              <LoadingDots />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {showSuggestions && messages.length === 0 && (
        <SuggestedQuestions onSelect={sendMessage} disabled={loading} />
      )}

      <div className="px-4 pb-4 pt-2">
        <div className="flex gap-2 items-end bg-white rounded-2xl border border-stone-200 shadow-sm p-2 focus-within:border-emerald-400 focus-within:ring-2 focus-within:ring-emerald-100 transition-all">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              adjustTextarea();
            }}
            onKeyDown={handleKeyDown}
            placeholder="Ask about Gaeltacht towns, heritage, volunteering..."
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm text-stone-800 placeholder-stone-400 outline-none px-2 py-1.5 leading-relaxed max-h-[140px] overflow-y-auto"
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || loading}
            className="flex-shrink-0 w-8 h-8 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:bg-stone-200 disabled:cursor-not-allowed text-white flex items-center justify-center transition-colors"
          >
            <Send size={14} />
          </button>
        </div>
        <p className="text-center text-[10px] text-stone-300 mt-2">
          Press Enter to send &middot; Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
