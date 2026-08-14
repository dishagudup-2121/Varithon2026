import { useState } from "react";

import {
  ArrowLeft,
  Bot,
  Send,
  Sparkles,
  Trash2,
} from "lucide-react";

import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

import ChatMessage from "../components/assistant/ChatMessage";
import SuggestionButton from "../components/assistant/SuggestionButton";

import {
  suggestedQuestions,
  mockResponses,
} from "../data/assistantData";

import HelpButton from "../components/common/HelpButton";
import HowItWorks from "../components/common/HowItWorks";
import logoImg from "../assets/logo_varithon.png";

export default function AIAssistant() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [helpOpen, setHelpOpen] = useState(false);

  const sendQuestion = (responseKey) => {
    const response = mockResponses[responseKey];

    if (!response) return;

    setMessages((previous) => [
      ...previous,

      {
        id: Date.now(),
        role: "user",
        text: response.questionKey,
        isTranslationKey: true,
      },

      {
        id: Date.now() + 1,
        role: "assistant",
        text: response.answerKey,
        isTranslationKey: true,
      },
    ]);
  };

  const sendCustomQuestion = () => {
    const question = input.trim();

    if (!question) return;

    setMessages((previous) => [
      ...previous,

      {
        id: Date.now(),
        role: "user",
        text: question,
        isTranslationKey: false,
      },

      {
        id: Date.now() + 1,
        role: "assistant",
        text: "assistant.responses.default",
        isTranslationKey: true,
      },
    ]);

    setInput("");
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="min-h-screen bg-[#FFFDF8]">

      {/* Header */}

      <header className="flex items-center justify-between border-b border-[#EDE2D0] bg-white px-4 py-3.5 md:px-8 md:py-4">

        <div className="flex items-center gap-3">

          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            className="rounded-lg p-2 text-[#6B421F] hover:bg-[#F8F1E5] cursor-pointer"
            aria-label="Back to dashboard"
          >
            <ArrowLeft size={20} />
          </button>

          <div className="flex items-center gap-2.5 sm:gap-3">
            <img
              src={logoImg}
              alt="VariSetu Logo"
              width="44"
              height="44"
              className="h-10 w-10 sm:h-11 sm:w-11 object-contain shrink-0"
            />

            <div>
              <h1 className="text-base sm:text-lg font-bold text-[#3D2918]">
                {t("assistant.title")}
              </h1>

              <p className="text-xs text-[#8B735D] hidden xs:block">
                {t("assistant.subtitle")}
              </p>
            </div>
          </div>

        </div>

        <div className="flex items-center gap-2">

          <button
            type="button"
            onClick={clearChat}
            className="rounded-lg p-2 text-[#8B735D] hover:bg-[#F8F1E5] cursor-pointer"
            title={t("assistant.clear")}
          >
            <Trash2 size={18} />
          </button>

          <HelpButton
            onClick={() => setHelpOpen(true)}
          />

        </div>

      </header>

      <main className="mx-auto flex max-w-5xl flex-col p-3 sm:p-4 md:p-8">

        {/* Introduction */}

        <section className="mb-4 sm:mb-6">

          <div className="flex items-center gap-2 text-[#E86F00]">

            <Sparkles size={17} />

            <span className="text-xs sm:text-sm font-semibold">
              {t("assistant.commandCenter")}
            </span>

          </div>

          <h2 className="mt-1 sm:mt-2 text-xl font-bold text-[#3D2918] sm:text-2xl md:text-3xl">
            {t("assistant.pageTitle")}
          </h2>

          <p className="mt-1.5 sm:mt-2 max-w-2xl text-xs sm:text-sm leading-5 sm:leading-6 text-[#8B735D]">
            {t("assistant.description")}
          </p>

        </section>

        {/* Chat area */}

        <section className="flex min-h-[450px] sm:min-h-[520px] md:min-h-[600px] flex-col overflow-hidden rounded-2xl border border-[#EDE2D0] bg-[#FDF9F2]">

          {/* Messages */}

          <div className="flex-1 space-y-4 overflow-y-auto p-3 sm:p-5 md:p-7">

            {messages.length === 0 ? (

              <div className="flex min-h-[300px] sm:min-h-[350px] flex-col items-center justify-center text-center px-2">

                <div className="flex h-14 w-14 sm:h-16 sm:w-16 items-center justify-center rounded-2xl bg-[#F8E7CF] text-[#E86F00]">
                  <Bot size={28} />
                </div>

                <h3 className="mt-4 sm:mt-5 text-base sm:text-lg font-bold text-[#3D2918]">
                  {t("assistant.emptyTitle")}
                </h3>

                <p className="mt-1.5 sm:mt-2 max-w-md text-xs sm:text-sm leading-5 sm:leading-6 text-[#8B735D]">
                  {t("assistant.emptyDescription")}
                </p>

                <div className="mt-5 sm:mt-6 grid w-full max-w-2xl grid-cols-1 gap-2.5 sm:gap-3 md:grid-cols-2">

                  {suggestedQuestions.map(
                    (suggestion, index) => (
                      <SuggestionButton
                        key={suggestion.id}
                        suggestion={suggestion}
                        onClick={() => {
                          const keys = [
                            "highRisk",
                            "nextAmbulance",
                            "routeRisk",
                            "simulation",
                          ];

                          sendQuestion(keys[index]);
                        }}
                      />
                    )
                  )}

                </div>

              </div>

            ) : (

              messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                />
              ))

            )}

          </div>

          {/* Input */}

          <div className="border-t border-[#EDE2D0] bg-white p-3 sm:p-4">

            <div className="flex items-end gap-2 rounded-2xl border border-[#EDE2D0] bg-[#FFFDF8] p-2">

              <textarea
                value={input}
                onChange={(event) =>
                  setInput(event.target.value)
                }
                onKeyDown={(event) => {
                  if (
                    event.key === "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();
                    sendCustomQuestion();
                  }
                }}
                rows={1}
                placeholder={t("assistant.placeholder")}
                className="max-h-32 min-w-0 flex-1 resize-none bg-transparent px-2.5 py-2 text-sm text-[#3D2918] outline-none placeholder:text-[#B19A82]"
              />

              <button
                type="button"
                onClick={sendCustomQuestion}
                disabled={!input.trim()}
                className="flex h-9 w-9 sm:h-10 sm:w-10 shrink-0 items-center justify-center rounded-xl bg-[#F28C00] text-white transition hover:bg-[#D96F00] disabled:cursor-not-allowed disabled:opacity-40 cursor-pointer"
              >
                <Send size={16} />
              </button>

            </div>

            <p className="mt-2 text-center text-[10px] sm:text-[11px] text-[#9B836B]">
              {t("assistant.disclaimer")}
            </p>

          </div>

        </section>

      </main>

      <HowItWorks
        feature="assistant"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />

    </div>
  );
}
