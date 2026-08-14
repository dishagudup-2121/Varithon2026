import { Bot, User } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function ChatMessage({ message }) {
  const { t } = useTranslation();

  const isUser = message.role === "user";

  return (
    <div
      className={`flex gap-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#D96F00]">
          <Bot size={18} />
        </div>
      )}

      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-[#F28C00] text-white"
            : "border border-[#EDE2D0] bg-white text-[#3D2918]"
        }`}
      >
        <p className="text-sm leading-6">
          {message.isTranslationKey
            ? t(message.text)
            : message.text}
        </p>
      </div>

      {isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#6B421F]">
          <User size={18} />
        </div>
      )}
    </div>
  );
}
