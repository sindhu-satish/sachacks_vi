import React, { Fragment } from "react";
import { Bot, User } from "lucide-react";
import "katex/dist/katex.min.css";
import { InlineMath, BlockMath } from "react-katex";

interface ChatMessageProps {
  isAi: boolean;
  message: string;
  isLoading?: boolean;
}

// New helper function to format text with bold markers (i.e. **bold**)
// and preserve line breaks.
const formatTextWithBold = (text: string) => {
  // Split text by ** for bold formatting
  const boldParts = text.split(/\*\*(.*?)\*\*/g);
  return boldParts.map((part, i) => {
    if (i % 2 === 1) {
      // Bold text
      return <strong key={i}>{part}</strong>;
    } else {
      // Regular text with preserved newlines
      return part.split("\n").map((line, j, arr) => (
        <Fragment key={`${i}-${j}`}>
          {line}
          {j !== arr.length - 1 && <br />}
        </Fragment>
      ));
    }
  });
};

const formatMessage = (text: string) => {
  // Split the text by LaTeX delimiters $$ for block math
  const blockParts = text.split(/\$\$(.*?)\$\$/g);
  return blockParts.map((part, index) => {
    if (index % 2 === 1) {
      // This is LaTeX content (odd indices in the split array)
      return <BlockMath key={index} math={part} />;
    } else {
      // This is regular text - now check for inline math
      const inlineParts = part.split(/\$(.*?)\$/g);
      return (
        <span key={index}>
          {inlineParts.map((inlinePart, inlineIndex) => {
            if (inlineIndex % 2 === 1) {
              // This is inline LaTeX
              return <InlineMath key={inlineIndex} math={inlinePart} />;
            } else {
              // Process regular text with bold formatting and newlines
              return (
                <Fragment key={inlineIndex}>
                  {formatTextWithBold(inlinePart)}
                </Fragment>
              );
            }
          })}
        </span>
      );
    }
  });
};

export const ChatMessage: React.FC<ChatMessageProps> = ({ isAi, message }) => {
  return (
    <div className={`flex ${isAi ? "justify-start" : "justify-end"} mb-4 items-start gap-2`}>
      {isAi && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500/20 to-indigo-500/20 flex items-center justify-center border border-blue-400/20">
          <Bot size={18} className="text-blue-400" />
        </div>
      )}
      <div
        className={`max-w-[80%] p-4 rounded-xl shadow-lg ${
          isAi
            ? "bg-gradient-to-r from-slate-700/50 to-slate-800/50 text-slate-200 border border-slate-700/50"
            : "bg-gradient-to-r from-blue-500 to-indigo-600 text-white"
        }`}
      >
        <div className="text-sm md:text-basespace-y-2 latex-content">
          {/* {isLoading ? message : formatMessage(message)} */}
          {formatMessage(message)}
        </div>
      </div>
      {!isAi && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center">
          <User size={18} className="text-white" />
        </div>
      )}
    </div>
  );
};
