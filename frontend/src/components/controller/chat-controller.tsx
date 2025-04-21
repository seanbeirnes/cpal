import UserChat from "@/components/chat/user-chat"
import ChatComposerController from "./chat-composer-controller"
import { AnswerChat, AnswerResponse } from "@/components/chat/answer-chat"
import { useState } from "react"
import axios from "axios"
import { useMutation } from "@tanstack/react-query"
import { LoaderCircle } from "lucide-react"


const QUERY_API_ENDPOINT = "/api/query"
const FIRST_ANSWER: AnswerResponse = { "answer": "Hello there!\n\nHow can I help you with Canvas today?", "sources": [] }

function ChatController() {
    const [chats, setChats] = useState<(AnswerResponse | string)[]>([FIRST_ANSWER])
    const [question, setQuestion] = useState<string>("")

    const askCallback = (question: string) => {
        setChats(prevChats => [...prevChats, question])
        setQuestion(question)
        askMutation.mutate(question)
    }

    const ask = (question: string) => {
        return axios.post(QUERY_API_ENDPOINT, { "query": question })
    }

    const askMutation = useMutation({
        mutationFn: ask,
        onSuccess: (data) => {
            setQuestion("")
            setChats(prevChats => [...prevChats, data as AnswerResponse])
        },
        onError: (error) => {
            console.error(error)
            alert("Oops! Something went wrong...")
        }
    })

    return (
        <>
            <div className="w-full flex flex-col p-4 mb-60">
                {chats.map((chat: (AnswerResponse | string)) => {
                    if (typeof (chat) == "string") {
                        return (
                            <UserChat message={chat} />
                        )
                    }
                    return (
                        <AnswerChat answer={chat} />
                    )
                })}
                {(question.length > 0) &&
                    <LoaderCircle className="self-center text-rose-200 animate-spin m-4" />
                }
            </div>
            <div className="w-full md:max-w-2xl fixed bottom-0 p-2 flex flex-col bg-white gap-4">
                <ChatComposerController callback={askCallback} disabled={question.length > 0} />
                <div>
                    <p className="text-center text-xs text-rose-300">CPAL is an AI-powered chatbot, so it may be wrong sometimes.<br />Be sure to verify all information with other sources.</p>
                    <p className="text-center text-xs text-rose-300 md:mt-4">
                        <span>Created by <a className="text-rose-500 underline" href="https://www.seanbeirnes.com" target="_blank">Sean Beirnes</a></span>
                        <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
                        <span><a className="text-rose-500 underline" href="https://github.com/seanbeirnes/cpal" target="_blank">View source code on GitHub</a></span></p>
                </div>
            </div>
        </>
    )
}

export default ChatController
