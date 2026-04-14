import { Message } from '../lib/types';
import { Leaf, User } from 'lucide-react';

interface Props {
  message: Message;
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start`}>
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm ${
          isUser
            ? 'bg-emerald-600 text-white'
            : 'bg-stone-100 border border-stone-200 text-emerald-700'
        }`}
      >
        {isUser ? <User size={14} /> : <Leaf size={14} />}
      </div>

      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 shadow-sm text-sm leading-relaxed ${
          isUser
            ? 'bg-emerald-600 text-white rounded-tr-sm'
            : 'bg-white border border-stone-100 text-stone-800 rounded-tl-sm'
        }`}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>
        <span
          className={`block text-[10px] mt-1.5 ${
            isUser ? 'text-emerald-200 text-right' : 'text-stone-400'
          }`}
        >
          {new Date(message.created_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>
    </div>
  );
}
